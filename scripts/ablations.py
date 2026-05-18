#!/usr/bin/env python
"""CLI for rendering LeJEPA ablation commands."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

from ablations.commands import render_command, render_markdown, render_shell_script
from ablations.common import CommandOptions, count_configs
from ablations.specs import BASE_OVERRIDES, get_spec, list_specs


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List available ablation specs.")

    show_parser = subparsers.add_parser("show", help="Show one ablation spec.")
    show_parser.add_argument("key", help="Ablation key.")

    render_parser = subparsers.add_parser("render", help="Render one or all specs.")
    render_parser.add_argument("key", help="Ablation key, or 'all'.")
    render_parser.add_argument(
        "--smoke",
        action="store_true",
        help="Render lightweight synthetic-dataset smoke commands.",
    )

    write_parser = subparsers.add_parser(
        "write-scripts", help="Write one shell script per ablation spec."
    )
    write_parser.add_argument(
        "--output",
        default="scripts/generated",
        help="Output directory for generated shell scripts.",
    )
    write_parser.add_argument(
        "--ready-only",
        action="store_true",
        help="Only write scripts for specs with status=ready.",
    )
    write_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated scripts.",
    )

    summarize_parser = subparsers.add_parser(
        "summarize", help="Summarize local CSV logs from ablation runs."
    )
    summarize_parser.add_argument("log_dir", help="Root directory containing run logs.")
    summarize_parser.add_argument(
        "--output",
        default="scripts/generated/results",
        help="Output directory for summary files.",
    )
    summarize_parser.add_argument(
        "--metric",
        default="val/knn_top1",
        help="Metric column to select per-run best rows.",
    )
    summarize_parser.add_argument(
        "--mode",
        default="max",
        choices=("max", "min", "last"),
        help="How to select one row per run for the metric.",
    )

    return parser


def _print_list() -> None:
    print(f"{'key':<18} {'status':<22} {'configs':>7} {'priority':>8}")
    for spec in list_specs():
        print(
            f"{spec.key:<18} {spec.status:<22} {count_configs(spec):>7} {spec.priority:>8}"
        )


def _format_dict(values: dict[str, Any], indent: str = "  ") -> list[str]:
    return [f"{indent}{key}: {value!r}" for key, value in values.items()]


def _print_show(key: str) -> int:
    try:
        spec = get_spec(key)
    except KeyError as exc:
        print(exc, file=sys.stderr)
        return 2

    print(f"key: {spec.key}")
    print(f"title: {spec.title}")
    print(f"status: {spec.status}")
    print(f"priority: {spec.priority}")
    print(f"configs: {count_configs(spec)}")
    print(f"question: {spec.question}")
    if spec.requires:
        print(f"requires: {', '.join(spec.requires)}")
    if spec.expected:
        print(f"expected: {spec.expected}")
    if spec.notes:
        print("notes:")
        for note in spec.notes:
            print(f"  - {note}")
    if spec.overrides:
        print("overrides:")
        print("\n".join(_format_dict(spec.overrides)))
    if spec.grid:
        print("grid:")
        print("\n".join(_format_dict(spec.grid)))
    if spec.cases:
        print("cases:")
        for index, case in enumerate(spec.cases, start=1):
            body = ", ".join(f"{key}={value!r}" for key, value in case.items())
            print(f"  {index}. {body}")
    print("base_overrides:")
    print("\n".join(_format_dict(BASE_OVERRIDES)))
    return 0


def _print_render(key: str, smoke: bool = False) -> int:
    options = CommandOptions(smoke=smoke)
    try:
        if key == "all":
            specs = list_specs()
            if smoke:
                specs = tuple(spec for spec in specs if spec.status == "ready")
            print(render_markdown(specs, options))
        else:
            rendered = render_command(get_spec(key), options)
            print(rendered.command)
    except KeyError as exc:
        print(exc, file=sys.stderr)
        return 2
    return 0


def _write_scripts(output: str, ready_only: bool, force: bool) -> int:
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

    specs = list_specs()
    if ready_only:
        specs = tuple(spec for spec in specs if spec.status == "ready")

    written = 0
    skipped = 0
    for spec in specs:
        path = output_dir / f"run_{spec.key}.sh"
        if path.exists() and not force:
            print(f"skip existing: {path}")
            skipped += 1
            continue

        path.write_text(render_shell_script(spec), encoding="utf-8")
        path.chmod(path.stat().st_mode | 0o111)
        print(f"wrote: {path}")
        written += 1

    print(f"summary: wrote={written} skipped={skipped} output={output_dir}")
    return 0


def _summarize(log_dir: str, output: str, metric: str, mode: str) -> int:
    from ablations.summarize import summarize_logs

    try:
        csv_path, md_path, summary = summarize_logs(
            log_dir=log_dir,
            output=output,
            metric=metric,
            mode=mode,
        )
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"wrote: {csv_path}")
    print(f"wrote: {md_path}")
    print(f"summary: runs={len(summary)} metric={metric} mode={mode}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "list":
        _print_list()
        return 0
    if args.command == "show":
        return _print_show(args.key)
    if args.command == "render":
        return _print_render(args.key, args.smoke)
    if args.command == "write-scripts":
        return _write_scripts(args.output, args.ready_only, args.force)
    if args.command == "summarize":
        return _summarize(args.log_dir, args.output, args.metric, args.mode)

    parser.error(f"unknown command {args.command!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
