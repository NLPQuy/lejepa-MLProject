# LeJEPA — Giải Thích Source Code & Pipeline

> **Paper**: [arXiv:2511.08544](https://arxiv.org/abs/2511.08544) — *Randall Balestriero & Yann LeCun, 2025*

---

## Mục Lục

1. [Tổng Quan Kiến Trúc](#1-tổng-quan-kiến-trúc)
2. [Cây Thư Mục](#2-cây-thư-mục)
3. [Ý Tưởng Cốt Lõi: SIGReg](#3-ý-tưởng-cốt-lõi-sigreg)
4. [Pipeline Huấn Luyện](#4-pipeline-huấn-luyện)
5. [Tại Sao Cần Các Test Thống Kê?](#5-tại-sao-cần-các-test-thống-kê)
6. [Module `lejepa.univariate`](#6-module-lejepaunivariate)
7. [Module `lejepa.multivariate`](#7-module-lejepamultivariate)
8. [Hàm Loss Tổng Hợp](#8-hàm-loss-tổng-hợp)
9. [Đánh Giá (Linear Probe)](#9-đánh-giá-linear-probe)
10. [Distributed Training](#10-distributed-training)
11. [Luồng Dữ Liệu End-to-End](#11-luồng-dữ-liệu-end-to-end)

---

## 1. Tổng Quan Kiến Trúc

LeJEPA (Lean Joint-Embedding Predictive Architecture) là framework Self-Supervised Learning (SSL) được xây dựng dựa trên nguyên lý JEPA nhưng **loại bỏ hoàn toàn** các heuristic phổ biến:
- ✗ Không dùng stop-gradient
- ✗ Không dùng teacher–student networks
- ✗ Không dùng register tokens hay momentum encoders
- ✗ Không cần schedule phức tạp cho các heuristic

Thay vào đó, LeJEPA dùng một **mục tiêu thống kê có lý thuyết chứng minh** gọi là **SIGReg** (Sketched Isotropic Gaussian Regularization), ép các embedding học được phải phân phối theo Gaussian đẳng hướng chuẩn N(0, I).

```
Input Image
    │
    ▼
[ Data Augmentation ]  ──→  V views (global + local crops)
    │
    ▼
[ Backbone Encoder ]  (ViT, ResNet, ConvNeXt, ...)
    │
    ├──→  emb  (backbone embedding, dùng cho linear probe)
    │
    ▼
[ Projection Head ]  (MLP 3-layer + BatchNorm)
    │
    ▼
  proj  (shape: [V, N, proj_dim])
    │
    ├──→  Invariance Loss  (các view phải predict nhau)
    │
    └──→  SIGReg Loss      (phân phối embedding → N(0, I))
              │
              ▼
         LeJEPA Loss = λ·SIGReg + (1-λ)·Inv
```

---

## 2. Cây Thư Mục

```
lejepa/
├── lejepa/                      # Core library
│   ├── __init__.py              # Export: univariate, multivariate
│   ├── univariate/              # Các test thống kê 1 chiều
│   │   ├── base.py              # Base class UnivariateTest
│   │   ├── epps_pulley.py       # EppsPulley (test ECF) ← CHÍNH
│   │   ├── jarque_bera.py       # ExtendedJarqueBera, VCReg
│   │   ├── anderson_darling.py  # Anderson-Darling test
│   │   ├── cramer_von_mises.py  # Cramér-von Mises test
│   │   ├── shapiro_wilk.py      # Shapiro-Wilk test
│   │   ├── likelihood.py        # NLL (Order-statistic likelihood)
│   │   ├── entropy.py           # Entropy-based test
│   │   ├── moments.py           # Moment-based test
│   │   ├── watson.py            # Watson test
│   │   └── utils.py             # Tiện ích (log_norm_cdf, v.v.)
│   └── multivariate/            # Các test thống kê đa chiều
│       ├── base.py              # Base class MultivariatetTest
│       ├── slicing.py           # SlicingUnivariateTest ← CHÍNH
│       ├── bhep.py              # BHEP (Beta-Henze Energy Projection)
│       ├── bhep_m.py            # BHEP_M (biến thể)
│       ├── hz.py                # Henze-Zirkler test
│       ├── hv.py                # HV test
│       └── comb.py              # COMB (combination test)
├── scripts/                     # Launch scripts & ablations
│   ├── launch_inet10.py
│   ├── launch_epps_ablation.md
│   ├── launch_proj_ablation.md
│   ├── launch_rtokens_ablation.md
│   └── launch_views_ablation.md
├── tests/                       # Unit tests cho mọi test thống kê
├── eval/                        # Demo GIFs + ảnh PCA visualization
├── MINIMAL.md                   # Ví dụ đầy đủ với ViT + ImageNette
└── README.md
```

---

## 3. Ý Tưởng Cốt Lõi: SIGReg

### 3.1 Xuất phát điểm lý thuyết

Mục tiêu của SSL là học một encoder `f` sao cho downstream task risk được tối thiểu hóa. Balestriero & LeCun chứng minh rằng điều này tương đương với việc ép phân phối của các embedding `f(x)` **hội tụ về Gaussian đẳng hướng** N(0, I).

Khoảng cách giữa phân phối thực nghiệm và N(0,1) được đo qua **Empirical Characteristic Function (ECF)**:

```
T(X) = N · ∫ |φ̂(t) - φ(t)|² · w(t) dt

Trong đó:
  φ̂(t) = (1/N) Σ e^(itXⱼ)   ← ECF thực nghiệm
  φ(t)  = exp(-t²/2)          ← CF của N(0,1)
  w(t)                        ← hàm trọng số tích phân
```

### 3.2 Cài đặt thực tế trong `MINIMAL.md`

```python
class SIGReg(torch.nn.Module):
    def __init__(self, knots=17):
        super().__init__()
        t = torch.linspace(0, 3, knots)        # điểm tích phân [0, 3]
        dt = 3 / (knots - 1)
        weights = torch.full((knots,), 2 * dt) # trọng số trapezoid x2 (đối xứng)
        weights[[0, -1]] = dt                   # đầu/cuối chỉ nhân 1x
        window = torch.exp(-t.square() / 2.0)  # φ(t) = exp(-t²/2)
        self.register_buffer("t", t)
        self.register_buffer("phi", window)
        self.register_buffer("weights", weights * window)  # đã fold window vào weights

    def forward(self, proj):
        # proj: [V, N, proj_dim]
        A = torch.randn(proj.size(-1), 256, device="cuda")
        A = A.div_(A.norm(p=2, dim=0))          # 256 hướng ngẫu nhiên (slicing)
        x_t = (proj @ A).unsqueeze(-1) * self.t  # chiếu lên t
        err = (x_t.cos().mean(-3) - self.phi).square() + x_t.sin().mean(-3).square()
        statistic = (err @ self.weights) * proj.size(-2)
        return statistic.mean()
```

**Giải thích từng bước:**
1. `A` — 256 hướng chiếu ngẫu nhiên được chuẩn hóa (random slicing)
2. `proj @ A` — chiếu embedding D-chiều xuống 256 hướng 1-chiều
3. `x_t.cos().mean(-3)` — phần thực của ECF: Re(φ̂(t)) = (1/N)Σ cos(tXⱼ)
4. `x_t.sin().mean(-3)` — phần ảo của ECF: Im(φ̂(t)) = (1/N)Σ sin(tXⱼ)
5. `err` — |φ̂(t) - φ(t)|² = (Re - φ(t))² + Im²
6. Tích phân bằng **quy tắc hình thang** với trọng số đã tính sẵn
7. Nhân N·world_size để có test statistic đúng scale

> **Trick quan trọng**: Khai thác tính đối xứng φ(t) = φ(-t) của Gaussian để chỉ tích phân trên [0, t_max], tăng gấp đôi hiệu quả quadrature.

---

## 4. Pipeline Huấn Luyện

### 4.1 Data Augmentation (Multi-crop)

Mỗi ảnh được tạo ra **V views** (mặc định V=4 cho inet10):

| View loại | Crop Size | Scale | Mục đích |
|-----------|-----------|-------|----------|
| Global (2) | 224×224 | (0.3, 1.0) | Học semantic toàn cục |
| Local (6)  | 98×98   | (0.05, 0.3) | Học đặc trưng cục bộ |

Cả hai loại đều dùng cùng augmentation:
- RandomHorizontalFlip (p=0.5)
- ColorJitter (p=0.8): brightness/contrast/saturation/hue
- RandomGrayscale (p=0.2)
- GaussianBlur (p=0.5)
- RandomSolarize (p=0.2, threshold=128)
- Normalize (ImageNet mean/std)

### 4.2 Forward Pass

```python
# net: ViTEncoder (backbone + projector)
# vs: [N, V, C, H, W]  ← batch N ảnh, mỗi ảnh V views

emb, proj = net(vs)
# emb:  [N*V, backbone_dim]  ← dùng cho linear probe
# proj: [V, N, proj_dim]     ← dùng cho LeJEPA loss
```

Bên trong `ViTEncoder.forward`:
```python
def forward(self, x):
    N, V = x.shape[:2]
    emb = self.backbone(x.flatten(0, 1))     # [N*V, 512]
    proj = self.proj(emb).reshape(N, V, -1).transpose(0, 1)  # [V, N, proj_dim]
    return emb, proj
```

### 4.3 Tính Loss

```python
# 1) Invariance Loss: mọi view phải converge về mean của chúng
inv_loss = (proj.mean(0) - proj).square().mean()

# 2) SIGReg Loss: phân phối embedding → N(0, I)
sigreg_loss = sigreg(proj)

# 3) LeJEPA Loss: cân bằng hai mục tiêu với duy nhất 1 hyperparameter λ
lejepa_loss = sigreg_loss * cfg.lamb + inv_loss * (1 - cfg.lamb)

# 4) Online Linear Probe Loss (không backprop vào backbone)
y_rep = y.repeat_interleave(cfg.V)
probe_loss = F.cross_entropy(probe(emb.detach()), y_rep)

# 5) Tổng loss
loss = lejepa_loss + probe_loss
```

### 4.4 Optimizer & Scheduler

```python
# AdamW với weight decay khác nhau cho backbone và probe
opt = torch.optim.AdamW([
    {"params": net.parameters(),   "lr": cfg.lr, "weight_decay": 5e-2},
    {"params": probe.parameters(), "lr": 1e-3,   "weight_decay": 1e-7},
])

# Linear warmup 1 epoch → Cosine annealing đến hết training
warmup_steps = len(train)
s1 = LinearLR(opt, start_factor=0.01, total_iters=warmup_steps)
s2 = CosineAnnealingLR(opt, T_max=total_steps - warmup_steps, eta_min=1e-3)
scheduler = SequentialLR(opt, schedulers=[s1, s2], milestones=[warmup_steps])
```

### 4.5 Mixed Precision

Training dùng **bfloat16** (bf16) — stable hơn float16 trong SSL vì range lớn hơn, không cần loss scaling phức tạp:

```python
scaler = GradScaler(enabled=True)
with autocast("cuda", dtype=torch.bfloat16):
    ...  # forward pass
scaler.scale(loss).backward()
scaler.step(opt)
scaler.update()
```

---

## 5. Tại Sao Cần Các Test Thống Kê?

> **Câu hỏi cốt lõi**: SIGReg muốn ép embedding → N(0, I). Nhưng làm sao đo được "khoảng cách" giữa phân phối thực nghiệm và N(0, I) một cách **khả vi** (differentiable) để backprop?

### Vai trò thực sự: Đây là **hàm loss**, không phải evaluation

Trong thống kê truyền thống, các test như Shapiro-Wilk hay Anderson-Darling dùng để *kiểm định giả thuyết* — trả lời câu hỏi "dữ liệu này có chuẩn không?". Nhưng trong LeJEPA, chúng được **tái sử dụng như hàm loss training**:

```
Thống kê truyền thống:    test_statistic → p-value → quyết định (reject/accept)
                                                              ↑ không khả vi, không backprop được

LeJEPA:                   test_statistic → .backward() → cập nhật trọng số encoder
                                ↑ chính là loss, gradient flow qua đây
```

Mỗi test univariate tính ra một con số **đo mức độ lệch** của phân phối embedding so với N(0,1). Khi loss này → 0, embedding đã hội tụ về phân phối Gaussian chuẩn — đây chính là điều kiện lý thuyết để downstream risk tối thiểu.

### Tại sao cần nhiều loại test khác nhau?

Mỗi test "nhìn" phân phối từ một góc độ khác nhau:

| Loại test | Cách đo khoảng cách | Nhạy với |
|-----------|--------------------|-----------|
| **EppsPulley** | So sánh Empirical Characteristic Function (ECF) với CF của N(0,1) | Toàn bộ phân phối — **mạnh nhất, dùng làm default** |
| **ExtendedJarqueBera** | So sánh 4 moment thống kê: mean, variance, skewness, kurtosis | Lệch vị trí, scale, độ lệch, đuôi nặng |
| **VCReg** | Chỉ so sánh mean và variance | Nhanh nhất, phù hợp nếu đã biết shape OK |
| **AndersonDarling** | So sánh CDF thực nghiệm vs CDF lý thuyết, **trọng số nặng ở đuôi** | Outlier, tail behavior |
| **CramerVonMises** | So sánh CDF thực nghiệm vs CDF lý thuyết, đều ở mọi điểm | Lệch phân phối tổng thể |
| **ShapiroWilk** | Tương quan giữa order statistics thực nghiệm và lý thuyết | Dạng tổng thể của phân phối |
| **NLL** | Negative log-likelihood của order statistics dưới N(0,1) | Likelihood fit, hỗ trợ trimming outlier |

### Tại sao EppsPulley là default?

ECF (Empirical Characteristic Function) là **bất biến đủ** cho phân phối — tức là nếu ECF = CF của N(0,1) tại mọi điểm t thì chắc chắn phân phối là N(0,1). Không có thông tin nào bị mất. Các test moment-based (JarqueBera, VCReg) chỉ kiểm tra một số moment cụ thể nên có thể bỏ sót sự lệch ở các moment bậc cao hơn.

Ngoài ra, EppsPulley:
- Tính toán **song song** tốt (vectorized trên tất cả t cùng lúc)
- Gradient **smooth** và ổn định cho backprop
- Tích phân số có thể trade-off chính xác ↔ tốc độ qua `n_points`

### Flow: từ embedding đến loss

```
embeddings ∈ ℝ^(N×D)
     │
     │ [SlicingUnivariateTest]  chiếu lên K hướng ngẫu nhiên
     ▼
chiếu 1D: x @ A  ∈ ℝ^(N×K)       ← giờ có K bài toán 1 chiều
     │
     │ [EppsPulley / JarqueBera / ...]  áp dụng test univariate
     ▼                                   song song trên cả K cột
test_statistic ∈ ℝ^K
     │
     │ .mean()  tổng hợp
     ▼
  loss  (scalar)  →  .backward()  →  encoder được update
```

Khi loss giảm, nghĩa là embedding trên **mọi hướng chiếu ngẫu nhiên** đều đang tiến gần hơn đến N(0,1) — theo định lý Cramér-Wold, đây là điều kiện **đủ** để phân phối D-chiều → N(0, I).

---

## 6. Module `lejepa.univariate`

Tất cả các test univariate đều kế thừa từ `UnivariateTest`:

### 6.1 Base Class (`base.py`)

```python
class UnivariateTest(torch.nn.Module):
    def __init__(self, eps=1e-5, sorted=False):
        self.g = Normal(0, 1)  # Standard Gaussian reference

    def prepare_data(self, x):
        # Sort along dim=-2 (sample dimension) nếu cần
        return x.sort(descending=False, dim=-2)[0]

    def dist_mean(self, x):
        # Distributed average qua all_reduce (cho DDP)
        ...
    
    @property
    def world_size(self):
        # Số GPU trong distributed setup
        ...
```

### 6.2 EppsPulley (`epps_pulley.py`) ← **Test chính của SIGReg**

Kiểm tra liệu sample có phân phối N(0,1) qua ECF (Empirical Characteristic Function):

```
T = N · ∫₀^t_max |φ̂(t) - exp(-t²/2)|² · 2dt
```

- **Input**: `x` shape `(*, N, K)` — N samples, K slices song song
- **Output**: thống kê test shape `(*, K)`
- **Tích phân**: Trapezoid rule trên `[0, t_max=3]` với `n_points=17` điểm
- **DDP**: `all_reduce` cos_mean và sin_mean trước khi tính err

```python
class EppsPulley(UnivariateTest):
    def forward(self, x):
        N = x.size(-2)
        x_t = x.unsqueeze(-1) * self.t       # (*, N, K, n_points)
        cos_mean = cos(x_t).mean(-3)          # (*, K, n_points)
        sin_mean = sin(x_t).mean(-3)          # (*, K, n_points)
        cos_mean = all_reduce(cos_mean)       # đồng bộ DDP
        sin_mean = all_reduce(sin_mean)
        err = (cos_mean - self.phi).square() + sin_mean.square()
        return (err @ self.weights) * N * self.world_size
```

### 6.3 ExtendedJarqueBera (`jarque_bera.py`)

Test 4 moment của N(0,1): mean=0, var=1, skewness=0, kurtosis=3.

```
JB_ext = S_mean + S_var + S_skew + S_kurt
       ~ χ²(4) dưới H₀: X ~ N(0,1)
```

| Component | Công thức | χ²(dof) |
|-----------|-----------|---------|
| Mean | n·μ̂²/σ̂² | χ²(1) |
| Variance | (n-1)·(σ̂²-1)²/2 | χ²(1) |
| Skewness+Kurtosis | n/6·(γ₁² + (γ₂-3)²/4) | χ²(2) |

### 6.4 VCReg (`jarque_bera.py`)

Phiên bản đơn giản hơn, chỉ test mean và variance (bỏ skewness/kurtosis):

```python
class VCReg(UnivariateTest):
    def forward(self, x):
        stat_mean = (mean**2) / (var / n)           # ~ χ²(1)
        stat_var = ((var - 1)**2) / (2 / (n-1))     # ~ χ²(1)
        return stat_mean + stat_var
```

### 6.5 AndersonDarling (`anderson_darling.py`)

Test EDF (Empirical Distribution Function) cho N(0,1), **cho thêm trọng số ở đuôi phân phối**:

```
A² = -n - (1/n) · Σᵢ (2i-1) · [log Φ(x_i) + log Φ(-x_{n+1-i})]
```

### 6.6 CramerVonMises (`cramer_von_mises.py`)

Test EDF cổ điển, không cho thêm trọng số ở đuôi:

```
T = (1/n) · Σ [F(xᵢ) - (2i-1)/(2n)]²
```

### 6.7 ShapiroWilk (`shapiro_wilk.py`)

Test tương quan giữa order statistics thực nghiệm và lý thuyết:

```
T = 1 - |ρ(x_(i), mᵢ)|
```

Hỗ trợ 3 chế độ plotting position: `elfving`, `blom`, `rahman`.  
Hỗ trợ 2 chế độ covariance: `shapiro_francia` (đơn giản) và `rahman` (tridiagonal).

### 6.8 NLL — Order Statistics Likelihood (`likelihood.py`)

Negative log-likelihood dựa trên order statistics:

```
NLL(xₖ) = -[log C(N,k) + (k-1)log Φ(xₖ) + (N-k)log(1-Φ(xₖ)) + log φ(xₖ)]
```

Hỗ trợ `alpha`-trimming để loại bỏ outliers ở đuôi.

---

## 7. Module `lejepa.multivariate`

### 7.1 SlicingUnivariateTest (`slicing.py`) ← **Wrapper chính**

Mở rộng bất kỳ univariate test nào sang đa chiều bằng **random slicing**:

```
x ∈ ℝᴰ  →  x @ A  ∈ ℝᴷ   (A: D×K, mỗi cột là unit vector ngẫu nhiên)
```

Sau đó áp dụng univariate test trên từng cột của `x @ A`:

```python
class SlicingUnivariateTest(torch.nn.Module):
    def forward(self, x):
        # x: (*, N, D)
        # Sinh A ngẫu nhiên với seed đồng bộ DDP
        A = torch.randn(D, num_slices, generator=g)
        A /= A.norm(p=2, dim=0)           # normalize to unit vectors
        
        stats = self.univariate_test(x @ A)  # (*, num_slices)
        return stats.mean()  # hoặc sum/None
```

**Seed đồng bộ**: `global_step` được sync qua `all_reduce(MAX)` để mọi GPU dùng cùng chiều chiếu.

### 7.2 BHEP (`bhep.py`) — Beta-Henze Energy-based Projection

```
T_N = (1/N²)∑ᵢⱼ exp(-β²/2·‖xᵢ-xⱼ‖²)
    - 2/[N(1+β²)^(D/2)] ∑ᵢ exp(-β²/(2+2β²)·‖xᵢ‖²)
    + 1/(1+2β²)^(D/2)
```

Dùng kernel Gaussian với bandwidth `β` cố định. Phức tạp: O(N²·D).

### 7.3 HZ (`hz.py`) — Henze-Zirkler

Bản BHEP với **adaptive bandwidth** tự động theo công thức:

```
β = (1/√2) · [(2D+1)·N/4]^(1/(D+4))
```

Không cần tuning tham số, tự điều chỉnh theo N và D.

### 7.4 COMB (`comb.py`)

Test kết hợp nhiều test statistics, tăng power tổng thể.

### 7.5 HV (`hv.py`)

Test dựa trên Hyperspherical Variance.

### 7.6 BHEP_M (`bhep_m.py`)

Biến thể của BHEP với marginalization.

---

## 8. Hàm Loss Tổng Hợp

### Cách dùng nhanh (API chuẩn từ README)

```python
import lejepa

# Bước 1: Chọn univariate test
univariate_test = lejepa.univariate.EppsPulley(num_points=17)

# Bước 2: Wrap thành multivariate loss qua slicing
loss_fn = lejepa.multivariate.SlicingUnivariateTest(
    univariate_test=univariate_test,
    num_slices=1024
)

# Bước 3: Tính loss
# embeddings: [num_samples, num_dims]
loss = loss_fn(embeddings)
loss.backward()
```

### Các test thay thế có thể dùng

| Test | Class | Đặc điểm | Tốc độ |
|------|-------|----------|--------|
| Epps-Pulley | `lejepa.univariate.EppsPulley` | Dựa ECF, song song tốt | ⚡⚡⚡ |
| Ext. Jarque-Bera | `lejepa.univariate.ExtendedJarqueBera` | 4 moments | ⚡⚡⚡ |
| VCReg | `lejepa.univariate.VCReg` | 2 moments (đơn giản nhất) | ⚡⚡⚡ |
| Anderson-Darling | `lejepa.univariate.AndersonDarling` | EDF, nhạy với đuôi | ⚡⚡ |
| Cramér-von Mises | `lejepa.univariate.CramerVonMises` | EDF cổ điển | ⚡⚡ |
| Shapiro-Wilk | `lejepa.univariate.ShapiroWilk` | Correlation-based | ⚡ |
| NLL | `lejepa.univariate.NLL` | Order statistics | ⚡ |
| BHEP | `lejepa.multivariate.BHEP` | Trực tiếp đa chiều | ⚡ |
| HZ | `lejepa.multivariate.HZ` | BHEP + adaptive β | ⚡ |

---

## 9. Đánh Giá (Linear Probe)

### Feature Extraction

```
Features = concat(CLS_token[-2], CLS_token[-1])   # 2 layer cuối của ViT
```

Với ViT không có CLS token → average tất cả patch tokens.

### Linear Probe Setup

| Hyperparameter | Giá trị |
|----------------|---------|
| Normalizer | LayerNorm (hoặc BatchNorm) |
| Optimizer | AdamW |
| Weight Decay | 1e-6 |
| LR Schedule | Linear warmup + Cosine annealing |

### Online Linear Probe (trong training loop)

Probe được train **song song** với pretraining nhưng **detach** gradient khỏi backbone:

```python
probe = nn.Sequential(nn.LayerNorm(512), nn.Linear(512, num_classes))
probe_loss = F.cross_entropy(probe(emb.detach()), labels)
```

> **Lợi điểm**: Không cần fine-tuning riêng sau pretraining để biết model đang học tốt không.

---

## 10. Distributed Training

### Sync ECF qua all_reduce

Trong `EppsPulley.forward`:
```python
cos_mean = all_reduce(cos_mean)  # AVG across GPUs
sin_mean = all_reduce(sin_mean)  # AVG across GPUs
```

Điều này tương đương với việc tính ECF trên toàn bộ batch từ tất cả GPU — đây là điểm mấu chốt giúp SIGReg hoạt động tốt với batch nhỏ!

### Sync Random Seed của Slicing

```python
global_step_sync = all_reduce(self.global_step.clone(), op="MAX")
seed = global_step_sync.item()
g = self._get_generator(x.device, seed)
A = torch.randn(proj_shape, generator=g)  # Cùng A trên mọi GPU
```

---

## 11. Luồng Dữ Liệu End-to-End

```
┌─────────────────────────────────────────────────────────────────┐
│                         Training Loop                           │
│                                                                 │
│  ┌──────────┐   V views   ┌───────────────┐                    │
│  │  Image   │ ──────────→ │  Augmentation │                    │
│  └──────────┘             └───────┬───────┘                    │
│                                   │ [N, V, C, H, W]            │
│                                   ▼                             │
│                         ┌─────────────────┐                    │
│                         │  ViT Backbone   │                    │
│                         │  (timm model)   │                    │
│                         └────────┬────────┘                    │
│              [N*V, backbone_dim] │                             │
│                    ┌─────────────┤                              │
│                    │             │                              │
│                    ▼             ▼                              │
│             ┌──────────┐  ┌────────────┐                       │
│             │  Linear  │  │ MLP Proj.  │                       │
│             │  Probe   │  │ (3-layer   │                       │
│             │(detached)│  │  + BN)     │                       │
│             └────┬─────┘  └─────┬──────┘                      │
│                  │              │ [V, N, proj_dim]              │
│                  │      ┌───────┴────────┐                     │
│                  │      │                │                      │
│                  │      ▼                ▼                      │
│                  │  ┌──────────┐  ┌──────────────┐            │
│                  │  │Invariance│  │  SIGReg:     │            │
│                  │  │  Loss    │  │  Slicing     │            │
│                  │  │          │  │  + EppsPulley│            │
│                  │  └────┬─────┘  └──────┬───────┘            │
│                  │       │               │                      │
│                  │       └───────┬───────┘                     │
│                  │               │                              │
│                  │    λ·SIGReg + (1-λ)·Inv                    │
│                  │               │                              │
│                  └───────┬───────┘                             │
│                          │ total_loss                           │
│                          ▼                                      │
│                   ┌─────────────┐                              │
│                   │  AdamW +    │                              │
│                   │  GradScaler │                              │
│                   │  + LR Sched │                              │
│                   └─────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tóm Tắt Hyperparameter Quan Trọng

| Hyperparameter | Mặc định | Vai trò |
|----------------|----------|---------|
| `λ (lamb)` | 0.02 | Cân bằng SIGReg vs Invariance. **Hyperparameter DUY NHẤT** |
| `V` | 4 | Số views per image |
| `proj_dim` | 16–128 | Chiều projection head |
| `lr` | 5e-4 | Learning rate backbone |
| `weight_decay` | 5e-2 (ViT) / 5e-4 (ResNet) | Regularization |
| `num_slices` | 256–1024 | Số chiều chiếu trong SlicingUnivariateTest |
| `num_points` | 17 | Số điểm quadrature trong EppsPulley |
| `t_max` | 3.0 | Giới hạn tích phân ECF |
| `bs` | 256+ | Batch size (DDP all_reduce giảm yêu cầu batch lớn) |

---

*Tài liệu này được tổng hợp từ source code tại [`/lejepa/`](.) và paper [arXiv:2511.08544](https://arxiv.org/abs/2511.08544).*
