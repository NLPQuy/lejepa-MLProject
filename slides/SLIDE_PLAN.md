# PLAN SLIDE CHI TIẾT: LeJEPA
**Công cụ:** LaTeX Beamer | **Tổng:** 30 slides | **Thời lượng:** ~35–40 phút

**Nguyên tắc bất biến:**
- Mỗi slide có đúng **1 message** — đặt làm `\frametitle{}`
- Visual bằng **TikZ / pgfplots** — không dùng ảnh từ paper
- Lý luận theo chuỗi **Why → How → Proof → Consequence**
- Mỗi slide kết thúc bằng 1 dòng `\alert{}` takeaway ở bottom
- **BẮT BUỘC viết tiếng Việt có dấu** trong toàn bộ slide (tiêu đề, bullet, takeaway, label TikZ). Không được dùng ASCII không dấu kiểu "Cong Thuc", "Khong" — phải là "Công Thức", "Không". Compile bằng `pdflatex` với `inputenc + T5 + babel{vietnamese}` (xem mục PHÒNG TRÁNH LỖI bên dưới — không cần xelatex/fontspec).

---

## SETUP BEAMER (đặt ở preamble)

**Compile bằng `pdflatex` (chạy 2 lần để TOC/nav đúng):**
```bash
pdflatex slides.tex && pdflatex slides.tex
```

```latex
\documentclass[aspectratio=169]{beamer}
\usetheme{Madrid}           % hoặc Metropolis cho modern look

% --- Tiếng Việt có dấu (pdflatex) ---
\usepackage[utf8]{inputenc}
\usepackage[T5]{fontenc}
\usepackage[vietnamese]{babel}

% --- Math, graphics ---
\usepackage{amsmath,amssymb}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{booktabs}
\usepackage{listings}
\usetikzlibrary{arrows.meta, positioning, shapes, fit, backgrounds, decorations.pathreplacing}

% Color palette — PROFESSIONAL / MUTED (academic style)
\definecolor{primary}{HTML}{2C3E6B}     % Navy xanh đậm — chủ đạo, tiêu đề, encoder
\definecolor{accent}{HTML}{C8A951}      % Gold nhạt — highlight, takeaway, câu chốt
\definecolor{bad}{HTML}{B85450}         % Terracotta (đỏ nâu) — limitation, ✗
\definecolor{good}{HTML}{5B8C6B}        % Sage (xanh rêu) — kết quả tốt, ✓
\definecolor{neutral}{HTML}{8C8C8C}     % Xám trung — chú thích, font phụ
\setbeamercolor{alerted text}{fg=accent}
\setbeamercolor{structure}{fg=primary}
```

**Lưu ý:** KHÔNG dùng `\usepackage{lmodern}` cùng với `[T5]fontenc` — babel sẽ tự kéo font `vnr` có đủ glyph tiếng Việt.

---

## PHẦN 1: BỐI CẢNH — AI HỌC NHƯ THẾ NÀO? (Slides 1–5)

---

### Slide 1 — Title

**`\frametitle{LeJEPA: Provable \& Scalable SSL Without the Heuristics}`**

**Layout:** Full-slide centered, 2 columns

**Cột trái — text:**
```
Randall Balestriero \& Yann LeCun (2025)
arXiv: 2511.08544

Presenter: [Tên bạn]
```

**Cột phải — TikZ:**
Vẽ pipeline nhỏ gồm 3 node tròn nối nhau:
- Node 1: icon ảnh (hình chữ nhật nhỏ)  
- Node 2: `$f_\theta$` (Encoder)  
- Node 3: cloud chấm tròn phân bố đều (minh hoạ `N(0,I)`)  
Dùng `\draw[->, thick, primary]` nối 3 node

---

### Slide 2 — Ba cách AI học từ dữ liệu

**`\frametitle{Ba Paradigm Học Máy}`**

**TikZ:** 3 box màu khác nhau đặt song song (dùng `\node[draw, rounded corners, fill=...]`)

```
+------------------+  +------------------+  +------------------+
|   SUPERVISED     |  | RECONSTRUCTION   |  | SELF-SUPERVISED  |
|                  |  |                  |  |                  |
| Image → Label    |  | Image → Image    |  | View1 ↔ View2    |
|                  |  |                  |  |                  |
| ✗ Cần label      |  | ✗ Lãng phí vào  |  | ✓ Tự sinh signal |
| ✗ Đắt, scarce    |  |   chi tiết pixel |  | ✓ Không cần nhãn |
+------------------+  +------------------+  +------------------+
    (màu neutral)         (màu neutral)          (màu good)
```

**Lý luận nói khi present:**
> Supervised cần annotation đắt. Reconstruction học chi tiết pixel thay vì semantic. SSL học bằng cách so khớp các "views" khác nhau của cùng 1 input — không cần label.

**Takeaway:** `\alert{SSL: AI học từ cấu trúc của dữ liệu, không từ nhãn con người}`

---

### Slide 3 — Vấn đề: Collapse

**`\frametitle{Vấn Đề Cốt Lõi Của SSL: Representation Collapse}`**

**TikZ — 2 panel:**

Panel trái — "Trivial solution":
```tikz
% Nhiều ảnh khác nhau (vẽ 4-5 node màu khác nhau)
% Tất cả có mũi tên trỏ vào 1 điểm duy nhất ở giữa
% Label: "f(x) = constant"
% Đánh dấu X đỏ
```

Panel phải — "What we want":
```tikz
% Các ảnh khác nhau → các điểm KHÁC NHAU trong không gian
% Điểm phân bố đều, có khoảng cách
% Label: "Meaningful embeddings"
% Dấu check xanh
```

**Lý luận:** Nếu mục tiêu là `min ||f(x₁) - f(x₂)||`, nghiệm tối ưu tầm thường là `f(x) = 0` cho mọi x. Đây là *complete collapse*. Còn *dimensional collapse*: tất cả embeddings nằm trên 1 subspace thấp chiều.

**Takeaway:** `\alert{Cần thêm ràng buộc chống collapse — nhưng ràng buộc NÀO là đúng?}`

---

### Slide 4 — JEPA: Kiến trúc cơ bản (LeCun, 2022)

**`\frametitle{JEPA: Joint-Embedding Predictive Architecture}`**

**TikZ — sơ đồ kiến trúc:**
```
  [view 1] ──► [Encoder f_θ] ──► z₁ ────────────────► (compare)
                                                            ↑
  [view 2] ──► [Encoder f_θ] ──► z₂ ──► [Predictor] ──► ẑ₁
```
Dùng màu `primary` cho encoder, `accent` cho predictor, `good` cho mũi tên compare.

**2 nguyên tắc — enumerate:**
1. **Predictability:** `Enc(xₙ,ₜ₊₁)` phải predict được từ `Enc(xₙ,ₜ)`
2. **Non-degeneracy:** Embeddings không được collapse

**So sánh với LLM** (bullet nhỏ):
- LLM: predict token tiếp theo (pixel space) → lãng phí compute vào noise
- JEPA: predict *abstract state* (embedding space) → học semantic structure

**Takeaway:** `\alert{JEPA học "thế giới thay đổi thế nào", không học "pixel trông như thế nào"}`

---

### Slide 5 — Các phương pháp chống collapse hiện tại: Whac-A-Mole

**`\frametitle{Heuristic Stack: Mỗi Method Vá Một Lỗ}`**

**TikZ — bảng 4 hàng với icon:**
```latex
\begin{tabular}{llll}
\toprule
\textbf{Method} & \textbf{Cơ chế chống collapse} & \textbf{Limitation} \\
\midrule
SimCLR   & Negative samples (contrastive)  & $\mathcal{O}(N^2)$ memory \\
BYOL     & Asymmetric arch + stop-gradient & Không có lý thuyết \\
DINO     & Teacher--student + EMA schedule & $>$5 hyperparameters \\
VICReg   & Whitening (variance term)       & Under-specified \\
I-JEPA   & Stop-gradient + mask prediction & Brittle, ViT-only \\
\bottomrule
\end{tabular}
```

Tô đỏ cột "Limitation" bằng `\cellcolor{bad!20}`.

**Lý luận — 4 limitations chung (dùng `\onslide` để reveal từng cái):**
1. **Under-specified:** Có thể minimize loss mà vẫn degenerate
2. **O(N²) complexity:** Không scale lên batch lớn
3. **Hyperparameter sensitive:** Đổi lr/arch → collapse
4. **No theory:** Không biết tại sao nó work

**Takeaway:** `\alert{Không có framework nào xuất phát từ first principles — chỉ là empirical patches}`

---

## PHẦN 2: CÂU HỎI LÝ THUYẾT — DISTRIBUTION NÀO LÀ TỐI ƯU? (Slides 6–11)

---

### Slide 6 — Câu hỏi pivot của bài báo

**`\frametitle{Câu Hỏi Thay Đổi Mọi Thứ}`**

**Layout:** Full-slide, chữ to ở giữa, ít text

**TikZ — arrow diagram:**
```
  Cách cũ:                        Cách LeJEPA:
  "Làm sao chống collapse?"   →   "Distribution NÀO là optimal?"
        (patch problem)                 (solve from roots)
```

**3 bullet — axioms của LeJEPA:**
1. Solve the prediction task *(standard)*
2. Enforce isotropic Gaussian distribution *(NEW)*
3. Không thêm gì khác

**Lý luận:** Thay vì hỏi "làm sao tránh collapse?", hỏi "distribution nào tối thiểu hoá downstream risk?". Nếu trả lời được câu 2, câu 1 tự giải quyết.

**Takeaway:** `\alert{Đổi góc nhìn từ "prevent collapse" sang "achieve optimal distribution"}`

---

### Slide 7 — Setup toán học: Linear Probe

**`\frametitle{Framework: Đánh Giá Qua Linear Probe}`**

**Equations — dùng `\begin{block}{}`:**

```latex
\begin{block}{Bài toán Linear Probe (Ridge Regression)}
\[
\hat{\beta} = \underset{\beta}{\arg\min} \|\mathbf{y} - \mathbf{Z}\beta\|_2^2 + \lambda\|\beta\|_2^2
\]
\end{block}
```

**TikZ — minh hoạ setup:**
- Ma trận Z (N × K): mỗi hàng là 1 embedding
- Vector y (N × 1): labels chưa biết
- Câu hỏi: distribution của Z nào giúp estimate β tốt nhất?

**Điểm then chốt:** Không biết y, nhưng vẫn phân tích bias/variance của estimator theo distribution của Z.

**Hai trường hợp so sánh:**
- `Z_aniso`: covariance eigenvalues `{λ₁ ≠ λ₂ ≠ ... ≠ λK}`
- `Z_iso`: covariance eigenvalues đều `= (1/K)·Σλk` (same energy, different geometry)

**Takeaway:** `\alert{Cùng "energy" (total variance) — geometry khác nhau → performance khác nhau}`

---

### Slide 8 — Lemma: Anisotropy khuếch đại Bias VÀ Variance

**`\frametitle{Bằng Chứng 1: Aniso Tệ Hơn Iso Về Cả Bias Và Variance}`**

**TikZ — 2 panel side by side:**

Panel trái — **Bias** (dùng pgfplots):
```tikz
% Trục X: số samples N
% Trục Y: cosine similarity giữa β_hat và β_true
% Đường aniso: thấp hơn
% Đường iso: gần 1 hơn
% Label: "Aniso luôn bias cao hơn iso"
```

Panel phải — **Variance** (scatter của decision boundary):
```tikz
% Vẽ 2D classification, 2 class
% Aniso (phải): nhiều đường tím chồng lên nhau (biến động lớn)
% Iso (trái): đường tập trung hơn
```

**2 Lemmas — dùng `\begin{alertblock}{}`:**

```latex
\begin{alertblock}{Lemma 3.1 — Aniso khuếch đại Bias}
Với $\lambda > 0$, luôn tồn tại task $\mathbf{y}$ sao cho
$\text{Bias}(\hat\beta_\text{aniso}) > \text{Bias}(\hat\beta_\text{iso})$
\end{alertblock}

\begin{alertblock}{Lemma 3.2 — Aniso khuếch đại Variance}
$\text{tr}(\text{Var}(\hat\beta_\text{aniso})) > \text{tr}(\text{Var}(\hat\beta_\text{iso}))$
\end{alertblock}
```

**Intuition nói khi present:** Aniso → một số chiều bị "squished" → estimator phải lean nhiều vào chiều đó → bias lên, variance lên.

**Takeaway:** `\alert{Iso thắng aniso về CẢ bias lẫn variance — với mọi downstream task}`

---

### Slide 9 — Theorem: Isotropic Gaussian tối ưu cho Nonlinear Probe

**`\frametitle{Bằng Chứng 2: Iso Gaussian Optimal Cho kNN Và Kernel Regression}`**

**TikZ — minh hoạ kNN bị bias:**
```tikz
% Vẽ 2D, data points lệch sang phải (aniso)
% Query point ở giữa
% Neighborhood ball: chứa toàn điểm bên phải → prediction biased
% So sánh với iso: neighborhood ball cân bằng hơn
```

**Theorem box:**
```latex
\begin{theorem}[Theorem 3.3 — Iso Gaussian Optimality]
Với constraint $\text{Tr}(\text{Cov}(\mathbf{Z})) = \kappa$, 
isotropic Gaussian là \textbf{nghiệm duy nhất} minimize 
Integrated Square Bias (ISB) cho cả kNN và kernel regression:
\[
\text{ISB}_{k\text{-NN}} = \frac{r_0^4}{(K+2)^2}\tau_g^2 J(p) + O(r_0^4)
\]
$J(p)$ = Fisher information của $p$ — minimize khi $p = \mathcal{N}(0, I)$.
\end{theorem}
```

**Takeaway:** `\alert{Kết quả này là UNIQUE — không có distribution nào khác đạt được}`

---

### Slide 10 — Tại sao Isotropic Gaussian? Intuition hình học

**`\frametitle{Geometric Intuition: Hình Cầu Là Tối Ưu}`**

**TikZ — 3D visualization (2D projection):**

```tikz
% Trái: Anisotropic cloud — hình ellipse dẹt
%   Vẽ ellipse, thêm mũi tên ở các hướng với độ dài KHÁC nhau
%   Label: "Khoảng cách méo — prediction biased"
%   Màu bad

% Phải: Isotropic cloud — hình tròn/cầu
%   Vẽ circle, thêm mũi tên ở các hướng với độ dài BẰNG nhau
%   Label: "Khoảng cách đều — prediction unbiased"  
%   Màu good
```

**Analogy text box (dùng `\begin{exampleblock}{}`):**
> Giống như bản đồ Mercator vs bản đồ đẳng diện: Mercator kéo dài ở vùng cực → đo khoảng cách sai. Iso Gaussian = bản đồ không méo cho embedding space.

**Key insight:** KNN và kernel regression phụ thuộc vào khoảng cách Euclidean → nếu data méo theo 1 chiều, mọi ước lượng dựa trên distance đều bị bias.

**Takeaway:** `\alert{N(0,I) = "bản đồ phẳng" của embedding space — mọi hướng như nhau}`

---

### Slide 11 — Tóm tắt phần lý thuyết

**`\frametitle{Kết Luận Lý Thuyết: Design Principle Cho LeJEPA}`**

**TikZ — flow diagram tóm tắt:**
```
[Bất kỳ downstream task] → [Linear probe] ─┐
                         → [kNN probe]     ─┼→ Optimal khi Z ~ N(0, I)
                         → [Kernel probe]  ─┘

⟹ Design principle: f_θ(x) nên ~ N(0, I)
```

**So sánh với prior work (table nhỏ):**
| | Prior SSL | LeJEPA |
|--|--|--|
| Lý do chọn distribution | "It works empirically" | **Proven optimal** |
| Guarantee | Không có | **Unique minimizer** |
| Valid cho linear + nonlinear | Chưa rõ | **Cả hai** |

**Takeaway:** `\alert{Lần đầu tiên: biết CHÍNH XÁC embeddings nên phân phối thế nào}`

---

## PHẦN 3: SIGReg — LÀM SAO ĐẠT ĐƯỢC N(0,I)? (Slides 12–18)

---

### Slide 12 — Thách thức: Test distribution trong high-dim

**`\frametitle{Thách Thức: Kiểm Tra Distribution Trong Không Gian Cao Chiều}`**

**TikZ — complexity comparison chart (horizontal bar chart):**
```pgfplots
% Bar chart so sánh
% Y-axis: methods (MMD, KL, Direct test, SIGReg)
% X-axis: complexity
% MMD: O(N²) — màu bad, dài
% KL: unstable — màu bad
% Direct multivariate: O(N²) — màu bad, dài
% SIGReg: O(N) — màu good, ngắn
```

**3 yêu cầu cần có — checklist:**
- [ ] Differentiable (cho gradient-based training)
- [ ] O(N) complexity (scale lên millions samples)
- [ ] Provably correct (guarantee convergence đến N(0,I))

**Lý luận:** Mọi multivariate normality test chuẩn (Henze-Zirkler, BHEP, Mardia) đều O(N²) hoặc tệ hơn. Curse of dimensionality → cần strategy khác.

**Takeaway:** `\alert{Không thể test N(0,I) trực tiếp trong high-dim — cần sketching}`

---

### Slide 13 — Ý tưởng: Random Slicing (Cramér-Wold)

**`\frametitle{Giải Pháp: Sketch Qua Random 1D Projections}`**

**TikZ — KEY DIAGRAM của paper (vẽ lại):**
```tikz
% Trái: Cloud điểm 3D (hoặc 2D với chiều thứ 3 ám chỉ)
% Giữa: 3-4 mũi tên hướng ngẫu nhiên từ cloud
% Phải: Mỗi mũi tên → 1 histogram 1D
%        Histogram xanh = khớp N(0,1)
%        Histogram đỏ = không khớp N(0,1)
```

**Theorem — `\begin{block}{}`:**
```latex
\begin{block}{Hyperspherical Cramér-Wold (Lemma 4.1)}
$X \stackrel{d}{=} Y \iff \langle \mathbf{u}, X \rangle \stackrel{d}{=} 
\langle \mathbf{u}, Y \rangle, \quad \forall \mathbf{u} \in \mathbb{S}^{K-1}$
\end{block}
```

**Practical version:** Không cần ALL directions — sample `M` directions ngẫu nhiên + reuse qua nhiều training steps.

**Theorem 4.2:** Với M random directions, test vẫn consistent (level + power) nếu M → ∞ cùng training.

**Takeaway:** `\alert{Bài toán K-chiều → M bài toán 1-chiều độc lập}`

---

### Slide 14 — Chọn test 1D nào? Họ Moment

**`\frametitle{Test 1D Họ Moment: Mạnh Nhưng Không Stable}`**

**Equation — Extended Jarque-Bera:**
```latex
\[
\text{EJB}(\mathbf{u}) = \frac{N\hat\mu^2}{\hat\sigma^2} 
+ \frac{(N-1)(\hat\sigma^2 - 1)^2}{2} 
+ \frac{N}{6}\left(\text{skew}^2 + \frac{(\text{kurt}-3)^2}{4}\right)
\]
```

**TikZ — gradient explosion visualization:**
```tikz
% X-axis: moment order k (1, 2, 3, 4, 5...)
% Y-axis: gradient norm ||∂L/∂z_i||
% Đường tăng theo O(k) → exploding
% Vùng đỏ: "Unstable gradient region"
```

**Theorem 4.3 (Insufficiency of K Moments):**
> Minimize `Σ cₖ(mₖ(P) - mₖ(Q))²` với finite K **không** imply `P = Q`

→ Với K nhỏ: shortcut solutions tồn tại. Với K lớn: gradient explode.

**Takeaway:** `\alert{Moment-based: identifiability vs stability — không thể có cả hai}`

---

### Slide 15 — Chọn test 1D nào? Họ CDF

**`\frametitle{Test 1D Họ CDF: Chính Xác Nhưng Không Differentiable}`**

**Equations — 2 test:**
```latex
T_w = N\int_{-\infty}^{\infty}(F_N(x) - F(x))^2 w(x)\, dF(x)
```
- `w(x) = 1` → Cramér-von Mises
- `w(x) = [F(x)(1-F(x))]⁻¹` → Anderson-Darling

**TikZ — sort operation visualization:**
```tikz
% Vẽ array các số ngẫu nhiên
% Mũi tên "sort" → array đã sort
% Label: "O(N log N), non-parallel"
% Gạch chân: "∂(sort)/∂x = undefined (piecewise)"
```

**2 limitations:**
1. **Sort breaks parallelism:** Multi-GPU cần synchronize → bottleneck
2. **Non-differentiable:** Cần relaxation (differentiable sort) → thêm hyperparameter

**Takeaway:** `\alert{CDF-based: cần sort → không parallel + non-differentiable → loại}`

---

### Slide 16 — Test 1D được chọn: Epps-Pulley (ECF-based)

**`\frametitle{Epps-Pulley: Stable, Scalable, Provable}`**

**Equation:**
```latex
\[
EP = N \int_{-\infty}^{\infty} \underbrace{|\hat\phi_X(t) - \phi(t)|^2}_{\text{ECF vs target CF}} 
\underbrace{w(t)}_{\text{Gaussian window}} dt
\]
\text{với } \hat\phi_X(t) = \frac{1}{N}\sum_{j=1}^N e^{itX_j}, \quad 
\phi(t) = e^{-t^2/2} \text{ (N(0,1) CF)}
```

**TikZ — ECF visualization:**
```tikz
% X-axis: t (từ -5 đến 5)
% Đường đen: theoretical CF = exp(-t²/2)
% Đường xanh (nhiều: mỗi batch): Empirical CF
% Nhận xét: ECF dao động quanh CF thật, bounded trong [-1, 1]
```

**Theorem 4.5 — Stability:**
```latex
\begin{alertblock}{Bounded Gradient (Theorem 4.5)}
\[
\left|\frac{\partial EP}{\partial z_i}\right| \leq \frac{4\sigma^2}{N}, \qquad
\left|\frac{\partial^2 EP}{\partial z_i^2}\right| \leq \frac{C\sqrt{\pi}\sigma^3}{2N}
\]
Gradient và curvature đều BOUNDED — bất kể distribution của input
\end{alertblock}
```

**3 lý do chọn (checklist ✓):**
- ✓ Differentiable (ECF = average of `eⁱᵗˣ`)
- ✓ O(N) — tính ECF là sum, no sort
- ✓ DDP-friendly (dùng `all_reduce` chuẩn)

**Takeaway:** `\alert{ECF bounded trong [-1,1] → gradient không bao giờ explode}`

---

### Slide 17 — SIGReg: Công thức hoàn chỉnh

**`\frametitle{SIGReg: Sketched Isotropic Gaussian Regularization}`**

**Definition box:**
```latex
\begin{block}{Definition (SIGReg)}
\[
\text{SIGReg}(\mathcal{A}, \{f_\theta(\mathbf{x}_n)\}) 
= \frac{1}{|\mathcal{A}|}\sum_{\mathbf{a}\in\mathcal{A}} 
\underbrace{EP\big(\{\mathbf{a}^\top f_\theta(\mathbf{x}_n)\}_{n=1}^N\big)}_{\text{Epps-Pulley trên 1D projection}}
\]
\end{block}
```

**PyTorch pseudocode** (dùng `lstlisting`):
```python
def SIGReg(x, global_step, num_slices=1024):
    g = torch.Generator(device=x.device)
    g.manual_seed(global_step)          # sync seed across GPUs
    A = torch.randn(x.size(1), num_slices, generator=g)
    A /= A.norm(p=2, dim=0)             # unit vectors
    t = torch.linspace(0, 3, 17)        # integration points
    phi = torch.exp(-0.5 * t**2)        # N(0,1) CF
    x_t = (x @ A).unsqueeze(-1) * t    # (N, M, T)
    cos_m = x_t.cos().mean(0)           # empirical CF (real)
    sin_m = x_t.sin().mean(0)           # empirical CF (imag)
    err = (cos_m - phi).square() + sin_m.square()
    return (err @ weights).mean() * N   # Epps-Pulley stat
```

**TikZ — 3 properties icons:**
```
[Differentiable] ───── [O(N) Scalable] ───── [Provably Correct]
  (ECF = avg)           (no sort)             (Cramér-Wold)
```

**Takeaway:** `\alert{~50 dòng code PyTorch, chạy trên bất kỳ GPU/TPU nào}`

---

### Slide 18 — SIGReg vượt qua Curse of Dimensionality

**`\frametitle{SIGReg Thoát Khỏi Curse of Dimensionality}`**

**TikZ — 2 charts side by side:**

Chart trái — **Fixed vs Resampled directions:**
```pgfplots
% X-axis: số directions M (16, 64, 256, 1024)
% Y-axis: test error sau training
% Đường xanh "Resampled each step": giảm nhanh
% Đường đỏ "Fixed directions": giảm chậm hơn nhiều
% Annotation: "M=16 resampled ≈ M=1000 fixed"
```

Chart phải — **Error bound vs smoothness:**
```pgfplots
% X-axis: Sobolev smoothness α
% Y-axis: required M để đạt ε error
% Đường giảm khi α tăng
% Annotation: "Smooth DNN → small M đủ"
```

**Theorem 4.7 — Unified Error Bound:**
```latex
\[
\mathbb{E}_{\mathbf{a}}\left[\int|\varphi_a(t) - \varphi_\mathcal{N}(t)|^2 dt\right] 
\leq C(K,\alpha)\cdot |\mathcal{A}|^{-2\alpha/(K-1)} \cdot \|\cdot\|_{H^\alpha}^2
\]
```

**2 lý do thoát curse:**
1. **Smoothness:** DNN naturally smooth (ví batch norm, dropout, weight decay) → α lớn → M = O(K) đủ
2. **SGD resampling:** Qua T steps, tổng số directions = M × T → coverage tích luỹ

**Takeaway:** `\alert{Nhờ smoothness + resampling: M=16 đủ dù K=2048}`

---

## PHẦN 4: LeJEPA — HỆ THỐNG HOÀN CHỈNH (Slides 19–23)

---

### Slide 19 — LeJEPA Loss: Kết hợp 2 thành phần

**`\frametitle{LeJEPA = Prediction Loss + SIGReg}`**

**Equations — highlight từng thành phần:**
```latex
\[
\mathcal{L}_\text{LeJEPA} = 
\underbrace{(1-\lambda)\cdot \frac{1}{B}\sum_{n=1}^B \mathcal{L}_\text{pred}(\{\mathbf{z}_{n,v}\})}_{\text{Invariance: các views phải agree}} 
+ \underbrace{\frac{\lambda}{V}\sum_{v=1}^V \text{SIGReg}(\{\mathbf{z}_{n,v}\})}_{\text{SIGReg: push về }N(0,I)}
\]
```

**Prediction loss:**
```latex
\mathcal{L}_\text{pred} = \frac{1}{V}\sum_{v'=1}^V \|\boldsymbol{\mu}_n - \mathbf{z}_{n,v'}\|_2^2, 
\quad \boldsymbol{\mu}_n = \frac{1}{V_g}\sum_{v=1}^{V_g}\mathbf{z}_{n,v}
```

**TikZ — pipeline hoàn chỉnh:**
```tikz
Image x
  │
  ├──aug──► view 1 (224×224, global) ──┐
  ├──aug──► view 2 (224×224, global) ──┤──► Encoder f_θ ──► Proj Head ──► z
  ├──aug──► view 3 (96×96,  local)  ──┤        (bất kỳ)    (3-layer MLP)
  ├── ...                             ──┤
  └──aug──► view 8 (96×96,  local)  ──┘
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
             Invariance Loss                                     SIGReg Loss
          (z_v ≈ μ, mean of globals)                        (z ~ N(0, I))
                     └────────────────────┬──────────────────────────┘
                                          ▼
                         L = (1-λ)·L_pred + λ·SIGReg
```

Tô **màu bad** + gạch chân XÓA: "No stop-gradient / No teacher-student / No EMA / No register tokens"

**Takeaway:** `\alert{1 loss · 1 hyperparameter · 0 heuristic}`

---

### Slide 20 — LeJEPA vs Prior JEPA: Head-to-head

**`\frametitle{Tại Sao LeJEPA Tốt Hơn DINO / I-JEPA}`**

**Bảng so sánh — dùng màu để highlight:**
```latex
\begin{tabular}{lccc}
\toprule
\textbf{Tiêu chí} & \textbf{DINO} & \textbf{I-JEPA} & \textbf{LeJEPA} \\
\midrule
Anti-collapse mechanism & \cellcolor{bad!20}EMA + stop-grad & \cellcolor{bad!20}Stop-grad + mask & \cellcolor{good!20}\textbf{Theorem} \\
\# Hyperparameters & \cellcolor{bad!20}$\geq$7 & \cellcolor{bad!20}$\geq$5 & \cellcolor{good!20}\textbf{1 ($\lambda$)} \\
Complexity & \cellcolor{neutral!20}$\mathcal{O}(N)$ & \cellcolor{neutral!20}$\mathcal{O}(N)$ & \cellcolor{good!20}$\mathcal{O}(N)$ \\
Architecture support & \cellcolor{bad!20}ViT only & \cellcolor{bad!20}ViT preferred & \cellcolor{good!20}\textbf{Any (60+)} \\
Loss informativeness & \cellcolor{bad!20}Low corr. & \cellcolor{bad!20}Low corr. & \cellcolor{good!20}\textbf{94\% Spearman} \\
Theory foundation & \cellcolor{bad!20}Post-hoc & \cellcolor{bad!20}Post-hoc & \cellcolor{good!20}\textbf{First-principles} \\
Core code (lines) & \cellcolor{bad!20}1000+ & \cellcolor{bad!20}500+ & \cellcolor{good!20}\textbf{$\approx$50} \\
\bottomrule
\end{tabular}
```

**Takeaway:** `\alert{Đơn giản hơn + lý thuyết chắc hơn + work trên mọi kiến trúc}`

---

### Slide 21 — λ Trade-off: Hyperparameter duy nhất

**`\frametitle{$\lambda$: Nút Duy Nhất Cần Chỉnh}`**

**TikZ — spectrum diagram:**
```tikz
% Thanh ngang từ 0 → 1
% λ = 0: "Pure Invariance" → collapse risk (màu bad)
% λ = 1: "Pure SIGReg" → uniform, no discrimination (màu bad)  
% λ ≈ 0.02–0.05: "Sweet spot" (màu good, highlight bracket)
% Dưới thanh: minh hoạ embedding cloud ở mỗi extreme + sweet spot
```

**pgfplots — performance vs λ curve:**
```pgfplots
% X-axis: λ (log scale: 0.001 → 0.5)
% Y-axis: linear probe accuracy (%)
% Đường cong với plateau rộng ở giữa
% Annotation: "Robust trên dải λ rộng"
% Highlight: λ = 0.02 (paper recommendation)
```

**Paper recommendation:**
```latex
\begin{block}{Recommended defaults}
$\lambda = 0.05$, $V_g = 2$, $V_l = 6$, batch size $\geq 128$, 
num\_slices $= 1024$, integration $t \in [-5, 5]$, 17 quadrature points
\end{block}
```

**Takeaway:** `\alert{λ robust trên dải rộng — không cần grid search}`

---

### Slide 22 — Informative Loss: Tính năng độc đáo

**`\frametitle{Bonus: Training Loss Dự Đoán Được Downstream Performance}`**

**TikZ — scatter plot (tự generate data):**
```pgfplots
% X-axis: LeJEPA training loss (normalized)
% Y-axis: Linear probe accuracy (%)
% Scatter points từ nhiều experiments (lr, wd, lambda khác nhau)
% Đường fit: Spearman correlation = 94%
% Label: "Mỗi điểm = 1 experiment configuration"
```

**Key result:**
```latex
\[
C^{(\alpha)} = \rho_s\!\left(\frac{\text{train\_loss}}{\lambda^\alpha}, \text{test\_acc}\right) 
\approx 94\%\ (\alpha=0),\ 99\%\ (\alpha=0.4)
\]
```

**Implication — `\begin{exampleblock}{}`:**
> Không cần chạy full linear probe để chọn model! Dùng training loss trực tiếp làm proxy → tiết kiệm 90% compute cho model selection.

**So sánh:**
- DINO loss: ~20% correlation với downstream
- I-JEPA loss: ~30% correlation
- **LeJEPA loss: 94% correlation**

**Takeaway:** `\alert{Lần đầu tiên: SSL có training signal thật sự có nghĩa}`

---

### Slide 23 — Relation to Prior Work: VICReg là special case

**`\frametitle{Kết Nối: LeJEPA Generalizes VICReg}`**

**TikZ — family tree diagram:**
```tikz
% Root: LeJEPA (SIGReg + Invariance)
%   Branch 1: T = Epps-Pulley → LeJEPA (recommended)
%   Branch 2: T = mean² + (std-1)² → VICReg (special case)
%   Branch 3: T = Jarque-Bera → Extended VICReg (unstable)
```

**Derivation box:**
```latex
\begin{block}{LeJEPA $\supset$ VICReg}
Khi $T(\mathbf{u}) = \hat\mu(\mathbf{u})^2 + (\hat\sigma(\mathbf{u})^2 - 1)^2$:
\[
\text{SIGReg} \xrightarrow{M \to \infty} \text{VICReg variance term}
\]
(SIGReg đảm bảo $\mathbb{E}[\mathbf{Z}]=\mathbf{0}$, $\text{Cov}(\mathbf{Z})=I$ trong expectation)
\end{block}
```

**Tại sao không dùng VICReg test?** Theorem 4.3: Finite moments → shortcut solutions → VICReg đã quan sát thấy điều này trong practice.

**Takeaway:** `\alert{VICReg là case đặc biệt của LeJEPA — nhưng với test yếu hơn}`

---

## PHẦN 5: KẾT QUẢ THỰC NGHIỆM (Slides 24–27)

---

### Slide 24 — Stability: 50+ kiến trúc, không cần tune

**`\frametitle{LeJEPA: Stable Trên 50+ Architectures Out-of-the-Box}`**

**pgfplots — dot plot:**
```pgfplots
% Y-axis: architecture names (grouped by family: ResNet, ViT, ConvNeXt, Swin, MaxViT...)
% X-axis: top-1 accuracy on ImageNet-10 (frozen linear probe)
% Mỗi dot = 1 model
% Range: 91.5% → 95%
% Label: "Spread chỉ 3.5% — không có model nào collapse"
% Color by family
```

**Key numbers (dùng `\begin{columns}`):**
- 50 models from 8 families
- Params range: 5M → 700M
- Best: 95% (ViT variants)
- Worst: 91.5% (EfficientNet variants)
- **Zero collapses** across all configs

**Ablation highlight** (từ paper Table 1):
- Batch size 128 → 1024: accuracy ~72% → 74% (stable)
- Num slices 512 → 4096: accuracy ~74% → 75% (minimal)
- Integration range [-1,1] → [-5,5]: accuracy 72% → 74% (small)

**Takeaway:** `\alert{50 models, zero collapses — không cần architecture-specific tuning}`

---

### Slide 25 — Scale: ViT-H/14 trên ImageNet-1K

**`\frametitle{LeJEPA Scales: ViT-H/14 Đạt 79\% Trên ImageNet-1K}`**

**pgfplots — comparison bar chart:**
```pgfplots
% X-axis: methods
% Y-axis: top-1 accuracy (frozen linear probe, %)
% Bars: I-JEPA ViT-H (300ep), LeJEPA ViT-L (100ep), LeJEPA ConvNeXtV2-H (100ep)
% Highlight: LeJEPA ViT-L (304M, 100ep) cạnh tranh với I-JEPA ViT-H (632M, 300ep)
```

**Transfer learning table (thu nhỏ từ paper Table 2):**
```latex
\small
\begin{tabular}{lrrrr}
\toprule
& \multicolumn{2}{c}{1-shot} & \multicolumn{2}{c}{10-shot} \\
Method & DTD & Avg & DTD & Avg \\
\midrule
I-JEPA ViT-H (300ep) & 27.71 & 30.20 & 57.68 & 60.51 \\
\textbf{LeJEPA ViT-L (100ep)} & \textbf{33.21} & 29.55 & \textbf{64.72} & \textbf{60.95} \\
\bottomrule
\end{tabular}
```

**Highlight:** LeJEPA ViT-L (304M, 100ep) ≥ I-JEPA ViT-H (632M, 300ep) — nhỏ hơn 2x, nhanh hơn 3x.

**Takeaway:** `\alert{3x ít compute, 2x nhỏ hơn — vẫn SOTA}`

---

### Slide 26 — In-Domain: Đánh bại DINOv2 trên Galaxy10

**`\frametitle{In-Domain SSL Đánh Bại Frontier Models}`**

**TikZ — side-by-side bar charts:**

Chart trái — Frozen backbone:
```pgfplots
% X-axis: shots per class (1, 5, 10, 50, full)
% Y-axis: accuracy
% Lines: DINOv2 ViT-S, DINOv3 ViT-S, LeJEPA ResNet-34, LeJEPA ConvNeXt-Nano
% LeJEPA lines ABOVE DINOv2/v3 consistently
```

Chart phải — Full finetuning:
```pgfplots
% Tương tự, LeJEPA vẫn thắng
```

**Lý luận quan trọng:** DINOv2/v3 được train trên hàng triệu ảnh tự nhiên. Galaxy10 là ảnh thiên hà — domain shift lớn. LeJEPA train trực tiếp trên 11,000 ảnh thiên hà → **in-domain SSL beats giant transfer learning**.

**Implication:**
```latex
\begin{exampleblock}{Paradigm Shift}
Không cần chờ Meta/Google ra frontier model cho domain của bạn.
Train LeJEPA trực tiếp trên data domain-specific với 1 GPU.
\end{exampleblock}
```

**Takeaway:** `\alert{Domain-specific SSL > Generic transfer — ngay cả với dataset 11K samples}`

---

### Slide 27 — Emergent Semantic Structure

**`\frametitle{Emergent Semantics: LeJEPA Học Segment Vật Thể}`**

**Visual — PCA visualization (tự tạo bằng matplotlib script):**

Hướng dẫn tự generate (không dùng ảnh paper):
```python
# Script để tạo PCA visualization tương tự:
# 1. Load pretrained ViT (timm)  
# 2. Extract last-layer features trên ảnh bất kỳ
# 3. PCA → 3 components → map to RGB
# 4. Overlay lên ảnh gốc
# => Màu ấm = foreground, màu lạnh = background
```

**TikZ placeholder (nếu không có GPU):**
```tikz
% Vẽ 2 box:
% Trái: ảnh gốc (hình chữ nhật màu xám)
% Phải: "PCA features" với gradient màu warm/cool
% Label: "Không có supervision — LeJEPA tự học"
```

**Kết quả:**
- Màu ấm (đỏ/tím) → foreground objects
- Màu lạnh (xanh/vàng) → background/foliage
- Video segmentation qua attention thresholding (zero labels)

**Takeaway:** `\alert{SSL objective đúng → semantic structure tự nổi lên}`

---

## PHẦN 6: IMPACT VÀ Ý NGHĨA (Slides 28–29)

---

### Slide 28 — Impact: Bản đồ ảnh hưởng

**`\frametitle{Impact: LeJEPA Mở Ra Những Gì?}`**

**TikZ — radial impact map (KHÔNG dùng chữ mô tả, dùng icon + tên ngắn):**
```tikz
% Center: LeJEPA (node tròn lớn, primary)
% 5 nhánh ra ngoài:
%   12h: Robotics / World Models (icon robot)
%   2h:  Scientific ML (icon telescope/microscope)  
%   4h:  Edge AI (icon chip/device)
%   8h:  Academic Theory (icon graduation cap)
%   10h: Open Ecosystem (icon GitHub/package)
% Mỗi nhánh có 1-2 example nhỏ

% Timeline ở dưới:
% 2020 SimCLR → 2021 DINO → 2023 DINOv2 → 2024 I-JEPA → 2025 LeJEPA★
%  (heuristic)   (scale)     (scale²)       (masking)    (theory)
```

**5 impact domains:**

| Domain | Cụ thể | Tại sao LeJEPA quan trọng |
|--------|---------|--------------------------|
| **World Models** | V-JEPA-2, robotics | JEPA cần foundation vững chắc |
| **Scientific ML** | Galaxy, medical imaging | Domain-specific SSL khả thi |
| **Edge AI** | 1-GPU training | Không cần data center |
| **Research** | Có thể prove được | Theory-friendly framework |
| **Open-source** | `pip install lejepa` | 50 LOC core |

**Takeaway:** `\alert{Nếu 2024 là năm của scaling laws, 2025 là năm tái khám phá structure}`

---

### Slide 29 — Sử dụng thực tế & Citation

**`\frametitle{Bắt Đầu Dùng LeJEPA}`**

**TikZ — node graph (dùng `\tikzstyle{node}`):**
```tikz
% Center: LeJEPA (circle, primary)
% Node 1 (trái): GitHub rbalestr-lab/lejepa
%   → sub-node: "50 LOC core" + "PyPI: pip install lejepa"
% Node 2 (trên): Integration
%   → sub-node: timm (any backbone) + Lightning (stable-pretraining)
% Node 3 (phải): Evaluation
%   → sub-node: OnlineProbe, OnlineKNN, RankMe callbacks
% Node 4 (dưới): Citation
%   → sub-node: arXiv 2511.08544, Balestriero & LeCun 2025
```

**Quick start code:**
```python
import lejepa

test = lejepa.multivariate.SlicingUnivariateTest(
    univariate_test=lejepa.univariate.EppsPulley(n_points=17),
    num_slices=1024
)
sigreg_loss = test(embeddings)  # embeddings: (N, D)
```

**Citation:**
```bibtex
@misc{balestriero2025lejepa,
  title={LeJEPA: Provable and Scalable Self-Supervised Learning},
  author={Balestriero, Randall and LeCun, Yann},
  year={2025}, eprint={2511.08544}
}
```

**Takeaway:** `\alert{pip install lejepa — bắt đầu trong 5 phút}`

---

## PHẦN 7: KẾT (Slide 30)

---

### Slide 30 — Kết luận

**`\frametitle{Kết Luận}`**

**TikZ — journey recap (3 bước, horizontal):**
```tikz
% Step 1: "Supervised / Heuristic SSL"
%   Icon: pile of patches/hacks
%   Label: "Fragile, expensive"

% Arrow →

% Step 2: "JEPA (2022)"  
%   Icon: encoder + predictor
%   Label: "Promising but no theory"

% Arrow →

% Step 3: "LeJEPA (2025)"
%   Icon: clean N(0,I) sphere
%   Label: "Theory + Practice united"
%   Màu good, larger size
```

**3 contributions — với icon check:**
```
✓ THEOREM:  Iso Gaussian uniquely minimizes downstream risk
✓ METHOD:   SIGReg = sliced Epps-Pulley, O(N), bounded gradient  
✓ RESULT:   SOTA trên 60+ archs, beats DINOv2 in-domain
```

**Big quote:**
```latex
\begin{center}
\Large\itshape
``If 2024 was the year of scaling laws,\\
2025 may be the year we rediscover structure.''
\end{center}
```

**Bottom:** Q\&A

---

## THỜI LƯỢNG

| Phần | Slides | Phút |
|------|--------|------|
| 1. Bối cảnh: AI học thế nào | 1–5 | 6 |
| 2. Lý thuyết: Distribution tối ưu | 6–11 | 8 |
| 3. SIGReg: Công cụ | 12–18 | 9 |
| 4. LeJEPA hoàn chỉnh | 19–23 | 7 |
| 5. Kết quả | 24–27 | 6 |
| 6. Impact | 28–29 | 3 |
| 7. Kết + Q&A | 30 | 5 |
| **Tổng** | **30** | **~44** |

---

## CHECKLIST CHO TỪNG SLIDE

Trước khi bàn giao cho Claude Sonnet để code LaTeX, mỗi slide phải có đủ:

- [ ] `\frametitle{}` rõ ràng
- [ ] TikZ hoặc pgfplots code (KHÔNG dùng `\includegraphics` từ paper)  
- [ ] Tối đa 5 bullet points per slide
- [ ] 1 `\alert{}` takeaway ở cuối
- [ ] Equations trong `\begin{block}{}` hoặc `\begin{alertblock}{}`
- [ ] Màu theo palette: `primary / accent / bad / good`

## HƯỚNG DẪN TIKZ CHO CLAUDE SONNET

Khi gen LaTeX, Sonnet cần:

1. **Scatter plots iso vs aniso** (slides 8, 10): dùng `pgfplots` với `\addplot[scatter, only marks]` + manually generate ~50 điểm trong code
2. **Architecture pipeline** (slide 19): dùng `tikz` với `node[rectangle, draw, rounded corners]` + `\draw[->]`
3. **Comparison tables** (slides 5, 17, 20): dùng `booktabs` + `\cellcolor{color!20}` để highlight
4. **Bar/line charts** (slides 24, 25, 26): dùng `pgfplots` với data embed trực tiếp (không đọc file)
5. **Radial impact map** (slide 28): dùng `tikz` với `\foreach` để vẽ 5 nhánh

Tất cả data cho charts phải được **hardcode** từ paper (không đọc file ngoài).

---

## PHÒNG TRÁNH LỖI KHI BIÊN DỊCH `slides.tex`

Phần này tổng hợp **tất cả các lỗi đã gặp** khi chạy `pdflatex slides.tex` cùng nguyên nhân gốc rễ và cách phòng tránh. **Đọc kỹ trước khi viết slide mới — mỗi rule đều xuất phát từ một lỗi thực tế đã xảy ra.**

### LỖI 1 — Lỗi nghiêm trọng (FATAL): `Illegal parameter number in definition of \iterate`

**Triệu chứng:**
```
! Illegal parameter number in definition of \iterate.
<to be read again>
l.994 \end{frame}
!  ==> Fatal error occurred, no output PDF file produced!
```

**Nguyên nhân gốc rễ:**
`\foreach` của TikZ xung đột với các **TeX primitive một chữ cái** đã được định nghĩa sẵn với tham số `#1`. Cụ thể đoạn code gây lỗi:
```latex
\foreach \a/\b in {emb/dir, dir/proj, proj/ep, ep/out}
  \draw[->, thick] (\a) -- (\b);
```
Ở đây `\b` trùng tên với primitive `\b#1` của LaTeX (dấu gạch dưới chữ cái). Khi `\foreach` cố gắng `\let` hoặc `\edef` lại `\b`, nó nhìn thấy tham số `#1` từ định nghĩa cũ và báo lỗi `Illegal parameter number`.

**Các tên macro 1 chữ cái KHÔNG ĐƯỢC dùng làm biến `\foreach`:**
- `\b` — bar-under accent (`\b{x}` → x̱)
- `\c` — cedilla (`\c{c}` → ç)
- `\d` — dot-under (`\d{x}` → ẋ)
- `\H` — Hungarian umlaut
- `\i`, `\j` — chữ i/j không chấm
- `\k` — ogonek
- `\l`, `\L` — chữ ł
- `\o`, `\O` — chữ ø
- `\r` — ring
- `\t` — tie-after
- `\u` — breve
- `\v` — caron / háček

**Cách phòng tránh — BẮT BUỘC tuân thủ:**

1. **Luôn dùng tên có ÍT NHẤT 2 ký tự** cho biến trong `\foreach`:
   ```latex
   % SAI:
   \foreach \a/\b in {...}
   \foreach \c/\d in {...}

   % ĐÚNG:
   \foreach \src/\dst in {emb/dir, dir/proj}
   \foreach \xa/\xb in {...}
   \foreach \nodeA/\nodeB in {...}
   ```

2. **Quy ước đặt tên thống nhất cho toàn bộ `slides.tex`:**
   - 1 biến: `\xx`, `\yy`, `\zz` hoặc tên mô tả `\angle`, `\rad`
   - 2 biến cặp đôi: `\src/\dst`, `\nodeA/\nodeB`, `\posX/\posY`
   - Toạ độ: `\px/\py` thay vì `\x/\y` (`\x`, `\y` ổn nhưng dễ va chạm với `\let\x=...` nội bộ TikZ)

3. **Trước khi commit slide có `\foreach`**, search `\foreach \[a-zA-Z]/` (regex) trong file và đảm bảo mọi biến **không phải** tên 1 chữ cái nguy hiểm.

4. **Test compile sớm:** Mỗi khi thêm `\foreach` mới, chạy `pdflatex -halt-on-error slides.tex` ngay để bắt lỗi sớm thay vì để dồn cuối.

---

### LỖI 2 — `Overfull \vbox (... pt too high)` (nội dung tràn xuống dưới slide)

**Triệu chứng (đã gặp tại nhiều slide):**
```
Overfull \vbox (37.73412pt too high) detected at line 187   % slide 2 outline
Overfull \vbox (116.48032pt too high) detected at line 398  % slide 6 — nặng nhất
Overfull \vbox (123.60107pt too high) detected at line 868  % slide 15
```

**Nguyên nhân:** Beamer 16:9 có chiều cao cố định ~57mm cho vùng nội dung. Khi nhồi quá nhiều: 1 bảng dài + 1 alertblock + 1 tikzpicture + `\takeaway{}` → tổng cao hơn slide.

**Cách phòng tránh — checklist BẮT BUỘC trước khi finalize mỗi slide:**

1. **Quy tắc 1-3-1 cho mỗi slide:**
   - **1** tiêu đề `\frametitle{}`
   - Tối đa **3** khối nội dung lớn (block / tikz / table / equation chính)
   - **1** dòng `\takeaway{}` cuối

2. **Dùng `\columns` để chia ngang thay vì xếp dọc:**
   ```latex
   \begin{columns}[t]   % [t] = top-aligned, không [c] (centered) khi nội dung dài
   \column{0.48\textwidth} ...
   \column{0.48\textwidth} ...
   \end{columns}
   ```

3. **Giảm font ở những khối phụ:** dùng `\small`, `\footnotesize`, `\tiny` (đặc biệt cho bảng so sánh và code listing).

4. **Bảng dài → cắt dòng:** nếu bảng có >5 hàng, cắt thành 2 cột song song hoặc chia 2 slide.

5. **`\vspace` âm cẩn thận:** tránh dùng `\vspace{-Xpt}` để ép nội dung — nó che mất chứ không sửa nguyên nhân. Thay vào đó: bỏ bớt content.

6. **TikZ `scale=0.7–0.85`** thay vì để mặc định `scale=1` khi figure cao quá.

7. **Test thường xuyên:** compile lại sau mỗi 2–3 slide; nếu thấy `Overfull \vbox > 30pt` thì sửa ngay slide đó, không để dồn.

8. **Đặc biệt cho slide có `tabular` + `alertblock` + `tikzpicture`:** ưu tiên xoá bớt `tikzpicture` hoặc đẩy sang slide kế tiếp. Đây là combo gây overfull nặng nhất (slide 6, 15).

---

### LỖI 3 — `Overfull \hbox` & `Underfull \hbox (badness 10000)` (chữ tràn ngang / xuống dòng xấu)

**Triệu chứng:**
```
Overfull \hbox (15.31937pt too wide) in paragraph at lines 351--351
Underfull \hbox (badness 10000) in paragraph at lines 868--868
```

**Nguyên nhân:**
- `Overfull \hbox`: 1 từ/công thức/`\texttt{...}` dài quá độ rộng cột.
- `Underfull \hbox` lặp đi lặp lại: bảng `tabular` có cột chữ dài bị bẻ dòng kiểu xấu (TeX không có chỗ để justify).

**Cách phòng tránh:**

1. **Dùng `tabularx` hoặc `>{\raggedright\arraybackslash}p{Xcm}` thay vì `l`/`c` cho cột chữ:**
   ```latex
   % SAI — text dài bị tràn:
   \begin{tabular}{llll}
   Method & Co che chong collapse & Limitation chinh \\

   % ĐÚNG — cột có độ rộng cố định, tự xuống dòng:
   \begin{tabular}{l p{4cm} p{3.5cm}}
   Method & Co che chong collapse & Limitation chinh \\
   ```

2. **Khi có `\texttt{very_long_command_name}`** trong cột bảng → bọc trong `\seqsplit{}` (gói `seqsplit`) hoặc tách thành dòng riêng dưới ô.

3. **Công thức toán dài** → dùng `\resizebox{\linewidth}{!}{$...$}` hoặc `\scalebox{0.85}{$...$}` cho công thức ngoại lai.

4. **Bullet text dài** → ưu tiên ý ngắn ≤ 12 chữ; nếu cần giải thích, dùng sub-bullet bằng `\begin{itemize}` lồng nhau với `\footnotesize`.

5. **Sửa `Underfull \hbox` cho bảng** bằng cách:
   - Tăng `\tabcolsep` (giãn cột) nếu bảng có chỗ trống.
   - Hoặc thêm `\arraystretch{1.2}` để hàng cao hơn cho phần chữ xuống dòng đẹp.

6. **`microtype` package** giúp giảm `Overfull/Underfull \hbox` đáng kể — nên thêm vào preamble:
   ```latex
   \usepackage{microtype}
   ```

---

### LỖI 4 — Tiếng Việt có dấu không hiển thị (hoặc render sai)

**Triệu chứng quan sát trong `slides.log`:**
```
[]|\T1/lmss/m/n/12 Cramer-
[]|\T1/lmss/m/n/12 Anderson-
```
→ font encoding `T1` (Western European) **không có** glyph cho ă, â, ê, ô, ư, đ, ạ, ậ... Cần encoding `T5` (Vietnamese) để render đúng.

**Trong file `slides.tex` cũ,** mọi text Việt đang viết **không dấu** (`Cong Thuc`, `Khong`, `Phuong Phap`) để né lỗi font — nhưng yêu cầu là phải có dấu.

**Cách phòng tránh — dùng `pdflatex` (KHÔNG cần xelatex/fontspec):**

1. **Preamble chuẩn cho `pdflatex` + tiếng Việt:**
   ```latex
   \usepackage[utf8]{inputenc}
   \usepackage[T5]{fontenc}              % T5 = Vietnamese encoding
   \usepackage[vietnamese]{babel}        % babel với option vietnamese
   ```
   `babel{vietnamese}` tự động kéo font `vntex/vnr` (Vietnamese Roman) — có đầy đủ glyph dấu.

2. **Compile chuẩn:**
   ```bash
   pdflatex slides.tex
   pdflatex slides.tex   # chạy 2 lần để TOC/nav đúng
   ```

3. **File phải lưu UTF-8 (không BOM):**
   ```bash
   file slides.tex   # phải in: "UTF-8 Unicode text"
   ```

4. **Test với 1 slide tiếng Việt ngắn TRƯỚC khi viết toàn bộ:**
   ```latex
   \begin{frame}{Kiểm Tra Dấu}
   Đầy đủ: ă â ê ô ơ ư đ Đ\\
   Sắc/huyền/hỏi/ngã/nặng: á à ả ã ạ — ế ề ể ễ ệ
   \end{frame}
   ```
   Nếu PDF hiển thị đúng → preamble OK, an tâm viết tiếp.

5. **Tránh xung đột `T5` với gói khác:**
   - **`fontenc`:** chỉ dùng `[T5]` (không phải `[T1]` hay `[T1,T5]`); babel sẽ tự setup
   - **`lmodern`:** **BỎ đi** — `vnr` là font Vietnamese-aware đã được babel kéo về tự động. Dùng cả `lmodern` + `T5` có thể gây thiếu glyph
   - **`fontspec`:** **TUYỆT ĐỐI KHÔNG dùng** với pdflatex — chỉ dành cho xelatex/lualatex

6. **Đối với `\frametitle`, `\textbf`, `\section`, label TikZ** — tất cả đều dùng UTF-8 trực tiếp. Không escape kiểu `\'a` `\^o`.

7. **Nếu vẫn lỗi `Package inputenc Error: Unicode char ... not set up`:**
   - Kiểm tra ký tự đó có nằm trong T5 không (T5 phủ đủ Vietnamese — dấu, dấu ngã ã, ơ, ư...)
   - Có thể do paste từ Word/Google Docs có dấu lạ (smart quote, em-dash khác): replace bằng dấu chuẩn
   - Backup: dùng `\usepackage{textcomp}` để có thêm glyph supplementary

---

### LỖI 5 — `lstlisting` lỗi khi chứa ký tự đặc biệt / tiếng Việt

**Nguyên nhân:** Listings mặc định không xử lý UTF-8; comment Python `# Phương pháp ...` chứa dấu sẽ vỡ với pdflatex.

**Cách phòng tránh:**

1. **Đơn giản nhất — comment Python viết tiếng Anh ngắn** (`# sync GPUs`, `# unit vectors`). Lý giải bằng tiếng Việt **trong text quanh listing**, không trong code. Đây là pattern khuyến nghị.

2. **Nếu BẮT BUỘC tiếng Việt trong code listing**, bật `extendedchars=true` + `literate=` để map dấu:
   ```latex
   \lstset{
     basicstyle=\ttfamily\tiny,
     keywordstyle=\color{primary}\bfseries,
     commentstyle=\color{neutral}\itshape,
     backgroundcolor=\color{black!5},
     frame=single, framerule=0pt,
     breaklines=true,
     language=Python,
     extendedchars=true,
     inputencoding=utf8,
     literate=
       {á}{{\'a}}1 {à}{{\`a}}1 {ả}{{\h{a}}}1 {ã}{{\~a}}1 {ạ}{{\d{a}}}1
       {ă}{{\u{a}}}1 {â}{{\^a}}1 {đ}{{\dj}}1 {ê}{{\^e}}1 {ô}{{\^o}}1
       {ơ}{{\o o}}1 {ư}{{\u u}}1 {ế}{{\'\^e}}1 {ệ}{{\d{\^e}}}1
   }
   ```

3. **Tránh `\` (backslash) ở cuối dòng Python** — viết gộp 1 dòng dùng `breaklines=true`:
   ```python
   # SAI (dễ vỡ trong listings):
   err = (x_t.cos().mean(0)-phi)**2 \
       +  x_t.sin().mean(0)**2

   # ĐÚNG (1 dòng, listings tự bẻ):
   err = (x_t.cos().mean(0)-phi)**2 + x_t.sin().mean(0)**2
   ```

---

### LỖI 6 — Mấy lỗi "ngầm" khác cần phòng

| Lỗi | Triệu chứng | Cách phòng |
|-----|-------------|------------|
| `Missing $ inserted` | Ký hiệu toán ngoài `$...$` | Mọi `<`, `>`, `\leq`, `\sim` PHẢI bọc `$...$` |
| `Undefined control sequence \cmark` trong tikzpicture | TikZ scope không thấy command ngoài | Định nghĩa `\cmark`/`\xmark` ở preamble (đã có), không trong frame |
| `! Package pgf Error: No shape named ... is known` | Quên `\usetikzlibrary{shapes.geometric}` | Preamble đã có — đừng xoá khi refactor |
| `caption={}` với `lstlisting` báo lỗi | Thiếu package `caption` | Bỏ option `caption=` khi không cần, hoặc `\usepackage{caption}` |
| `! Argument of \beamer@doifinframe has an extra }` | `\end{frame}` thiếu/thừa, lồng env sai | Dùng editor có brace-matching (VS Code LaTeX Workshop) |
| Bảng `\cellcolor` không lên màu | Quên `\usepackage{colortbl}` hoặc đặt sau `\\` | `\cellcolor{...}` phải đặt ở đầu ô, trước nội dung |
| Beamer + 16:9 cắt ảnh | TikZ vượt `\textwidth` | Bọc `\resizebox{\textwidth}{!}{...}` quanh `tikzpicture` |

---

### QUY TRÌNH BIÊN DỊCH AN TOÀN

```bash
# 1. Lưu file đảm bảo UTF-8
file slides.tex                              # phải là "UTF-8 Unicode text"

# 2. Compile lần 1 (bắt lỗi syntax)
pdflatex -interaction=nonstopmode -halt-on-error slides.tex

# 3. Nếu fatal error → đọc log, sửa, lặp lại
LANG=C grep -B2 -A5 "^!" slides.log

# 4. Compile lần 2 (cập nhật references, TOC, navigation)
pdflatex slides.tex

# 5. Kiểm tra warnings còn lại
LANG=C grep -E "Overfull|Underfull|Warning" slides.log | sort -u
```

**Quy tắc vàng:** bất kỳ `Overfull \vbox > 20pt` hoặc `Overfull \hbox > 10pt` đều phải sửa, **không** ignore. Beamer slide khác article — lỗi tràn box nghĩa là khán giả thấy chữ bị che / cắt.

---

### CHECKLIST CUỐI CÙNG TRƯỚC KHI HOÀN THÀNH

- [ ] Compile bằng `pdflatex` (chạy 2 lần) — tiếng Việt hiển thị đầy đủ dấu
- [ ] Preamble có đủ 3 dòng: `inputenc{utf8}` + `fontenc{T5}` + `babel{vietnamese}`
- [ ] KHÔNG có `\usepackage{lmodern}` + KHÔNG có `\usepackage{fontspec}`
- [ ] `slides.log` không còn dòng `! ` (lỗi fatal)
- [ ] Không còn `Overfull \vbox > 20pt` ở bất kỳ slide nào
- [ ] Mọi `\foreach` dùng biến ≥ 2 ký tự (không `\a`, `\b`, `\c`, `\d`, `\i`, `\j`, `\k`, `\l`, `\o`, `\r`, `\t`, `\u`, `\v`, `\H`)
- [ ] Mọi text tiếng Việt **có dấu**: `Công Thức`, `Không`, `Bằng Chứng`, `Lý Thuyết` (không `Cong Thuc`, `Khong`)
- [ ] Mọi bảng có cột chữ dài dùng `p{Xcm}` thay vì `l`/`c`
- [ ] PDF mở ra: 30 slide đủ, navigation hoạt động, không có ô đỏ "??" do reference vỡ

---

## NGUYÊN TẮC THIẾT KẾ SLIDE ĐẸP (DESIGN PRINCIPLES)

Slide đẹp **không** phải vẽ nhiều hình, dùng nhiều màu — mà là **truyền tải 1 ý duy nhất** sao cho khán giả hiểu trong **3 giây liếc nhìn đầu tiên**. Phần này tổng hợp các nguyên tắc thiết kế bắt nguồn từ Tufte (visual display), Reynolds (Presentation Zen), và Beamer best-practices.

### NGUYÊN TẮC 1 — Một slide, một message (1S1M)

**Quy tắc vàng:** Đọc tiêu đề slide, khán giả phải đoán được nội dung. Nếu tiêu đề là "Kết Quả" hay "Phương Pháp" thì SAI — quá rộng. Tiêu đề phải là **1 câu khẳng định** chứa kết luận của slide.

```latex
% SAI — tiêu đề mô tả chủ đề:
\frametitle{SIGReg}
\frametitle{Kết Quả Thực Nghiệm}

% ĐÚNG — tiêu đề là kết luận:
\frametitle{SIGReg: Bounded Gradient Cho Mọi Distribution}
\frametitle{LeJEPA Đạt 79\% ImageNet-1K Với Chỉ 100 Epoch}
```

**Test 1S1M:** che hết phần body, chỉ đọc `\frametitle{}` của 30 slide. Nếu chuỗi tiêu đề kể được toàn bộ câu chuyện paper → đạt. Nếu cần đọc body mới hiểu → tiêu đề chưa đủ mạnh.

---

### NGUYÊN TẮC 2 — Tỷ lệ vàng cho layout (Golden Ratio Layout)

Beamer 16:9 có vùng nội dung ~ `12.8cm × 6.5cm`. Phân chia theo **tỷ lệ 60/40** hoặc **1/3 — 2/3** cho hầu hết slide:

| Layout | Khi dùng | Tỷ lệ cột |
|--------|----------|-----------|
| **Visual + Text** | Có 1 hình/biểu đồ chính | `0.55 / 0.43` (visual lớn) |
| **Theorem + Diagram** | Định lý + minh họa | `0.50 / 0.47` |
| **Compare 2 things** | DINO vs LeJEPA, iso vs aniso | `0.48 / 0.48` (cân bằng) |
| **Big Equation Center** | Equation là main message | full-width, vspace lớn |
| **Hero Slide** | Title, transition, kết luận | full-slide, center, ít chữ |

**Tránh layout 3+ cột** — quá chật, khán giả không biết đọc đâu trước.

```latex
% Template Visual-heavy (60/40):
\begin{columns}[c]
\column{0.55\textwidth}
  \begin{tikzpicture}[scale=0.85] ... \end{tikzpicture}
\column{0.43\textwidth}
  \begin{block}{Key Insight}
    \small ...
  \end{block}
\end{columns}
```

---

### NGUYÊN TẮC 3 — Visual Hierarchy (cấu trúc thị giác)

Mắt khán giả quét slide theo **F-pattern** (trái-trên → phải-trên → trái-giữa). Tận dụng:

1. **Top-left = nơi đặt thông tin quan trọng nhất** (tiêu đề, key fact, "câu mở đầu")
2. **Center = visual chính** (TikZ diagram, biểu đồ)
3. **Bottom = takeaway** — điểm hạ cánh của mắt

**3 cấp độ visual hierarchy** trong 1 slide (ánh xạ ra font + màu):

```latex
% LEVEL 1 — Hook chính (chỉ 1 cái mỗi slide):
{\Large\bfseries\color{primary} Iso Gaussian là tối ưu duy nhất}

% LEVEL 2 — Supporting facts (2-4 cái):
\textbf{\color{primary} Theorem 3.3:} với constraint Tr(Cov)=κ...

% LEVEL 3 — Detail / chú thích (font nhỏ, màu xám):
{\footnotesize\color{neutral} J(p) = Fisher information of p}
```

**Quy tắc tương phản font-size:** giữa 2 cấp liền kề, **size phải khác ≥ 30%** (không phải 10%) để mắt phân biệt được. Ví dụ: `\Large` (14.4pt) → `\normalsize` (10pt) → `\footnotesize` (8pt).

---

### NGUYÊN TẮC 4 — White space (khoảng trắng) là bạn

Khoảng trắng KHÔNG phải lãng phí — nó là **bộ điều hướng mắt**. Slide quá đầy = khán giả mất phương hướng.

**Quy tắc 60/40 cho mật độ:**
- ~60% slide là content (text, hình, công thức)
- ~40% là khoảng trắng (margin, gap giữa block, padding trong block)

**Cách tăng white space hiệu quả:**

```latex
% Tăng vspace giữa các khối:
\vspace{8pt}    % nhỏ — giữa các bullet
\vspace{12pt}   % trung — giữa các block
\vspace{20pt}   % lớn — chia 2 phần slide

% Tăng margin block:
\setbeamertemplate{block begin}{
  \vspace{6pt}\begin{beamercolorbox}[sep=8pt]{...}
}

% Padding trong tikzpicture:
\begin{tikzpicture}[every node/.style={inner sep=6pt}]
```

**Test mật độ:** in slide ra giấy, nheo mắt. Nếu thấy 1 "khối đen đặc" → quá đầy. Nếu thấy ranh giới rõ ràng giữa các vùng → tốt.

---

### NGUYÊN TẮC 5 — Bảng màu có hệ thống (Color System) — PHONG CÁCH CHUYÊN NGHIỆP

**KHÔNG** dùng màu tùy hứng. Mỗi màu phải có **ngữ nghĩa cố định** trong toàn slide deck.

> **Triết lý màu sắc:** Dùng bảng màu **muted / desaturated** theo phong cách paper Nature/Science — không dùng màu bão hoà kiểu dashboard (đỏ tươi, xanh lá neon, cam sáng). Màu nhạt tạo cảm giác **uy quyền, chín chắn** và giúp khán giả tập trung vào nội dung thay vì bị phân tâm bởi màu sắc chói.

| Vai trò | Màu | HEX | Mô tả | Khi nào dùng |
|---------|-----|-----|-------|--------------|
| **Primary** (chủ đạo) | Navy đậm | `#2C3E6B` | Xanh navy truyền thống | Tiêu đề, encoder, "chủ thể chính" |
| **Accent** (nhấn) | Gold nhạt | `#C8A951` | Vàng đồng, không chói | Highlight, takeaway, "câu chốt" |
| **Good** (tích cực) | Sage green | `#5B8C6B` | Xanh rêu nhẹ | Kết quả tốt, ✓, "chọn cái này" |
| **Bad** (tiêu cực) | Terracotta | `#B85450` | Đỏ nâu ấm | Limitation, ✗, "tránh cái này" |
| **Neutral** (trung tính) | Warm gray | `#8C8C8C` | Xám trung tính | Chú thích, font phụ, baseline |

**Phiên bản nhạt** cho background — dùng tỷ lệ thấp (`!10` hoặc `!15` thay vì `!20`) để nền không quá đậm:
```latex
% Background tints — rất nhạt, không gây nhiễu thị giác
\definecolor{lightnavy}{HTML}{E8EAF0}     % nền nhạt cho block chính
\definecolor{lightgold}{HTML}{F5F0E0}     % nền cho takeaway
\definecolor{lightsage}{HTML}{E5EDE8}     % nền cho exampleblock
\definecolor{lightterracotta}{HTML}{F2E6E5}  % nền cho alertblock
\definecolor{lightgray}{HTML}{F5F5F5}     % nền trung tính

% Text trên nền trắng — dùng màu đầy đủ (không cần !80):
\textcolor{good}{kết quả tốt}
\textcolor{bad}{cần cải thiện}
```

**Beamer color mapping chuyên nghiệp:**
```latex
\setbeamercolor{structure}{fg=primary}
\setbeamercolor{alerted text}{fg=accent}
\setbeamercolor{block title}{bg=primary, fg=white}
\setbeamercolor{block body}{bg=lightnavy}
\setbeamercolor{block title alerted}{bg=primary!90, fg=white}   % KHÔNG dùng bad cho takeaway
\setbeamercolor{block body alerted}{bg=lightgold}
\setbeamercolor{block title example}{bg=good!80, fg=white}
\setbeamercolor{block body example}{bg=lightsage}
```

> **QUAN TRỌNG:** `\takeaway{}` dùng nền `primary!90` (navy đậm) + chữ trắng — KHÔNG dùng nền đỏ. Takeaway là câu kết luận tích cực, không phải cảnh báo. Nền đỏ gây hiểu nhầm là "lỗi" hoặc "nguy hiểm".

**Quy tắc 3 màu:** mỗi slide tối đa **3 màu chính** (không tính text đen + nền trắng). Hơn 3 → khán giả không biết đâu là điểm nhấn.

**Quy tắc saturation:** Không bao giờ dùng màu có saturation > 70% trên HSL color wheel. Màu bão hoà cao (ví dụ `#DC2626` pure red, `#10B981` neon green, `#F59E0B` bright amber) trông "màu mè" trên projector và mất chuyên nghiệp.

**Test mù màu:** ~8% nam giới mù màu đỏ-xanh. Đừng phụ thuộc DUY NHẤT vào màu để truyền tin — luôn kèm icon (✓/✗) hoặc text:
```latex
% SAI — chỉ màu phân biệt:
\textcolor{good}{Method A} vs \textcolor{bad}{Method B}

% ĐÚNG — màu + icon + text:
\good{\cmark\ Method A (winner)} vs \bad{\xmark\ Method B (collapse)}
```

**So sánh trước/sau bảng màu:**

| | Cũ (màu mè) | Mới (chuyên nghiệp) |
|--|-------------|---------------------|
| Primary | `#1E40AF` (xanh đậm bão hoà) | `#2C3E6B` (navy muted) |
| Accent | `#F59E0B` (cam chói) | `#C8A951` (gold nhạt) |
| Good | `#10B981` (xanh lá neon) | `#5B8C6B` (sage muted) |
| Bad | `#DC2626` (đỏ tươi) | `#B85450` (terracotta) |
| Takeaway bg | Đỏ tươi (`bad`) | Navy đậm (`primary!90`) |
| Block bg | Màu nền đậm (`!20`) | Màu nền rất nhạt (`!10`) |

---

### NGUYÊN TẮC 6 — Typography rules

**Font hierarchy cho Beamer:**
```latex
\setbeamerfont{title}{size=\Large, series=\bfseries}        % 14.4pt bold
\setbeamerfont{frametitle}{size=\large, series=\bfseries}   % 12pt bold
\setbeamerfont{block title}{size=\normalsize, series=\bfseries}
\setbeamerfont{normal text}{size=\normalsize}                % 11pt
\setbeamerfont{caption}{size=\footnotesize, shape=\itshape}  % 8pt italic
```

**KHÔNG bao giờ dùng:**
- Comic Sans, Times New Roman trong slide tech (lỗi thời / khó đọc xa)
- ALL CAPS cho nguyên đoạn (giảm tốc độ đọc 13–18%)
- Underline để nhấn (gây nhầm lẫn với hyperlink) — dùng **bold** hoặc *italic*
- 4+ kiểu font khác nhau trong 1 slide

**Khuyến nghị:**
- Sans-serif cho toàn slide (`Latin Modern Sans`, `Fira Sans`, `Source Sans Pro`)
- Serif chỉ trong công thức toán (`Latin Modern Math`)
- Mono (`ttfamily`) cho code, tên file, command

---

### NGUYÊN TẮC 7 — Animation reveal (xuất hiện từng phần)

**Dùng `\onslide<2->` / `\pause` / `\uncover`** khi:
- Có > 4 bullet → reveal từng cái để khán giả không đọc trước
- Có 2 sơ đồ "before/after" → show trước, click → show sau
- Equation phức tạp → show từng term

```latex
\begin{frame}{LeJEPA Loss}
\[
\mathcal{L}_\text{LeJEPA} =
\onslide<2->{(1-\lambda)\cdot \mathcal{L}_\text{pred}} +
\onslide<3->{\lambda\cdot \text{SIGReg}}
\]
\onslide<2->{\textbf{Term 1:} invariance giữa các views}\\
\onslide<3->{\textbf{Term 2:} push embeddings về $\mathcal{N}(0,I)$}
\end{frame}
```

**KHÔNG lạm dụng animation:**
- Slide tĩnh (table, figure đơn) → không cần `\pause`
- Tránh `\transblindshorizontal` và các transition kiểu PowerPoint — phân tâm
- Mỗi slide tối đa **3-4 reveal** (không 10+)

---

## BỐ CỤC TEMPLATES — 8 LAYOUT CHUẨN CHO LeJEPA

Dưới đây là 8 layout đã được kiểm chứng cho slide tech. Tái sử dụng — không phát minh layout mới giữa chừng.

### LAYOUT A — Title Slide (Hero)

**Khi dùng:** Slide 1, slide kết, slide chuyển section lớn.

```latex
\begin{frame}[plain]
\vspace{1cm}
\begin{center}
  {\Huge\bfseries\color{primary} LeJEPA}\\[8pt]
  {\Large Provable \& Scalable SSL}\\
  {\large Without the Heuristics}\\[24pt]
  {\large Randall Balestriero \& Yann LeCun}\\
  {\normalsize arXiv: 2511.08544}\\[16pt]
  \begin{tikzpicture}[scale=0.6]
    % Logo nhỏ ở giữa
  \end{tikzpicture}
\end{center}
\end{frame}
```

**Đặc điểm:** ít chữ (≤ 20 từ), font lớn, center, có 1 element visual nhỏ.

---

### LAYOUT B — Visual Dominant (60/40)

**Khi dùng:** Slide có 1 hình quan trọng + giải thích ngắn (slides 4, 9, 13, 19).

```
┌────────────────────────────────┐
│ Frametitle                     │
├──────────────────┬─────────────┤
│                  │ Block:      │
│   TIKZ /         │ Key insight │
│   PGFPLOT        │ ────────    │
│   (60%)          │ Bullet 1    │
│                  │ Bullet 2    │
│                  │ Bullet 3    │
├──────────────────┴─────────────┤
│ \takeaway{...}                 │
└────────────────────────────────┘
```

```latex
\begin{frame}{Frametitle là kết luận của slide}
\begin{columns}[c]
\column{0.58\textwidth}
  \begin{tikzpicture}[scale=0.9] ... \end{tikzpicture}
\column{0.40\textwidth}
  \begin{block}{Insight}
    \footnotesize 2-3 dòng
  \end{block}
  \begin{itemize}\footnotesize
    \item Bullet 1
    \item Bullet 2
  \end{itemize}
\end{columns}
\takeaway{Câu chốt 1 dòng}
\end{frame}
```

---

### LAYOUT C — Comparison (50/50)

**Khi dùng:** So sánh 2 thứ song song — DINO vs LeJEPA, iso vs aniso, before vs after (slides 7, 10, 11).

```
┌────────────────────────────────┐
│ Frametitle                     │
├───────────────┬────────────────┤
│ ✗ BAD SIDE    │ ✓ GOOD SIDE    │
│               │                │
│ TikZ + bullet │ TikZ + bullet  │
│ (đỏ)          │ (xanh)         │
│               │                │
├───────────────┴────────────────┤
│ \takeaway{...}                 │
└────────────────────────────────┘
```

```latex
\begin{columns}[t]
\column{0.48\textwidth}
  \begin{center}\bad{\xmark\ \textbf{Anisotropic}}\end{center}
  \begin{tikzpicture}[scale=0.75] ... \end{tikzpicture}
  \footnotesize Bias cao, variance cao
\column{0.48\textwidth}
  \begin{center}\good{\cmark\ \textbf{Isotropic}}\end{center}
  \begin{tikzpicture}[scale=0.75] ... \end{tikzpicture}
  \footnotesize Bias thấp, variance thấp
\end{columns}
```

**Mẹo:** **luôn để cái "đúng" bên phải** — mắt người dừng cuối cùng ở đây, gây ấn tượng mạnh hơn.

---

### LAYOUT D — Big Equation (Center Stage)

**Khi dùng:** Khi 1 công thức LÀ message của slide (slides 17, 19).

```
┌────────────────────────────────┐
│ Frametitle                     │
│                                │
│         ┌────────────┐         │
│         │  EQUATION  │         │
│         └────────────┘         │
│                                │
│   Term 1 = ...   Term 2 = ...  │
│                                │
│   \takeaway{...}               │
└────────────────────────────────┘
```

```latex
\begin{frame}{LeJEPA = Prediction + SIGReg}
\vspace{0.4cm}
\begin{center}
  \large
  \[
  \mathcal{L}_\text{LeJEPA} =
  \underbrace{(1-\lambda)\,\mathcal{L}_\text{pred}}_{\color{primary}\text{invariance}}
  + \underbrace{\lambda\,\text{SIGReg}}_{\color{good}\text{regularize}}
  \]
\end{center}
\vspace{0.3cm}
\begin{columns}
\column{0.48\textwidth}
  \begin{block}{\color{primary} Invariance}\footnotesize ... \end{block}
\column{0.48\textwidth}
  \begin{block}{\color{good} SIGReg}\footnotesize ... \end{block}
\end{columns}
\takeaway{1 hyperparameter $\lambda$ điều phối 2 lực}
\end{frame}
```

**Mẹo:** dùng `\underbrace` + `\overbrace` để annotate term ngay trong equation — KHÔNG để khán giả tự match equation với text bên dưới.

---

### LAYOUT E — Theorem Box

**Khi dùng:** Slide phát biểu định lý / lemma quan trọng (slides 8, 9, 14).

```
┌────────────────────────────────┐
│ Frametitle: Tên Theorem        │
│                                │
│  ╔══════════════════════════╗  │
│  ║ Theorem (alertblock đỏ)  ║  │
│  ║   Statement              ║  │
│  ╚══════════════════════════╝  │
│                                │
│  Intuition + visual nhỏ        │
│                                │
│  \takeaway{...}                │
└────────────────────────────────┘
```

```latex
\begin{frame}{Theorem 3.3 — Iso Gaussian Là Tối Ưu Duy Nhất}
\begin{alertblock}{Theorem 3.3 (Balestriero \& LeCun, 2025)}
  Với constraint $\text{Tr}(\text{Cov}(\mathbf{Z})) = \kappa$:
  \[ \arg\min_p \text{ISB}(p) = \mathcal{N}(\mathbf{0}, \tfrac{\kappa}{K}I) \]
  \textbf{Unique} minimizer cho cả kNN và kernel regression.
\end{alertblock}

\begin{columns}[c]
\column{0.55\textwidth}
  \footnotesize
  \textbf{Intuition:} Fisher information $J(p)$ minimize duy nhất tại Gaussian
  $\Rightarrow$ minimize ISB cũng tại Gaussian.
\column{0.42\textwidth}
  \begin{tikzpicture}[scale=0.75] ... \end{tikzpicture}
\end{columns}
\takeaway{Không phải bất kỳ regularizer nào — phải là $\mathcal{N}(0,I)$}
\end{frame}
```

---

### LAYOUT F — Comparison Table

**Khi dùng:** So sánh ≥ 3 phương pháp trên ≥ 3 tiêu chí (slides 6, 20).

**Quy tắc:**
- Tối đa **5 hàng × 4 cột** (nếu nhiều hơn → cắt slide)
- Cột cuối là phương pháp đề xuất, cell tô màu **good!20**
- Các cell limitation tô **bad!20**

```latex
\begin{frame}{LeJEPA So Với SOTA: 7 Tiêu Chí}
\centering\footnotesize
\begin{tabular}{l p{2.2cm} p{2.2cm} p{2.5cm}}
\toprule
\textbf{Tiêu chí} & DINO & I-JEPA & \textbf{LeJEPA} \\
\midrule
Anti-collapse
  & \cellcolor{bad!20}EMA + stop-grad
  & \cellcolor{bad!20}Stop-grad + mask
  & \cellcolor{good!20}\textbf{Theorem} \\
\# Hyperparameters
  & \cellcolor{bad!20}$\geq$ 7
  & \cellcolor{bad!20}$\geq$ 5
  & \cellcolor{good!20}\textbf{1 ($\lambda$)} \\
% ... 3-5 hàng nữa
\bottomrule
\end{tabular}
\takeaway{Đơn giản hơn + lý thuyết chặt hơn + work mọi kiến trúc}
\end{frame}
```

**Mẹo:**
- Header in đậm, có `\toprule` `\midrule` `\bottomrule` (booktabs)
- Cột cuối in `\textbf` để nhấn
- KHÔNG dùng `\hline` (mỏng, xấu) — luôn dùng `booktabs`

---

### LAYOUT G — Pipeline / Architecture Diagram

**Khi dùng:** Vẽ kiến trúc LeJEPA, JEPA, training pipeline (slides 5, 19).

```
┌────────────────────────────────┐
│ Frametitle                     │
│                                │
│  Input → Encoder → Proj → z    │
│                       │        │
│                   ┌───┴───┐    │
│                   ▼       ▼    │
│                  Loss1  Loss2  │
│                                │
│  \takeaway{...}                │
└────────────────────────────────┘
```

```latex
\begin{tikzpicture}[
  node distance=1.2cm,
  every node/.style={font=\small},
  box/.style={draw, rounded corners=4pt, minimum height=0.8cm, minimum width=1.6cm},
  primary box/.style={box, fill=primary!80, text=white},
  accent box/.style={box, fill=accent!80, text=white},
  good box/.style={box, fill=good!30, draw=good},
]
  \node[box, fill=lightblue] (img) {Image};
  \node[primary box, right=of img] (enc) {$f_\theta$};
  \node[accent box, right=of enc] (proj) {Proj};
  \node[good box, right=of proj] (z) {$\mathbf{z}$};

  \draw[->, thick] (img) -- (enc);
  \draw[->, thick] (enc) -- (proj);
  \draw[->, thick] (proj) -- (z);
\end{tikzpicture}
```

**Mẹo:**
- Dùng `\tikzset` define style 1 lần ở preamble, reuse trong mọi slide
- `node distance` cố định để các diagram nhìn nhất quán
- Mũi tên: `->, thick` cho luồng chính, `->, dashed, thin` cho luồng phụ
- Block to nhỏ tỉ lệ với "tầm quan trọng" — encoder to hơn projection head

---

### LAYOUT H — Result Highlight (Big Number)

**Khi dùng:** Khoe 1 con số/kết quả ấn tượng (slides 25, 26).

```
┌────────────────────────────────┐
│ Frametitle                     │
│                                │
│    ┌────────────────────┐      │
│    │      79.0%         │      │
│    │   ImageNet-1K      │      │
│    │   (linear probe)   │      │
│    └────────────────────┘      │
│                                │
│  Context: ViT-H/14, 100 ep     │
│  Beat: I-JEPA ViT-H 300 ep     │
│                                │
│  \takeaway{...}                │
└────────────────────────────────┘
```

```latex
\begin{frame}{LeJEPA Scales: ViT-H/14 Đạt 79\% ImageNet-1K}
\vspace{0.5cm}
\begin{center}
  \begin{tcolorbox}[
    colback=primary!10, colframe=primary,
    width=0.6\textwidth, halign=center
  ]
    {\Huge\bfseries\color{primary} 79.0\%}\\[4pt]
    {\normalsize Linear probe accuracy}\\
    {\footnotesize\color{neutral} ImageNet-1K, ViT-H/14, 100 epochs}
  \end{tcolorbox}
\end{center}
\vspace{0.3cm}
\begin{columns}
\column{0.48\textwidth}
  \begin{block}{Setup}\footnotesize
    304M params, 100 epochs, $\lambda = 0.05$
  \end{block}
\column{0.48\textwidth}
  \begin{exampleblock}{So với baseline}\footnotesize
    I-JEPA ViT-H (632M, 300ep): 77.3\%\\
    \good{$\Rightarrow$ 2× nhỏ hơn, 3× nhanh hơn}
  \end{exampleblock}
\end{columns}
\takeaway{Bigger result với less compute}
\end{frame}
```

**Mẹo:** Big number font phải **≥ 3× font body** để gây ấn tượng. Dùng `\Huge` hoặc `\fontsize{48pt}{56pt}\selectfont`.

---

## 10 LỖI DESIGN PHỔ BIẾN — TRÁNH NGAY

| # | Lỗi | Hệ quả | Cách sửa |
|---|-----|--------|----------|
| 1 | "Wall of text" — bullet 5+ dòng mỗi cái | Khán giả không đọc kịp | ≤ 12 từ/bullet, dùng sub-bullet |
| 2 | Font dưới 9pt | Hàng cuối hội trường không thấy | Min `\footnotesize` (8pt), ưu tiên `\small` |
| 3 | 4+ màu trên 1 slide | Mất focus, rối | Tối đa 3 màu chính + neutral |
| 4 | Code listing > 15 dòng | Không ai đọc | Cắt phần quan trọng nhất, tối đa 12 dòng |
| 5 | Equation > 1.2× độ rộng slide | Bị cắt / tràn | `\resizebox{\linewidth}{!}{...}` hoặc `\begin{align*}` đa dòng |
| 6 | Chart không có axis label | Vô nghĩa | LUÔN có `xlabel`, `ylabel`, đơn vị |
| 7 | TikZ không có legend với `\addplot` ≥ 2 | Không phân biệt được lines | Bắt buộc `\legend{...}` khi ≥ 2 đường |
| 8 | Screenshot từ paper | Mờ, font không khớp, lười | Vẽ lại bằng TikZ — đẹp hơn + nhất quán |
| 9 | Đặt logo/tên ở mọi slide | Phân tâm, lặp lại | Logo chỉ ở title slide; footer đủ tên ngắn |
| 10 | Animation phức tạp (rotate, fly-in) | Trông "PowerPoint 2003" | Chỉ dùng `\pause`, `\onslide<2->` |

---

## QUY TRÌNH THIẾT KẾ 1 SLIDE (TỪ Ý TƯỞNG → CODE)

**Bước 1 — Viết tiêu đề trước (1 phút):**
- Hỏi: "Sau slide này, khán giả phải nhớ điều gì?"
- Viết câu trả lời thành `\frametitle{}` (1 câu khẳng định)

**Bước 2 — Chọn layout (1 phút):**
- Visual chính? → Layout B
- So sánh 2 thứ? → Layout C
- 1 công thức? → Layout D
- Định lý? → Layout E
- Bảng? → Layout F
- Kiến trúc? → Layout G
- 1 con số? → Layout H

**Bước 3 — Sketch trên giấy (3 phút):**
- Vẽ tay layout, ghi vị trí: title, visual, text block, takeaway
- KHÔNG mở LaTeX trước khi sketch xong

**Bước 4 — Viết code (10–20 phút):**
- Copy template layout đã chọn
- Fill content
- Compile sau mỗi 3 phút (bắt lỗi sớm)

**Bước 5 — Refine (5 phút):**
- In ra A4, lùi xa 2m → vẫn đọc được tiêu đề + takeaway?
- Khán giả 3 giây → hiểu message?
- Nếu KHÔNG → đơn giản hóa, không thêm

**Bước 6 — Takeaway (1 phút):**
- 1 dòng, ≤ 15 từ, là **kết luận** (không lặp lại tiêu đề)
- Format: `\takeaway{...}` hoặc `\alert{...}` cuối slide

---

## CHECKLIST DESIGN — TRƯỚC KHI SHIP MỖI SLIDE

- [ ] **Tiêu đề là câu kết luận**, không phải tên chủ đề
- [ ] **Khán giả 3-giây-test:** che body, đọc title → đoán được nội dung
- [ ] **Tối đa 3 màu chính** trên slide (primary + accent + 1 cái nữa)
- [ ] **Font size ≥ `\footnotesize` (8pt)** ở mọi text — không có chữ < 8pt
- [ ] **Bullet ≤ 12 từ**, tổng ≤ 5 bullet
- [ ] **Equation có `\underbrace`/`\overbrace`** annotate term
- [ ] **Chart có `xlabel`, `ylabel`, `\legend`** (nếu ≥ 2 lines)
- [ ] **`\takeaway{}` ở cuối slide** với câu chốt khác tiêu đề
- [ ] **White space ≥ 30%** mặt slide (không bị "wall of content")
- [ ] **Compile không có warning Overfull > 20pt**
- [ ] **Tiếng Việt có đủ dấu** trên mọi text
- [ ] **In thử A4 → đọc được ở 2m**
