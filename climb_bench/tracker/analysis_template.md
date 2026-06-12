# Phần A — Giải thích các metrics (kNN, linear probe, RankMe, train loss)

## 1. Ý nghĩa từng metric

| Metric | Cách tính | Đo cái gì | Cần label? | Cần train? |
|---|---|---|---|---|
| **kNN top1** | Đóng băng backbone, trích feature cho train+val, phân loại mỗi mẫu val bằng vote của k feature train gần nhất (cosine) | Feature có **gom cụm theo ngữ nghĩa** tốt không (cấu trúc cục bộ của không gian feature) | Có (label train để vote) | **Không** (không có tham số học) |
| **Linear probe top1** | Đóng băng backbone, train 1 classifier **tuyến tính** trên feature | Feature có **tách tuyến tính** được không — proxy chuẩn cho chất lượng biểu diễn | Có | Có (chỉ lớp linear) |
| **RankMe** | Effective rank (soft rank = entropy Shannon của các singular value đã chuẩn hóa) của ma trận feature | **Mức dàn trải chiều** của feature → phát hiện *dimensional collapse* | **Không** | Không |
| **train loss** (`fit/loss_epoch`) | Chính hàm LeJEPA: `λ·SIGReg + (1−λ)·Invariance` | Tiến trình tối ưu hóa | Không | — |

Lưu ý bản chất:
- **kNN & linear probe** = đo **chất lượng downstream** (cùng đo separability, kNN theo cụm cục bộ, linear theo siêu phẳng toàn cục).
- **RankMe** = **predictor không nhãn** cho chất lượng downstream, KHÔNG phải là accuracy. RankMe cao ↔ ít collapse ↔ *thường* downstream tốt hơn. Dùng để **chọn checkpoint / phát hiện collapse**, không phải để báo cáo như "kết quả".
- **train loss** = **chẩn đoán**, KHÔNG phải metric chất lượng. Loss thấp ≠ feature tốt (có thể collapse mà invariance loss vẫn thấp). Chỉ dùng để biết training có chạy/diverge không.

## 2. Tại sao đo các metrics này TRƯỚC khi eval giống paper?

- **Rẻ + online**: chúng được tính ngay trong/sau pretrain, **không** cần bước eval paper-spec đắt đỏ (trích lại feature concat-CLS-2-lớp-cuối + LN, rồi train probe 100 epoch). → dùng để **triage**: lọc nhanh idea nào đáng bỏ GPU eval đầy đủ.
- **Không cần train (kNN/RankMe)** hoặc không cần nhãn (RankMe) → cực rẻ, hợp cho **early-stopping / chọn checkpoint best / bắt collapse sớm**.
- **Loại idea dở sớm** mà không tốn compute (vd batch-2: LLRD/Muon bị online loại ngay).

## 3. Dùng các metrics này đánh giá có VALID không? Paper nào dùng?

| Metric | Valid để báo cáo? | Paper tham chiếu |
|---|---|---|
| **kNN** | ✅ Có — metric SSL chính thống, đứng độc lập | DINO (Caron et al. 2021); phổ biến trong SSL |
| **Linear probe** | ✅ Có — **THE** metric chuẩn của SSL | SimCLR, BYOL, MAE, DINO... |
| **RankMe** | ⚠️ Chỉ valid cho **model selection / proxy không nhãn**, KHÔNG báo cáo như accuracy | RankMe (Garrido et al. 2023) |
| **train loss** | ❌ Không — chỉ chẩn đoán | — |

**Cảnh báo cực quan trọng (đã kiểm chứng ở batch-2):**
> Recipe linear probe **phải khớp** mới so được. Online probe ở đây (single CLS, lr 0.03, **không** LN) ≠ recipe paper (concat CLS 2 lớp cuối + LN, AdamW lr 1e-3 wd 1e-6, 100 ep). Khác recipe gây dịch ~2.5pp — **lớn hơn delta của hầu hết idea**. Bằng chứng batch-2: QK-Norm/PCGrad +0.006..+0.010 trên online nhưng về ≈/dưới baseline trên paper-spec.
>
> ➡️ **Online metrics chỉ để XẾP HẠNG/LOẠI, không để KẾT LUẬN.** Metric-of-record là **linear probe đúng recipe paper**. Chỉ delta đủ lớn (vd conv-stem +0.04 online → +0.025 paper) mới sống sót.

---

# Phần B — Template báo cáo chung cho các batch

> Copy phần dưới vào `climb_bench/tracker/batch<N>-analysis.md` rồi điền. Tham chiếu mẫu đã điền: [batch1-analysis.md](batch1-analysis.md), [batch2-analysis.md](batch2-analysis.md).

```markdown
# Báo cáo Batch-<N> — <chủ đề batch, vd "Optimizer & Architecture">

**Nguồn**: online metrics (`climb_bench/viz/metric_results/batch_<N>/`) + eval paper-spec (`climb_bench/viz/eval_results/batch_<N>/*.json`). Viz: `climb_bench/viz/figures/batch_<N>/`.
**Setup**: LeJEPA pretrain in-domain trên imagenet10 (local ~28k train — ≈2.2× inet10 paper), ViT-S/16, cosine <số> epoch. Eval: frozen backbone + linear probe.
**Ngày**: <YYYY-MM-DD>.

> ⚠️ Tập local ~28k > inet10 paper (~13k) → con số tuyệt đối KHÔNG so Table 5 paper; chỉ dùng Δ giữa các idea cùng batch.

## 1. Các idea ban đầu chạy những gì?
<1 câu phạm vi batch (loss / optimizer / augmentation / architecture...).>

| exp | Idea | Bản chất can thiệp |
|---|---|---|
| exp1 | <tên> | <mô tả 1 dòng> |
| ... | ... | ... |

Đã eval paper-spec: <liệt kê>. Chưa eval: <liệt kê> (lý do: <gating / online loại>).

## 2. Online metrics — xếp hạng nhanh (TRIAGE, không kết luận)
Online linear-probe (single CLS, lr 0.03 — KHÔNG phải recipe paper). Baseline online lp = <x>.

| Idea | online lp | Δ vs base | kNN | RankMe | Ghi chú |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

**Kết luận online**: <cái nào tách khỏi baseline / cái nào trong nhiễu / cái nào loại>.

## 3. Eval frozen backbone + linear probe theo paper (METRIC-OF-RECORD)
Recipe: concat CLS 2 lớp cuối + LN, AdamW lr 1e-3 wd 1e-6, cosine, 100 ep probe; backbone đóng băng. Full set (n_train, n_val). Baseline = <x>.

| Idea | top1 | top5 | **Δtop1 vs base** | best probe ep |
|---|---|---|---|---|
| baseline | ... | ... | — | ... |
| ... | ... | ... | ... | ... |

### 🔑 Phát hiện chính
- <Online ranking có sống sót qua recipe paper không? Idea nào đảo dấu / triệt tiêu / giữ được biên?>
- Kiểm tra chéo baseline (nếu eval >1 lần): <độ lệch — xác nhận recipe ổn định>.

## 4. Ghi chú đặc biệt / caveats
- <Idea nào đổi kiến trúc / phá protocol frozen vit_small → tách track, cần re-baseline + report params?>
- <Idea nào không ổn định cuối train (best ≠ last)? Idea nào cần checkpoint đặc biệt, vd SWA dùng swa_avg.ckpt?>
- <Confound chưa kiểm soát?>

## TL;DR & hướng tiếp
- **Trong phạm vi luật chơi (frozen vit_small)**: <có winner không?>.
- **Ngoài phạm vi**: <conv-stem-like nếu có>.
- **Còn nợ**: <eval/multi-seed gì>.
- **Lever lớn nhất**: <kết luận chiến lược, nối với batch trước>.

Liên quan: [batch<N-1>-analysis.md](batch<N-1>-analysis.md).
```
