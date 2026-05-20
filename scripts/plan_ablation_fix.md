# Plan: Chuyển `scripts/generated/*.sh` thành Kaggle jupytext notebooks

## 0. Mục tiêu

Sinh **6 file jupytext** trong thư mục `kaggle/`, mỗi file = 1 ablation spec
"ready", để chạy trên Kaggle GPU. Không động vào bất kỳ module gốc nào
(`scripts/ablations/`, `scripts/train_lejepa_ablation.py`,
`stable-pretraining/`).

## 1. Quyết định đã chốt

| Mục | Giá trị | Ghi chú |
|---|---|---|
| Backbone | `vit_small_patch16_224` | ViT-S/16, ~22M params |
| Patch size | `16` | khớp backbone |
| Batch size | `512` | phù hợp RTX Pro 6000 96GB; có thể nâng `1024` nếu cần |
| Max epochs | `50` | giữ như plan gốc, ViT-S nhanh hơn nhiều ViT-L |
| Resolution | `224` global, `96` local | khớp ViT-S/16 |
| Precision | `bf16-mixed` | RTX Pro 6000 hỗ trợ bf16 native |
| Accelerator / devices | `gpu` / `1` | single-GPU |
| Multi-crop | `n_views=8`, `n_global_views=2` | giữ baseline |
| Dataset | đã upload lên `/kaggle/input/...` | format & slug do user nhập vào biến `DATA_SOURCE` trong notebook |
| Monkeypatch | `BASE_OVERRIDES.update(KAGGLE_OVERRIDES)` tại runtime | không sửa `specs.py` |
| Blocked specs | **SKIP cả 2** (`projector_dims`, `reg_tokens`) | xem §5 phân tích rủi ro |
| Logger | W&B offline + CSV | sync sau session |
| Sweep splitting | có chunk control cho `epps` và `views` | xem §4 |

## 2. Cấu trúc thư mục output

```
lejepa-MLProject/
├── kaggle/                              ← THƯ MỤC MỚI, KHÔNG đụng nơi khác
│   ├── README.md                        ← hướng dẫn upload, dataset slug, workflow
│   ├── _common.py                       ← helper dùng chung (env, paths, KAGGLE_OVERRIDES, render)
│   ├── generate_kaggle_notebooks.py     ← script sinh 6 jupytext từ specs.py
│   ├── kaggle_epps.py                   ← 6 file jupytext sinh ra
│   ├── kaggle_drop_path.py
│   ├── kaggle_projector_depth.py
│   ├── kaggle_patch_masking.py
│   ├── kaggle_aggregation.py
│   ├── kaggle_sigreg_target.py
│   ├── kaggle_predictor.py
│   └── kaggle_views.py
└── scripts/generated/                   ← KHÔNG đụng vào
```

## 3. `kaggle/_common.py` — helper chung

Helper này được import từ mỗi notebook, gom logic lặp lại:

```python
# kaggle/_common.py
"""Helper chung cho các Kaggle ablation notebooks. KHÔNG sửa file này khi chạy."""
from __future__ import annotations
import os, sys, types
from pathlib import Path

# -------- Đường dẫn Kaggle (override trong notebook nếu khác) --------
DEFAULT_SOURCE = "/kaggle/input/lejepa-mlproject"
DEFAULT_HF_CACHE = "/kaggle/input/lejepa-imagenette-hfcache"
DEFAULT_WORKING = "/kaggle/working"

# -------- Scale-down baseline cho RTX Pro 6000 96GB --------
KAGGLE_OVERRIDES = dict(
    dataset_name="imagenette",
    backbone="vit_small_patch16_224",
    batch_size=512,
    max_epochs=50,
    resolution=224,
    local_resolution=96,
    patch_size=16,
    num_workers=4,
    precision="bf16-mixed",
    accelerator="gpu",
    devices=1,
)


def setup_kaggle_env(
    source: str = DEFAULT_SOURCE,
    hf_cache: str = DEFAULT_HF_CACHE,
    working: str = DEFAULT_WORKING,
    spec_key: str = "ablation",
) -> dict:
    """Cài env vars + sys.path + requests_cache stub. Trả dict path đã setup."""
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

    # Insert paths so we can import stable_pretraining + scripts.ablations
    for p in [f"{source}/stable-pretraining", source]:
        if p not in sys.path:
            sys.path.insert(0, p)

    # Stub requests_cache nếu Kaggle Python thiếu
    try:
        import requests_cache  # noqa: F401
    except ImportError:
        import requests
        m = types.ModuleType("requests_cache")
        class _CachedSession(requests.Session):
            def __init__(self, *a, **kw):
                super().__init__()
        m.CachedSession = _CachedSession
        sys.modules["requests_cache"] = m

    return {
        "source": source,
        "hf_cache": hf_cache,
        "working": working,
        "ckpt_dir": str(ckpt_dir),
        "log_dir": str(log_dir),
    }


def apply_kaggle_overrides(extra: dict | None = None) -> dict:
    """Monkeypatch BASE_OVERRIDES bằng KAGGLE_OVERRIDES tại runtime.

    QUAN TRỌNG: mutation in-memory; không ghi vào specs.py.
    Trả về snapshot trước-mutation để rollback nếu cần.
    """
    from scripts.ablations import specs as _specs
    snapshot = dict(_specs.BASE_OVERRIDES)
    _specs.BASE_OVERRIDES.update(KAGGLE_OVERRIDES)
    if extra:
        _specs.BASE_OVERRIDES.update(extra)
    return snapshot


def render_spec_command(spec_key: str, smoke: bool = False) -> str:
    """Render 1 spec ra shell command, dùng renderer gốc."""
    from scripts.ablations.specs import get_spec
    from scripts.ablations.commands import render_command
    from scripts.ablations.common import CommandOptions

    spec = get_spec(spec_key)
    opts = CommandOptions(
        target="scripts/train_lejepa_ablation.py",
        multirun=True,
        smoke=smoke,
        env={"HYDRA_FULL_ERROR": "1"},
    )
    return render_command(spec, opts).command


def slice_grid_for_chunk(spec_key: str, chunk_index: int, chunk_size: int):
    """Trả về grid mới chỉ gồm chunk thứ `chunk_index` (cho sweep dài).

    Implementation:
    - Lấy spec.grid (dict[str, list]).
    - Tính product cartesian → list of (k1=v1, k2=v2, ...).
    - Slice [chunk_index*chunk_size : (chunk_index+1)*chunk_size].
    - Trả về list các dict overrides riêng để render từng command 1.
    """
    from itertools import product
    from scripts.ablations.specs import get_spec
    spec = get_spec(spec_key)
    if spec.grid:
        keys = list(spec.grid.keys())
        all_combos = [
            dict(zip(keys, values))
            for values in product(*(spec.grid[k] for k in keys))
        ]
    elif spec.cases:
        all_combos = list(spec.cases)
    else:
        return []
    start = chunk_index * chunk_size
    return all_combos[start : start + chunk_size]
```

## 4. Template `kaggle/kaggle_<spec>.py`

Mỗi file jupytext có 7-8 cell, generator tự điền `<spec_key>`,
`<spec_title>`, `<num_configs>`, `<chunk_block>`:

```python
# ---
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

# %% [markdown]
# # LeJEPA Ablation — <spec_title>
# - **Spec key**: `<spec_key>`
# - **Question**: <spec.question>
# - **Configs**: <num_configs>
# - **Status**: <spec.status>
#
# **Hướng dẫn**:
# 1. Adjust `SOURCE`, `HF_CACHE` ở cell [1] nếu Kaggle slug khác mặc định.
# 2. Lần đầu: uncomment cell [1b] để cài wheels.
# 3. Với `epps` / `views`: chọn `CHUNK_INDEX` ở cell [4].

# %% [1] Setup env + sys.path
SOURCE   = "/kaggle/input/lejepa-mlproject"          # ← EDIT nếu slug khác
HF_CACHE = "/kaggle/input/lejepa-imagenette-hfcache" # ← EDIT nếu slug khác

import sys, os
sys.path.insert(0, f"{SOURCE}")
from kaggle._common import setup_kaggle_env, apply_kaggle_overrides
paths = setup_kaggle_env(source=SOURCE, hf_cache=HF_CACHE, spec_key="<spec_key>")
print("Setup OK:", paths)

# %% [1b] Install wheels (UNCOMMENT lần đầu, comment lại các lần sau)
# !pip install {SOURCE}/wheels/*.whl --no-deps -q && echo "Wheels installed"

# %% [2] GPU check
import torch
print(f"PyTorch {torch.__version__} | CUDA {torch.cuda.is_available()}")
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    print(f"  GPU {i}: {p.name}  {p.total_memory // 2**20} MB")

# %% [3] Apply Kaggle overrides (monkeypatch BASE_OVERRIDES runtime)
snapshot = apply_kaggle_overrides()
print("BASE_OVERRIDES patched. Snapshot saved for rollback.")

# %% [4] Render command  <-- generator tự chèn chunk-block nếu cần
<chunk_block>

# %% [5] Execute
import subprocess
print("Running:")
print(command)
ret = subprocess.run(command, shell=True, check=False)
print(f"Exit code: {ret.returncode}")

# %% [6] Dump CSV summary
# !python -m stable_pretraining.cli dump-csv-logs {paths['log_dir']} ablation_<spec_key> max
```

**`<chunk_block>` cho spec không cần chunk** (drop_path, projector_depth,
patch_masking, aggregation, sigreg_target, predictor):
```python
from kaggle._common import render_spec_command
command = render_spec_command("<spec_key>")
print(f"# Configs: <num_configs>")
```

**`<chunk_block>` cho spec cần chunk** (epps: 27 → 3 chunks × 9;
views: 11 → 2 chunks × 6):
```python
CHUNK_INDEX = 0    # ← chọn 0..(num_chunks-1) mỗi session
CHUNK_SIZE  = 9    # epps; views dùng 6

from kaggle._common import slice_grid_for_chunk
from scripts.ablations.specs import get_spec
from scripts.ablations.commands import render_command
from scripts.ablations.common import CommandOptions, AblationSpec

spec_full = get_spec("<spec_key>")
combos = slice_grid_for_chunk("<spec_key>", CHUNK_INDEX, CHUNK_SIZE)
print(f"Chunk {CHUNK_INDEX}: {len(combos)} configs")

# Build sub-spec for renderer
sub_spec = AblationSpec(
    key=f"<spec_key>_chunk{CHUNK_INDEX}",
    title=spec_full.title,
    question=spec_full.question,
    priority=spec_full.priority,
    grid={},
    cases=combos,
    overrides=spec_full.overrides,
    requires=spec_full.requires,
    status=spec_full.status,
    expected=spec_full.expected,
    notes=spec_full.notes,
)
opts = CommandOptions(
    target="scripts/train_lejepa_ablation.py",
    multirun=True,
    smoke=False,
    env={"HYDRA_FULL_ERROR": "1"},
)
command = render_command(sub_spec, opts).command
```

> **Lưu ý**: `AblationSpec` hiện có validation `grid` XOR `cases`. Nếu spec
> gốc dùng `grid`, ta convert sang `cases` (đã liệt kê cartesian). Validator
> hợp lệ vì ta chỉ truyền `cases`. Không sửa dataclass.

## 5. Phân tích rủi ro 2 blocked specs

### `projector_dims` (10 configs)
- **Vấn đề**: grid có `embedding_dim` [512, 2048] nhưng LeJEPA lấy
  `embed_dim` từ timm tự động. Override sẽ bị bỏ silent → 5 cặp
  `(embedding_dim, projector_dim)` thực ra trùng nhau, tốn x2 GPU-hours
  cho kết quả lặp.
- **Rủi ro**: TỐN tiền compute, kết quả vô nghĩa, dễ misinterpret.
- **Quyết định**: **SKIP**. Document trong README rằng cần thêm
  `embedding_dim` arg vào `LeJEPA.__init__` trước (việc này thuộc kế hoạch
  Phase 4 trong `ablation_code_plan.md`).

### `reg_tokens` (5 configs)
- **Vấn đề**: `_check_timm_reg_token_support()` check tại import time với
  backbone trong `BASE_OVERRIDES["backbone"]`. Hiện check với
  `vit_large_patch14_224` → fail. Nếu monkeypatch sang `vit_small_patch16_224`
  **sau** import thì check không re-run, spec vẫn ở status `needs_model_support`.
- **Rủi ro**: Nếu force chạy, có 2 khả năng:
  - (a) timm vit_small_patch16_224 chấp nhận reg_tokens → chạy OK
  - (b) timm raise TypeError → crash giữa multirun, lãng phí compute trước đó
- **Quyết định**: **SKIP**. Nếu muốn enable sau, có 2 cách KHÔNG sửa
  modules: (1) override `BASE_OVERRIDES["backbone"]` **trước** import specs
  (nhưng specs.py chạy `_check` ở module-load time → vẫn check ViT-L), hoặc
  (2) force status ready bằng `get_spec("reg_tokens")._replace(status="ready")`
  — nhưng `AblationSpec` là frozen dataclass nên cũng không trivial.
  → Việc enable đúng cần sửa specs.py để check lazy hoặc nhận backbone arg.
  Đó là model-support work, không thuộc scope chuyển .sh → notebook.

→ Generator **chỉ sinh 8 file** ban đầu: `epps, drop_path, projector_depth,
patch_masking, aggregation, sigreg_target, predictor, views`. Không sinh
`projector_dims` và `reg_tokens`. README ghi rõ lý do.

Wait — tôi đếm lại: 10 specs gốc, skip 2 = **8 file**. Đúng số .sh trong
`scripts/generated/`. Sửa §0 cho khớp.

## 6. `kaggle/generate_kaggle_notebooks.py`

Script này chạy LOCAL (không phải trên Kaggle) để regenerate các file
jupytext khi `specs.py` thay đổi:

```python
"""Sinh kaggle/kaggle_<spec>.py từ specs.py. Chạy lại khi spec thay đổi."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ablations.specs import list_specs

SKIP = {"projector_dims", "reg_tokens"}  # xem plan §5
CHUNK_CONFIG = {
    "epps":  {"chunk_size": 9},   # 27 / 9 = 3 chunks
    "views": {"chunk_size": 6},   # 11 / 6 = 2 chunks
}

TEMPLATE_NOCHUNK = """..."""  # đầy đủ template từ §4
TEMPLATE_CHUNK   = """..."""  # đầy đủ template chunk-block

def render_one(spec) -> str:
    title = spec.title
    key   = spec.key
    nconf = ...  # count from grid or cases
    if key in CHUNK_CONFIG:
        return TEMPLATE_CHUNK.format(spec_key=key, spec_title=title, num_configs=nconf, chunk_size=CHUNK_CONFIG[key]["chunk_size"], ...)
    return TEMPLATE_NOCHUNK.format(spec_key=key, spec_title=title, num_configs=nconf, ...)

def main():
    out_dir = ROOT / "kaggle"
    out_dir.mkdir(exist_ok=True)
    for spec in list_specs():
        if spec.key in SKIP:
            continue
        (out_dir / f"kaggle_{spec.key}.py").write_text(render_one(spec))
        print(f"wrote kaggle/kaggle_{spec.key}.py")

if __name__ == "__main__":
    main()
```

## 7. `kaggle/README.md` content checklist

Tối thiểu phải có:
1. Mục đích, link sang `scripts/ablation_plan.md` và `plan_ablation_fix.md`
2. **Kaggle dataset cần upload**:
   - `lejepa-mlproject`: chứa `lejepa/`, `stable-pretraining/`, `scripts/`,
     `kaggle/`, `wheels/`
   - `lejepa-imagenette-hfcache`: chứa `frgfm___imagenette/...` (HF cache)
3. **Cách build wheels offline**:
   ```bash
   pip wheel -r requirements.txt -w wheels/ --no-deps
   ```
4. **Workflow**:
   - Mở 1 notebook (vd `kaggle_drop_path.py`)
   - Run cell [1b] một lần để cài wheels
   - Run các cell tiếp theo
   - Sau khi xong: download `/kaggle/working/` về local; `wandb sync ./wandb/offline-*`
5. **Specs bị skip** + lý do (§5 plan này)
6. **Bảng ước lượng thời gian** trên RTX Pro 6000:
   | Spec | Configs | Time/config | Total |
   |---|---|---|---|
   | drop_path | 5 | ~30 phút | ~2.5h |
   | projector_depth | 4 | ~30 phút | ~2h |
   | aggregation | 3 | ~30 phút | ~1.5h |
   | sigreg_target | 3 | ~35 phút | ~1.7h |
   | predictor | 3 | ~30 phút | ~1.5h |
   | patch_masking | 6 | ~30 phút | ~3h |
   | views | 11 (2 chunks) | ~30 phút | ~5.5h (2.7h/chunk) |
   | epps | 27 (3 chunks) | ~30 phút | ~13.5h (4.5h/chunk) |

   _(estimate dựa trên ViT-S/16 @ batch 512 × 8 views × imagenette 28K trên
   RTX Pro 6000 96GB bf16; cần đo lại sau lần chạy thật đầu tiên)_
7. **Regenerate notebooks** sau khi sửa `specs.py`:
   ```bash
   python kaggle/generate_kaggle_notebooks.py
   ```

## 8. Acceptance criteria (codex phải verify)

1. `python kaggle/generate_kaggle_notebooks.py` chạy không lỗi, sinh đúng
   8 file `kaggle/kaggle_*.py`.
2. Mỗi file `kaggle/kaggle_*.py` parse được bằng jupytext:
   ```bash
   pip install jupytext  # nếu chưa
   for f in kaggle/kaggle_*.py; do
     jupytext --to notebook "$f" --output /tmp/test.ipynb && rm /tmp/test.ipynb
   done
   ```
3. Smoke test offline (CPU, không Kaggle):
   ```bash
   cd <repo>
   python -c "
   import sys; sys.path.insert(0, '.')
   from kaggle._common import apply_kaggle_overrides, render_spec_command
   apply_kaggle_overrides()
   for key in ['epps','drop_path','projector_depth','patch_masking',
              'aggregation','sigreg_target','predictor','views']:
       cmd = render_spec_command(key)
       assert 'vit_small_patch16_224' in cmd
       assert 'imagenette' in cmd
       assert 'batch_size=512' in cmd
       print(key, 'OK')
   "
   ```
4. `scripts/ablations/`, `scripts/train_lejepa_ablation.py`,
   `stable-pretraining/` **không có thay đổi** (verify bằng
   `git status` / `git diff --stat`).
5. `kaggle/README.md` mô tả đủ workflow và dataset slug placeholder.

## 9. Files codex sẽ tạo (KHÔNG file nào sửa)

- `kaggle/__init__.py` (empty, để import được `from kaggle._common ...`)
- `kaggle/_common.py`
- `kaggle/generate_kaggle_notebooks.py`
- `kaggle/README.md`
- `kaggle/kaggle_{epps,drop_path,projector_depth,patch_masking,aggregation,sigreg_target,predictor,views}.py`

Tổng: **11 file mới**, 0 file sửa.

## 10. Out-of-scope (nói rõ để codex không lan)

- KHÔNG sửa `scripts/ablations/specs.py` để enable reg_tokens
- KHÔNG sửa `scripts/train_lejepa_ablation.py` để thêm `data_root` /
  ImageFolder
- KHÔNG sửa `stable-pretraining/` để add embedding_dim hay projector args
- KHÔNG build wheels (đó là việc thủ công của user)
- KHÔNG upload Kaggle dataset (việc thủ công của user)
- KHÔNG viết job runner / submit script (sẽ làm phase sau)
