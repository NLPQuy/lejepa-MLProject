"""Generate slim Kaggle jupytext notebooks, one per ablation spec."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.ablations.common import AblationSpec, count_configs  # noqa: E402
from scripts.ablations.specs import list_specs  # noqa: E402

OUT_DIR = ROOT / "scripts" / "ablation_jupytext"
INCLUDE = {"epps", "drop_path", "projector_depth", "patch_masking", "aggregation", "sigreg_target", "predictor", "views"}
CHUNKS = {"epps": (9, 3), "views": (6, 2)}
DEFAULT_OVERRIDES = {
    "dataset_name": "imagenet10",
    "backbone": "vit_small_patch16_224",
    "batch_size": 512,
    "max_epochs": 100,
    "resolution": 224,
    "local_resolution": 96,
    "patch_size": 0,
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


def _overrides_literal(d: dict) -> str:
    return "OVERRIDES = {\n" + "\n".join(f"    {k!r}: {v!r}," for k, v in d.items()) + "\n}"


def _render_cell(spec: AblationSpec, n: int) -> str:
    if spec.key not in CHUNKS:
        return f'command = render(SPEC_KEY, OVERRIDES, ENTRYPOINT)\nprint("# {spec.key}: {n} configs")'
    chunk_size, num_chunks = CHUNKS[spec.key]
    return f"""CHUNK_INDEX, CHUNK_SIZE, NUM_CHUNKS = 0, {chunk_size}, {num_chunks}
command = render(
    SPEC_KEY, OVERRIDES, ENTRYPOINT,
    chunk_index=CHUNK_INDEX, chunk_size=CHUNK_SIZE,
)
print(f"# {{SPEC_KEY}} chunk {{CHUNK_INDEX}}/{{NUM_CHUNKS - 1}} of {n} configs")"""


def render_one(spec: AblationSpec) -> str:
    n, chunked = count_configs(spec), spec.key in CHUNKS
    guide = "4. Set `CHUNK_INDEX` in cell [4]." if chunked else "4. Run cell [4] to render the command."
    md = f"""# LeJEPA Ablation - {spec.title}
- **Spec key**: `{spec.key}`
- **Question**: {spec.question}
- **Configs**: {n}
- **Status**: {spec.status}

**Instructions**:
1. Adjust `SOURCE` / `DATA_ROOT` in cell [1] if your Kaggle slugs differ.
2. First run only: uncomment `install_wheels(SOURCE)` in cell [1b].
3. Edit `OVERRIDES` in cell [3].
{guide}
"""
    return f"""{HEADER}# %% [markdown]
{_md(md)}

# %%
# [1] Setup
SOURCE = "/kaggle/input/lejepa-mlproject"
DATA_ROOT = "/kaggle/input/lejepa-data/data/imagenet10"
SPEC_KEY = "{spec.key}"

import sys
sys.path.insert(0, SOURCE)
from scripts.ablation_jupytext.kaggle_setup import setup, patch_entrypoint, install_wheels, gpu_info, render

paths = setup(SOURCE, DATA_ROOT, spec_key=SPEC_KEY)
ENTRYPOINT = patch_entrypoint(SOURCE, DATA_ROOT)
print("Setup OK:", paths)
print("Patched entrypoint:", ENTRYPOINT)

# %%
# [1b] First-run only: install offline wheels
# install_wheels(SOURCE)

# %%
# [2] GPU check
gpu_info()

# %%
# [3] Edit per-spec overrides
{_overrides_literal(DEFAULT_OVERRIDES)}

# %%
# [4] Render command
{_render_cell(spec, n)}

# %%
# [5] Execute
import subprocess
print("Running:")
print(command)
ret = subprocess.run(command, shell=True, check=False)
print(f"Exit code: {{ret.returncode}}")
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in list_specs():
        if spec.key in INCLUDE:
            path = OUT_DIR / f"kaggle_{spec.key}.py"
            path.write_text(render_one(spec), encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
