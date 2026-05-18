# LeJEPA Ablation Coding Plan

## 0. Mục tiêu của file này

File này là plan để biến `scripts/ablation_plan.md` từ một tập hợp command markdown rời rạc thành một pipeline ablation có thể chạy, kiểm tra, tái sử dụng và mở rộng.

Plan không chỉ nói "chạy lệnh nào", mà mô tả:

- Cần tổ chức code ở đâu.
- Cần viết thành phần nào trước.
- Thành phần nào nên tái sử dụng từ `stable-pretraining`.
- Thành phần nào cần thêm vào `LeJEPA`.
- Script nào sinh command.
- Script nào chạy sweep.
- Script nào gom kết quả.
- Cách tránh viết lại training pipeline.
- Cách kiểm tra từng bước trước khi tốn GPU.

Nguyên tắc chính: **không tạo một training framework thứ hai**. Ablation phải là lớp cấu hình mỏng bọc quanh pipeline hiện có.

---

## 1. Hiện trạng repo sau khi quét

### 1.1. Code package chính

Root package:

- `lejepa/`
- `tests/`
- `pyproject.toml`
- `setup.py`

Package này cung cấp statistical tests:

- `lejepa.univariate.EppsPulley`
- `lejepa.multivariate.SlicingUnivariateTest`
- các test univariate/multivariate khác

Đây là package loss/statistics gọn. Không nên nhồi ablation runner lớn vào package này.

### 1.2. Training harness

Training harness nằm trong:

- `stable-pretraining/`
- package import là `stable_pretraining`

Các phần quan trọng:

- `stable_pretraining.methods.lejepa.LeJEPA`
- `stable_pretraining.Module`
- `stable_pretraining.Manager`
- `stable_pretraining.data`
- `stable_pretraining.callbacks`
- `stable_pretraining.run`
- CLI `spt run`

Pipeline hiện tại đã có:

- Lightning `Trainer`
- manual optimization
- Hydra-compatible runner
- DataModule
- transforms
- callbacks
- KNN/probe callbacks
- timm backbone wrappers

Do đó ablation code nên reuse `stable-pretraining`.

### 1.3. Ablation docs hiện tại

Hiện có:

- `scripts/ablation_plan.md`
- `scripts/launch_epps_ablation.md`
- `scripts/launch_proj_ablation.md`
- `scripts/launch_rtokens_ablation.md`
- `scripts/launch_views_ablation.md`
- `scripts/launch_inet10.py`

Các file markdown đang chứa command thủ công.

Vấn đề:

- nhiều command trỏ `scripts/je.py`, nhưng file này không có trong tree hiện tại.
- nhiều command dùng `inet1k`, `100 epochs`, `teacher_student=true`.
- plan tổng lại nói dùng `inet100`, `50 epochs`, `teacher_student=false`.
- các knob mới như `sigreg_target`, `predictor`, `aggregator`, `projector_arch=MLP2/MLP4` chưa được `LeJEPA` hỗ trợ trực tiếp.
- `patch_mask_ratio` có code hỗ trợ masking trong `stable-pretraining`, nhưng `LeJEPA` hiện gọi `timm.create_model` trực tiếp, không dùng `MaskedEncoder`.
- `reg_tokens` có support trong backbone utils, nhưng `LeJEPA` hiện chưa truyền `reg_tokens` vào `timm.create_model`.

Kết luận: cần code hóa ablation ở 2 lớp:

- lớp runner/spec: sinh config/command nhất quán.
- lớp model/config support: thêm các option thật vào `LeJEPA` hoặc adapter quanh `LeJEPA`.

---

## 2. Mục tiêu kỹ thuật

### 2.1. Mục tiêu tối thiểu

Sau khi implement xong, ta cần chạy được:

```bash
python scripts/ablations.py list
python scripts/ablations.py show patch_masking
python scripts/ablations.py render patch_masking
python scripts/ablations.py render all
```

Và output là các command hợp lệ theo pipeline hiện có.

### 2.2. Mục tiêu tốt hơn

Có thêm:

```bash
python scripts/ablations.py write-scripts
python scripts/ablations.py write-configs
python scripts/ablations.py dry-run patch_masking
python scripts/ablations.py summarize logs/
```

### 2.3. Mục tiêu không làm trong phase đầu

Không viết lại:

- dataloader riêng
- trainer riêng
- wandb logger riêng
- checkpoint manager riêng
- KNN evaluator riêng nếu callback hiện có dùng được

Không cố gắng:

- chạy toàn bộ ablation ngay trong một Python process.
- tự spawn multi-GPU jobs nếu Hydra/Submitit đã đủ dùng.
- viết config DSL quá phức tạp.

---

## 3. Nguyên tắc thiết kế

### 3.1. Single source of truth

Baseline config phải nằm ở một chỗ.

Ví dụ:

```python
BASE_OVERRIDES = {
    "method": "lejepa",
    "dataset_name": "inet100",
    "max_epochs": 50,
    "backbone": "vit_large_patch14_224",
    "batch_size": 512,
    "lr": 5e-4,
    "weight_decay": 5e-2,
    "bstat_lambda": 0.05,
    "bstat_num_slices": 1024,
    "bstat_t_max": 3.0,
    "bstat_n_points": 17,
    "embedding_dim": 512,
    "projector_dim": 512,
    "projector_arch": "MLP",
    "teacher_student": False,
    "n_views": 8,
    "n_global_views": 2,
    "drop_path_rate": 0.1,
    "multi_crop": True,
    "resolution": 238,
    "local_resolution": 98,
    "patch_size": 14,
    "patch_mask_ratio": 0.3,
    "autostop": False,
}
```

Tất cả ablation chỉ override key khác baseline.

### 3.2. Ablation spec phải khai báo metadata

Mỗi ablation cần có:

- id
- name
- question
- priority
- implementation status
- dependent code support
- grid
- expected configs count
- notes

Không chỉ có command string.

### 3.3. Render command, không viết command thủ công

Command markdown hiện tại dễ drift.

Nên sinh command từ spec:

```bash
python scripts/ablations.py render epps
```

Script sẽ render:

```bash
HYDRA_FULL_ERROR=1 python -m stable_pretraining.run ...
```

hoặc:

```bash
spt run configs/lejepa_inet100.yaml ...
```

### 3.4. Tách "supported now" và "requires code"

Không phải ablation nào cũng chạy được ngay.

Ví dụ:

- Epps params: gần như supported bởi `LeJEPA(n_slices,t_max,n_points,lamb)`.
- Drop path: supported bởi `LeJEPA(drop_path_rate=...)`.
- Projector dims: supported nếu truyền projector custom.
- Projector depth: cần builder.
- Patch masking: cần model path dùng `MaskedEncoder`.
- Aggregator: cần backbone feature extraction support.
- SIGReg target: cần sửa loss.
- Predictor: cần thêm head và loss path.

Spec cần có trường:

```python
requires = ["lejepa.projector_builder", "lejepa.sigreg_target"]
status = "blocked"
```

### 3.5. Tái sử dụng `stable_pretraining.run`

Entry point nên là:

```bash
python -m stable_pretraining.run --config-path ... --config-name ...
```

hoặc CLI:

```bash
spt run path/to/config.yaml ...
```

Không nên phục hồi `scripts/je.py` theo kiểu copy/paste nếu `stable_pretraining.run` đã làm cùng vai trò.

### 3.6. Test nhỏ trước GPU

Mỗi feature mới phải có test CPU/smoke:

- instantiate model
- forward 2 global + 2 local views
- check loss finite
- check embedding shape
- check gradients exist

Không đợi 50 epochs mới biết `predictor="mlp"` hỏng.

---

## 4. Cấu trúc file đề xuất

### 4.1. Minimal structure

Đề xuất tạo:

```text
scripts/
  ablations.py
  ablations/
    __init__.py
    specs.py
    render.py
    validate.py
    summarize.py
```

Nếu muốn ít file hơn ở phase 1:

```text
scripts/
  ablations.py
```

Nhưng nên tách sớm vì plan có nhiều ablation.

### 4.2. Preferred structure

Nên dùng:

```text
scripts/
  ablations.py
  ablations/
    __init__.py
    common.py
    specs.py
    commands.py
    configs.py
    results.py
```

Vai trò:

- `scripts/ablations.py`: CLI mỏng.
- `scripts/ablations/common.py`: dataclass và helper chung.
- `scripts/ablations/specs.py`: khai báo baseline + ablation grid.
- `scripts/ablations/commands.py`: render command shell/Hydra.
- `scripts/ablations/configs.py`: render YAML nếu chọn config-file route.
- `scripts/ablations/results.py`: gom CSV/W&B logs sau này.

### 4.3. Không đặt trong `lejepa/`

Không nên tạo:

```text
lejepa/ablations/
```

Lý do:

- ablation runner là research orchestration, không phải public library API.
- nó phụ thuộc `stable-pretraining`, Hydra, datasets, W&B.
- package root `lejepa` nên giữ nhỏ.

### 4.4. Không đặt trong `stable-pretraining/`

Không nên đặt ablation project-specific vào package vendored nếu không cần.

Lý do:

- `stable-pretraining` là training harness chung.
- ablation plan này thuộc LeJEPA paper/repo.
- chỉ sửa `stable-pretraining` khi cần thêm capability generic cho method.

---

## 5. Dataclass design

### 5.1. `GridValue`

Có thể chưa cần class riêng.

Grid có thể là:

```python
dict[str, list[object]]
```

Ví dụ:

```python
grid = {
    "method.n_slices": [512, 1024, 4096],
    "method.t_max": [1, 3, 5],
    "method.n_points": [5, 17, 41],
}
```

### 5.2. `AblationSpec`

Nên có:

```python
@dataclass(frozen=True)
class AblationSpec:
    key: str
    title: str
    question: str
    priority: int
    grid: dict[str, list[Any]]
    overrides: dict[str, Any] = field(default_factory=dict)
    requires: tuple[str, ...] = ()
    status: str = "ready"
    expected: str = ""
    notes: tuple[str, ...] = ()
```

Giải thích:

- `key`: dùng CLI, ví dụ `epps`, `patch_masking`.
- `title`: in ra markdown/script.
- `question`: context nghiên cứu.
- `priority`: dùng sort.
- `grid`: các biến sweep.
- `overrides`: override riêng không phải sweep.
- `requires`: capability cần có trong code.
- `status`: `ready`, `needs_model_support`, `needs_config_support`, `blocked`.
- `expected`: expected outcome.
- `notes`: notes implementation.

### 5.3. `RunBackend`

Nên hỗ trợ 2 mode:

```python
class Backend(str, Enum):
    STABLE_PRETRAINING_RUN = "stable_pretraining.run"
    SPT_CLI = "spt"
```

Phase đầu có thể chỉ hỗ trợ `stable_pretraining.run`.

### 5.4. `CommandOptions`

```python
@dataclass(frozen=True)
class CommandOptions:
    config_path: str
    config_name: str
    launcher: str | None = None
    multirun: bool = True
    env: dict[str, str] = field(default_factory=lambda: {"HYDRA_FULL_ERROR": "1"})
```

### 5.5. `RenderedCommand`

```python
@dataclass(frozen=True)
class RenderedCommand:
    spec_key: str
    command: str
    num_configs: int
    status: str
    warnings: tuple[str, ...]
```

### 5.6. Vì sao dùng dataclass

Ưu điểm:

- dễ test.
- dễ serialize.
- dễ render markdown.
- tránh string command hardcode.
- dễ validate số configs.

---

## 6. Mapping config keys

### 6.1. Vấn đề hiện tại

Markdown dùng flat Hydra override:

```text
++bstat_num_slices=1024
++backbone="vit_large_patch14_224"
++dataset_name="inet100"
```

Nhưng `stable_pretraining.run` config thực tế có thể là nested:

```text
module.n_slices=1024
module.encoder_name=vit_large_patch14_224
trainer.max_epochs=50
```

Do đó cần quyết định route:

- route A: viết config YAML tương thích `stable_pretraining.run`.
- route B: tạo compatibility script nhận old flat keys và build objects.

### 6.2. Khuyến nghị route A

Viết config YAML chuẩn `stable_pretraining.run`.

Ví dụ:

```yaml
seed: 42
matmul_precision: high

module:
  _target_: stable_pretraining.methods.lejepa.LeJEPA
  encoder_name: vit_large_patch14_224
  lamb: 0.05
  n_slices: 1024
  t_max: 3.0
  n_points: 17
  pretrained: false
  drop_path_rate: 0.1

trainer:
  _target_: lightning.pytorch.Trainer
  max_epochs: 50
  accelerator: gpu
  devices: auto
  precision: bf16-mixed

data:
  _target_: stable_pretraining.data.DataModule
  ...
```

Sau đó ablation override dùng:

```text
module.n_slices=512,1024,4096
module.t_max=1,3,5
module.n_points=5,17,41
trainer.max_epochs=50
```

### 6.3. Vì sao route A tốt hơn

- dùng runner đang tồn tại.
- không phụ thuộc `scripts/je.py` đã mất.
- nested key rõ nghĩa.
- Hydra validate tốt hơn.
- dễ thêm callback KNN.

### 6.4. Khi nào dùng route B

Chỉ dùng route B nếu có nhu cầu giữ y nguyên command cũ.

Khi đó tạo:

```text
scripts/je.py
```

Nó parse Hydra flat config và tự build:

- DataModule
- LeJEPA
- Trainer
- callbacks

Nhưng route này rủi ro vì dễ duplicate `stable_pretraining.run`.

---

## 7. Config YAML cần tạo

### 7.1. Đề xuất path

```text
scripts/configs/
  lejepa_inet100.yaml
  lejepa_smoke.yaml
```

### 7.2. `lejepa_smoke.yaml`

Mục tiêu:

- CPU hoặc single GPU.
- dataset nhỏ.
- batch nhỏ.
- max_steps=3.
- dùng trong dry-run/smoke.

Nên dựa trên logic từ:

- `stable-pretraining/stable_pretraining/tests/integration/test_lejepa_inet10.py`

Nội dung smoke cần:

- `vit_tiny_patch16_224`
- `frgfm/imagenette`
- 2 global views
- 2 local views
- batch size 8 hoặc 16
- n_slices 64
- drop_path_rate 0
- trainer `max_steps=3`
- logger false
- checkpoint false

### 7.3. `lejepa_inet100.yaml`

Mục tiêu:

- config thật cho ablation.
- dataset `inet100`.
- backbone `vit_large_patch14_224`.
- 50 epochs.
- batch 512.
- bf16.
- KNN top-1 callback.

Điểm cần kiểm tra:

- repo hiện có dataset name `inet100` ở đâu không.
- nếu không có, cần định nghĩa dataset mapping trong config/data helper.
- nếu `stable-pretraining` có benchmark config cho ImageNet100, reuse pattern từ `benchmarks/imagenet100/*.py`.

### 7.4. Nếu config YAML quá khó

Phase đầu có thể render Python command gọi một local training script.

Nhưng phải ghi rõ:

- script đó là compatibility layer.
- lâu dài nên chuyển sang `stable_pretraining.run`.

---

## 8. Reuse pipeline hiện có

### 8.1. Reuse `LeJEPA`

Hiện có:

- `LeJEPA.__init__(encoder_name, projector, n_slices, t_max, n_points, lamb, pretrained, drop_path_rate)`
- `LeJEPA.forward(global_views, local_views, images)`
- `_compute_loss(all_projected, n_global, sigreg, lamb)`

Nên reuse:

- backbone creation qua timm.
- SlicedEppsPulley implementation.
- loss implementation baseline.
- eval mode trả embedding.

### 8.2. Reuse `Module`

Nếu dùng config full của `stable_pretraining.run`, có thể dùng subclass `LeJEPA` trực tiếp vì `LeJEPA` extends `Module`.

Nếu cần forward theo batch dict, dùng pattern từ test:

```python
def lejepa_forward(self, batch, stage):
    if stage == "fit":
        global_views = [...]
        local_views = [...]
        output = LeJEPA.forward(self, global_views=global_views, local_views=local_views)
    else:
        output = LeJEPA.forward(self, images=batch["image"])
    return {"loss": output.loss, "embedding": output.embedding, "label": labels}
```

Nên tránh copy function này vào nhiều nơi. Đưa vào:

```text
stable_pretraining/methods/lejepa.py
```

hoặc:

```text
scripts/ablations/forward.py
```

Tốt hơn: thêm helper generic trong `stable_pretraining.methods.lejepa`.

### 8.3. Reuse transforms

Trong test có:

- `transforms.MultiViewTransform`
- `transforms.Compose`
- `transforms.RGB`
- `transforms.RandomResizedCrop`
- `transforms.ToImage`

Nên dùng lại để tạo:

- global views
- local views

Không viết transform mới.

### 8.4. Reuse `DataModule`

Trong test dùng:

```python
spt.data.DataModule(train=DataLoader(...), val=DataLoader(...))
```

Ablation config nên instantiate DataModule tương tự.

### 8.5. Reuse KNN callback

Có:

- `stable_pretraining.callbacks.knn`
- test unit cho KNN/probing.

Plan cần kiểm tra API cụ thể của callback này trước khi viết config.

Mục tiêu:

- dùng frozen embeddings từ `output["embedding"]`.
- dùng `output["label"]`.
- log `val/knn_top1` hoặc tương đương.

### 8.6. Reuse log summarizer

CLI đã có:

```bash
spt dump-csv-logs DIR output_name agg
```

Plan kết quả nên gọi lại tool này, không viết summarizer mới ngay.

---

## 9. Model support cần thêm vào `LeJEPA`

### 9.1. Projector builder

Hiện `LeJEPA` default projector là hardcoded:

```python
nn.Sequential(
    nn.Linear(embed_dim, 512),
    MLP(512, [2048, 2048, 512], norm_layer="batch_norm"),
)
```

Ablation cần:

- `Linear`
- `MLP2`
- `MLP`
- `MLP4`
- `projector_dim`
- maybe `projector_hidden_dim`
- maybe norm type

Đề xuất thêm function:

```python
def build_projector(
    in_dim: int,
    out_dim: int = 512,
    arch: str = "MLP",
    hidden_dim: int = 2048,
    norm_layer: str = "batch_norm",
) -> nn.Module:
    ...
```

Mapping:

- `Linear`: `nn.Linear(in_dim, out_dim)`
- `MLP2`: `MLP(in_dim, [hidden_dim, out_dim], norm_layer=norm_layer)`
- `MLP`: `MLP(in_dim, [hidden_dim, hidden_dim, out_dim], norm_layer=norm_layer)`
- `MLP4`: `MLP(in_dim, [hidden_dim, hidden_dim, hidden_dim, out_dim], norm_layer=norm_layer)`

### 9.2. Norm layer support

`stable_pretraining.backbone.MLP` hiện chỉ support `batch_norm` string.

Nếu ablation cần BN vs LN:

- extend `MLP` to support `layer_norm`.
- hoặc local builder tự tạo layers.

Preferred:

- extend `MLP` generically.
- add tests to `test_aggregator` or new `test_mlp`.

### 9.3. Patch masking support

Hiện `LeJEPA` dùng `timm.create_model(..., num_classes=0)`, output embedding directly.

Patch masking cần:

- dùng `MaskedEncoder`.
- hoặc patch timm forward path để mask patches.

`stable-pretraining` đã có:

- `MaskedEncoder`
- `PatchMasking`

Nên reuse:

```python
from stable_pretraining.backbone import MaskedEncoder, PatchMasking, TensorAggregator
```

Đề xuất:

- thêm param `patch_mask_ratio: float = 0.0`
- nếu `patch_mask_ratio == 0`, giữ path timm hiện tại.
- nếu `patch_mask_ratio > 0`, tạo `MaskedEncoder(..., masking=PatchMasking(mask_ratio=patch_mask_ratio), dynamic_img_size=True, patch_size=patch_size)`
- thêm aggregation từ token output sang embedding.

Rủi ro:

- `MaskedEncoder` output là token sequence, không phải pooled embedding.
- cần aggregator rõ ràng.

### 9.4. Aggregator support

Ablation cần:

- `cls`
- `mean`
- `cls_mean`
- `cls2`

Hiện `TensorAggregator` support:

- `mean`
- `max`
- `cls`
- `flatten`
- `adaptive`

Nhưng `cls_mean` chưa có trực tiếp.

Đề xuất:

- tạo helper trong `LeJEPA`:

```python
def aggregate_tokens(tokens, mode):
    if mode == "cls":
        return tokens[:, 0]
    if mode == "mean":
        return tokens[:, 1:].mean(dim=1)
    if mode == "cls_mean":
        return torch.cat([tokens[:, 0], tokens[:, 1:].mean(dim=1)], dim=-1)
```

`cls2` phức tạp hơn vì cần features từ 2 layer cuối.

Phase đầu:

- support `cls`, `mean`, `cls_mean`.
- mark `cls2` as requiring `feature_layers` support.

Nếu làm `cls2`:

- dùng timm `forward_intermediates` nếu backbone support.
- hoặc hook last two blocks.
- hoặc use `features_only` nếu timm model support.

Không nên implement `cls2` chung chung mà không test kỹ.

### 9.5. `sigreg_target`

Hiện SIGReg áp dụng trên:

```python
all_projected.reshape(-1, all_projected.size(-1))
```

Cần variants:

- `proj`
- `embed`
- `both`

Đề xuất sửa `_compute_loss` signature:

```python
def _compute_loss(
    all_features,
    all_projected,
    n_global,
    sigreg,
    lamb,
    sigreg_target="proj",
):
```

Logic:

- invariance vẫn trên projected or predictor output tùy predictor.
- `proj`: `sigreg(all_projected_flat)`
- `embed`: `sigreg(all_features_flat)`
- `both`: `0.5 * sigreg(projected) + 0.5 * sigreg(features)`

Rủi ro:

- embedding dim có thể rất lớn.
- SIGReg on embed dùng same `n_slices`.
- cost tăng.

### 9.6. Predictor support

Variants:

- `none`
- `linear`
- `mlp`

Đề xuất:

```python
def build_predictor(kind, dim, hidden_dim=2048):
    if kind in (None, "none", False):
        return nn.Identity()
    if kind == "linear":
        return nn.Linear(dim, dim)
    if kind == "mlp":
        return MLP(dim, [hidden_dim, dim], norm_layer="batch_norm")
```

Loss path:

- Projected representations: `z = projector(features)`.
- Predictor output: `p = predictor(z)`.
- Centers should be computed from target `z` or predicted `p`?

Need decide:

- For a simple ablation, use predictor only on online branch.
- Current LeJEPA has symmetric multi-view invariance to center.
- A minimal predictor version can compute center from global `z` and penalize all `p` against center.

Pseudo:

```python
target = all_projected.detach() if predictor_detach_target else all_projected
pred = predictor(all_projected)
centers = target[:n_global].mean(0)
inv_loss = (centers.unsqueeze(0) - pred).square().mean()
sigreg_loss = sigreg(all_projected_flat)
```

But using detach changes method. Since LeJEPA claim avoids stop-gradient, default should avoid detach.

Recommended ablation:

- `predictor=none`: current.
- `predictor=linear/mlp`: `pred = predictor(z)`, center from `z`, no detach.
- Log clearly that this tests added asymmetry/capacity, not BYOL exact stop-grad setup.

### 9.7. Register tokens

Existing ablation wants `reg_tokens`.

Need check how timm accepts register tokens:

- Some timm ViT models accept `reg_tokens`.
- `stable_pretraining.backbone.utils` includes support.

Minimal model support:

```python
timm.create_model(..., reg_tokens=reg_tokens)
```

But not all models accept it.

Implementation should conditionally pass only for ViT and catch unsupported kwargs.

Better:

- use existing backbone utility if it already wraps register tokens robustly.
- add smoke test for `reg_tokens=0` and `reg_tokens=2`.

### 9.8. Drop path

Already supported by `LeJEPA(drop_path_rate=...)`.

No model change needed.

### 9.9. Epps params

Already supported:

- `n_slices`
- `t_max`
- `n_points`

Need only map config names from old `bstat_*` to actual `LeJEPA` args.

### 9.10. Projector dims

Partly supported by `projector` param.

Need builder or config can instantiate custom projector.

Better to add:

- `projector_dim`
- `projector_arch`
- `projector_hidden_dim`

directly to `LeJEPA.__init__`.

---

## 10. Implementation phases

## Phase 1: Create ablation spec renderer

### 10.1. Goal

Tạo CLI sinh command từ plan, chưa cần chạy training.

### 10.2. Files

Create:

```text
scripts/ablations.py
scripts/ablations/__init__.py
scripts/ablations/common.py
scripts/ablations/specs.py
scripts/ablations/commands.py
```

### 10.3. `common.py`

Add:

- `AblationSpec`
- `CommandOptions`
- `RenderedCommand`
- helper `as_hydra_value`
- helper `format_override`
- helper `count_grid`

### 10.4. `specs.py`

Add:

- `BASE_OVERRIDES`
- `ABLATIONS`
- `get_spec(key)`
- `list_specs()`

Specs:

- `epps`
- `projector_dims`
- `reg_tokens`
- `views`
- `projector_depth`
- `patch_masking`
- `drop_path`
- `aggregation`
- `sigreg_target`
- `predictor`

### 10.5. `commands.py`

Add:

- `render_command(spec, options)`
- `render_markdown(specs, options)`
- `render_shell_script(specs, options)`

### 10.6. `scripts/ablations.py`

Use `argparse`, not Typer, to avoid new dependency.

Commands:

```bash
python scripts/ablations.py list
python scripts/ablations.py show epps
python scripts/ablations.py render epps
python scripts/ablations.py render all
python scripts/ablations.py write-scripts
```

### 10.7. Output style

For `list`:

```text
key                 status                configs  priority
epps                ready                 27       1
projector_dims      needs_model_support   10       2
...
```

For `render`:

```bash
HYDRA_FULL_ERROR=1 python -m stable_pretraining.run --multirun \
  --config-path scripts/configs \
  --config-name lejepa_inet100 \
  module.n_slices=512,1024,4096 \
  module.t_max=1,3,5 \
  module.n_points=5,17,41
```

### 10.8. Phase 1 tests

Add lightweight tests? Could be overkill.

At minimum run:

```bash
python scripts/ablations.py list
python scripts/ablations.py render epps
python scripts/ablations.py render all
```

No GPU needed.

---

## Phase 2: Add config YAML smoke path

### 11.1. Goal

Make one tiny config runnable.

### 11.2. Files

Create:

```text
scripts/configs/lejepa_smoke.yaml
```

Possibly:

```text
scripts/configs/lejepa_inet100.yaml
```

### 11.3. Reuse test logic

Base logic should mirror:

```text
stable-pretraining/stable_pretraining/tests/integration/test_lejepa_inet10.py
```

### 11.4. Critical details

Need ensure training batch format matches `LeJEPA.forward`.

Current direct `LeJEPA.forward` does not accept batch dict. Test monkey-patches a `lejepa_forward`.

Config route needs a callable forward.

Options:

1. Add a reusable function in `stable_pretraining.methods.lejepa`.
2. Put function in `scripts/ablations/forward.py`.
3. Use a subclass/wrapper.

Preferred:

Add in `stable_pretraining.methods.lejepa`:

```python
def multiview_forward(self, batch, stage):
    ...
```

Then config:

```yaml
module:
  _target_: stable_pretraining.methods.lejepa.LeJEPA
  forward: stable_pretraining.methods.lejepa.multiview_forward
```

But `LeJEPA` already inherits `Module` and has its own forward method. Passing `forward` into `LeJEPA.__init__` will not work unless constructor accepts it through `Module`.

Safer:

- keep `LeJEPA.forward` as model forward.
- create `LeJEPALightning` wrapper subclass if needed.

Alternative:

- use `stable_pretraining.Module` as outer module and set `model=LeJEPA(...)`.

Need inspect current config examples before final implementation.

### 11.5. Practical route

For ablations, easiest robust path:

Create:

```text
scripts/train_lejepa_ablation.py
```

This script:

- uses Hydra.
- builds transforms.
- builds DataModule.
- builds `LeJEPA`.
- defines forward adapter.
- builds Trainer.
- runs `Manager`.

But this duplicates less than full `scripts/je.py` because it still uses:

- `LeJEPA`
- `DataModule`
- `Manager`
- transforms
- callbacks
- Trainer

This may be more practical than forcing YAML into existing generic runner.

Decision:

- Phase 2 can use `scripts/train_lejepa_ablation.py`.
- Phase 3 can migrate to pure config if needed.

### 11.6. CLI command if using local train script

```bash
HYDRA_FULL_ERROR=1 python scripts/train_lejepa_ablation.py --multirun \
  dataset_name=inet100 \
  max_epochs=50 \
  backbone=vit_large_patch14_224 \
  n_slices=512,1024,4096
```

This is close to old markdown but points to a real script.

### 11.7. Avoid old `scripts/je.py`

Do not name it `je.py` unless compatibility is required.

Better name:

- `train_lejepa_ablation.py`
- `run_lejepa_ablation.py`

Clearer and searchable.

---

## Phase 3: Build `train_lejepa_ablation.py`

### 12.1. Goal

Create one executable training entrypoint for all ablations.

### 12.2. Inputs

Hydra config fields:

```yaml
dataset_name: inet100
max_epochs: 50
max_steps: null
batch_size: 512
num_workers: 8
backbone: vit_large_patch14_224
pretrained: false
resolution: 238
local_resolution: 98
patch_size: 14
n_views: 8
n_global_views: 2
multi_crop: true
lr: 5e-4
weight_decay: 5e-2
precision: bf16-mixed
accelerator: gpu
devices: auto
drop_path_rate: 0.1
projector_arch: MLP
projector_dim: 512
projector_hidden_dim: 2048
bstat_lambda: 0.05
bstat_num_slices: 1024
bstat_t_max: 3.0
bstat_n_points: 17
patch_mask_ratio: 0.3
reg_tokens: 0
aggregator: cls
sigreg_target: proj
predictor: none
knn_eval: true
wandb_project: null
autostop: false
seed: 42
```

### 12.3. Output

It should log:

- config
- train loss
- invariance loss
- sigreg loss
- learning rate
- KNN top-1
- elapsed time

### 12.4. Internal functions

Organize script with functions:

```python
def build_train_transform(cfg): ...
def build_eval_transform(cfg): ...
def build_dataset(cfg, split, transform): ...
def build_data(cfg): ...
def build_model(cfg): ...
def build_callbacks(cfg): ...
def build_trainer(cfg, callbacks): ...
def lejepa_forward(self, batch, stage): ...
def main(cfg): ...
```

### 12.5. Keep script thin

Script should call into `stable_pretraining` components.

Do not define:

- custom optimizer logic unless needed.
- custom callback unless no existing callback works.
- custom dataset class unless no existing dataset mapping works.

### 12.6. Dataset mapping

Need a mapping:

```python
DATASETS = {
    "inet10": {...},
    "inet100": {...},
    "imagenette": {...},
}
```

But before writing this, inspect existing dataset helpers.

If `stable_pretraining.data.datasets.HFDataset` can load HF datasets directly, use:

- dataset id
- split
- revision if needed

For `inet100`, need know source:

- possibly local ImageFolder.
- possibly HuggingFace dataset.
- possibly benchmark code already assumes ImageNet100 location.

If unavailable, make `dataset_name=imagenette` the smoke default and document `inet100` needs dataset path.

### 12.7. Local dataset path support

Add optional:

```yaml
data_root: null
train_split: train
val_split: validation
```

If `data_root` is set:

- use `torchvision.datasets.ImageFolder`.

If not:

- use `HFDataset`.

### 12.8. Optimizer config

`LeJEPA` extends `Module`; test sets:

```python
module.optim = {
    "optimizer": {
        "type": "AdamW",
        "lr": 5e-4,
        "weight_decay": 0.05,
        "betas": (0.9, 0.999),
    },
    "scheduler": {"type": "LinearWarmupCosineAnnealing"},
    "interval": "epoch",
}
```

Reuse this.

### 12.9. Trainer config

Use Lightning:

```python
pl.Trainer(
    max_epochs=cfg.max_epochs,
    max_steps=cfg.max_steps or -1,
    precision=cfg.precision,
    accelerator=cfg.accelerator,
    devices=cfg.devices,
    callbacks=callbacks,
    logger=logger,
)
```

Need handle:

- `num_sanity_val_steps`
- checkpointing
- gradient clipping maybe default none

### 12.10. Multirun compatibility

Decorate:

```python
@hydra.main(version_base=None, config_path="configs", config_name="lejepa_ablation")
def main(cfg):
    ...
```

Then commands from spec can target it.

---

## Phase 4: Model feature support

### 13.1. Order of model changes

Implement in this order:

1. projector builder
2. `sigreg_target`
3. predictor
4. reg tokens
5. aggregator `cls/mean/cls_mean`
6. patch masking
7. aggregator `cls2`

Reason:

- projector builder is low-risk and unlocks multiple ablations.
- `sigreg_target` is central and small.
- predictor is self-contained.
- reg tokens may depend on timm quirks.
- aggregator/patch masking touches backbone output shape and is riskier.
- `cls2` is most likely to require hooks/intermediate features.

### 13.2. Projector builder change

Modify:

```text
stable-pretraining/stable_pretraining/methods/lejepa.py
```

Add:

```python
def build_projector(...)
```

Add `LeJEPA.__init__` args:

```python
projector_arch: str = "MLP"
projector_dim: int = 512
projector_hidden_dim: int = 2048
projector_norm: str = "batch_norm"
```

Backwards compatibility:

- if `projector is not None`, use passed projector.
- else build from args.

### 13.3. SIGReg target change

Add arg:

```python
sigreg_target: str = "proj"
```

Validate:

```python
if sigreg_target not in {"proj", "embed", "both"}:
    raise ValueError(...)
```

Need modify `_compute_loss`.

### 13.4. Predictor change

Add args:

```python
predictor: str = "none"
predictor_hidden_dim: int = 2048
```

Avoid name conflict:

- if arg named `predictor`, attribute also `self.predictor`.
- OK, but builder should normalize bool false.

### 13.5. Reg token change

Add arg:

```python
reg_tokens: int = 0
```

When creating timm model:

```python
create_kwargs = {...}
if reg_tokens:
    create_kwargs["reg_tokens"] = reg_tokens
```

Potential issue:

- timm may not accept `reg_tokens` for all models.

Option:

```python
try:
    self.backbone = timm.create_model(..., reg_tokens=reg_tokens)
except TypeError:
    if reg_tokens:
        raise
    self.backbone = timm.create_model(...)
```

### 13.6. Aggregator change

Add arg:

```python
aggregator: str = "cls"
```

But current timm model with `num_classes=0` returns pooled features, not tokens.

To support aggregator, need different forward path:

- for default `cls`, current path OK.
- for `mean/cls_mean`, need token output.

Approach:

- set `self.return_tokens = aggregator != "cls" or patch_mask_ratio > 0`
- create backbone in a way that can return tokens.

For timm ViT:

```python
features = self.backbone.forward_features(x)
```

Usually returns tokens or pooled depending model.

Need inspect actual timm model behavior.

Add helper:

```python
def encode(self, images):
    if self.aggregator == "cls" and not self.requires_tokens:
        return self.backbone(images)
    tokens = self.backbone.forward_features(images)
    return aggregate_tokens(tokens, self.aggregator)
```

Need handle if `forward_features` returns dict.

### 13.7. Patch masking change

Patch masking should likely force token path.

Use `MaskedEncoder` if feasible.

Potential design:

```python
if patch_mask_ratio > 0:
    self.encoder = MaskedEncoder(
        encoder_name,
        masking=PatchMasking(mask_ratio=patch_mask_ratio),
        dynamic_img_size=True,
        patch_size=patch_size,
        pretrained=pretrained,
    )
else:
    self.encoder = timm.create_model(...)
```

Then:

```python
out = self.encoder(images)
if isinstance(out, MaskedEncoderOutput):
    tokens = out.encoded
    features = aggregate_tokens(tokens, aggregator)
else:
    features = out
```

Risk:

- encoded includes CLS/register tokens and visible patches only.
- mean pooling visible patches may change semantics.
- local/global resolutions with dynamic size need test.

### 13.8. `cls2` support

Defer until above stable.

Implementation options:

- forward hooks on last two blocks.
- timm `forward_intermediates`.
- timm feature extraction utility.

Spec should mark `cls2` as blocked until implemented.

---

## Phase 5: Ablation specs

### 14.1. Baseline spec

Baseline:

```python
BASE = {
    "dataset_name": "inet100",
    "max_epochs": 50,
    "backbone": "vit_large_patch14_224",
    "batch_size": 512,
    "bstat_name": "epps_pulley",
    "bstat_num_slices": 1024,
    "bstat_t_max": 3.0,
    "bstat_n_points": 17,
    "bstat_lambda": 0.05,
    "embedding_dim": 512,
    "projector_dim": 512,
    "projector_arch": "MLP",
    "lr": 5e-4,
    "weight_decay": 5e-2,
    "teacher_student": False,
    "n_views": 8,
    "n_global_views": 2,
    "drop_path_rate": 0.1,
    "multi_crop": True,
    "resolution": 238,
    "local_resolution": 98,
    "patch_size": 14,
    "patch_mask_ratio": 0.3,
    "autostop": False,
}
```

Need normalize names to actual train script config.

### 14.2. Epps ablation

Grid:

```python
{
    "bstat_num_slices": [512, 1024, 4096],
    "bstat_t_max": [1, 3, 5],
    "bstat_n_points": [5, 17, 41],
}
```

Configs:

- 27

Status:

- ready after train script maps args.

### 14.3. Projector dims ablation

Grid:

```python
{
    "embedding_dim": [512, 2048],
    "projector_dim": [64, 128, 256, 512, 1024],
}
```

But note:

- `embedding_dim` in old markdown may mean input to projector or output from backbone.
- Current `LeJEPA` gets backbone `embed_dim` from timm.
- It cannot set `embedding_dim=2048` unless adding a pre-projector linear layer or choosing different aggregator.

Recommendation:

- rename this to `projector_input_dim` only if actual code supports it.
- otherwise use:

```python
{
    "projector_dim": [64, 128, 256, 512, 1024],
}
```

and make `embedding_dim` a derived value.

Status:

- needs clarification.

### 14.4. Register tokens

Grid:

```python
{"reg_tokens": [0, 1, 2, 4, 8]}
```

Configs:

- 5

Status:

- needs model support.

### 14.5. Views

Current markdown has manually adjusted batch sizes.

Better encode explicit grid list, not cartesian.

Need support non-cartesian sweeps:

```python
cases = [
    {"n_views": 4, "n_global_views": 2, "batch_size": 256},
    {"n_views": 6, "n_global_views": 2, "batch_size": 432},
    {"n_views": 8, "n_global_views": 2, "batch_size": 512},
    {"n_views": 10, "n_global_views": 2, "batch_size": 640},
    ...
]
```

Therefore `AblationSpec` should support either:

- `grid`
- `cases`

Dataclass:

```python
grid: dict[str, list[Any]] = field(default_factory=dict)
cases: list[dict[str, Any]] = field(default_factory=list)
```

Render mode:

- cartesian grid uses one Hydra multirun command.
- cases may use one command per case or Hydra zip syntax.

Simpler:

- render one command per case.

### 14.6. Projector depth

Grid:

```python
{"projector_arch": ["Linear", "MLP2", "MLP", "MLP4"]}
```

Status:

- needs projector builder.

### 14.7. Patch masking

Grid:

```python
{"patch_mask_ratio": [0.0, 0.1, 0.2, 0.3, 0.5, 0.7]}
```

Status:

- needs model support with `MaskedEncoder`.

### 14.8. Drop path

Grid:

```python
{"drop_path_rate": [0.0, 0.05, 0.1, 0.2, 0.4]}
```

Status:

- ready.

### 14.9. Feature aggregation

Grid:

```python
{"aggregator": ["cls", "mean", "cls_mean", "cls2"]}
```

Status:

- partially blocked.

Recommendation:

- phase 1 grid: `["cls", "mean", "cls_mean"]`
- add `cls2` later after tests.

### 14.10. SIGReg target

Grid:

```python
{"sigreg_target": ["proj", "embed", "both"]}
```

Status:

- needs model support.

### 14.11. Predictor head

Grid:

```python
{"predictor": ["none", "linear", "mlp"]}
```

Status:

- needs model support.

---

## 15. Script rendering details

### 15.1. Hydra value formatting

Need handle:

- bool: `true/false`
- string: quote only when needed
- float scientific: `5e-4`
- null: `null`
- list values in multirun: `a,b,c`

Implementation:

```python
def hydra_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, str):
        if value in {"true", "false", "null"}:
            return f'"{value}"'
        return value
    return str(value)
```

### 15.2. Override prefix

If using Hydra config with existing keys:

```text
key=value
```

If using no base config:

```text
++key=value
```

Preferred:

- define base config.
- use `key=value`.

### 15.3. Multirun commands

Command:

```bash
HYDRA_FULL_ERROR=1 python scripts/train_lejepa_ablation.py --multirun \
  bstat_num_slices=512,1024,4096 \
  bstat_t_max=1,3,5 \
  bstat_n_points=5,17,41
```

### 15.4. Case commands

For non-cartesian:

```bash
HYDRA_FULL_ERROR=1 python scripts/train_lejepa_ablation.py \
  n_views=4 \
  n_global_views=2 \
  batch_size=256
```

or render a shell script with multiple commands.

### 15.5. Shell script output

`write-scripts` can write:

```text
scripts/generated/
  run_epps.sh
  run_projector_dims.sh
  run_views.sh
  run_all_ready.sh
```

Generated scripts should start with:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

But avoid background `&` unless explicitly requested.

### 15.6. Slurm / submitit

Optional future:

```text
hydra/launcher=submitit_slurm
hydra.launcher.gpus_per_node=...
hydra.launcher.timeout_min=...
```

Do not hardcode cluster settings in baseline.

Make CLI option:

```bash
python scripts/ablations.py render epps --launcher submitit_slurm
```

---

## 16. Results summarization

### 16.1. Phase 1

Do nothing custom.

Use:

```bash
spt dump-csv-logs logs/ ablation_results max
```

### 16.2. Phase 2

Add:

```bash
python scripts/ablations.py summarize logs/
```

It should:

- find CSV logs.
- load them with existing `CSVLogAutoSummarizer` if possible.
- group by ablation key.
- select best KNN top-1.
- write CSV and markdown.

### 16.3. Metadata required in logs

Each run should log:

- `ablation_key`
- `ablation_title`
- all swept keys
- baseline version
- git commit if available

If using Hydra:

- working directory will contain `.hydra/config.yaml`.
- summarizer can read config from there.

### 16.4. Output files

```text
scripts/generated/results/
  epps.csv
  epps.md
  all_ablation_summary.csv
  all_ablation_summary.md
```

---

## 17. Tests and validation plan

### 17.1. Renderer tests

Run:

```bash
python scripts/ablations.py list
python scripts/ablations.py show epps
python scripts/ablations.py render epps
python scripts/ablations.py render views
```

Check:

- no missing keys.
- config count correct.
- ready/blocked statuses correct.
- no `scripts/je.py` in generated command unless intentionally choosing compatibility.

### 17.2. Model unit tests

Add tests under:

```text
stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py
```

Test cases:

- `projector_arch=Linear`
- `projector_arch=MLP2`
- `projector_arch=MLP`
- `projector_arch=MLP4`
- `sigreg_target=proj/embed/both`
- `predictor=none/linear/mlp`
- `drop_path_rate=0`

Use tiny backbone:

```python
vit_tiny_patch16_224
```

Use tiny images:

```python
torch.randn(2, 3, 224, 224)
```

Use:

- 2 global views
- 1 or 2 local views
- n_slices 8 or 16

### 17.3. Aggregator tests

Add:

- `aggregator=cls`
- `aggregator=mean`
- `aggregator=cls_mean`

Check output dims.

### 17.4. Patch masking tests

Add:

- `patch_mask_ratio=0.0`
- `patch_mask_ratio=0.3`

Check:

- loss finite.
- training/eval both work.
- dynamic local resolution works.

### 17.5. Smoke training test

Run:

```bash
python scripts/train_lejepa_ablation.py max_steps=3 batch_size=8 backbone=vit_tiny_patch16_224 bstat_num_slices=16
```

Goal:

- no crash.
- logs loss.
- saves no huge output.

### 17.6. One ablation dry-run

Run:

```bash
python scripts/ablations.py render drop_path
```

Then manually run with tiny overrides:

```bash
python scripts/train_lejepa_ablation.py --multirun \
  max_steps=3 \
  batch_size=8 \
  backbone=vit_tiny_patch16_224 \
  bstat_num_slices=16 \
  drop_path_rate=0.0,0.1
```

---

## 18. Concrete coding order

### 18.1. Step 1

Create `scripts/ablations/common.py`.

Add dataclasses and helper functions.

### 18.2. Step 2

Create `scripts/ablations/specs.py`.

Port all ablations from `scripts/ablation_plan.md`.

Mark status realistically:

- `epps`: ready
- `drop_path`: ready
- `projector_depth`: needs_projector_builder
- `patch_masking`: needs_masked_encoder
- `sigreg_target`: needs_loss_support
- `predictor`: needs_predictor_support
- `aggregation`: partial
- `reg_tokens`: needs_backbone_support
- `views`: ready once train script supports multiview counts
- `projector_dims`: needs clarification

### 18.3. Step 3

Create `scripts/ablations/commands.py`.

Support render of cartesian grids.

Support render of explicit cases.

### 18.4. Step 4

Create `scripts/ablations.py`.

Implement CLI:

- `list`
- `show`
- `render`

Do not implement run yet.

### 18.5. Step 5

Run renderer commands.

Fix formatting.

### 18.6. Step 6

Create base Hydra config:

```text
scripts/configs/lejepa_ablation.yaml
```

or implement default config inside `train_lejepa_ablation.py`.

### 18.7. Step 7

Create `scripts/train_lejepa_ablation.py`.

Start with only supported baseline:

- backbone
- n_slices
- t_max
- n_points
- lamb
- drop_path_rate
- n_views
- n_global_views
- transforms
- DataModule
- Trainer

### 18.8. Step 8

Run smoke:

```bash
python scripts/train_lejepa_ablation.py max_steps=3 batch_size=8 backbone=vit_tiny_patch16_224 bstat_num_slices=16 dataset_name=imagenette
```

### 18.9. Step 9

Update renderer backend to target real script.

### 18.10. Step 10

Implement projector builder in `stable_pretraining.methods.lejepa`.

Add tests.

### 18.11. Step 11

Enable `projector_arch` and `projector_dim` in train script.

Mark `projector_depth` as ready.

### 18.12. Step 12

Implement `sigreg_target`.

Add tests.

Mark `sigreg_target` ready.

### 18.13. Step 13

Implement predictor.

Add tests.

Mark `predictor` ready.

### 18.14. Step 14

Implement `reg_tokens`.

Add tests on ViT model.

Mark `reg_tokens` ready if timm supports chosen backbone.

### 18.15. Step 15

Implement aggregators.

Start with `cls`, `mean`, `cls_mean`.

Mark `aggregation` partially ready.

### 18.16. Step 16

Implement patch masking via `MaskedEncoder`.

Add tests.

Mark `patch_masking` ready.

### 18.17. Step 17

Decide whether to implement `cls2`.

If not, split ablation:

- `aggregation_basic`: `cls/mean/cls_mean`
- `aggregation_cls2`: blocked/future

### 18.18. Step 18

Implement results summarizer if needed.

---

## 19. Script calling strategy

### 19.1. Human workflow

User workflow should be:

```bash
python scripts/ablations.py list
python scripts/ablations.py render drop_path
python scripts/ablations.py render drop_path > /tmp/drop_path.sh
bash /tmp/drop_path.sh
```

### 19.2. Generated scripts workflow

```bash
python scripts/ablations.py write-scripts --output scripts/generated
bash scripts/generated/run_drop_path.sh
```

### 19.3. Ready-only workflow

```bash
python scripts/ablations.py write-scripts --ready-only
```

This should exclude blocked specs.

### 19.4. Smoke workflow

```bash
python scripts/ablations.py render drop_path --smoke
```

This should override:

- `dataset_name=imagenette`
- `max_steps=3`
- `batch_size=8`
- `backbone=vit_tiny_patch16_224`
- `bstat_num_slices=16`

### 19.5. Slurm workflow

Future:

```bash
python scripts/ablations.py render epps --launcher submitit_slurm
```

Should append:

```text
hydra/launcher=submitit_slurm
```

and maybe:

```text
hydra.launcher.gpus_per_node=...
```

Only if user supplies cluster options.

---

## 20. Naming conventions

### 20.1. Ablation keys

Use lowercase snake case:

- `epps`
- `projector_dims`
- `reg_tokens`
- `views`
- `projector_depth`
- `patch_masking`
- `drop_path`
- `aggregation`
- `sigreg_target`
- `predictor`

### 20.2. Run names

Run name format:

```text
{ablation_key}_{short_hash_or_index}
```

Examples:

- `epps_s512_t3_p17`
- `drop_path_0p1`
- `predictor_mlp`

### 20.3. Output dirs

Hydra output:

```text
outputs/ablations/${ablation_key}/${now:%Y-%m-%d}/${now:%H-%M-%S}
```

For multirun:

```text
multirun/ablations/${ablation_key}/${now:%Y-%m-%d}/${now:%H-%M-%S}
```

### 20.4. Generated artifacts

Generated command scripts:

```text
scripts/generated/
```

Do not manually edit generated scripts.

---

## 21. Risks and mitigations

### 21.1. Missing `inet100`

Risk:

- `dataset_name=inet100` may not be directly supported.

Mitigation:

- implement `dataset_name=imagenette` smoke first.
- add `data_root` for local ImageFolder.
- document exact expected dataset layout.

### 21.2. Old config names drift

Risk:

- old markdown keys do not map to new model args.

Mitigation:

- create explicit mapping table in code.
- renderer warns on unsupported keys.

### 21.3. Patch masking shape mismatch

Risk:

- local views at 98 with patch size 14 produce different token counts.
- aggregation must handle variable visible tokens.

Mitigation:

- aggregate each view independently after encoder.
- do not assume fixed token count.

### 21.4. `cls_mean` doubles embedding dim

Risk:

- projector input dim changes.

Mitigation:

- use LazyLinear in projector builder or infer dim with dummy forward.
- simpler: compute `feature_dim` after encoder init for known aggregator.

### 21.5. `cls2` complexity

Risk:

- implementation becomes timm-version-specific.

Mitigation:

- defer `cls2`.
- keep spec blocked.

### 21.6. Predictor semantics

Risk:

- predictor ablation accidentally introduces stop-gradient/teacher behavior inconsistent with paper.

Mitigation:

- document exact loss formula.
- default no detach.
- log predictor kind in config.

### 21.7. Config explosion

Risk:

- running `all` launches too many jobs.

Mitigation:

- `render all` should print total configs.
- `run all` should require `--yes` if implemented.
- support `--ready-only`.

---

## 22. Documentation updates

### 22.1. Update `scripts/ablation_plan.md`

After code is in place, update the existing plan:

- replace stale `scripts/je.py` commands.
- replace `inet1k/100/teacher_student=true` with canonical baseline.
- add link to generated scripts.
- mark implementation status.

### 22.2. Add short README

Create:

```text
scripts/ablations/README.md
```

or add section to `scripts/ablation_plan.md`:

```bash
python scripts/ablations.py list
python scripts/ablations.py render epps
python scripts/ablations.py write-scripts
```

### 22.3. Keep `AGENTS.md` updated

If new scripts are added, update:

- training entrypoint section.
- ablation commands section.

---

## 23. Final target behavior

When everything is implemented, these should work:

```bash
python scripts/ablations.py list
python scripts/ablations.py show sigreg_target
python scripts/ablations.py render sigreg_target
python scripts/ablations.py write-scripts --ready-only
python scripts/train_lejepa_ablation.py max_steps=3 dataset_name=imagenette backbone=vit_tiny_patch16_224
```

And these ablations should be runnable:

```bash
bash scripts/generated/run_epps.sh
bash scripts/generated/run_drop_path.sh
bash scripts/generated/run_projector_depth.sh
bash scripts/generated/run_sigreg_target.sh
bash scripts/generated/run_predictor.sh
```

The code should make it obvious which ablations are still blocked by model support.

---

## 24. Recommended immediate next commit

The first implementation commit should contain only:

- `scripts/ablations.py`
- `scripts/ablations/common.py`
- `scripts/ablations/specs.py`
- `scripts/ablations/commands.py`
- generated command rendering for all current ablations

No training model edits yet.

Why:

- gives immediate structure.
- reveals stale/unsupported keys.
- does not risk breaking training.
- lets us review command shape before GPU work.

The second commit should add:

- `scripts/train_lejepa_ablation.py`
- smoke config/defaults
- one smoke run

The third commit should add:

- projector builder.
- drop_path/epps/projector_depth ready.

Then continue with higher-risk model options.

