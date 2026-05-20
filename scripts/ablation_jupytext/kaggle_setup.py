"""Shared helpers for Kaggle ablation notebooks."""

from __future__ import annotations

import dataclasses
import os
import sys
import types
from itertools import product
from pathlib import Path


def setup(source: str, data_root: str, spec_key: str, working: str = "/kaggle/working") -> dict:
    os.environ["SPT_LIGHT_IMPORT"] = "0"
    os.environ["HF_DATASETS_OFFLINE"] = "1"
    os.environ["LEJEPA_DATA_ROOT"] = data_root
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl_cfg")
    os.environ.setdefault("WANDB_MODE", "offline")
    os.environ.setdefault("HYDRA_FULL_ERROR", "1")
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    ckpt_dir, log_dir = Path(working) / "checkpoints" / spec_key, Path(working) / "logs" / spec_key
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    for path in (f"{source}/stable-pretraining", source):
        if path not in sys.path:
            sys.path.insert(0, path)
    os.environ["PYTHONPATH"] = ":".join(
        [source, f"{source}/stable-pretraining", os.environ.get("PYTHONPATH", "")]
    ).rstrip(":")
    try:
        import requests_cache  # noqa: F401
    except ImportError:
        import requests
        module = types.ModuleType("requests_cache")

        class _CachedSession(requests.Session):
            def __init__(self, *args, **kwargs):
                super().__init__()

        module.CachedSession = _CachedSession
        sys.modules["requests_cache"] = module
    return {
        "source": source, "data_root": data_root, "working": working,
        "ckpt_dir": str(ckpt_dir), "log_dir": str(log_dir),
    }


def patch_entrypoint(source: str, data_root: str, working: str = "/kaggle/working") -> str:
    original = Path(source) / "scripts" / "train_lejepa_ablation.py"
    patched = Path(working) / "train_lejepa_ablation_kaggle.py"
    text = original.read_text(encoding="utf-8")
    marker = '    hf_name = "frgfm/imagenette" if name == "imagenette" else name\n'
    insert = (
        f'    data_root = os.environ.get("LEJEPA_DATA_ROOT", {data_root!r})\n'
        '    if data_root and name != "synthetic":\n'
        '        split_name = "validation" if split in {"val", "validation"} else "train"\n'
        '        split_path = Path(data_root) / split_name\n'
        '        if not split_path.exists():\n'
        '            raise FileNotFoundError("Local dataset split not found: " + str(split_path))\n'
        '        return spt.data.HFDataset(str(split_path), transform=transform)\n\n'
    )
    if marker not in text:
        raise RuntimeError("Could not find dataset loading insertion point")
    patched.write_text(text.replace(marker, insert + marker, 1), encoding="utf-8")
    return str(patched)


def install_wheels(source: str) -> None:
    import subprocess
    subprocess.run(f"pip install {source}/wheels/*.whl --no-deps -q", shell=True, check=True)


def gpu_info() -> None:
    import torch
    print(f"PyTorch {torch.__version__} | CUDA {torch.cuda.is_available()}")
    for i in range(torch.cuda.device_count()):
        p = torch.cuda.get_device_properties(i)
        print(f"  GPU {i}: {p.name}  {p.total_memory // 2**20} MB")


def render(spec_key: str, overrides: dict, entrypoint: str, chunk_index=None, chunk_size=None) -> str:
    from scripts.ablations.commands import render_command
    from scripts.ablations.common import CommandOptions
    from scripts.ablations.specs import get_spec

    spec = get_spec(spec_key)
    if chunk_index is not None:
        if chunk_size is None:
            raise ValueError("chunk_size required when chunk_index is set")
        if spec.grid:
            keys = list(spec.grid)
            all_cases = [dict(zip(keys, vals)) for vals in product(*(spec.grid[k] for k in keys))]
        else:
            all_cases = list(spec.cases)
        cases = all_cases[chunk_index * chunk_size : (chunk_index + 1) * chunk_size]
        if not cases:
            raise ValueError(f"{spec_key}: empty chunk {chunk_index}")
        spec = dataclasses.replace(spec, grid={}, cases=cases, key=f"{spec.key}_chunk{chunk_index}")
    spec = dataclasses.replace(spec, overrides={**spec.overrides, **overrides})
    opts = CommandOptions(target=f"python {entrypoint}", multirun=True, smoke=False, env={"HYDRA_FULL_ERROR": "1"})
    return render_command(spec, opts).command
