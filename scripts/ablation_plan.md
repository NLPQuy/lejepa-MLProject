# LeJEPA Ablation Plan

## Conventions

- **Dataset**: ImageNet-100 (`inet100`) for all new ablations — ~10× faster than ImageNet-1K, rankings transfer well.
- **Epochs**: 50 for all ablations.
- **Backbone**: `vit_large_patch14_224` throughout for consistency with main experiments.
- **Evaluation**: KNN top-1 on frozen features (faster and more stable than linear probe at low epoch counts).
- **Baseline config** (shared across all new ablations unless noted):
  ```
  bstat_name=epps_pulley  bstat_num_slices=1024  bstat_t_max=3  bstat_n_points=17
  embedding_dim=512  projector_dim=512  projector_arch=MLP
  lr=5e-4  weight_decay=5e-2  bstat_lambda=0.05
  teacher_student=false  n_views=8  n_global_views=2
  drop_path_rate=0.1  patch_mask_ratio=0.3
  multi_crop=true  resolution=238  local_resolution=98  patch_size=14
  ```

---

## Executable Ablation Pipeline

The current runnable ablation path is the lightweight renderer plus local
training entrypoint:

```bash
python scripts/ablations.py list
python scripts/ablations.py render epps
python scripts/ablations.py write-scripts --ready-only
python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 accelerator=cpu devices=1 precision=32
```

Use `scripts/ablations.py` as the source of executable sweep commands.  Do not
use `scripts/je.py`: that file is referenced by older notes but does not exist
in this checkout.

The old `scripts/launch_*_ablation.md` files are legacy/manual launch notes.
Keep them as historical ablation sketches, but prefer rendering fresh commands
with `scripts/ablations.py`.

---

## Existing Ablations (legacy/manual notes; keep, adjust dataset/epochs)

| # | File | What varies | Recommended epochs |
|---|------|-------------|-------------------|
| 1 | `launch_epps_ablation.md` (legacy/manual) | `t_max` × `n_points` × `num_slices` | 50 |
| 2 | `launch_proj_ablation.md` (legacy/manual) | `embedding_dim` × `projector_dim` | 50 |
| 3 | `launch_rtokens_ablation.md` (legacy/manual) | `reg_tokens` | 50 |
| 4 | `launch_views_ablation.md` (legacy/manual) | `n_views` × `n_global_views` | 50 |

---

## New Ablations

---

### 5. Projector Architecture — Depth and Normalization

**Question**: How many MLP layers are needed in the projector? Does normalization type (BN vs LN) matter?  
**Why it matters**: Projector design heavily affects SSL performance (SimCLR, VICReg ablations). The current 3-layer BN-MLP is a default, not an ablated choice. SIGReg explicitly reshapes the output distribution — so the projector's capacity to do so may matter more here than in other SSL methods.

```bash
HYDRA_FULL_ERROR=1 python scripts/je.py --multirun \
    ++bstat_name="epps_pulley" \
    ++bstat_num_slices=1024 \
    ++backbone="vit_large_patch14_224" \
    ++dataset_name="inet100" \
    ++max_epochs=50 \
    ++batch_size=512 \
    ++bstat_lambda=0.05 \
    ++embedding_dim=512 \
    ++projector_dim=512 \
    ++projector_arch="Linear","MLP2","MLP","MLP4" \
    ++lr=5e-4 \
    ++weight_decay=5e-2 \
    ++teacher_student=false \
    ++n_views=8 \
    ++n_global_views=2 \
    ++drop_path_rate=0.1 \
    ++multi_crop=true \
    ++resolution=238 \
    ++local_resolution=98 \
    ++patch_size=14 \
    ++patch_mask_ratio=0.3 \
    ++autostop=false
```

> **Note**: Requires `MLP2` (2-layer) and `MLP4` (4-layer) variants registered in the projector arch registry, hoặc dùng `projector_hidden_layers=1,2,3,4` nếu config hỗ trợ.

**Expected outcome**: Linear head underperforms vì SIGReg cần projector có đủ capacity để reshape distribution. 3-layer likely optimal.

---

### 6. Patch Masking Ratio — How Much Masking Is Optimal?

**Question**: What is the effect of patch masking on representation quality? Is 30% optimal?  
**Why it matters**: Patch masking là augmentation đặc thù của ViT, kiểm soát độ khó của self-supervised task. Khác với MAE (mask ratio cao để reconstruction), LeJEPA dùng invariance loss nên optimal ratio có thể khác.

```bash
HYDRA_FULL_ERROR=1 python scripts/je.py --multirun \
    ++bstat_name="epps_pulley" \
    ++bstat_num_slices=1024 \
    ++backbone="vit_large_patch14_224" \
    ++dataset_name="inet100" \
    ++max_epochs=50 \
    ++batch_size=512 \
    ++bstat_lambda=0.05 \
    ++embedding_dim=512 \
    ++projector_dim=512 \
    ++projector_arch="MLP" \
    ++lr=5e-4 \
    ++weight_decay=5e-2 \
    ++teacher_student=false \
    ++n_views=8 \
    ++n_global_views=2 \
    ++drop_path_rate=0.1 \
    ++multi_crop=true \
    ++resolution=238 \
    ++local_resolution=98 \
    ++patch_size=14 \
    ++patch_mask_ratio=0.0,0.1,0.2,0.3,0.5,0.7 \
    ++autostop=false
```

**Expected outcome**: Sweet spot quanh 0.2–0.4. Ratio quá cao (≥0.5) mất quá nhiều spatial context cho invariance term. `patch_mask_ratio=0.0` là no-masking baseline.

---

### 7. Stochastic Depth (Drop Path Rate)

**Question**: How sensitive is LeJEPA to stochastic depth regularization in ViT?  
**Why it matters**: Drop path là regularization knob quan trọng với ViT-L — quá cao → underfitting, quá thấp → overfit augmentation. Cần xác định giá trị tối ưu cho SSL setting (khác với supervised).

```bash
HYDRA_FULL_ERROR=1 python scripts/je.py --multirun \
    ++bstat_name="epps_pulley" \
    ++bstat_num_slices=1024 \
    ++backbone="vit_large_patch14_224" \
    ++dataset_name="inet100" \
    ++max_epochs=50 \
    ++batch_size=512 \
    ++bstat_lambda=0.05 \
    ++embedding_dim=512 \
    ++projector_dim=512 \
    ++projector_arch="MLP" \
    ++lr=5e-4 \
    ++weight_decay=5e-2 \
    ++teacher_student=false \
    ++n_views=8 \
    ++n_global_views=2 \
    ++drop_path_rate=0.0,0.05,0.1,0.2,0.4 \
    ++multi_crop=true \
    ++resolution=238 \
    ++local_resolution=98 \
    ++patch_size=14 \
    ++patch_mask_ratio=0.3 \
    ++autostop=false
```

**Expected outcome**: Moderate drop path (0.1–0.2) optimal cho ViT-L. `drop_path_rate=0.0` là sanity check.

---

### 8. Feature Aggregation — Which Backbone Output to Use?

**Question**: Nên pool feature từ ViT bằng cách nào trước khi đưa vào projector?  
**Why it matters**: ViT cho ra nhiều loại token. CLS token tổng hợp global info, mean patch tokens giữ spatial info, ghép cả hai cho richer representation. Linear probe eval trong paper dùng last-2-layers CLS concat — ablation này kiểm tra xem điều đó có tốt hơn trong training loop không.

Các variants:
- `cls` — chỉ CLS token của layer cuối (hiện tại)
- `mean` — mean pooling toàn bộ patch tokens
- `cls_mean` — concat CLS + mean patch tokens
- `cls2` — concat CLS của 2 layer cuối (giống linear probe eval setup)

```bash
HYDRA_FULL_ERROR=1 python scripts/je.py --multirun \
    ++bstat_name="epps_pulley" \
    ++bstat_num_slices=1024 \
    ++backbone="vit_large_patch14_224" \
    ++dataset_name="inet100" \
    ++max_epochs=50 \
    ++batch_size=512 \
    ++bstat_lambda=0.05 \
    ++projector_dim=512 \
    ++projector_arch="MLP" \
    ++lr=5e-4 \
    ++weight_decay=5e-2 \
    ++teacher_student=false \
    ++n_views=8 \
    ++n_global_views=2 \
    ++drop_path_rate=0.1 \
    ++multi_crop=true \
    ++resolution=238 \
    ++local_resolution=98 \
    ++patch_size=14 \
    ++patch_mask_ratio=0.3 \
    ++aggregator="cls","mean","cls_mean","cls2" \
    ++autostop=false
```

> **Note**: `embedding_dim` sẽ khác nhau tùy aggregator (`cls_mean` và `cls2` cho dim gấp đôi). Cần đảm bảo projector đầu vào tự adapt hoặc set `embedding_dim` phù hợp.

**Expected outcome**: `cls_mean` hoặc `cls2` có thể tốt hơn CLS đơn thuần vì cung cấp richer signal cho cả invariance lẫn SIGReg. Nếu `cls` vẫn tốt nhất thì xác nhận thiết kế hiện tại là đúng.

---

### 9. SIGReg Application Point — Before vs After Projector

**Question**: Nên áp dụng SIGReg trên backbone embedding hay projector output?  
**Why it matters**: Đây là lựa chọn kiến trúc cơ bản: regularize representation space (backbone output) hay projection space (sau projector). Regularize backbone trực tiếp có thể ảnh hưởng mạnh hơn đến feature quality nhưng cũng có thể cản trở backbone học được structure tốt.

Các variants:
- `proj` — SIGReg trên projector output (hiện tại)
- `embed` — SIGReg trên backbone embedding, trước projector
- `both` — SIGReg trên cả hai, mỗi cái với λ/2

```bash
# variant: proj (baseline)
HYDRA_FULL_ERROR=1 python scripts/je.py --multirun \
    ++bstat_name="epps_pulley" \
    ++bstat_num_slices=1024 \
    ++backbone="vit_large_patch14_224" \
    ++dataset_name="inet100" \
    ++max_epochs=50 \
    ++batch_size=512 \
    ++bstat_lambda=0.05 \
    ++embedding_dim=512 \
    ++projector_dim=512 \
    ++projector_arch="MLP" \
    ++lr=5e-4 \
    ++weight_decay=5e-2 \
    ++teacher_student=false \
    ++n_views=8 \
    ++n_global_views=2 \
    ++drop_path_rate=0.1 \
    ++multi_crop=true \
    ++resolution=238 \
    ++local_resolution=98 \
    ++patch_size=14 \
    ++patch_mask_ratio=0.3 \
    ++sigreg_target="proj","embed","both" \
    ++autostop=false
```

> **Note**: Cần implement `sigreg_target` param trong forward pass của LeJEPA nếu chưa có.

**Expected outcome**: `proj` (baseline) likely tốt nhất vì projector có thể học cách reshape distribution mà không ảnh hưởng backbone. `embed` có thể gây conflict với invariance term nếu backbone embedding space bị ép về N(0,I) quá sớm.

---

### 10. Predictor Head — Symmetric vs Asymmetric Architecture

**Question**: Thêm predictor head (như BYOL / I-JEPA) có giúp ích không?  
**Why it matters**: I-JEPA dùng predictor trong latent space để không cần EMA teacher. LeJEPA bỏ predictor lẫn EMA. Ablation này kiểm tra xem predictor có bổ sung gì cho invariance term hay không — nếu không, điều đó củng cố sự đơn giản của LeJEPA.

Các variants:
- `none` — không có predictor (hiện tại)
- `linear` — 1-layer linear predictor
- `mlp` — 2-layer MLP predictor (tương tự BYOL)

```bash
HYDRA_FULL_ERROR=1 python scripts/je.py --multirun \
    ++bstat_name="epps_pulley" \
    ++bstat_num_slices=1024 \
    ++backbone="vit_large_patch14_224" \
    ++dataset_name="inet100" \
    ++max_epochs=50 \
    ++batch_size=512 \
    ++bstat_lambda=0.05 \
    ++embedding_dim=512 \
    ++projector_dim=512 \
    ++projector_arch="MLP" \
    ++lr=5e-4 \
    ++weight_decay=5e-2 \
    ++teacher_student=false \
    ++n_views=8 \
    ++n_global_views=2 \
    ++drop_path_rate=0.1 \
    ++multi_crop=true \
    ++resolution=238 \
    ++local_resolution=98 \
    ++patch_size=14 \
    ++patch_mask_ratio=0.3 \
    ++predictor="none","linear","mlp" \
    ++autostop=false
```

> **Note**: Cần implement `predictor` param. Predictor chỉ được dùng ở nhánh online khi tính invariance loss; SIGReg vẫn áp dụng trên projector output (trước predictor).

**Expected outcome**: `none` (không predictor) likely không thua kém, điều đó validate thiết kế đơn giản của LeJEPA. Nếu `mlp` predictor giúp ích thì cần giải thích thêm trong paper.

---

## Summary Table

| # | Ablation | Key variable(s) | Configs | Epochs | Dataset |
|---|----------|-----------------|---------|--------|---------|
| 1 | EppsPulley params | `t_max`, `n_points`, `num_slices` | 27 | 50 | inet1k |
| 2 | Projector dims | `embedding_dim`, `projector_dim` | 10 | 50 | inet1k |
| 3 | Register tokens | `reg_tokens` | 5 | 50 | inet1k |
| 4 | Views | `n_views`, `n_global_views` | 11 | 50 | inet1k |
| **5** | **Projector depth** | `projector_arch` | **4** | **50** | **inet100** |
| **6** | **Patch masking** | `patch_mask_ratio` | **6** | **50** | **inet100** |
| **7** | **Drop path rate** | `drop_path_rate` | **5** | **50** | **inet100** |
| **8** | **Feature aggregation** | `aggregator` | **4** | **50** | **inet100** |
| **9** | **SIGReg target** | `sigreg_target` | **3** | **50** | **inet100** |
| **10** | **Predictor head** | `predictor` | **3** | **50** | **inet100** |

**Total new GPU-epochs** (ablations 5–10, inet100):  
`(4+6+5+4+3+3) × 50 = 1,250 epoch-equivalents on inet100`  
≈ **125 epoch-equivalents on inet1k**.

---

## Priority Order (if compute is tight)

1. **#9 SIGReg target** — kiểm tra lựa chọn kiến trúc cốt lõi nhất
2. **#10 Predictor head** — so sánh trực tiếp với I-JEPA, củng cố đóng góp của paper
3. **#8 Feature aggregation** — ảnh hưởng đến cả representation quality lẫn SIGReg
4. **#6 Patch masking** — dễ chạy, rõ ràng cho analysis section
5. **#7 Drop path** — ViT-specific, hữu ích cho camera-ready
6. **#5 Projector depth** — thấp nhất, phụ thuộc implementation registry
