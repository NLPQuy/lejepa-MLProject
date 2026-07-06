# Ablation kết quả đo được — imagenet10 / ViT-S/16

Nguồn: `mlinh776/lejepa-ablation-full` (22 version Kaggle) → gộp vào
`ablation_results/` (62 job, 8 ablation). Metric = **paper-spec linear probe top1**
(concat CLS last-2 + LN + AdamW lr1e-3 wd1e-6), lấy từ `summary.json → paper_eval`.

**Artefacts:**
- Bảng số đầy đủ: `ablation_results/ablation_summary.{md,csv}`
- Hình (theo pipeline paper `tab:ablations`): `ablation_results/figures/`
  — `A_epps_heatmap`, `B_views_heatmap`, `C_components_bars`, `D_sensitivity_tornado`,
  và `paper_tables` (bản dựng lại bảng (a)–(e) của paper trên dữ liệu ta).
- Sinh lại: `python scripts/ablations/{collect_summaries,viz_ablation,viz_paper_tables}.py ablation_results/`

## Framing theo paper
Paper (`tab:ablations`, arXiv:2511.08544) dùng ablation để chứng minh **"LeJEPA ổn định
qua mọi siêu tham số; vài cái cải thiện nhẹ (num_slices, projector dim); KHÔNG lựa chọn
nào gây collapse"**. Ta dựng lại đúng pipeline đó (bảng grid top1 theo trục hyperparameter
+ collapse study) trên **regime khác**: ViT-S/16 · imagenet10 · batch lớn. Kết luận:
robustness được xác nhận ở hyperparameter chính, **nhưng** một số xu hướng đảo ngược
(t_max, views) và **đặt sai component vẫn collapse** — chi tiết bên dưới.

## Setup
- ViT-Small/16, imagenet10 (~28k train / 11.8k val), 100 epoch pretrain, seed=42.
- **Baseline chung (anchor): top1 = 0.5946** — config `slices=1024, t_max=3, n_pts=17,
  agg=cls, sigreg=proj, predictor=none, proj=MLP, drop_path=0.1, mask=0.3, n_views=8`.
  Anchor này tái lập **y hệt** (0.5946 / loss 1.078 / best_ep 72) qua 7 ablation
  → deterministic, đáng tin làm mốc.

## ⚠️ Comparability — đọc trước khi trích số (QUAN TRỌNG)

Có **hai** thang khác nhau, đừng trộn:

**(1) so với paper.** Paper Table 1 = ViT-L/14, ImageNet-1K, frozen probe. Của ta =
ViT-S/16, imagenet10. **Absolute KHÔNG so được** — chỉ so *xu hướng/hình dạng*. Eval
recipe khớp paper.

**(2) so với baseline dự án (batch1/2).** `climb_bench/.../eval_results/batch_2/baseline_100.json`
cho **top1 = 0.8949** — **cùng eval recipe, cùng data imagenet10 28k, cùng frozen ViT-S/16**.
Nhưng anchor của bộ ablation này = **0.5946**, thấp hơn **~30 điểm**, vì **khác harness
pretrain**:

Config baseline = `batch1/exp_baseline.py` → `LeJEPA(lamb=0.02, n_slices=1024,
n_points=17, projector_dim=512)` + default `_common.py`; đối chiếu với config ablation
(`summary.json`):

| tham số | baseline dự án (0.8949) | anchor ablation (0.5946) |
|---|---|---|
| **train transform** | **RRC + flip + color-jitter + grayscale + blur + solarize** | **chỉ RandomResizedCrop** (thiếu photometric!) |
| **batch_size** | **128** | **512** (4×) |
| **λ (lamb)** | **0.02** | **0.05** (2.5×) |
| **patch_mask_ratio** | **0.0** (default) | **0.3** |
| lr | 4e-4 | 5e-4 |
| precision | 16-mixed (fp16) | bf16-mixed |
| max_epochs | ~100 (ckpt `epoch=099`) | 100 |
| drop_path_rate | 0.1 (default) | 0.1 — **giống** |
| backbone/n_slices/n_points/t_max/proj_dim/views(2+6)/wd/res(224,96)/sigreg=proj/predictor=none/agg=cls | giống | giống |

→ top5 cũng chênh (0.99 vs 0.92) nên là **backbone thật sự yếu hơn**, không phải lỗi
đo probe. **Nguyên nhân chính (phát hiện qua review code):** harness ablation
[`train_lejepa_ablation.py:152`](../../scripts/train_lejepa_ablation.py#L152) thiếu **toàn
bộ photometric augmentation** (color-jitter / blur / grayscale / flip / solarize) — chỉ
`RandomResizedCrop`, trong khi baseline có đủ. SSL invariance-based thường mất **15–30pt**
khi thiếu color+blur → giải thích trần thấp *toàn hệ thống* (ngay config tốt nhất cũng chỉ
~73%). Phụ: batch 512 (~4× ít steps → under-train), λ=0.05, fp16. patch_mask 0.3 chỉ
±1.6pt, **không** phải thủ phạm.
**Hệ quả:** mọi số ablation ở đây **chỉ dùng để so Δ nội bộ** (quanh 0.5946); **KHÔNG**
ghép cạnh baseline 0.8949 hay các idea batch1/2.

## Tính hợp lệ của pipeline & độ tin cậy kết luận

Pipeline ablation chạy ở **regime under-fit** (thiếu photometric aug + batch lớn) → absolute
thấp. **Nhưng vẫn hợp lệ cho mục tiêu benchmark**, vì (a) đồ án so *Δ giữa các cấu hình*,
không phải absolute; (b) **mọi run cùng điều kiện** → so sánh tương đối công bằng; (c) đã
tách bạch không ghép với thang baseline dự án. **→ Không cần chạy lại.**

Phân loại độ tin cậy từng kết luận:

| Kết luận | Phụ thuộc regime? | Tin cậy |
|----------|-------------------|---------|
| Collapse: `sigreg=embed/both`, `projector=Linear` | ❌ structural (capacity/toán học) | ✅ **vững** |
| `predictor` không cần | ❌ structural | ✅ **vững** |
| epps `num_slices`↑ tốt · `n_points` phẳng | ❌ tính chất SIGReg estimator | ✅ **vững** |
| epps `t_max` nhỏ tốt hơn | ~ regime-dependent | 🟡 giữ, ghi chú |
| **Nhóm C: `drop_path` / `patch_mask` không giúp** | ✅ **regime under-fit** | 🔴 **hạ tone** |
| **Views: ít view tốt hơn** | ✅ một phần regime | 🔴 **hạ tone** |

**Về nhóm C — cơ chế chính xác (không phải "confound augmentation"):** `drop_path` là
regularization *weight-space* (stochastic depth), `patch_mask` là *input-space* — khác họ
với photometric aug. Điểm chung khiến chúng bị hạ tone là: **cả hai đều chống-overfit, mà
model đang *under-fit***. Trong regime under-fit, thêm bất kỳ reg nào cũng bị phạt → "=0 tốt
nhất" là **hành vi kỳ vọng của under-fitting**, chưa phản ánh giá trị thật khi model được
train tới ngưỡng overfit (data 28k *có* nguy cơ overfit nếu train đủ). → không kết luận
"reg vô dụng cho LeJEPA"; chỉ nói "trong regime này, reg chưa cần".

## Câu hỏi nghiên cứu → Trả lời (từng ablation)

Nhóm benchmark 8 ablation, chia 3 chủ đề. Mỗi ablation quét 1 trục và cố định phần
còn lại ở baseline (anchor 59.46%). Câu hỏi + kỳ vọng lấy từ `scripts/ablations/specs.py`.

### A. Siêu tham số của mục tiêu học (SIGReg & multi-view)

**A1 · Epps-Pulley grid** — `epps` (27 cấu hình: slices{512,1024,4096} × $t_{\max}${1,3,5} × n_points{5,17,41})
- ❓ **Câu hỏi:** SIGReg nhạy thế nào với lưới tích phân Epps-Pulley (số lát cắt, miền, số điểm cầu phương)?
- 🔮 **Kỳ vọng:** lưới vừa phải là đủ; lưới quá nhỏ có thể under-regularize.
- 📊 **Kết quả:** `num_slices` là yếu tố mạnh nhất (512→4096 ≈ **+10pt**); `n_points` gần như **phẳng**; `t_max` nhỏ ([−1,1]) lại **tốt hơn** [−3,3]/[−5,5]. Cao nhất 70.07 (5/4096/1).
- ✅ **Trả lời:** SIGReg **nhạy với số lát cắt và miền tích phân**, **không nhạy với số điểm cầu phương**. Càng nhiều lát cắt càng tốt; miền hẹp thắng ở regime này (xem caveat under-reg).

**A2 · Số lượng view** — `views` (11 cấu hình: n_views{4,6,8,10} × n_global{1,2,4})
- ❓ **Câu hỏi:** Cần bao nhiêu view tổng và view global cho LeJEPA?
- 🔮 **Kỳ vọng:** nhiều view giúp ích đến giới hạn bộ nhớ; số global view kiểm tra ước lượng tâm (center).
- 📊 **Kết quả:** **ít view thắng** — V=4 (72.8) > V=6 > V=8 > V=10; global view 1–2 > 4.
- ❌ **Trả lời (ngược kỳ vọng):** ở imagenet10 low-data, **4 view là đủ và tốt nhất**; thêm view làm giảm chất lượng. Cần grid sạch (cố định num_slices/autostop) để loại confound.

### B. Thành phần kiến trúc (nơi & cách áp mục tiêu)

**B1 · Vị trí áp SIGReg** — `sigreg_target` (3: proj / embed / both)
- ❓ **Câu hỏi:** Nên regularize output của projector, embedding của backbone, hay cả hai?
- 🔮 **Kỳ vọng:** áp trên không gian projector (proj) là mạnh nhất.
- 📊 **Kết quả:** proj **59.5** ≫ embed **23.7** / both **24.9** (2 cái sau **collapse**, loss 2.1–2.9).
- ✅ **Trả lời (khớp mạnh):** **bắt buộc** áp SIGReg trên projection; ép embedding về N(0,I) trực tiếp phá backbone → collapse.

**B2 · Kiến trúc projector** — `projector_depth` (4: Linear / MLP2 / MLP / MLP4)
- ❓ **Câu hỏi:** Cần mấy lớp MLP trong projector, head tuyến tính có đủ không?
- 🔮 **Kỳ vọng:** projector phi tuyến vượt head tuyến tính.
- 📊 **Kết quả:** Linear **collapse** (23.4); MLP4 (61.3) > MLP (59.5) > MLP2 (57.1).
- ✅ **Trả lời (khớp):** head tuyến tính **không đủ** (collapse) — SIGReg cần projector phi tuyến đủ capacity để reshape phân phối; sâu hơn tốt hơn chút.

**B3 · Predictor head** — `predictor` (3: none / linear / mlp)
- ❓ **Câu hỏi:** Thêm predictor kiểu BYOL/I-JEPA có giúp invariance không?
- 🔮 **Kỳ vọng:** baseline không predictor vẫn cạnh tranh.
- 📊 **Kết quả:** none **59.5** ≫ mlp **48.3** > linear **43.9**.
- ✅ **Trả lời (khớp):** **không cần predictor** — thêm vào còn **hại**. Củng cố tính tối giản của LeJEPA (khác I-JEPA/BYOL).

**B4 · Tổng hợp feature** — `aggregation` (3: cls / mean / cls_mean; **thiếu cls2**)
- ❓ **Câu hỏi:** Output ViT nào nên đưa vào projector?
- 🔮 **Kỳ vọng:** cls_mean hoặc cls2 cho tín hiệu giàu hơn cls đơn.
- 📊 **Kết quả:** cls **59.5** ≈ cls_mean **59.3** > mean **55.8**.
- ❌ **Trả lời (ngược kỳ vọng):** **CLS đơn đã đủ**; ghép mean không giúp; mean-pool đơn thuần kém hơn. (`cls2` = concat CLS 2 lớp cuối chưa chạy — nên chạy vì đó là setup gần recipe eval nhất.)

### C. Regularization chống-overfit (đọc kèm mục "Tính hợp lệ" — regime under-fit)

**C1 · Tỉ lệ patch masking** — `patch_masking` (6: 0.0–0.7)
- ❓ **Câu hỏi:** Tỉ lệ mask nào tối ưu cho invariance + SIGReg?
- 🔮 **Kỳ vọng:** mask vừa phải ~0.2–0.4 là tốt nhất.
- 📊 **Kết quả:** **0.0 tốt nhất** (61.1); tăng mask → giảm nhẹ, gần phẳng.
- 🔴 **Trả lời (thận trọng):** trong **regime under-fit** này, không mask tốt nhất — chưa
  kết luận mask vô dụng cho LeJEPA; ở pipeline train đủ (overfit) có thể đảo.

**C2 · Stochastic depth (drop-path)** — `drop_path` (5: 0.0–0.4)
- ❓ **Câu hỏi:** LeJEPA nhạy thế nào với stochastic depth trong ViT?
- 🔮 **Kỳ vọng:** drop-path vừa (0.1–0.2) tốt nhất cho ViT.
- 📊 **Kết quả:** **0.0 tốt nhất** (61.7); tăng drop-path → giảm dần.
- 🔴 **Trả lời (thận trọng):** drop-path chỉ giúp khi model *overfit*; ở đây model
  **under-fit** nên thêm drop-path bị phạt — hành vi kỳ vọng, chưa phản ánh giá trị thật.

> **Nhìn xuyên suốt:** nhóm B (thành phần cốt lõi) **khớp lý thuyết LeJEPA** — SIGReg-trên-projection và bỏ-predictor là đúng, các thành phần này *collapse thật* nếu đặt sai (structural, tin cậy cao). Nhóm A2 + C (view/mask/drop-path) đảo ngược kỳ vọng **nhưng ở regime under-fit** (thiếu photometric aug + batch lớn) → mọi reg chống-overfit đều bị phạt; hạ tone, không kết luận tuyệt đối.

## Xu hướng từng ablation (sort top1 desc)

| ablation | best → worst | best top1 | Δ vs anchor | ghi chú |
|----------|--------------|-----------|-------------|---------|
| **views** | nv4 > nv6 > nv8 > nv10; g1–2 > g4 | **0.7277** (nv4,g1) | **+13.3** | ít view thắng ⚠️ |
| **epps** | slices↑, t_max↓ | **0.7007** (5,4096,t1) | **+10.6** | t_max ngược paper ⚠️ |
| projector_depth | MLP4 > MLP > MLP2 ≫ Linear | 0.6126 (MLP4) | +1.8 | Linear collapse (0.234) |
| drop_path | 0.0 > 0.05 > 0.2 > 0.1 > 0.4 | 0.6165 (dp0) | +2.2 | drop_path không giúp |
| patch_masking | 0.0 > 0.2 > 0.1 > 0.3 ≈ 0.5 ≈ 0.7 | 0.6108 (mask0) | +1.6 | masking không giúp |
| aggregation | cls ≈ cls_mean > mean | 0.5946 (cls) | 0.0 | CLS đủ |
| predictor | none ≫ mlp > linear | 0.5946 (none) | 0.0 | predictor **hại** |
| sigreg_target | proj ≫ both > embed | 0.5946 (proj) | 0.0 | embed/both collapse |

## Phát hiện chính

1. **Hai đòn bẩy thật:** `num_slices` cao (4096 ≫ 1024 ≫ 512, rõ rệt trong epps) và
   ít view / t_max thấp. Đây là các thay đổi đẩy top1 lên 0.70–0.73.

2. **Reg chống-overfit chưa cần trong regime under-fit:** drop_path, patch_mask, nhiều
   view — đều ≤ hoặc hại so với anchor. Nhưng pipeline đang **under-fit** (thiếu photometric
   aug + batch lớn), nên đây là hành vi kỳ vọng, **không** phải "reg vô dụng cho LeJEPA"
   (xem mục *Tính hợp lệ*). Hạ tone kết luận này.

3. **3 collapse thật (không phải lỗi run):** đều đi kèm loss bất thường cao →
   - `sigreg_target=embed` (0.237, loss 2.08) / `both` (0.249, loss 2.86)
   - `projector_arch=Linear` (0.234, loss 3.42)
   - `predictor=linear/mlp` (0.44/0.48, loss ~0.8) — predictor kéo tụt probe.
   → khẳng định mặc định `proj` / `MLP` / `predictor=none` là đúng.

## So với paper (chỉ xu hướng)

| tham số | paper | đo được | khớp? |
|---------|-------|---------|-------|
| epps num_slices | more = marginal↑ | more = **mạnh**↑ | ✅ (mạnh hơn) |
| epps n_points | negligible | gần phẳng | ✅ |
| epps t_max | [−3,3]+ > [−1,1] | **[−1,1] > [−3,3]** | ❌ ngược |
| views | (b) noisy, ~V=6/g2 tốt | ít view (V=4) tốt hơn | ~ (paper noisy) |

## ⚠️ Caveat cần kiểm chứng trước khi kết luận
Hai kết quả top (t_max=1, ít-view) **đi kèm final_loss thấp + best_ep sớm** (t_max1:
loss 0.32, ep39; nv4/g1: loss 0.42, ep40). Nghi vấn: **under-regularize + early best
epoch** làm probe cao "may mắn" chứ chưa chắc feature tốt bền. Cần:
- Đối chiếu kNN (không probe) cho các config này.
- Kiểm tra đường loss (`metrics.csv`) xem có dấu hiệu bắt đầu collapse muộn không.
- Chạy lại eval-frozen-paperspec đủ 100 ep trên vài config top nếu muốn số chắc.

## Độ lệch so với plan ban đầu (`scripts/ablation_plan.md`)
Plan gốc dự định chạy trên **inet100 · ViT-L/14 · 50ep · KNN eval**. Thực tế chạy
(notebook `lejepa-ablation-full`) trên **imagenet10 · ViT-S/16 · 100ep · linear probe
paper-spec**. → khác dataset/backbone/eval, nên các "Expected outcome" của plan (vốn
ngầm giả định regime ViT-L/inet100) cần đọc lại dưới ánh sáng regime nhỏ/low-data.

Trong 10 ablation của plan: **8 cái đã chạy**; **#2 projector_dims** và **#3 reg_tokens**
KHÔNG chạy (`needs_model_support`). #8 aggregation chạy **3/4** biến thể — thiếu `cls2`
(concat CLS 2 layer cuối) dù đó là setup gần recipe eval nhất.

## Đối chiếu Expected (plan) vs Measured (đo được)

| # | Ablation | Expected (plan gốc) | Measured | Khớp? |
|---|----------|---------------------|----------|-------|
| 5 | Projector depth | Linear kém; **3-layer (MLP) optimal** | Linear **collapse** (23.4); nhưng MLP4 (61.3) > MLP (59.5) > MLP2 | ⚠️ một nửa: Linear kém ✅, "3-layer optimal" ❌ (4-layer tốt hơn) |
| 6 | Patch masking | **sweet spot 0.2–0.4**; ratio cao mất context | **0.0 tốt nhất** (61.1), gần phẳng, masking không giúp | ❌ ngược (no-mask thắng) |
| 7 | Drop path | **moderate 0.1–0.2 optimal** | **0.0 tốt nhất** (61.7), tăng dp → giảm | ❌ ngược (no-drop thắng) |
| 8 | Aggregation | `cls_mean`/`cls2` **tốt hơn** `cls` | `cls` (59.5) ≈ `cls_mean` (59.3) > `mean`; `cls2` chưa chạy | ❌ cls đủ (xác nhận thiết kế) |
| 9 | SIGReg target | `proj` tốt nhất; `embed` conflict | `proj` (59.5) ≫ `embed`/`both` **collapse** (23.7/24.9) | ✅ khớp mạnh |
| 10 | Predictor | `none` không thua kém (validate simplicity) | `none` (59.5) ≫ `mlp` (48.3) > `linear` (43.9) | ✅ khớp (predictor **hại**) |
| 1 | Epps params | moderate grid đủ; grid nhỏ under-reg | slices↑ **mạnh**↑; n_points phẳng; **t_max nhỏ tốt hơn** | ~ (slices/n_points khớp; t_max ngược) |
| 4 | Views | more views help đến giới hạn mem | **ít view (V=4) tốt hơn** | ❌ ngược |

**Đọc tổng:** các ablation *component cốt lõi* (#9 SIGReg target, #10 predictor, và
Linear-collapse ở #5) **khớp đúng dự kiến** — củng cố thiết kế LeJEPA (SIGReg trên
projection, bỏ predictor); đây là các kết luận **structural, tin cậy cao**. Ngược lại,
các ablation *reg chống-overfit* (#6 mask, #7 drop-path, #4 views) **đảo ngược dự kiến**,
nhưng vì pipeline chạy ở **regime under-fit** (thiếu photometric aug + batch lớn) nên đây
là hành vi kỳ vọng của under-fitting — **hạ tone**, không kết luận tuyệt đối (xem mục
*Tính hợp lệ*).

## Đề xuất bước tiếp
- Thử vùng chưa quét: `num_slices` > 4096, `t_max ∈ {0.5, 1, 2}` × slices cao.
- Kết hợp 2 đòn bẩy: nv4/g1 + slices4096 + t_max1 (chưa có config nào giao cả hai).
- Views cần grid sạch (cố định num_slices, autostop=False) để tách confound.
