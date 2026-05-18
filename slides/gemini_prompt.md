# Prompt cho Gemini 3.1 Pro — Sửa slides_v2.tex theo batch

> **Cách dùng:** Chia làm **6 batch độc lập**. Mỗi batch là 1 conversation/turn riêng với Gemini. Sau mỗi batch, bạn paste output vào local file rồi feed batch tiếp theo cùng với file đã sửa từ batch trước.
>
> **Files cần đính kèm cho MỌI batch:**
> - `slides_v2.tex` (file gốc, KHÔNG đổi qua các batch)
> - `feedback_and_improvement.md` (feedback đầy đủ — Gemini chỉ đọc PHẦN tương ứng với batch đó)
> - `slides_v2_working.tex` (file đang sửa — sau batch 1 thì đây là output của batch trước)

---

## TỔNG QUAN 6 BATCH

| Batch | Slides | Focus | Files cần đọc trong feedback |
|-------|--------|-------|------------------------------|
| **0** | (preamble) | Setup + audit baseline | Preamble + intro |
| **1** | 1, 2, 3, 4 | Title + intro paradigms + collapse + JEPA | Đợt 1 + 2 |
| **2** | 5, 6, 7, 8 | Heuristic + pivot question + linear probe | Đợt 3 + 4 |
| **3** | 9, 10, 11, 12 | Theory proof + intuition + summary + challenge | Đợt 5 + 6 |
| **4** | 13, 14, 15, 16 | Random slicing + tests + Epps-Pulley | Đợt 7 + 8 |
| **5** | (verification) | Compile check + final report | Toàn bộ |

---

# 📋 BATCH 0 — SETUP & BASELINE AUDIT

## Prompt

```
Bạn là một LaTeX/Beamer expert chuyên sửa slide hội nghị học thuật tiếng Việt.

Tôi đính kèm:
1. slides_v2.tex — file slide gốc (30 slide, Beamer + TikZ + pgfplots)
2. feedback_and_improvement.md — feedback chi tiết của giáo viên hướng dẫn

NHIỆM VỤ BATCH 0 (chỉ làm task setup, KHÔNG sửa slide):

1. Đọc preamble file slides_v2.tex (dòng 1-130, kết thúc trước \begin{document}).

2. Đọc phần đầu feedback_and_improvement.md (đến hết "Đợt 1") để nắm context.

3. Output 1 file duy nhất: slides_v2_working.tex
   = bản copy chính xác của slides_v2.tex
   + thêm comment block sau dòng \documentclass:

   % ============================================================
   %  slides_v2_working.tex — work-in-progress
   %  Source: slides_v2.tex
   %  Applied feedback from: feedback_and_improvement.md
   %  Batch progress:
   %    [ ] Batch 1 — Slides 1-4
   %    [ ] Batch 2 — Slides 5-8
   %    [ ] Batch 3 — Slides 9-12
   %    [ ] Batch 4 — Slides 13-16
   %    [ ] Batch 5 — Verification
   % ============================================================

4. Sau file, output BÁO CÁO BASELINE gồm:
   - Đếm tổng số block: grep -c "begin{block}\|begin{alertblock}\|begin{exampleblock}"
   - Liệt kê tất cả slide có \resizebox hoặc [shrink=N] (mùi hôi)
   - Liệt kê 9 màu trong palette (primary, accent, bad, good, neutral, lightblue, lightyellow, lightgreen, lightred, lightgray)
   - Liệt kê tất cả TikZ styles đã định nghĩa (stdbox, primarybox, ...)

KHÔNG SỬA NỘI DUNG SLIDE NÀO. Chỉ tạo working file + báo cáo.

RÀNG BUỘC:
- Giữ nguyên \documentclass[aspectratio=169,11pt]{beamer}
- Giữ nguyên \usetheme{Madrid}
- Giữ nguyên toàn bộ preamble
- Output file LaTeX hợp lệ.
```

---

# 📋 BATCH 1 — SLIDES 1-4 (Title + Paradigms + Collapse + JEPA)

## Prompt

```
Bạn là LaTeX/Beamer expert. Tôi tiếp tục dự án sửa slides_v2.tex theo batch.

Files đính kèm:
1. slides_v2_working.tex — file đang sửa (output từ batch trước)
2. feedback_and_improvement.md — feedback đầy đủ
3. slides_v2.tex — file gốc (chỉ tham khảo, KHÔNG sửa)

NHIỆM VỤ BATCH 1: Sửa slides 1, 2, 3, 4 (chỉ 4 slide này, KHÔNG đụng vào slide khác).

ĐỌC TRONG FEEDBACK:
- Đợt 1 (Slide 1 + 2)
- Đợt 2 (Slide 3 + 4)
- Phần "Nguyên tắc thiết kế TikZ cho slide khoa học" (5 nguyên tắc)

DANH SÁCH SỬA CỤ THỂ — THỰC HIỆN TUẦN TỰ:

═══ SLIDE 1 (Title) ═══
[CRITICAL]
□ Thay placeholder "[Tên bạn]" thành "[CHỦ-SLIDE-ĐIỀN]" (placeholder rõ hơn)

[HIGH]
□ Thêm đường tròn dashed bao đám 5 embedding nodes:
  \draw[dashed, color=good!50, thick] (4.5, -0.2) circle (1.4cm);
  Đẩy nhãn $\mathcal{N}(0,I)$ ra góc trên-phải đường tròn

[HIGH]
□ Đồng bộ độ dày 5 mũi tên từ encoder: tất cả thick HOẶC tất cả thin
  (hiện 3 thick + 2 thin — không đối xứng có lý do)

[MEDIUM]
□ Subtitle "Provable & Scalable SSL / Without the Heuristics" gộp 1 dòng:
  {\large\itshape Provable \& Scalable SSL — Without the Heuristics}

[MEDIUM]
□ Tách "Presenter:" khỏi "arXiv:" bằng \vspace*{12pt}

═══ SLIDE 2 (3 Paradigms) ═══
[HIGH]
□ Rút title từ "SSL Học Từ Cấu Trúc Dữ Liệu — Không Cần Nhãn"
  → "Ba Paradigm Học Máy" (hoặc tương đương ≤ 5 từ)

[HIGH]
□ Đổi "Ảnh → Ảnh" (cột Reconstruction) thành "Ảnh → Pixel"
  (đối lập semantic với "View ↔ View")

[MEDIUM]
□ Nhấn cột Self-Supervised: thêm dòng cuối exampleblock:
  \textbf{\color{good} ← LeJEPA ở đây}

[MEDIUM]
□ Bỏ \centering trong \begin{block}{\centering Supervised} 
  (gây glitch trong Beamer Madrid theme — chỉ giữ tên block)
  Áp cho cả 3 block

[LOW]
□ Đổi takeaway thành "Annotation đắt — cấu trúc dữ liệu thì miễn phí"

═══ SLIDE 3 (Collapse) ═══
[CRITICAL — TikZ redesign]
Áp PHƯƠNG ÁN A trong feedback (giữ layout 2-panel nhưng cải thiện):

PANEL TRÁI (collapse):
□ Vẽ region ellipse mờ làm "không gian embedding":
  \draw[dashed, color=neutral!40, fill=lightred] (0,0) circle (1.6cm);
□ Phóng to chấm collapse từ 0.7cm lên 1.0cm, fill=bad đậm
  Thêm drop shadow: drop shadow={opacity=0.3}
□ 4 mũi tên từ x_i đến collapse — dùng curved arrows (bend left=10) thay vì thẳng
□ Caption "f(x_1) = f(x_2) = ... = c" đặt PHÍA TRÊN collapse, font \small\bfseries

PANEL PHẢI (diversity):
□ Cũng có region ellipse mờ (lightgreen)
□ Phân bố 4 chấm z_i theo 2D scatter (không xếp dọc):
  z_1 at (-0.8, 0.7), z_2 at (0.9, 0.5), 
  z_3 at (-0.6, -0.8), z_4 at (0.7, -0.6)
□ Mũi tên 1-1 từ x đến z, thin (color=good!60)

═══ SLIDE 4 (JEPA) ═══
[CRITICAL — Lỗi học thuật]
□ Trong alertblock "JEPA vs LLM": sửa "LLM: dự báo pixel"
  → "Pixel models (MAE, PixelCNN, AR pixel models): dự báo pixel"
  (LLM dự báo TOKEN, không phải pixel — sẽ bị academic chất vấn)

[HIGH — TikZ redesign]
Thay TOÀN BỘ pipeline TikZ bằng pipeline MỚI:

Yêu cầu:
□ Thêm node "Ảnh gốc x" ở trái nhất (lightbluebox)
□ 2 nhánh view 1 (trên) và view 2 (dưới) — đều xuất phát từ ảnh gốc
□ "Loss" là focal point bên phải (goodbox to, fill=good!60, text=white, font=\small\bfseries)
□ KHÔNG có mũi tên ngược: ẑ_1 đi THẲNG đến Loss, không đi lên
□ Encoder share: dùng \begin{pgfonlayer}{background} + \node[fit=...] dashed background
  thay vì brace decoration nhỏ
□ Chỉ 4 màu node: data (lightbluebox), model (primarybox), latent (accentbox), loss (goodbox)
□ Bỏ neutralbox cho "predictor" — đổi thành primarybox

Code đầy đủ ở mục "SLIDE 4 — Bước 3" trong feedback. PASTE Y NGUYÊN.

[MEDIUM]
□ Bỏ block "JEPA vs LLM" khỏi cột phải (đã sửa lỗi học thuật trong alertblock cũ)
  HOẶC giữ block nhưng sửa nội dung pixel models
□ Block "2 Nguyên Tắc" giữ nguyên

OUTPUT:
1. File slides_v2_working.tex đã sửa 4 slides (giữ nguyên slides 5-30 + preamble)
2. Báo cáo cuối:
   - Diff summary: dòng nào đã đổi
   - Atom count slide 1, 2, 3, 4 (sau sửa)
   - Box count chênh lệch (trước/sau cho 4 slide này)
   - Liệt kê warning nào nếu có
   - Update progress checkbox: [✓] Batch 1

RÀNG BUỘC:
- KHÔNG đụng slides 5-30
- KHÔNG đổi preamble
- KHÔNG thêm package mới
- KHÔNG dùng \resizebox hay [shrink]
- KHÔNG dùng màu ngoài palette
- Tiếng Việt phải có dấu đầy đủ
- Mọi \begin{...} phải có \end{...}
- Mọi \node trong TikZ phải đóng ;
- Giữ \takeaway{...} ở cuối mỗi slide
```

---

# 📋 BATCH 2 — SLIDES 5-8 (Heuristic + Pivot + Linear Probe)

## Prompt

```
Tiếp tục dự án sửa slides theo batch. Đây là BATCH 2 — slides 5, 6, 7, 8.

Files đính kèm:
1. slides_v2_working.tex (output từ batch 1)
2. feedback_and_improvement.md
3. slides_v2.tex (gốc, tham khảo)

NHIỆM VỤ BATCH 2: Sửa slides 5, 6, 7, 8.

ĐỌC TRONG FEEDBACK:
- Đợt 3 (Slide 5 + 6 — slide 6 là CRITICAL)
- Đợt 4 (Slide 7 + 8 + Vấn đề "Box Everywhere")
- Phần "Quy tắc 4 câu hỏi trước khi viết \begin{block}"

═══ SLIDE 5 (Heuristic Stack) ═══
[HIGH]
□ Rút title: "Heuristic Stack: Vá Lỗ, Không Có Lý Thuyết"

[HIGH]
□ Thêm cột "# Hyperparameters" giữa "Cơ chế" và "Hạn chế"
  Giá trị: SimCLR=3, BYOL=5, DINO=7+, VICReg=4, I-JEPA=5

[CRITICAL]
□ Thêm hàng cuối bảng "LeJEPA" highlight xanh:
  \midrule
  \rowcolor{good!15}
  \textbf{LeJEPA} & \textbf{Iso Gaussian} & \textbf{1} & \textcolor{good}{\cmark}\;Provable \\
  \bottomrule

[MEDIUM]
□ \renewcommand{\arraystretch}{1.3} để giãn dòng

[LOW]
□ Đổi "Whitening (whitening)" → "Whitening (variance)" (tránh redundant)

═══ SLIDE 6 (Câu Hỏi Pivot) — ƯU TIÊN CAO NHẤT ═══
Slide hiện có 21 atom, dùng [shrink=5] (mùi hôi). PHẢI cắt xuống ≤ 8 atom.

[CRITICAL — REWRITE]
Áp PHƯƠNG ÁN B (Cắt gọt mạnh) trong feedback. Code đầy đủ trong mục:
"SLIDE 6 — Phương án B — Giữ 1 slide nhưng cắt gọt mạnh"

PASTE NGUYÊN code đó. Lưu ý:
□ Bỏ [shrink=5] khỏi \begin{frame}
□ 2 block bên trái CHỈ CHỨA câu hỏi (không có 3 bullet)
□ TikZ phải CHỈ có 3 node chính (Prevent → Pivot → Optimal), bỏ 3 axiom phụ
□ Bỏ label "đổi góc nhìn" trên mũi tên
□ Atom target: 7 (2 block + 3 TikZ node + 1 label theorem 3.3 + 1 takeaway)

═══ SLIDE 7 (Linear Probe Setup) ═══
[HIGH]
Bỏ 2 box (alertblock + exampleblock). Thay bằng heading màu inline.

PASTE Y NGUYÊN code trong feedback "SLIDE 7 — Hướng cải thiện — phương án ít box hơn".

Lưu ý:
□ Equation top giữ nguyên nhưng KHÔNG \Large (dùng default size)
□ Mỗi cột: heading màu (\textcolor{bad}{\textbf{\large \xmark\ Anisotropic}}) + 4 dòng text
□ Cuối mỗi cột: 1 dòng tổng kết bold màu (\textbf{\color{bad}Bias \& Variance đều CAO})

═══ SLIDE 8 (Lemma Aniso) ═══
[CRITICAL — Visual fixes]
□ Title figure: thay \begin{center}\textbf{Bias theo số mẫu N}\end{center}
  bằng option title= của pgfplots:
  \begin{axis}[
    ...,
    title={Bias theo số mẫu $N$},
    title style={font=\footnotesize\bfseries},
  ]
  Áp cho cả 2 plot.

□ Legend position: đổi at={(0.98,0.08)} thành legend pos=outer north east
  để legend KHÔNG đè data. Áp cả 2 plot.

[HIGH]
□ Bỏ 2 alertblock "Lemma 3.1" và "Lemma 3.2"
  Thay bằng caption text dưới figure:
  \begin{center}\scriptsize
    \textbf{Lemma 3.1:} Với $\lambda>0$, $\exists\,\mathbf{y}$:
    $\text{Bias}(\hat\beta_{\text{aniso}}) > \text{Bias}(\hat\beta_{\text{iso}})$
  \end{center}

[MEDIUM]
□ Variance plot: 3 đường aniso đang cùng slope (song song) — không thể hiện variance
  Đổi thành 4-5 đường aniso với slope khác nhau (-0.4 đến 0.8)
  + 4-5 đường iso slope similar (-0.5 to -0.6 — clustered tight)

OUTPUT:
1. File slides_v2_working.tex đã sửa 4 slides (giữ nguyên slides 1-4 từ batch 1, slides 9-30 nguyên)
2. Báo cáo:
   - Atom count slide 6 (target ≤ 8)
   - Box count chênh lệch (trước/sau cho batch 2)
   - Verify [shrink=5] đã được xóa khỏi slide 6
   - Update progress: [✓] Batch 2

RÀNG BUỘC:
- KHÔNG đụng slides 1-4 (đã sửa) hoặc 9-30 (chưa đến lượt)
- Áp dụng quy tắc box hygiene xuyên suốt
- Mọi yêu cầu về compilation, palette, tiếng Việt như batch 1
```

---

# 📋 BATCH 3 — SLIDES 9-12 (Theory Proof + Intuition + Summary)

## Prompt

```
Tiếp tục. Đây là BATCH 3 — slides 9, 10, 11, 12.

Files đính kèm:
1. slides_v2_working.tex (output từ batch 2)
2. feedback_and_improvement.md
3. slides_v2.tex

NHIỆM VỤ BATCH 3: Sửa slides 9, 10, 11, 12.

ĐỌC TRONG FEEDBACK:
- Đợt 5 (Slide 9 + 10 + brainstorm aniso/iso 8 ideas)
- Đợt 6 (Slide 11 + 12 + brainstorm minimize visual 6 phương án)
- Phần "Tips chung để TikZ đẹp hơn" (6 tips)

═══ SLIDE 9 (Bằng Chứng 2 — Iso Optimal) ═══
[CRITICAL — Layout rewrite]
□ BỎ alertblock to "Theorem 3.3" với math \tiny — chiếm ~50% slide
  Thay thế bằng: 3 dòng inline ở cột trái:
  \scriptsize\color{neutral}
  \textbf{Theorem 3.3:} 
  $\arg\min_p \text{ISB}(p) = \mathcal{N}(\mathbf{0}, \tfrac{\kappa}{K} I)$
  \quad (\textbf{unique})

□ Cột phải: PHÓNG TO TikZ aniso/iso lên — đây phải là focal point.
  Áp IDEA 2 (Iso-Distance Contours) trong feedback "Slide 10 brainstorm"

  Code có sẵn ở "💡 IDEA 2 — Concentric Iso-Distance Contours"
  PASTE Y NGUYÊN, đặt ở cột phải slide 9.

[HIGH]
□ Cột trái: thay 2 paragraphs hiện tại bằng:
  \textcolor{primary}{\textbf{Vì sao $\mathcal{N}(0,I)$?}}\\[6pt]
  \footnotesize
  kNN \& kernel regression dựa trên\\\textbf{khoảng cách Euclidean}.
  \\[8pt]
  \textcolor{bad}{\xmark\ Aniso:} neighborhood lệch trục dài → bias\\[3pt]
  \textcolor{good}{\cmark\ Iso:} neighborhood đối xứng → unbiased\\[10pt]

═══ SLIDE 10 (Geometric Intuition) ═══
[CRITICAL — Aesthetic redesign]
Áp IDEA 1 + 7 COMBINE (3D Shaded + Eigenvalue Bar Chart) trong feedback.

Code đầy đủ ở mục "CODE HOÀN CHỈNH — IDEA 1 + 7" trong đợt 5.
PASTE Y NGUYÊN.

Lưu ý quan trọng:
□ Dùng \shade[ball color=bad!50, opacity=0.85] cho ellipsoid aniso
□ Dùng \shade[ball color=good!60, opacity=0.9] cho sphere iso
□ Thêm shadow mờ dưới mỗi shape: \fill[bad!15, opacity=0.5] (0,-0.75) ellipse (1.6cm and 0.10cm);
□ Thêm highlight reflection: \fill[white, opacity=0.45] (-0.5, 0.18) ellipse (0.32cm and 0.08cm);
□ Bar chart eigenvalue ở TRÊN mỗi shape (4 bar cho aniso giảm dần, 4 bar iso bằng nhau)
□ Mũi tên giữa thay cho ⇒: \draw[->, ultra thick, primary] (-1.5, 0.5) -- (1.5, 0.5);
□ BỎ axes labels (λ_1, λ_2) trong shape vì đã có bar chart riêng — tránh redundant

═══ SLIDE 11 (Theory Summary) — URGENT ═══
Slide hiện 14 atom, diagram bị nén, bảng so sánh redundant với slide 5/20.

[CRITICAL — REWRITE]
Áp PHƯƠNG ÁN A (Hero Equation) trong feedback "đợt 6". 

Code đầy đủ ở mục "💡 PHƯƠNG ÁN A — Hero Equation minimal".
PASTE Y NGUYÊN.

Lưu ý:
□ BỎ TikZ flow diagram phức tạp 5-node
□ BỎ block "So sánh với Prior SSL" + bảng (đã có ở slide 5 và 20)
□ BỎ exampleblock "Ý nghĩa" (1 câu — vi phạm box hygiene)
□ Hero element: phương trình $f_\theta(\mathbf{x}) \sim \mathcal{N}(\mathbf{0}, I)$ ở \Huge
□ 3 cột nhỏ phía dưới (Linear/kNN/Kernel probe) KHÔNG box, chỉ heading + bullet
□ \vfill 2 phía để slide thở
□ Atom target: 5

═══ SLIDE 12 (Challenge High-Dim) ═══
[HIGH]
□ Đổi bar chart thủ công thành pgfplots xbar:
  \begin{tikzpicture}
  \begin{axis}[
    xbar, width=6cm, height=4cm, bar width=10pt,
    symbolic y coords={SIGReg, Direct, KL, MMD},
    ytick=data,
    nodes near coords,
    point meta=explicit symbolic,
    ...
  ]
    \addplot+[fill=bad!70, draw=none] coordinates {
      (3, MMD) [O(N^2)]
      (1.5, KL) [Unstable]  
      (3, Direct) [O(N^2)]
    };
    \addplot+[fill=good!80, draw=good, line width=1pt] coordinates {
      (0.8, SIGReg) [O(N)]
    };
  \end{axis}
  \end{tikzpicture}

[HIGH]
□ Bỏ alertblock "Vấn Đề" (1 dòng — vi phạm box hygiene)
  Thay bằng caption dưới chart:
  \begin{center}\scriptsize\color{neutral}
    \textbf{Vấn đề:} Mọi multivariate normality test chuẩn (BHEP, Mardia) đều $\mathcal{O}(N^2)$
  \end{center}

[MEDIUM]
□ Bỏ block "3 Yêu Cầu Bắt Buộc" — dùng heading + bullet inline
  (xem code mẫu trong feedback đợt 6)

[LOW]
□ Highlight SIGReg bar: thêm icon ⭐ và caption "← LeJEPA"

OUTPUT:
1. File slides_v2_working.tex
2. Báo cáo:
   - Atom count slide 9 (target ≤ 8) và 11 (target ≤ 6)
   - Box count chênh lệch
   - Verify aniso/iso visual: có \shade[ball color] không?
   - Update progress: [✓] Batch 3

RÀNG BUỘC TIKZ AESTHETICS:
- Mọi shape lớn (>1cm) PHẢI dùng \shade[ball color=...] thay \draw[fill=...]
- Mọi shape lớn THÊM shadow + highlight
- KHÔNG dùng \draw sin/cos cho histogram/distribution
- Caption ≥ \scriptsize, không \tiny
```

---

# 📋 BATCH 4 — SLIDES 13-16 (Random Slicing + Tests + Epps-Pulley)

## Prompt

```
Tiếp tục. Đây là BATCH 4 — slides 13, 14, 15, 16.

Files đính kèm:
1. slides_v2_working.tex (output từ batch 3)
2. feedback_and_improvement.md
3. slides_v2.tex

NHIỆM VỤ BATCH 4: Sửa slides 13, 14, 15, 16.

ĐỌC TRONG FEEDBACK:
- Đợt 7 (Slide 13 brainstorm 7 ideas + Slide 14)
- Đợt 8 (Slide 15 brainstorm 6 ideas + Slide 16)

═══ SLIDE 13 (Random 1D Projections) ═══
[CRITICAL — Lỗi gốc]
Phát hiện: code hiện tại dùng \draw sin/cos để vẽ "histogram" — đây THỰC RA là sin curve, KHÔNG phải distribution!

Áp IDEA 3 (Real Histograms via pgfplots ybar) trong feedback đợt 7.
Code đầy đủ ở mục "CODE ĐỀ XUẤT HOÀN CHỈNH" trong đợt 7.

PASTE Y NGUYÊN. Lưu ý:
□ Cloud: \shade[ball color=primary!50, opacity=0.55] (0,0) ellipse (1.3cm and 0.8cm);
  + 10 chấm density bên trong
□ 3 histogram THẬT bằng pgfplots ybar interval
□ Mỗi histogram có Normal curve overlay:
  - "Khớp": Normal curve solid (color=primary, thick)
  - "Không khớp": Normal curve dashed (so sánh với histogram bimodal)
□ Histogram 1 và histogram 3 (cùng "Khớp N(0,1)") phải có DATA KHÁC NHAU (mỗi sample khác)
□ BỎ alertblock "Hyperspherical Cramér-Wold" → heading + math inline
□ BỎ block "Phiên bản thực tế" → heading + text inline
□ Theorem 4.2 → 1 dòng \scriptsize\color{neutral} ở cuối

═══ SLIDE 14 (Moment Tests) ═══
[HIGH]
□ Bỏ \resizebox cho EJB formula:
  Hoặc break thành 2 dòng align*:
  \begin{align*}
    \text{EJB}(\mathbf{u}) &= \tfrac{N\hat\mu^2}{\hat\sigma^2} 
    + \tfrac{(N-1)(\hat\sigma^2-1)^2}{2}\\
    &+ \tfrac{N}{6}\!\left(\text{skew}^2 + \tfrac{(\text{kurt}-3)^2}{4}\right)
  \end{align*}
  
  HOẶC đơn giản hóa thành:
  \[ \text{EJB}(\mathbf{u}) = \sum_{k=1}^{4} c_k \cdot (m_k - m_k^{\mathcal{N}})^2 \]

[MEDIUM]
□ Bỏ alertblock "Theorem 4.3" (chỉ 1 dòng — vi phạm box hygiene)
  Thay bằng caption inline dưới block EJB:
  \centering\scriptsize
  \textcolor{bad}{\textbf{Theorem 4.3:}} Minimize finite moments \textbf{KHÔNG} imply $P=Q$.

[MEDIUM]
□ 2 bullet "K nhỏ / K lớn" → đổi thành table:
  \centering\footnotesize
  \begin{tabular}{l l}
  \toprule
  $K$ \textbf{nhỏ} & shortcut solutions tồn tại \\
  $K$ \textbf{lớn} & gradient explode \\
  \bottomrule
  \end{tabular}

[LOW]
□ Plot gradient: ymax=80 thay vì 100 (curve "chạm trần", explode mạnh hơn)
□ Thêm dashed line ngang ở y=10 làm "ngưỡng stable threshold"

═══ SLIDE 15 (CDF Tests) ═══
[HIGH — Figure redesign]
Sort visualization hiện chỉ show "operation" — không show "vấn đề" (non-parallel + non-differentiable).

Áp COMBINE IDEA 1 (GPU Breakdown) + IDEA 4 (Gradient Flow) trong feedback đợt 8.
Code đầy đủ ở mục "Code cho figure đề xuất (Idea 1+4 combined)".

Layout: 2 mini-panel STACK DỌC trong cột phải:
□ Panel trên: "Vấn đề 1: Non-parallel"
  - 2 GPU box (lightgray)
  - sync arrow (bad, 2 chiều)
  - bottleneck box (lightred)
□ Panel dưới: "Vấn đề 2: Non-differentiable"
  - Forward: x → sort → z (mũi tên primary)
  - Backward: ⊘ to ở giữa, dashed lines bad bên 2 cạnh
  - Caption: "gradient = 0 a.e."

[HIGH]
□ Cột trái — bỏ alertblock "2 Hạn Chế" (đã được visualize trong figure phải)
  Giữ block "Công Thức CDF Test" với formula T_w (vẫn cần)
  2 hạn chế chuyển thành caption inline DƯỚI figure phải:
  \centering\footnotesize
  \textcolor{bad}{\xmark\ Non-parallel} (Multi-GPU sync)\\
  \textcolor{bad}{\xmark\ Non-differentiable} (cần relaxation)

[LOW]
□ Sửa caption "∂(sort)/∂x = undefined" thành "gradient = 0 a.e. với jumps"
  (chính xác về toán học hơn)

═══ SLIDE 16 (Epps-Pulley) ═══
[HIGH]
□ Math top: 1 formula chính EP + 2 definition phụ.
  Đổi 2 definition thành caption \tiny\color{neutral} dưới formula chính:
  
  \begin{center}
    \[ EP = N \int |\hat\phi_X(t) - \phi(t)|^2 \, e^{-t^2/2} \, dt \]
    \tiny\color{neutral}
    $\hat\phi_X(t) = \tfrac{1}{N}\sum e^{itX_j}$ (empirical CF) \quad
    $\phi(t) = e^{-t^2/2}$ (CF của $\mathcal{N}(0,1)$)
  \end{center}

[HIGH]
□ Plot CF Value: 2 đường (Empirical + Target) hiện gần như chồng nhau.
  Tăng noise của Empirical:
  \addplot[color=good, only marks, mark=*, mark size=0.8pt, samples=30, domain=-5:5] 
    {exp(-x^2/2) + 0.05*sin(deg(8*x))};
  HOẶC thêm comment: % illustrative — empirical CF should be noisy

[HIGH]
□ Đơn giản hóa alertblock "Bounded Gradient (Theorem 4.5)":
  - Bỏ \resizebox
  - Chỉ giữ 1 inequality:
    $\left|\frac{\partial EP}{\partial z_i}\right| \leq \frac{4\sigma^2}{N}$
  - Bỏ inequality về curvature (∂²)

[MEDIUM]
□ 3 bullet "Differentiable / O(N) / DDP-friendly" → đổi thành 3 mini-card ngang
  dùng goodbox (như slide 17 đã làm):
  \begin{tikzpicture}[every node/.style={font=\tiny}, scale=0.85]
    \node[goodbox, minimum width=2.0cm, align=center] (p1) at (0,0) 
      {\cmark\ Differentiable\\(ECF = avg)};
    \node[goodbox, minimum width=2.0cm, align=center] (p2) at (2.6,0) 
      {\cmark\ $\mathcal{O}(N)$ Scale\\(no sort)};
    \node[goodbox, minimum width=2.0cm, align=center] (p3) at (5.2,0) 
      {\cmark\ DDP-friendly\\(\texttt{all\_reduce})};
  \end{tikzpicture}

OUTPUT:
1. File slides_v2_working.tex
2. Báo cáo:
   - Verify slide 13 KHÔNG còn \draw sin hoặc \draw cos cho histogram
   - Verify slide 14 KHÔNG còn \resizebox
   - Box count chênh lệch
   - Update progress: [✓] Batch 4

RÀNG BUỘC TIKZ:
- Histogram/distribution plot PHẢI dùng pgfplots ybar, KHÔNG \draw sin/cos
- Cloud/sphere PHẢI dùng \shade[ball color]
- Mỗi shape lớn có shadow + highlight
- Caption ≥ \scriptsize
```

---

# 📋 BATCH 5 — VERIFICATION & FINAL POLISH

## Prompt

```
Đây là BATCH CUỐI — Verification + Final Polish + Cosmetic.

Files đính kèm:
1. slides_v2_working.tex (output từ batch 4)
2. feedback_and_improvement.md
3. slides_v2.tex (gốc, chỉ tham khảo nếu cần verify)

NHIỆM VỤ BATCH 5:

PHẦN A — Cosmetic toàn deck (slides 1-30):

□ Tìm tất cả \tiny trong TikZ \node[font=\tiny] và đổi thành \scriptsize
  TRỪ KHI là legend/sublabel phụ (tick label trong axis OK giữ \tiny)
  Trên màn chiếu \tiny không đọc được — chỉ giữ cho phụ chú thực sự nhỏ

□ Slide 24 — Đổi màu cyan, magenta, orange (vi phạm palette) 
  thành các màu trong palette: primary, accent, good, bad, neutral, ...
  Hoặc dùng !N gradients (primary!60, primary!80, ...)

□ Verify mọi slide có \takeaway{...} ở cuối (kiểm tra slides 1-30)

PHẦN B — Compile verification (mental):

□ Đếm tổng cộng \begin{ và \end{ — phải khớp 1-1
□ Đếm tổng cộng \begin{frame} và \end{frame} — phải = 30 (hoặc 31 nếu split slide 6)
□ Mỗi \begin{tikzpicture} có \end{tikzpicture}
□ Mỗi \begin{axis} có \end{axis}
□ Mỗi \begin{scope} có \end{scope}
□ Mỗi \node có dấu ; cuối cùng
□ Không có ký tự đặc biệt LaTeX bị escape sai trong text Việt:
  - % phải escape thành \%
  - & trong tabular OK, ngoài tabular phải \&
  - _ trong text phải \_  (hoặc trong math mode OK)
  - # phải \#

□ Search và liệt kê:
  - Mọi \resizebox còn sót (target = 0)
  - Mọi [shrink=N] còn sót (target = 0)
  - Mọi \tiny trong node TikZ chính (không phải tick label)

PHẦN C — Output cuối cùng:

□ Đổi tên file output từ slides_v2_working.tex thành slides_v2_fixed.tex
□ Cập nhật comment block đầu file:

  % ============================================================
  %  slides_v2_fixed.tex — FINAL
  %  Source: slides_v2.tex
  %  Applied feedback from: feedback_and_improvement.md
  %  Batch progress:
  %    [✓] Batch 1 — Slides 1-4
  %    [✓] Batch 2 — Slides 5-8
  %    [✓] Batch 3 — Slides 9-12
  %    [✓] Batch 4 — Slides 13-16
  %    [✓] Batch 5 — Verification
  %  Date: [today's date]
  %  
  %  Major changes:
  %    - [3-5 bullet points cao cấp nhất]
  %  
  %  Compile: pdflatex slides_v2_fixed.tex && pdflatex slides_v2_fixed.tex
  % ============================================================

□ BÁO CÁO CUỐI CÙNG (riêng, ngoài file LaTeX):

  1. BẢNG TÓM TẮT
  | Slide | Trước (atom) | Sau (atom) | Box trước | Box sau | Status |
  |-------|--------------|------------|-----------|---------|--------|
  | 1 | ... | ... | ... | ... | ✓/⚠/✗ |
  | ... | ... | ... | ... | ... | ... |

  2. METRICS DECK-WIDE
  - Tổng box trước: 38, sau: ___ (target ≤ 22)
  - Tổng \resizebox còn lại: ___ (target = 0)
  - Tổng [shrink] còn lại: ___ (target = 0)
  - Tiếng Việt: 100% có dấu? ___

  3. WARNINGS / RỦI RO
  - Slide nào có thể overflow nếu font khác
  - Slide nào dùng synthetic data illustrative (cần data thật)
  - Slide nào còn TODO/comment chưa giải quyết

  4. SLIDE CHƯA SỬA (slides 17-30)
  Vì feedback chỉ cover slides 1-16, các slide 17-30 GIỮ NGUYÊN từ file gốc.
  Liệt kê các slide này và note "feedback đề xuất sửa thêm ở pass tiếp theo":
  - Slide 17 (SIGReg formula)
  - Slide 18 (Curse of dim)
  - Slide 19 (LeJEPA loss)
  - ... etc

  5. NEXT STEPS CHO USER
  - Compile thử: pdflatex slides_v2_fixed.tex (2 lần)
  - Replace [CHỦ-SLIDE-ĐIỀN] thành tên thật
  - Review synthetic plots và thay bằng data thật nếu có
  - Schedule pass 2 cho slides 17-30

RÀNG BUỘC:
- KHÔNG sửa nội dung slide (chỉ cosmetic + verification ở batch này)
- KHÔNG xóa slide
- File output phải compile được (mental check)
```

---

# 🎯 TIPS QUẢN LÝ BATCH

## Cho user (bạn)

1. **Sau mỗi batch:**
   - Save output Gemini vào `slides_v2_working.tex`
   - Chạy thử `pdflatex slides_v2_working.tex` để bắt lỗi compile sớm
   - Nếu có lỗi compile, paste error message vào batch tiếp theo + yêu cầu fix
   - Nếu OK, tiếp tục batch sau

2. **Nếu Gemini output sai/incomplete:**
   - Reply: "Output thiếu slide X. Re-do batch và chỉ output slide X."
   - Hoặc: "Slide X vẫn còn `\resizebox` ở dòng Y. Sửa lại."

3. **Khi lo Gemini quên context:**
   - Mỗi batch luôn paste lại files đính kèm đầy đủ
   - Đầu batch nhắc: "Đây là batch N/5, batches trước đã làm: ..."

4. **Token economy:**
   - Mỗi batch ~10-15K tokens cho prompt + ~30K cho output
   - Tổng 5 batch ~250K tokens → vừa với context window 1M của Gemini 2.5/3.x

## Cho Gemini (đã built into prompts)

- Mỗi batch giới hạn 4 slides → focus, không lan man
- Mỗi prompt liệt kê CHÍNH XÁC việc cần làm với ưu tiên (CRITICAL/HIGH/MEDIUM/LOW)
- Rõ "PASTE Y NGUYÊN" cho code đã có vs "REWRITE" cho phần cần sáng tạo
- Output format chuẩn (file + báo cáo) → dễ verify
- Ràng buộc rõ → giảm hallucination

---

# 📊 CHECKLIST TỔNG (sau 5 batch)

- [ ] Batch 0 — Setup file working + baseline audit
- [ ] Batch 1 — Slides 1-4 (Title + Paradigms + Collapse + JEPA)
- [ ] Batch 2 — Slides 5-8 (Heuristic + Pivot + Linear Probe)
- [ ] Batch 3 — Slides 9-12 (Theory Proof + Intuition + Summary)
- [ ] Batch 4 — Slides 13-16 (Random Slicing + Tests + Epps-Pulley)
- [ ] Batch 5 — Verification + Cosmetic + Report

**Sau khi xong cả 5 batch:** bạn có file `slides_v2_fixed.tex` đã sửa hoàn chỉnh slides 1-16 + báo cáo chi tiết. Slides 17-30 chưa được cover trong feedback hiện tại — cần pass 2 sau khi bạn cap tiếp các slide đó.
