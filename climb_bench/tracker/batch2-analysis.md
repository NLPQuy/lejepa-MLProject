# Báo cáo Batch-2 — Optimizer & Architecture

**Nguồn**: CSVLogger online metrics (`climb_bench/viz/metric_results/batch_2/`) + kết quả eval frozen theo chuẩn paper (`climb_bench/viz/eval_results/batch_2/*.json`). Viz: `climb_bench/viz/figures/batch_2/`.
**Setup**: LeJEPA pretrain in-domain trên imagenet10 (bản local ~28k train — **≈2.2× inet10 của paper**), backbone ViT-S/16, schedule cosine 100 epoch. Eval bằng frozen backbone + linear probe.
**Ngày**: 2026-06-12.

> ⚠️ **Cảnh báo so sánh**: tập local ~28k train (28407) lớn hơn inet10 paper (~13k), nên **con số tuyệt đối KHÔNG so trực tiếp với Table 5 của paper** — chỉ dùng **Δ giữa các idea** trong cùng batch.

---

## 1. Các idea ban đầu chạy những gì?

Batch-2 tập trung vào **optimizer / hình học training + kiến trúc** (không đụng loss-term — đó là batch-1). Đã implement 10 idea + baseline (baseline giống hệt batch-1):

| exp | Idea | Bản chất can thiệp |
|---|---|---|
| exp1 | **SAM** | Sharpness-Aware Minimization — tìm minima phẳng, 2 bước forward/backward mỗi step |
| exp2 | **QK-Norm** | LayerNorm cho query/key trước attention (timm `qk_norm=True`) — ổn định attention |
| exp3 | **Muon** | Optimizer Muon (orthogonalize gradient bằng Newton-Schulz) cho các lớp trọng số 2D |
| exp4 | **Schedule-Free** | AdamW Schedule-Free (Polyak averaging, bỏ LR schedule) |
| exp5 | **PCGrad** | Gradient surgery — chiếu bỏ thành phần xung đột giữa gradient SIGReg và invariance |
| exp6 | **conv-stem** | Thay patch-embed (1 conv stride-16) bằng stem 4 lớp conv (BN+GELU) — *đổi kiến trúc* |
| exp7 | **SWA** | Stochastic Weight Averaging, cổng theo RankMe |
| exp8 | **LLRD** | Layer-wise learning-rate decay |
| exp9 | **prog. stoch-depth** | Tăng dần drop-path rate theo tiến trình train |
| exp10 | **deep-sup** | Deep supervision — áp SIGReg+invariance lên các lớp trung gian |

Tất cả train xong 100 epoch trên Kaggle. **Eval frozen theo paper mới chạy cho 4 cái** (baseline, conv-stem, QK-Norm, PCGrad — nhóm ưu tiên); 7 idea còn lại mới có online metric, chưa eval paper-spec.

---

## 2. Online metrics — kết quả xếp hạng nhanh

Online linear-probe (single CLS, lr 0.03 — recipe RẺ dùng để rank, **không** phải recipe paper). Baseline online lp = 0.8638.

| Idea | online lp tốt nhất | Δ vs baseline | kNN | Ghi chú |
|---|---|---|---|---|
| **conv-stem** | **0.904** | **+0.040** | 0.897 | vượt trội rõ |
| QK-Norm | 0.873 | +0.010 | 0.850 | nhỉnh nhẹ |
| SAM | 0.870 | +0.007 | 0.844 | vùng nhiễu |
| PCGrad | 0.869 | +0.006 | 0.853 | vùng nhiễu |
| SWA | 0.868 | +0.005 | 0.847 | vùng nhiễu |
| prog. stoch-depth | 0.868 | +0.004 | 0.844 | vùng nhiễu |
| Schedule-Free | 0.864 | +0.001 | 0.847 | ≈ baseline |
| deep-sup | 0.863 | −0.001 | 0.836 | ≈ baseline |
| LLRD | 0.836 | −0.028 | 0.795 | kém, sụp cuối train |
| Muon | 0.814 | −0.050 | 0.805 | kém, đỉnh sớm rồi tụt |

**Kết luận online**: chỉ conv-stem tách hẳn khỏi đường baseline; nhóm giữa (+0.004..+0.010) nằm trong nhiễu; LLRD/Muon thua rõ.

---

## 3. Eval frozen backbone + linear probe theo paper

Recipe paper: **concat CLS 2 lớp cuối + LayerNorm**, classifier tuyến tính, AdamW lr 1e-3 wd 1e-6, cosine, 100 epoch probe; backbone **đóng băng**. Full set (n_train=28407, n_val=11775). Baseline = 0.8949. **Đã eval đủ 10 idea.**

| Idea | top1 | top5 | **Δtop1 vs baseline** | best probe ep | online Δ |
|---|---|---|---|---|---|
| **conv-stem** | **0.9208** | 0.9918 | **+0.0259** | 24 | +0.040 |
| SAM | 0.8972 | 0.9899 | +0.0023 | 27 | +0.007 |
| prog. stoch-depth | 0.8950 | 0.9896 | +0.0001 | 15 | +0.004 |
| **baseline** | 0.8949 | 0.9908 | — | 31 | — |
| PCGrad | 0.8944 | 0.9901 | −0.0005 | 20 | +0.006 |
| SWA | 0.8911 | 0.9903 | −0.0038 | 18 | +0.005 |
| QK-Norm | 0.8909 | 0.9897 | −0.0040 | 16 | +0.010 |
| deep-sup | 0.8894 | 0.9907 | −0.0055 | 19 | −0.001 |
| Schedule-Free | 0.8872 | 0.9885 | −0.0077 | 18 | +0.001 |
| LLRD | 0.8616 | 0.9893 | −0.0333 | 28 | −0.028 |
| Muon | 0.8574 | 0.9873 | −0.0375 | 27 | −0.050 |

### 🔑 Phát hiện chính: KHÔNG idea optimizer nào vượt baseline; online ranking KHÔNG sống sót qua recipe paper
- **Chỉ conv-stem (kiến trúc) thắng thật** (+2.6pp). Trong 9 idea optimizer/training-geometry: **SAM +0.0023 và prog-stoch-depth +0.0001 = trong nhiễu (≈ baseline)**; 7 cái còn lại **đều dưới baseline**.
- **Cả cụm online dương nhẹ +0.004..+0.010 đều sụp**: QK-Norm (+0.010→−0.004), SWA (+0.005→−0.004), PCGrad (+0.006→−0.001), SAM (+0.007→+0.002). Online thổi phồng vì recipe khác (dịch ~2.5pp > delta của chúng).
- **LLRD/Muon** thua rõ trên cả hai (−0.033/−0.038 paper) — nhất quán với online.
- → Bằng chứng đầy đủ (10/10 idea): **online chỉ để LOẠI cái dở; chỉ biên ≥~0.02 mới trụ được qua recipe paper.** conv-stem (+0.04 online) sống, mọi thứ <0.01 chết.

### Kiểm tra chéo baseline
baseline eval nhiều lần (full ckpt 0.8949; backbone .pt batch-1 0.8954) → lệch 0.0005, nhất quán. Recipe ổn định, nên các delta nhỏ ở trên là thật chứ không phải lỗi đo.

---

## 4. Ghi chú về conv-stem

conv-stem là cái **duy nhất** thắng thật theo paper-spec (+2.5pp), **nhưng đây không phải cải tiến *LeJEPA*** mà là cải tiến *kiến trúc backbone*:

1. **Không động đến đóng góp của LeJEPA** (loss SIGReg + invariance giữ nguyên). Nó chỉ thay `patch_embed` → trick "early convolutions help ViTs" (Xiao 2021), vốn giúp **mọi** phương pháp SSL/supervised.
2. **Phá protocol benchmark**: bài toán ghim cứng *frozen `vit_small_patch16_224`*. conv-stem làm backbone không còn là vit_small chuẩn → +2.5pp **lẫn lộn** giữa "objective tốt hơn" và "encoder mạnh hơn / nhiều param hơn / inductive bias tốt hơn". Eval đã rebuild đúng kiến trúc (cờ `--conv_stem`, ConvStem 4 lớp conv) nên số là thật, nhưng **không quy công cho LeJEPA được**.
3. **Confound chưa kiểm soát**: cần re-baseline cùng kiến trúc (conv-stem + phương pháp khác) để biết LeJEPA có hưởng lợi *nhiều hơn* không. Nếu mọi method lợi như nhau → free lunch kiến trúc.

**Khuyến nghị**: báo cáo conv-stem như một **track riêng "architecture co-design"** kèm số param/FLOPs, KHÔNG xếp cùng cột "ý tưởng cải tiến LeJEPA". Đối chiếu: trong chính batch-2 ta đã loại depth/width reallocation vì "phá frozen vit_small identity" — conv-stem vi phạm cùng nguyên tắc.

---

## TL;DR & hướng tiếp

- **Theo đúng luật chơi (frozen vit_small)**: **KHÔNG idea optimizer/training-geometry nào vượt baseline** theo recipe paper (đã eval đủ 10/10). SAM/prog-stoch-depth chỉ chạm baseline (trong nhiễu); 7 cái còn lại dưới baseline. → batch-2 (optimizer-only) **không có winner trong phạm vi**. Kết luận đã chốt, không còn nợ eval.
- **conv-stem**: thắng +2.6pp nhưng ngoài phạm vi (đổi kiến trúc) — tách track, cần re-baseline (conv-stem + method khác) + report params/FLOPs.
- **Lever lớn nhất vẫn là anti-overfit lúc pretrain** (kết luận từ batch-1), không phải đổi optimizer. Đây là **kết quả âm có giá trị**: với LeJEPA trên data này, chỉnh optimizer/training-geometry là ngõ cụt → dồn sức vào loss/regularization/data và kiến trúc.

Liên quan: [batch1-analysis.md](batch1-analysis.md).
