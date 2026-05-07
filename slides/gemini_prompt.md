# Prompt cho Gemini 3.1 Pro — Sửa slides_v2.tex theo feedback

> Copy toàn bộ block markdown bên dưới (từ dòng `---` đầu tiên đến dòng `---` cuối) và paste vào Gemini 3.1 Pro. Đính kèm 2 file: `slides_v2.tex` và `feedback_and_improvement.md`.

---

# NHIỆM VỤ

Bạn là một LaTeX/Beamer expert chuyên sửa slide hội nghị học thuật. Tôi đính kèm 2 file:

1. **`slides_v2.tex`** — file slide hiện tại (30 slide, tiếng Việt, Beamer + TikZ + pgfplots, compile bằng `pdflatex` với `[T5]fontenc + babel{vietnamese}`)
2. **`feedback_and_improvement.md`** — feedback chi tiết của giáo viên hướng dẫn cho slides 1-16, gồm:
   - Phân tích từng slide (atom-count, vấn đề cụ thể, screenshot reference)
   - Code LaTeX gợi ý sửa (paste-ready)
   - Bảng ưu tiên sửa tổng thể
   - Quy tắc thiết kế (box hygiene, TikZ aesthetics, font hierarchy)

Output cuối cùng: **file `slides_v2_fixed.tex`** đã sửa, **compile được bằng `pdflatex slides_v2_fixed.tex && pdflatex slides_v2_fixed.tex`** (không lỗi, không warning đáng kể).

---

# WORKFLOW BẮT BUỘC

## Bước 1 — Đọc + tổng hợp

1. Đọc **toàn bộ** `feedback_and_improvement.md` từ đầu đến cuối (KHÔNG skip).
2. Đặc biệt chú ý:
   - **Bảng "CẬP NHẬT BẢNG ƯU TIÊN SỬA TỔNG THỂ"** ở cuối mỗi đợt feedback — đây là **danh sách việc cần làm theo thứ tự**.
   - Các block code LaTeX trong feedback được đánh dấu **"Code đề xuất"** hoặc **"Code hoàn chỉnh"** — đây là **paste-ready**, dùng nguyên xi.
   - Các phần **"BRAINSTORM N IDEA"** — chọn idea được **gắn ⭐ recommended**, không cần tự sáng tạo lại.
3. Tạo 1 internal todo list theo bảng ưu tiên cuối cùng (đợt 8) — đây là single source of truth.

## Bước 2 — Sửa theo thứ tự ưu tiên

Áp dụng **chính xác** thứ tự sau (KHÔNG skip, KHÔNG đảo):

### Tier 1 — CRITICAL (sửa trước nhất)
1. **Slide 4** — Sửa lỗi học thuật `"LLM dự báo pixel"` → `"Pixel models (MAE, PixelCNN) dự báo pixel"`. Đây là **lỗi nội dung sẽ bị academic audience chất vấn**.
2. **Slide 1** — Thay placeholder `[Tên bạn]` thành `[CHỦ-SLIDE-ĐIỀN]` (placeholder mới rõ ràng hơn, để user biết phải điền). KHÔNG tự đoán tên.
3. **Slide 6** — Cắt từ 21 atom xuống ≤ 7 atom theo **Phương án B (giữ 1 slide)** trong feedback. Code đầy đủ ở mục "SLIDE 6 — Câu Hỏi Thay Đổi Mọi Thứ → Phương án B".
4. **Slide 11** — Áp dụng **Phương án A (Hero Equation)** trong feedback — code đầy đủ có sẵn.

### Tier 2 — HIGH (TikZ + figure redesign)
5. **Slide 4** — Sửa pipeline TikZ theo code đề xuất ở "SLIDE 4 — Bước 3" (mũi tên 1 chiều, 4 màu, có ảnh gốc, dùng `fit` background thay brace).
6. **Slide 9** — Bỏ alertblock Theorem to → 3 dòng inline; áp **IDEA 2 (Iso-Distance Contours)** cho TikZ phải.
7. **Slide 10** — Áp **IDEA 1 + 7 combine** (3D `\shade[ball color]` + bar chart eigenvalue) — code đầy đủ trong feedback.
8. **Slide 13** — Áp **IDEA 3 (Real Histograms via pgfplots)** — code đầy đủ trong feedback. **Đặc biệt: thay tất cả `\draw sin/cos` bằng `pgfplots ybar`**.
9. **Slide 15** — Combine **IDEA 1 + 4** (GPU Breakdown + Gradient Flow) thành 2 panel stack dọc. Bỏ alertblock "2 Hạn Chế" → caption inline.

### Tier 3 — MEDIUM (box hygiene + caption)
10. **Slide 7** — Bỏ 2 alertblock/exampleblock → heading màu + bullet inline (code có sẵn).
11. **Slide 8** — Đổi `\begin{center}` title figure thành `title=` của pgfplots; đổi `legend pos=outer north east`; bỏ 2 alertblock Lemma → caption text dưới figure.
12. **Slide 5** — Thêm cột "# HP" và hàng "LeJEPA" highlight xanh ở cuối bảng.
13. **Slide 3** — Vẽ ellipse bao "không gian embedding" ở cả 2 panel; phân bố `z_i` 2D thay vì xếp dọc; phóng to chấm collapse.
14. **Slide 12** — Đổi bar chart thủ công thành `pgfplots xbar`; bỏ alertblock "Vấn Đề" → caption.
15. **Slide 14** — Bỏ `\resizebox` cho EJB formula → break thành 2 dòng `align*` HOẶC đơn giản hóa thành $\sum_{k=1}^{4} c_k(m_k-m_k^{\mathcal{N}})^2$.
16. **Slide 16** — Thay plot ECF noisy vs target bằng plot Gradient comparison (EJB explode vs Epps-Pulley bounded); đơn giản hóa alertblock Theorem 4.5 còn 1 inequality.

### Tier 4 — LOW (cosmetic)
17. **Tất cả slide** — Đổi label `\tiny` trong TikZ thành `\scriptsize` (chỉ giữ `\tiny` cho legend/sublabel phụ).
18. **Slide 2** — Rút title còn ≤ 5 từ; bỏ `\centering` trong block title; thêm 3 mini-icon TikZ.

## Bước 3 — Verification (BẮT BUỘC)

Sau khi sửa, verify:

1. **Compile check** — bạn KHÔNG thực sự chạy được `pdflatex`, nhưng PHẢI tự kiểm tra:
   - Mọi `\begin{...}` có `\end{...}` tương ứng
   - Mọi `\node` trong TikZ có dấu `;` ở cuối
   - Không có `\resizebox` mới được thêm (vi phạm rule)
   - Không có `[shrink=N]` mới
   - Mọi `pgfplots` có `\begin{axis}` ... `\end{axis}` đầy đủ
   - Không có ký tự đặc biệt LaTeX bị escape sai (`%`, `&`, `_`, `#`)
   - Tiếng Việt có dấu (KHÔNG dùng "Cong Thuc" thay vì "Công Thức")

2. **Atom count check** — với mỗi slide đã sửa, đếm atom (mỗi block/bullet/node TikZ/figure label = 1 atom):
   - Slide 6 sau sửa phải ≤ 8 atom
   - Slide 11 sau sửa phải ≤ 6 atom
   - Slide 7 sau sửa phải ≤ 9 atom
   - Slide 9 sau sửa phải ≤ 8 atom

3. **Box count check** — đếm `\begin{block}\|\begin{alertblock}\|\begin{exampleblock}` tổng deck:
   - Trước: 38 block (bạn có thể đếm trong file gốc để verify baseline)
   - Sau khi sửa: **target ≤ 22 block**.

4. **Color palette check** — KHÔNG được introduce màu mới ngoài 9 màu đã định nghĩa: `primary, accent, bad, good, neutral, lightblue, lightyellow, lightgreen, lightred, lightgray`. Riêng slide 24 hiện đang dùng `cyan, magenta, orange` — sửa thành các màu trong palette.

5. **Vietnamese consistency check** — mọi text tiếng Việt phải có dấu. Math operator giữ tiếng Anh (sort, predict, encoder). Không trộn ngôn ngữ trong cùng cụm từ.

---

# RÀNG BUỘC TUYỆT ĐỐI (KHÔNG ĐƯỢC VI PHẠM)

## R1 — Không phá compilation
- Không xóa `\usepackage{...}` nào trong preamble.
- Không đổi class document (`\documentclass[aspectratio=169,11pt]{beamer}` giữ nguyên).
- Không đổi theme (`\usetheme{Madrid}` giữ nguyên).
- Không thêm package mới trừ khi thực sự cần — nếu cần, document lý do trong comment.

## R2 — Không invent thông tin
- KHÔNG bịa số liệu (accuracy %, dataset size, theorem number).
- KHÔNG thay đổi citation (`Balestriero \& LeCun, 2025`, `arXiv: 2511.08544`).
- KHÔNG thay tên paper, tên author.
- Nếu plot dùng synthetic data illustrative (như slide 18 với `0.8 * exp(-x/500)`), có thể giữ NHƯNG thêm comment `% illustrative, not real data` cạnh code.

## R3 — Tôn trọng cấu trúc deck
- 30 slide, KHÔNG được tự ý thêm/bớt slide.
- Riêng feedback ĐỀ XUẤT tách slide 6 — nếu bạn theo Phương án A (tách thành 6a + 6b), phải báo trong comment đầu file `% NOTE: Slide 6 split into 6a, 6b — total now 31 slides`. Mặc định **giữ 30 slide** (Phương án B).
- Mỗi slide GIỮ takeaway ở footer (template `\takeaway{...}`).

## R4 — Tôn trọng phong cách
- Mọi takeaway dùng macro `\takeaway{...}` đã định nghĩa, không tự viết `\begin{beamercolorbox}` raw.
- Giữ TikZ styles đã định nghĩa: `stdbox`, `primarybox`, `accentbox`, `goodbox`, `badbox`, `neutralbox`, `lightbluebox`, `mainarrow`, `subarrow`, `dashedarrow`, `embnode`. Không tự define style mới trùng tên.
- Nếu cần style TikZ mới, đặt tên có prefix `lj-` (LeJEPA) để dễ identify.

## R5 — Output format
- Output 1 file duy nhất: **`slides_v2_fixed.tex`** (full file, không phải patch/diff).
- Đầu file thêm comment block:
  ```latex
  % ============================================================
  %  slides_v2_fixed.tex — generated by Gemini 3.1 Pro
  %  Source: slides_v2.tex
  %  Applied feedback from: feedback_and_improvement.md
  %  Date: [today's date]
  %  Changes summary: [3-5 bullet points cao cấp nhất]
  % ============================================================
  ```
- Cuối output, kèm 1 báo cáo (ngoài file LaTeX) gồm:
  - Bảng "Đã sửa / Chưa sửa" theo Tier 1-4.
  - Box count trước/sau.
  - Atom count cho 4 slide critical (6, 7, 9, 11).
  - Liệt kê warning hoặc rủi ro (ví dụ: "Slide X có thể overflow nếu font khác").
  - Liệt kê tất cả synthetic plots đã giữ nguyên (để user biết cần thay data thật khi có).

---

# CÁC TIPS HIỆU SUẤT CHO CÔNG VIỆC NÀY

## Tip 1 — Đọc feedback theo chiều dọc, sửa theo chiều ngang
Feedback được tổ chức theo **đợt** (đợt 1 = slides 1-2, đợt 2 = 3-4, v.v.). Đừng sửa từng đợt — đọc hết, gom các Tier 1 (cùng critical) sửa trước.

## Tip 2 — Khi feedback có "code đề xuất", paste y nguyên
Code trong feedback đã được kiểm tra cú pháp + thẩm mỹ. ĐỪNG cố "improve thêm" — chỉ paste và adjust path/reference.

## Tip 3 — Khi nghi ngờ, giữ phiên bản cũ
Nếu feedback có 2 phương án mâu thuẫn, hoặc bạn không chắc về fix nào, chọn **phương án ít aggressive hơn** và document trong comment `% TODO: review — feedback suggests X but kept Y because Z`.

## Tip 4 — Test compilation mentally
Mỗi khi đổi 1 environment hoặc TikZ block, mentally simulate:
- Brace count cân bằng?
- Mọi `\node[...]` đóng `;`?
- Mọi `\addplot[...]` có data hoặc function valid?

## Tip 5 — Atom-count là kim chỉ nam
Khi không chắc cắt gì, dùng atom count. Slide nên ≤ 8 atom. Nếu slide đã sửa vẫn > 8 atom → cắt thêm.

## Tip 6 — TikZ aesthetics quick-wins
- Mọi shape lớn (> 1cm) → dùng `\shade[ball color=...]` thay vì `\draw[fill=...]`
- Mọi shape lớn → thêm shadow mờ (`\fill[neutral!10, opacity=0.5] ... ellipse`)
- Mọi histogram/distribution plot → dùng `pgfplots ybar` thật, KHÔNG dùng `\draw sin/cos`
- Caption dưới figure → `\footnotesize` hoặc `\scriptsize`, KHÔNG `\tiny`

---

# CHECKLIST CUỐI CÙNG TRƯỚC KHI OUTPUT

- [ ] Đã đọc toàn bộ feedback_and_improvement.md
- [ ] Đã sửa toàn bộ Tier 1 (4 việc critical)
- [ ] Đã sửa ≥ 80% Tier 2
- [ ] Đã sửa ≥ 60% Tier 3
- [ ] File compile được mentally (brace balance, env match)
- [ ] Box count ≤ 22
- [ ] Slide 6 ≤ 8 atom, slide 11 ≤ 6 atom
- [ ] Không có `\resizebox` hoặc `[shrink]` mới
- [ ] Không màu ngoài palette
- [ ] Tiếng Việt có dấu đầy đủ
- [ ] Output đầy đủ + báo cáo

---

# CÂU HỎI MỞ ĐẦU NẾU CẦN

Nếu sau khi đọc feedback, bạn còn câu hỏi quan trọng (ví dụ: "Phương án A hay B cho slide 6?", "Có nên tách slide 11?", "synthetic plot nào nên giữ?"), hãy đặt **TỐI ĐA 3 câu hỏi clarification** ở đầu output, sau đó proceed với best guess. KHÔNG hỏi quá 3 câu — phần còn lại tự quyết theo "ít aggressive hơn".

---

**BẮT ĐẦU.** Đọc 2 file đính kèm, sau đó output `slides_v2_fixed.tex` + báo cáo.
