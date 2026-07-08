# Tóm tắt Baseline LeJEPA

> **Nguồn gốc:** Balestriero & LeCun, *"LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics"*, arXiv:2511.08544 (2025).  
> **Repository:** https://github.com/rbalestr-lab/lejepa

---

## 1. Bối cảnh và Vấn đề

Học biểu diễn tự giám sát (Self-Supervised Learning – SSL) thông qua kiến trúc **Joint-Embedding Predictive Architecture (JEPA)** gặp phải vấn đề cốt lõi: **sụp đổ biểu diễn (representation collapse)**, tức là mô hình ánh xạ tất cả đầu vào về một điểm hoặc không gian con, làm mất đi tính phân biệt.

Các phương pháp hiện có (I-JEPA, VICReg, DINO, v.v.) giải quyết collapse bằng nhiều thủ thuật heuristic:
- **Stop-gradient / EMA** (Exponential Moving Average teacher–student)
- **Bộ điều chỉnh đa mục tiêu** (VICReg dùng 7 hệ số)
- **Encoder đóng băng** từ mô hình nền (foundation model)
- **Scheduler học tốc độ phức tạp**

Tất cả đều tăng độ phức tạp huấn luyện và giảm tính ổn định.

---

## 2. LeJEPA: Ý tưởng Cốt lõi

LeJEPA đề xuất một hàm mất mát mới gọi là **Sketched Isotropic Gaussian Regularization (SIGReg)**, giúp:

- Ràng buộc phân phối embedding học được tiến gần đến một **Gaussian đẳng hướng (isotropic Gaussian)** – phân phối tối ưu về rủi ro dự đoán downstream.
- Loại bỏ hoàn toàn các heuristic: không stop-gradient, không EMA, không scheduler thêm.
- Đảm bảo lý thuyết về phòng tránh collapse thông qua **Cramér–Wold theorem**.

### Kiến trúc tổng quát (Vision SSL)

```
Image → Encoder (ViT / ConvNeXt) → Embedding z ∈ R^d
                                         ↓
                              SIGReg(z) + Prediction Loss
```

**Hàm mất mát:**

```
L_LeJEPA = L_pred + λ · SIGReg(Z)
```

---

## 3. SIGReg – Cơ chế Hoạt động

SIGReg đánh giá tính chuẩn (normality) của embedding bằng **phép chiếu ngẫu nhiên (random slicing)**:

1. **Chiếu** embedding `Z ∈ R^(N×d)` lên `M` hướng đơn vị ngẫu nhiên `u^(m) ∈ S^(d-1)` → thu được `h^(m) = Z · u^(m)` (1-D samples).
2. **Áp dụng kiểm định thống kê** univariate (mặc định: **Epps–Pulley test**) để đo độ lệch khỏi N(0,1) trên từng chiều chiếu.
3. **Trung bình** qua tất cả các hướng:

```
SIGReg(Z) = (1/M) · Σ_m T(h^(m))
```

> Theo Cramér–Wold theorem: nếu mọi hình chiếu 1-D đều khớp với N(0,1), thì phân phối joint cũng là Gaussian đẳng hướng.

### Các kiểm định thống kê được hỗ trợ

| Module | Kiểm định |
|--------|-----------|
| `lejepa.univariate` | EppsPulley, AndersonDarling, CramerVonMises, ShapiroWilk, Watson, Moments, NLL, ExtendedJarqueBera, VCReg |
| `lejepa.multivariate` | `SlicingUnivariateTest` (wrapper cho bất kỳ univariate test) |

---

## 4. Cấu hình Huấn luyện Chuẩn

### Data Augmentation (Multi-crop, theo DINO)

| | **Global Views (×2)** | **Local Views (×6)** |
|---|---|---|
| Crop Resolution | 224×224 | 98×98 |
| Scale | 0.3–1.0 | 0.05–0.3 |
| ColorJitter (p=0.8) | B=0.4, C=0.4, S=0.2, H=0.1 | idem |
| GaussianBlur | p=0.5 | p=0.5 |
| RandomSolarize | p=0.2 | p=0.2 |
| RandomGrayscale | p=0.2 | p=0.2 |

### Optimizer & Schedule

| Tham số | Giá trị |
|---------|---------|
| Optimizer | AdamW |
| Learning Rate | 5e-4 |
| Weight Decay | 5e-2 (ViT) / 5e-4 (ResNet) |
| Precision | bfloat16 (bf16) |
| LR Schedule | Linear warmup + Cosine annealing (final = lr/1000) |
| Batch Size | 512 (effective) |

### Hyperparameter SIGReg

| Tham số | Giá trị mặc định | Ghi chú |
|---------|-----------------|---------|
| `M` (số chiều chiếu) | 1024 | Ít nhạy cảm |
| `λ` (trọng số SIGReg) | 0.1 | Hyperparameter duy nhất cần tune |
| Num slices | 1024 | Trong `SlicingUnivariateTest` |

> **Điểm mạnh:** Chỉ có **1 hyperparameter thực sự cần tìm** (λ), có thể bisection search với độ phức tạp O(log n).

---

## 5. Linear Probe Evaluation

Đánh giá downstream bằng **few-shot linear probe**:

- **Feature**: Ghép CLS token từ **2 layer cuối** của ViT (với non-CLS ViT thì average patch tokens).
- **Chuẩn hóa**: LayerNorm trên concatenated features (theo DINO).
- **Classifier**: Linear layer + AdamW, weight decay = 1e-6.
- **Schedule**: Giống pre-training (warmup + cosine annealing).

---

## 6. Kết quả Benchmark (Paper)

Được đánh giá trên 8 dataset fine-grained với các mô hình pretrain 100 epochs trên ImageNet-1K:

| shots | Model | Params | DTD | Aircraft | Cars | CIFAR-10 | CIFAR-100 | Flowers | Food | Pets | **Avg** |
|-------|-------|--------|-----|---------|------|----------|-----------|---------|------|------|---------|
| 1 | **LeJEPA ViT-L** | 304M | **33.21** | 9.37 | 3.40 | 51.65 | 27.01 | 48.53 | 17.14 | 46.11 | 29.55 |
| 1 | LeJEPA ConvNeXtV2-H | 660M | 32.15 | 8.07 | 4.28 | 50.95 | **31.48** | **48.74** | **17.95** | **58.98** | **31.58** |
| 1 | I-JEPA ViT-H | 632M | 27.71 | **9.86** | **4.33** | **56.52** | 30.58 | 44.69 | 14.53 | 53.38 | 30.20 |
| 10 | **LeJEPA ViT-L** | 304M | **64.72** | **35.25** | 22.25 | 85.15 | 59.77 | **92.53** | **50.90** | 77.00 | **60.95** |
| 10 | I-JEPA ViT-H | 632M | 57.68 | 33.82 | 21.96 | **88.77** | **66.42** | 88.24 | 43.97 | **83.23** | 60.51 |
| all | **LeJEPA ViT-L** | 304M | **78.30** | 57.01 | **57.28** | 96.50 | 83.71 | **91.21** | **82.05** | 89.74 | **79.48** |
| all | I-JEPA ViT-H | 632M | 73.32 | **56.61** | 54.47 | **97.54** | **86.42** | 86.47 | 81.02 | **92.11** | 78.50 |

> LeJEPA ViT-L (304M, 100 epoch) **vượt** I-JEPA ViT-H (632M, 300 epoch) ở 10-shot và all-shot trung bình.

---

## 7. Kết quả Baseline Thực nghiệm của Nhóm (ViT-B/16, 1 epoch)

> Kết quả từ `REPORT.md` – chạy thử nghiệm 1 epoch trên ImageNet-1K với ViT-B/16 (86M params).

| Dataset | 1-shot (%) | 10-shot (%) | All-shot (%) |
|---------|:----------:|:-----------:|:------------:|
| DTD | 10.98 | 25.25 | 39.26 |
| CIFAR-10 | 23.99 | 41.07 | 71.48 |
| CIFAR-100 | 7.29 | 22.10 | 49.85 |
| Flowers102 | 19.74 | 49.51 | 65.29 |
| Food-101 | 4.09 | 13.98 | 39.49 |
| Stanford Cars | 1.81 | 5.32 | 10.77 |

**Cấu hình chạy:**
- Backbone: `timm/vit_base_patch16_224` (86M params)
- Dataset: ImageNet-1K, **1 epoch** (~2h 23min)
- Batch size: 512 (64 × 8 gradient accumulation steps)
- Multi-crop: 2 global views + 4 local views
- Optimizer: AdamW, lr=5e-4, wd=5e-2

---

## 8. Mở rộng: LeWorldModel (LeWM)

Từ LeJEPA cho SSL ảnh, framework SIGReg được mở rộng sang **world model** cho robot/control (arXiv:2603.19312):

- **Mục tiêu:** Học world model từ pixel observation + action sequence, không cần reward.
- **Kiến trúc:**
  - Encoder (ViT-tiny, ~5M params): `z_t = enc(o_t)`
  - Predictor (Transformer 6 layers, ~10M params): `ẑ_{t+1} = pred(z_t, a_t)` (action qua AdaLN)
- **Hàm mất mát:**

```
L_LeWM = L_pred + λ · SIGReg(Z)
```

- **Planning:** Tối ưu action sequence trong latent space bằng CEM (Cross-Entropy Method).
- **Kết quả:** Lập kế hoạch **48× nhanh hơn** (< 1 giây) so với baseline, vượt PLDM trên PushT.

---

## 9. Quick Start

```python
import lejepa

# Khởi tạo univariate test
univariate_test = lejepa.univariate.EppsPulley(num_points=17)

# Tạo multivariate slicing test
loss_fn = lejepa.multivariate.SlicingUnivariateTest(
    univariate_test=univariate_test, 
    num_slices=1024
)

# Tính loss (embeddings: [num_samples, num_dims])
loss = loss_fn(embeddings)
loss.backward()
```

**Cài đặt:**
```bash
pip install lejepa
# Hoặc editable install từ source
pip install -e .
pip install scipy  # cho một số tests
```

---

## 10. Ưu điểm So sánh

| Tiêu chí | I-JEPA | VICReg/DINO | **LeJEPA** |
|----------|--------|------------|-----------|
| Số hyperparameter | Nhiều | Nhiều (VICReg: 7 weights) | **1** (λ) |
| Stop-gradient | ✓ | ✓ | ✗ |
| EMA teacher | ✓ | ✓ | ✗ |
| Đảm bảo lý thuyết | Hạn chế | Không | **Có** |
| Độ phức tạp code | Cao | Cao | ~50 dòng core |
| Tương thích phân tán | Có | Có | **Có (DDP-aware)** |
| Thời gian train (đạt SOTA) | 300 epoch | 200+ epoch | **100 epoch** |

---

## Tài liệu tham khảo

- Balestriero, R. & LeCun, Y. (2025). *LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics*. arXiv:2511.08544.
- LeWorldModel extension: arXiv:2603.19312.
- Epps, T.W. & Pulley, L.B. (1983). *A test for normality based on the empirical characteristic function*.
- Cramér, H. & Wold, H. (1936). *Some theorems on distribution functions*.
