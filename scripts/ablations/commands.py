"""Render LeJEPA ablation specs into shell commands."""

from __future__ import annotations

from collections.abc import Iterable

from .common import (
    AblationSpec,
    CommandOptions,
    RenderedCommand,
    count_configs,
    format_override,
    format_sweep_override,
)
from .specs import BASE_OVERRIDES, SMOKE_OVERRIDES, TRAIN_ENTRYPOINT_SUPPORTED_KEYS


def _warning_lines(spec: AblationSpec, omitted_keys: set[str]) -> tuple[str, ...]:
    warnings: list[str] = []
    if spec.status != "ready":
        warnings.append(
            f"{spec.key}: status is {spec.status}; rendered command may not run yet."
        )
    if spec.requires:
        warnings.append(f"{spec.key}: requires {', '.join(spec.requires)}.")
    if omitted_keys:
        warnings.append(
            f"{spec.key}: omitted unsupported train entrypoint keys: "
            f"{', '.join(sorted(omitted_keys))}."
        )
    return tuple(warnings)


def _base_command(options: CommandOptions) -> str:
    env = " ".join(f"{key}={value}" for key, value in options.env.items())
    pieces = [piece for piece in (env, options.target) if piece]
    if options.multirun:
        pieces.append("--multirun")
    return " ".join(pieces)


def _fixed_overrides(spec: AblationSpec, dynamic_keys: set[str]) -> dict[str, object]:
    fixed = dict(BASE_OVERRIDES)
    fixed.update(spec.overrides)
    for key in dynamic_keys:
        fixed.pop(key, None)
    return fixed


def _apply_smoke_overrides(
    overrides: dict[str, object], dynamic_keys: set[str]
) -> dict[str, object]:
    merged = dict(overrides)
    for key, value in SMOKE_OVERRIDES.items():
        if key not in dynamic_keys:
            merged[key] = value
    return merged


def _filter_supported(overrides: dict[str, object]) -> tuple[dict[str, object], set[str]]:
    supported = {}
    omitted = set()
    for key, value in overrides.items():
        if key in TRAIN_ENTRYPOINT_SUPPORTED_KEYS:
            supported[key] = value
        else:
            omitted.add(key)
    return supported, omitted


def _filter_supported_grid(
    grid: dict[str, list[object]],
) -> tuple[dict[str, list[object]], set[str]]:
    supported = {}
    omitted = set()
    for key, values in grid.items():
        if key in TRAIN_ENTRYPOINT_SUPPORTED_KEYS:
            supported[key] = values
        else:
            omitted.add(key)
    return supported, omitted


def _format_multiline_command(command: str, overrides: list[str]) -> str:
    if not overrides:
        return command
    lines = [f"{command} \\"]
    for index, override in enumerate(overrides):
        suffix = " \\" if index < len(overrides) - 1 else ""
        lines.append(f"  {override}{suffix}")
    return "\n".join(lines)


def render_command(spec: AblationSpec, options: CommandOptions | None = None) -> RenderedCommand:
    """Render one spec into a command block."""

    options = options or CommandOptions()
    command = _base_command(options)
    omitted_keys: set[str] = set()

    if spec.cases:
        commands: list[str] = []
        for index, case in enumerate(spec.cases, start=1):
            dynamic_keys = set(case)
            fixed = _apply_smoke_overrides(
                _fixed_overrides(spec, dynamic_keys), dynamic_keys
            ) if options.smoke else _fixed_overrides(spec, dynamic_keys)
            case_overrides = dict(case)
            if options.smoke:
                for key, value in SMOKE_OVERRIDES.items():
                    if key in case_overrides:
                        case_overrides[key] = value
            fixed, fixed_omitted = _filter_supported(fixed)
            case_overrides, case_omitted = _filter_supported(case_overrides)
            omitted_keys.update(fixed_omitted)
            omitted_keys.update(case_omitted)
            overrides = [format_override(key, value) for key, value in fixed.items()]
            overrides.extend(
                format_override(key, value) for key, value in case_overrides.items()
            )
            commands.append(
                "\n".join(
                    [
                        f"# case {index}/{len(spec.cases)}",
                        _format_multiline_command(command, overrides),
                    ]
                )
            )
        rendered = "\n\n".join(commands)
    else:
        grid, grid_omitted = _filter_supported_grid(spec.grid)
        omitted_keys.update(grid_omitted)
        dynamic_keys = set(grid)
        fixed = _apply_smoke_overrides(
            _fixed_overrides(spec, dynamic_keys), dynamic_keys
        ) if options.smoke else _fixed_overrides(spec, dynamic_keys)
        fixed, fixed_omitted = _filter_supported(fixed)
        omitted_keys.update(fixed_omitted)
        overrides = [format_override(key, value) for key, value in fixed.items()]
        overrides.extend(
            format_sweep_override(key, values) for key, values in grid.items()
        )
        rendered = _format_multiline_command(command, overrides)

    warnings = _warning_lines(spec, omitted_keys)
    if warnings:
        rendered = "\n".join(f"# WARNING: {warning}" for warning in warnings) + "\n" + rendered

    return RenderedCommand(
        spec_key=spec.key,
        command=rendered,
        num_configs=count_configs(spec),
        status=spec.status,
        warnings=warnings,
    )


def render_markdown(
    specs: Iterable[AblationSpec], options: CommandOptions | None = None
) -> str:
    """Render one or more specs as markdown-ish command blocks."""

    blocks = []
    for spec in specs:
        rendered = render_command(spec, options)
        blocks.append(
            "\n".join(
                [
                    f"## {spec.key}: {spec.title}",
                    f"# status: {rendered.status}",
                    f"# configs: {rendered.num_configs}",
                    rendered.command,
                ]
            )
        )
    return "\n\n".join(blocks)


def render_shell_script(spec: AblationSpec, options: CommandOptions | None = None) -> str:
    """Render one executable shell script for a spec."""

    rendered = render_command(spec, options)
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        f"# {spec.key}: {spec.title}",
        f"# status: {rendered.status}",
        f"# configs: {rendered.num_configs}",
        rendered.command,
        "",
    ]
    return "\n".join(lines)
