"""Shared data structures for LeJEPA ablation command rendering."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import reduce
from operator import mul
import shlex
from typing import Any, Literal


Status = Literal["ready", "needs_model_support", "needs_config_support", "blocked"]


@dataclass(frozen=True)
class AblationSpec:
    """Declarative description of one ablation sweep."""

    key: str
    title: str
    question: str
    priority: int
    grid: dict[str, list[Any]] = field(default_factory=dict)
    cases: list[dict[str, Any]] = field(default_factory=list)
    overrides: dict[str, Any] = field(default_factory=dict)
    requires: tuple[str, ...] = ()
    status: Status = "ready"
    expected: str = ""
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.grid and self.cases:
            raise ValueError(f"{self.key}: define either grid or cases, not both")
        if not self.grid and not self.cases:
            raise ValueError(f"{self.key}: define grid or cases")


@dataclass(frozen=True)
class CommandOptions:
    """Options that control shell command rendering."""

    target: str = "python scripts/train_lejepa_ablation.py"
    multirun: bool = True
    smoke: bool = False
    env: dict[str, str] = field(default_factory=lambda: {"HYDRA_FULL_ERROR": "1"})


@dataclass(frozen=True)
class RenderedCommand:
    """Rendered shell command plus metadata for display."""

    spec_key: str
    command: str
    num_configs: int
    status: Status
    warnings: tuple[str, ...] = ()


def as_hydra_value(value: Any) -> str:
    """Format a Python value as a Hydra-style override value."""

    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, float):
        return f"{value:g}"
    if isinstance(value, str):
        return shlex.quote(value)
    return str(value)


def format_override(key: str, value: Any) -> str:
    """Format a single key/value pair as ``key=value``."""

    return f"{key}={as_hydra_value(value)}"


def format_sweep_override(key: str, values: list[Any]) -> str:
    """Format one comma-separated multirun sweep override."""

    if not values:
        raise ValueError(f"{key}: sweep values cannot be empty")
    return f"{key}={','.join(as_hydra_value(value) for value in values)}"


def count_grid(grid: dict[str, list[Any]]) -> int:
    """Return the cartesian product size for a grid."""

    if not grid:
        return 0
    lengths = [len(values) for values in grid.values()]
    if any(length == 0 for length in lengths):
        return 0
    return reduce(mul, lengths, 1)


def count_configs(spec: AblationSpec) -> int:
    """Return the number of concrete configs described by a spec."""

    if spec.cases:
        return len(spec.cases)
    return count_grid(spec.grid)
