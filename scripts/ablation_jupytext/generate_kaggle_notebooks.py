"""Generate Kaggle jupytext notebooks from the ablation specs.

Each generated notebook is self-contained: it owns a literal ``OVERRIDES``
dict the user can edit per-spec, then calls ``render`` / ``render_chunk``
from ``_common`` to produce the shell command via ``dataclasses.replace``
(no monkeypatching of ``BASE_OVERRIDES``).
"""

from __future__ import annotations

from pathlib import Path
import sys
import textwrap


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
OUT_SUBDIR = Path("scripts") / "ablation_jupytext"
NOTEBOOK_DIR_REL = OUT_SUBDIR.as_posix()

from scripts.ablations.common import AblationSpec, count_configs  # noqa: E402
from scripts.ablations.specs import list_specs  # noqa: E402


SKIP = {"projector_dims", "reg_tokens"}
INCLUDE = {
    "epps",
    "drop_path",
    "projector_depth",
    "patch_masking",
    "aggregation",
    "sigreg_target",
    "predictor",
    "views",
}
CHUNK_CONFIG = {
    "epps": {"chunk_size": 9, "num_chunks": 3},
    "views": {"chunk_size": 6, "num_chunks": 2},
}

# Default OVERRIDES rendered into every notebook. Users edit the literal dict
# inside the notebook itself; this constant is only the seed.
DEFAULT_OVERRIDES = {
    "dataset_name": "imagenette",
    "backbone": "vit_small_patch16_224",
    "batch_size": 512,
    "max_epochs": 50,
    "resolution": 224,
    "local_resolution": 96,
    "patch_size": 16,
    "num_workers": 4,
    "precision": "bf16-mixed",
    "accelerator": "gpu",
    "devices": 1,
}


HEADER = """# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---
"""


def _md(text: str) -> str:
    return "\n".join(f"# {line}" if line else "#" for line in text.splitlines())


def _format_overrides_literal(overrides: dict) -> str:
    """Pretty-print an OVERRIDES dict the way it should appear in a notebook."""
    lines = ["OVERRIDES = {"]
    for key, value in overrides.items():
        lines.append(f"    {key!r}: {value!r},")
    lines.append("}")
    return "\n".join(lines)


def _base_cells(spec: AblationSpec, num_configs: int) -> str:
    guide = "4. For epps / views: set CHUNK_INDEX in cell [4]."
    if spec.key not in CHUNK_CONFIG:
        guide = "4. Run cell [4] to render and execute the command."
    markdown = f"""# LeJEPA Ablation - {spec.title}
- **Spec key**: `{spec.key}`
- **Question**: {spec.question}
- **Configs**: {num_configs}
- **Status**: {spec.status}

**Instructions**:
1. Adjust `SOURCE` and `HF_CACHE` in cell [1] if your Kaggle slugs differ.
2. First run only: uncomment cell [1b] to install offline wheels.
3. Edit `OVERRIDES` in cell [3] to tune Kaggle-specific params.
{guide}
"""
    overrides_literal = _format_overrides_literal(DEFAULT_OVERRIDES)
    return f"""{HEADER}

# %% [markdown]
{_md(markdown)}

# %% [1] Setup env + sys.path
SOURCE = "/kaggle/input/lejepa-mlproject"
HF_CACHE = "/kaggle/input/lejepa-imagenette-hfcache"

import os
import sys

sys.path.insert(0, SOURCE)
from scripts.ablation_jupytext._common import setup_kaggle_env

paths = setup_kaggle_env(source=SOURCE, hf_cache=HF_CACHE, spec_key="{spec.key}")
print("Setup OK:", paths)

# %% [1b] Install wheels (UNCOMMENT first run, then comment again)
# !pip install {{SOURCE}}/wheels/*.whl --no-deps -q && echo "Wheels installed"

# %% [2] GPU check
import torch

print(f"PyTorch {{torch.__version__}} | CUDA {{torch.cuda.is_available()}}")
for i in range(torch.cuda.device_count()):
    props = torch.cuda.get_device_properties(i)
    print(f"  GPU {{i}}: {{props.name}}  {{props.total_memory // 2**20}} MB")

# %% [3] Edit per-spec overrides here (replaces baseline BASE_OVERRIDES values)
{overrides_literal}

# %% [4] Render command
"""


def _execute_cells(spec_key: str) -> str:
    return f"""

# %% [5] Execute
import subprocess

print("Running:")
print(command)
ret = subprocess.run(command, shell=True, check=False)
print(f"Exit code: {{ret.returncode}}")

# %% [6] Dump CSV summary
# !python -m stable_pretraining.cli dump-csv-logs {{paths['log_dir']}} ablation_{spec_key} max
"""


def _chunk_block(spec: AblationSpec, num_configs: int) -> str:
    chunk_size = CHUNK_CONFIG[spec.key]["chunk_size"]
    num_chunks = CHUNK_CONFIG[spec.key]["num_chunks"]
    return f"""CHUNK_INDEX = 0
CHUNK_SIZE = {chunk_size}
NUM_CHUNKS = {num_chunks}

from scripts.ablation_jupytext._common import render_chunk

if not 0 <= CHUNK_INDEX < NUM_CHUNKS:
    raise ValueError(f"CHUNK_INDEX must be in 0..{{NUM_CHUNKS - 1}}")

command = render_chunk("{spec.key}", OVERRIDES, CHUNK_INDEX, CHUNK_SIZE)
print(f"# {spec.key} chunk {{CHUNK_INDEX}}/{{NUM_CHUNKS - 1}} of {num_configs} total configs")
"""


def _nochunk_block(spec: AblationSpec, num_configs: int) -> str:
    return f"""from scripts.ablation_jupytext._common import render

command = render("{spec.key}", OVERRIDES)
print("# Configs: {num_configs}")
"""


def render_one(spec: AblationSpec) -> str:
    num_configs = count_configs(spec)
    block = (
        _chunk_block(spec, num_configs)
        if spec.key in CHUNK_CONFIG
        else _nochunk_block(spec, num_configs)
    )
    return textwrap.dedent(
        _base_cells(spec, num_configs) + block + _execute_cells(spec.key)
    ).strip() + "\n"


def main() -> None:
    out_dir = ROOT / OUT_SUBDIR
    out_dir.mkdir(parents=True, exist_ok=True)
    for spec in list_specs():
        if spec.key in SKIP:
            continue
        if spec.key not in INCLUDE:
            continue
        path = out_dir / f"kaggle_{spec.key}.py"
        path.write_text(render_one(spec), encoding="utf-8")
        print(f"wrote {NOTEBOOK_DIR_REL}/kaggle_{spec.key}.py")


if __name__ == "__main__":
    main()
