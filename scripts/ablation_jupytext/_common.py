"""Shared helpers for Kaggle ablation notebooks.

The notebooks own their OVERRIDES dict (visible in cell [3]). This module only
provides:

- ``setup_kaggle_env``: environment + sys.path + offline shims.
- ``render``: render one spec to a shell command, merging notebook overrides
  via ``dataclasses.replace`` (no global state is mutated).
- ``render_chunk``: same, but slices a long sweep into one chunk.
"""

from __future__ import annotations

import dataclasses
import os
import sys
import types
from itertools import product
from pathlib import Path
from typing import Any


DEFAULT_SOURCE = "/kaggle/input/lejepa-mlproject"
DEFAULT_HF_CACHE = "/kaggle/input/lejepa-imagenette-hfcache"
DEFAULT_WORKING = "/kaggle/working"


def setup_kaggle_env(
    source: str = DEFAULT_SOURCE,
    hf_cache: str = DEFAULT_HF_CACHE,
    working: str = DEFAULT_WORKING,
    spec_key: str = "ablation",
) -> dict[str, str]:
    """Configure Kaggle paths, offline cache variables, and import shims."""

    os.environ["SPT_LIGHT_IMPORT"] = "0"
    os.environ["HF_DATASETS_CACHE"] = hf_cache
    os.environ["HF_DATASETS_OFFLINE"] = "1"
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl_cfg")
    os.environ.setdefault("WANDB_MODE", "offline")
    os.environ.setdefault("HYDRA_FULL_ERROR", "1")

    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    ckpt_dir = Path(working) / "checkpoints" / spec_key
    log_dir = Path(working) / "logs" / spec_key
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    for path in (f"{source}/stable-pretraining", source):
        if path not in sys.path:
            sys.path.insert(0, path)

    try:
        import requests_cache  # noqa: F401
    except ImportError:
        import requests

        module = types.ModuleType("requests_cache")

        class _CachedSession(requests.Session):
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__()

        module.CachedSession = _CachedSession
        sys.modules["requests_cache"] = module

    return {
        "source": source,
        "hf_cache": hf_cache,
        "working": working,
        "ckpt_dir": str(ckpt_dir),
        "log_dir": str(log_dir),
    }


def _command_options(smoke: bool):
    from scripts.ablations.common import CommandOptions

    return CommandOptions(
        target="python scripts/train_lejepa_ablation.py",
        multirun=True,
        smoke=smoke,
        env={"HYDRA_FULL_ERROR": "1"},
    )


def render(spec_key: str, overrides: dict[str, Any], *, smoke: bool = False) -> str:
    """Render one spec command.

    ``overrides`` are merged into ``spec.overrides`` via ``dataclasses.replace``;
    the global ``BASE_OVERRIDES`` is not touched. Keys in ``overrides`` take
    precedence over the spec's own overrides and over ``BASE_OVERRIDES``.
    """

    from scripts.ablations.commands import render_command
    from scripts.ablations.specs import get_spec

    spec = get_spec(spec_key)
    spec = dataclasses.replace(spec, overrides={**spec.overrides, **overrides})
    return render_command(spec, _command_options(smoke)).command


def render_chunk(
    spec_key: str,
    overrides: dict[str, Any],
    chunk_index: int,
    chunk_size: int,
) -> str:
    """Render one chunk of a long sweep as a multi-case command.

    The spec's grid (or cases) is flattened into a list, sliced, and reattached
    via ``dataclasses.replace`` so the renderer emits one command per case.
    """

    from scripts.ablations.commands import render_command
    from scripts.ablations.specs import get_spec

    spec = get_spec(spec_key)
    if spec.grid:
        keys = list(spec.grid.keys())
        all_combos = [
            dict(zip(keys, values, strict=True))
            for values in product(*(spec.grid[key] for key in keys))
        ]
    elif spec.cases:
        all_combos = list(spec.cases)
    else:
        raise ValueError(f"{spec_key}: no grid or cases to chunk")

    start = chunk_index * chunk_size
    combos = all_combos[start : start + chunk_size]
    if not combos:
        raise ValueError(
            f"{spec_key}: chunk {chunk_index} is empty "
            f"(total configs={len(all_combos)}, chunk_size={chunk_size})"
        )

    spec = dataclasses.replace(
        spec,
        grid={},
        cases=combos,
        overrides={**spec.overrides, **overrides},
        key=f"{spec.key}_chunk{chunk_index}",
    )
    return render_command(spec, _command_options(smoke=False)).command
