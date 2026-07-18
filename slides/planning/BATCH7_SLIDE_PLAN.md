# Plan: thêm kết quả Batch-7 vào slides_main.tex (Nghiên cứu mở rộng)

**Ngày**: 2026-07-18 · **Nguồn số liệu**: `climb_bench/viz/eval_results/batch_7/*.json`
**Đích**: `slides/slides_main.tex` §"Nghiên cứu mở rộng: Benchmark Climb trên Imagenette"
**Figure mới**: `slides/figures/fig_climb_batch7_bars.{tex,pdf}`

---

## 0. Số liệu chốt (best checkpoint / idea = max top1 qua ep60/80/100)

Baseline neo = **89.5%** (dùng đúng giá trị của leaderboard Hướng 2 — cùng ckpt batch_1/2,
`eval_results/batch_2/baseline_100.json` = 0.8949). KHÔNG dùng 89.54 (đó là neo của Hướng 1).

| Idea (tag) | best top1 | epoch chọn | Δpp | nhóm cơ chế |
|---|---|---|---|---|
| ETF (`etf`) | 89.02 | ep100 | −0.47 | prototype head cố định (không đụng objective) |
| RL-crop hard (`rlhard`) | 87.20 | ep100 | −2.29 | augmentation policy |
| FM-invariance (`fminv`) | 58.42 | ep100 | −31.07 | thay invariance term |
| FM-SIGReg A (`fmsigreg_a`) | 25.43 | ep60 | −64.06 | thay SIGReg — form A (control) |
| FM-SIGReg B (`fmsigreg`) | 18.68 | ep100 | −70.81 | thay SIGReg — form B (đã sửa) |
| KL-score (`klscore`) | 17.68 | ep80 | −71.81 | score-matching thay SIGReg |

Mốc random 10 lớp = top1 10% → 3 dòng cuối = collapse thật (đã xác nhận loader khớp 100%,
không phải artifact eval).

**Payload trí tuệ của batch-7 (câu để nhấn):** klscore + fm_b **đã CONVERGE ở Phase-0 free-z
gate** (`tracker/batch7-analysis.md`) nhưng full-training lại collapse → *free-z hội tụ KHÔNG
kéo theo full-pipeline*. Hai idea sống sót (ETF, RL-crop) đều **không thay lõi SIGReg/invariance**.
Củng cố insight Hướng 1+2: objective EppsPulley là điểm cân bằng mong manh; thay lõi = vỡ.

**Cấu trúc treatment vs control (khung chính của slide Hướng 3):** batch-7 = 4 idea **thay lõi
objective** (nhân vật chính) + 2 idea **không đụng objective** (đối chứng). Không phải cả 6 đều
"thay lõi" — ETF là *head/loss cụm bổ sung* (Simplex-ETF cố định + Sinkhorn, SIGReg giữ nguyên),
RL-crop là *augmentation policy online* (REINFORCE chọn crop, đụng input không đụng objective).
Đối chứng nằm cùng slide để **cô lập nguyên nhân**: đụng objective ⇒ collapse; để objective
nguyên ⇒ giữ baseline (nhưng cũng không vượt). Đây là lý do gom 1 slide KHÔNG kì.

| nhóm | idea | Δpp |
|---|---|---|
| đối chứng (không đụng objective) | ETF head · RL-crop | −0.5 · −2.3 |
| thay invariance | FM-invariance | −31 |
| thay SIGReg | FM-SIGReg (form B) · KL-score | −71 · −72 |

---

## 1. Deliverable A — Figure standalone `fig_climb_batch7_bars`

Bám y hệt `figures/fig_climb_objective_bars.tex` (pgfplots `ybar`, không fontspec →
compile bằng `pdflatex`/`lualatex` standalone). Khác biệt duy nhất: 7 cột + annotation collapse.

- Cùng preamble màu (mprimary/maccent/mgood/mbad/mgray HTML như file mẫu).
- **Gộp A/B → 1 cột FM-SIGReg (dùng form B = 18.68, bỏ A khỏi chart).** 6 cột.
- `symbolic x coords` = Baseline, ETF, RL-crop, FM-inv, {FM-SIGReg}, KL-score.
- Màu tô theo **2 nhóm** (không phải gradient sức khỏe): đối chứng = xanh, thay-objective = đỏ.
  - Baseline 89.49 → `fill=mprimary`
  - ETF 89.02, RL-crop 87.20 → `fill=mgood` (nhóm đối chứng — không đụng objective)
  - FM-inv 58.42, FM-SIGReg 18.68, KL-score 17.68 → `fill=mbad` (nhóm thay objective)
- `\draw[mprimary, thick, dashed]` baseline 89.49 line ngang; label "baseline 89.5\%".
- `\draw[mbad, dashed]` mốc 10 (random) mảnh + node "≈ random 10\%".
- Node `collapse` (mbad, scriptsize\bfseries) đặt trên cụm FM-SIGReg/KL-score.
- Ymax=100, ylabel "Frozen linear top1 (\%)".
- (Tùy chọn) 2 group label dưới trục: "đối chứng" dưới ETF/RL-crop, "thay objective" dưới 3 cột đỏ.

Compile: `cd slides/figures && pdflatex fig_climb_batch7_bars.tex` → sinh `.pdf`.
(Ghi chú: `viz/eval_results/batch_7/paperspec_batch_7.png` là bản Python của viz_paperspec.py —
**KHÔNG** dùng cho deck; deck theo convention standalone-PDF.)

---

## 2. Deliverable B — Thẻ "Giả thuyết 3" ở frame "Câu hỏi nghiên cứu"

Vị trí: frame `Câu hỏi nghiên cứu: headroom còn nằm ở đâu?` (slides_main.tex ~L2259–2297).
Hiện có 2 thẻ `\begin{columns}[T]` mỗi cột `0.47\textwidth`. → đổi thành **3 cột `0.31\textwidth`**,
thêm thẻ thứ 3 tông gold (maccent / `mlightgold`).

Nội dung thẻ 3 (cô đọng, đối xứng với thẻ 1–2 — đây là *giả thuyết chính* của batch-7,
tức nhánh treatment; ETF/RL-crop là đối chứng nên KHÔNG nêu ở thẻ giả thuyết):
```
{\footnotesize\color{mgray}Giả thuyết 3}\hfill{\footnotesize\color{mgray}baseline $\approx$ 89.5\%}
{\bfseries\color{maccent!70!black}Thay lõi objective}
{\footnotesize Đổi hẳn SIGReg/invariance sang mục tiêu sinh có cơ sở lý thuyết
(score-matching, flow-matching) $\Rightarrow$ vượt EppsPulley?}
```
Màu khung: `linecolor=maccent!60, backgroundcolor=mlightgold`.
Lưu ý: text 3 cột hẹp hơn — giữ đúng độ dài ngắn như trên là vừa; không thêm dòng.

---

## 3. Deliverable C — Frame "Hướng 3" (chèn sau Hướng 2)

Vị trí chèn: **sau** frame `Hướng 2: Optimizer và training geometry` (kết ở ~L2419),
**trước** `Conv-stem: architecture co-design riêng` (~L2422). Đánh dấu comment
`% ─── CLIMB 4.5: Direction 3 — objective replacement ───`.

Layout = mirror Hướng 1 (figure trái 0.56 + bảng phải 0.42 + `\takeaway`):

Title: `\begin{frame}{Hướng 3: Thay lõi objective bằng mục tiêu sinh (score / flow-matching)}`.
(KHÔNG để "ETF" trong title — ETF/RL-crop là đối chứng, không phải objective-swap.)

- **Cột trái (0.56):** `\includegraphics[width=\linewidth]{fig_climb_batch7_bars.pdf}`
  + caption scriptsize "Frozen linear top1 (best ckpt/idea); nét đứt = baseline 89.5\%."
- **Cột phải (0.42):** bảng scriptsize có cột **Nhóm**, tô `rowcolor` 2 nhóm như leaderboard
  Hướng 2 (`mgood!..` cho đối chứng, `mbad!..` cho thay-objective) — mã hoá bằng màu để thấy
  ngay 2 nhánh. `\begin{tabular}{@{}l r l@{}}`:

  | Can thiệp | Δpp | Nhóm |
  |---|---|---|
  | ETF head | −0.5 | đối chứng (không đụng objective) |
  | RL-crop | −2.3 | đối chứng (không đụng objective) |
  | FM-inv | −31 | thay invariance |
  | FM-SIGReg | −71 | thay SIGReg (form B; collapse) |
  | KL-score | −72 | thay SIGReg (collapse) |

  Gộp A/B: một dòng "FM-SIGReg", số = form B (−70.8 → làm tròn −71). Không tách A.

- **`\takeaway{...}`:** "Thay lõi SIGReg/invariance đều collapse — dù klscore & FM-SIGReg đã qua
  Phase-0 free-z gate; free-z hội tụ không kéo theo full-pipeline. Đối chứng không đụng objective
  (ETF, RL-crop) giữ được baseline nhưng cũng không vượt. EppsPulley vẫn là neo."

---

## 4. Thứ tự thực hiện + verify

1. Viết `figures/fig_climb_batch7_bars.tex` → `pdflatex` → xác nhận sinh `.pdf`, mắt thường
   thấy 7 cột đúng cao/thấp. ✓ verify: `.pdf` tồn tại, 3 cột phải thấp lè tè.
2. Sửa frame "Câu hỏi nghiên cứu": 2→3 cột, thêm thẻ Giả thuyết 3. ✓ verify compile không lỗi box.
3. Chèn frame Hướng 3 sau Hướng 2. ✓ verify: figure include đúng tên, bảng số khớp §0.
4. Build deck: `cd slides && xelatex → bibtex → xelatex → xelatex slides_main.tex`.
   ✓ verify: PDF có 2 slide mới (thẻ GT3 trong frame câu hỏi; frame Hướng 3 giữa Hướng 2 và Conv-stem),
   pagination không vỡ, không có `??` reference.

## 5. Ngoài phạm vi (không làm trừ khi được yêu cầu)
- KHÔNG đụng frame "Tổng hợp" đang `\iffalse` (L2469–2514) — nếu muốn cập nhật kết luận batch-7
  vào đó là task riêng.
- KHÔNG sửa các figure orphan khác.
- KHÔNG thêm multi-seed/error-bar (batch-7 single seed như batch-1/2; nêu ở takeaway nếu cần
  nhưng không bịa error bar).
- Có thể ghi 1 dòng vào `tracker/batch7-analysis.md` (eval-time results) như task nối tiếp.
