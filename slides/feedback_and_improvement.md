# Feedback & Hướng Dẫn Cải Thiện — Slides LeJEPA

> **Phạm vi review:** Slides 1–4 (theo từng đợt cap màn hình của bạn).
> **Vai trò:** Thầy hướng dẫn, đọc slide với góc nhìn của khán giả lần đầu nghe paper LeJEPA.
> **Ngữ cảnh:** Bạn có ~35–40 phút trình bày cho 30 slide, nghĩa là mỗi slide chỉ ~70 giây. Hai slide đầu phải "câu" được khán giả ngay.

---

## SLIDE 1 — Title Slide

### Ấn tượng đầu tiên (10 giây đầu)
Bố cục 2 cột (text bên trái, sơ đồ bên phải) đã đúng phong cách hội nghị. Tone màu navy + sage + gold rất chuyên nghiệp, không "diêm dúa". Nhưng có một số chi tiết khiến slide chưa đạt mức "professional" mà bạn đang nhắm tới.

### Vấn đề cụ thể

#### 1. ❌ Placeholder `[Tên bạn]` còn nguyên
- File [slides_v2.tex:143](slides_v2.tex#L143) vẫn ghi `Presenter: [Tên bạn]`.
- **Hệ quả:** Đây là lỗi "amateur" thấy ngay trong 2 giây đầu — khán giả sẽ nghi ngờ phần còn lại có được kiểm tra kỹ không.
- **Cách sửa:** Thay bằng tên + đơn vị + ngày báo cáo, ví dụ:
  ```latex
  {\footnotesize Presenter: Nguyễn Văn A — Lab XYZ}\\[2pt]
  {\footnotesize\color{neutral} Seminar SSL — 05/2026}
  ```

#### 2. ⚠️ Tiêu đề "LeJEPA" chưa có "drama" đủ cho slide khai mạc
- Hiện tại "LeJEPA" cỡ `\Huge` đã to, nhưng **subtitle** "Provable & Scalable SSL / Without the Heuristics" lại bị xé thành 2 dòng `\large` + `\normalsize`, làm mất nhịp.
- **Cách sửa:** Gộp subtitle thành một dòng có dấu nhấn:
  ```latex
  {\large\itshape Provable \& Scalable SSL — Without the Heuristics}
  ```
  Ý "Without the Heuristics" chính là **thông điệp paper** — phải in nghiêng hoặc đậm, đừng cho cùng cấp với "Provable & Scalable SSL".

#### 3. ⚠️ Sơ đồ TikZ bên phải bị "lệch trọng lượng"
Quan sát từ screenshot:
- Box "Ảnh" (`lightbluebox`) và box "$f_\theta$" (`primarybox`) ở trục y = 0.
- 5 chấm tròn (embedding nodes) phân tán bên phải — nhưng **không có đường tròn/ellipse bao quanh** cho thấy đây là **distribution** $\mathcal{N}(0,I)$.
- **Hệ quả:** Khán giả nhìn 5 chấm rời rạc, KHÔNG cảm nhận được "phân phối Gaussian đẳng hướng" — đây chính là **ý chính** của paper!
- **Cách sửa:** Thêm một đường tròn `dashed` mờ bao quanh đám chấm để gợi distribution + đẩy nhãn `$\mathcal{N}(0,I)$` ra góc trên-phải:
  ```latex
  \draw[dashed, color=good!50, thick] (4.5, -0.2) circle (1.4cm);
  \node[font=\small, color=good] at (5.8, 1.2) {$\mathcal{N}(0,I)$};
  ```
  Có thể dùng `decorate` hoặc 1 đường isoline để tăng visual cue.

#### 4. ⚠️ Mũi tên từ encoder đi 5 hướng — không đồng đều
Trong [slides_v2.tex:159-163](slides_v2.tex#L159-L163), 3 mũi tên `thick` + 2 mũi tên `thin` — sự bất đối xứng này không có lý do ngữ nghĩa, dễ khiến khán giả nghĩ "có gì đó quan trọng hơn ở 3 nhánh trên".
- **Cách sửa:** Hoặc tất cả `thick`, hoặc tất cả `thin` — nhất quán. Nếu muốn nhấn ý "samples từ distribution", dùng 1 cụm chấm phân bố tự nhiên hơn (rải rác trong ellipse) thay vì 5 mũi tên phóng từ tâm.

#### 5. 💡 Takeaway "50 dòng Python" — câu chốt mạnh nhưng đặt không đúng chỗ
- Câu "*LeJEPA: chứng minh lý thuyết được, triển khai trong 50 dòng Python*" là **hook tuyệt vời** — nhưng đang nằm ở footer cỡ `\small` cùng phong cách như mọi slide khác.
- **Cách sửa:** Trên slide title, takeaway có thể được "phóng đại" hơn các slide nội dung:
  ```latex
  \begin{beamercolorbox}[sep=8pt, center, rounded=true]{block title alerted}
    \normalsize\bfseries LeJEPA: \emph{provable theory} $\cdot$ \emph{50 dòng Python}
  \end{beamercolorbox}
  ```
  Hoặc tách thành 2 vế đối xứng (chứng minh được ↔ implement được) để tạo nhịp đọc.

#### 6. 🎨 Khoảng cách dọc chưa cân
- Cụm text bên trái nén lại ở nửa trên slide, để lại khoảng trắng dưới khá lớn.
- TikZ bên phải cũng dồn quanh trục y = 0.
- **Cách sửa:** Thêm `\vfill` hoặc `\vspace*{\fill}` giữa cụm text + presenter để text "thở" hơn. Cụm `Presenter` nên cách `arXiv` ít nhất 24pt để tách nhóm "thông tin paper" và "thông tin người trình bày".

### Tổng điểm slide 1: **6.5/10**
Đã có form chuyên nghiệp, nhưng đang ở mức "good template" chứ chưa "memorable". Sửa 6 điểm trên sẽ lên ~8.5/10.

---

## SLIDE 2 — "SSL Học Từ Cấu Trúc Dữ Liệu — Không Cần Nhãn"

### Ấn tượng đầu tiên
Bố cục 3 cột (Supervised | Reconstruction | Self-Supervised) là layout cổ điển và **đúng** cho slide này. Việc 2 cột đầu dùng `\begin{block}` (xanh navy) và cột thứ 3 dùng `\begin{exampleblock}` (xanh sage) là cách phân biệt visual rất khôn ngoan — khán giả nhìn 1 giây đã hiểu "cột phải là cột chiến thắng".

Tuy nhiên, slide đang **gần đạt** chứ chưa **đạt**.

### Vấn đề cụ thể

#### 1. ❌ Tiêu đề slide quá dài + có dấu "—" không cần thiết
- Hiện: `SSL Học Từ Cấu Trúc Dữ Liệu — Không Cần Nhãn`
- **Vấn đề:** 9 từ, có "em-dash" — đọc tới giữa câu khán giả đã quên đoạn đầu. Trong screenshot thấy title bị **dồn vào header**, đọc không êm.
- **Cách sửa:** Rút gọn về 1 message:
  - Phương án A: `Ba Cách Học: Vì Sao SSL Thắng?`
  - Phương án B: `Ba Paradigm Học Máy`
  - Phương án C: `SSL: Học Từ Dữ Liệu, Không Từ Nhãn` (giữ ý gốc nhưng ngắn)

  Nhớ nguyên tắc đầu của `SLIDE_PLAN.md`: **"Mỗi slide có đúng 1 message — đặt làm `\frametitle{}`"**. Tiêu đề hiện tại đang gộp 2 message: "học từ cấu trúc" + "không cần nhãn".

#### 2. ⚠️ Cột "Self-Supervised" nội dung quá ít so với hai cột bên cạnh
Quan sát screenshot:
- Cột 1 (Supervised): `Ảnh → Nhãn` + 3 ✗
- Cột 2 (Reconstruction): `Ảnh → Ảnh` + 3 ✗
- Cột 3 (Self-Supervised): `View1 ↔ View2` + 3 ✓

Vấn đề: Đây là cột **phải nhấn mạnh** (vì là chủ đề paper), nhưng nội dung **đối xứng** với 2 cột kia → bị "ngang hàng" thay vì "vượt trội".

- **Cách sửa:** Thêm 1 dòng nhỏ phía dưới ✓ thứ 3 ở cột Self-Supervised:
  ```latex
  \textcolor{good}{\cmark}\ Scale tốt\\[3pt]
  \textbf{\color{good} ← LeJEPA ở đây}
  ```
  Hoặc dùng `\fbox` bao quanh exampleblock để nó "nổi" hơn 2 block còn lại.

#### 3. ⚠️ Hai dấu "Ảnh → Ảnh" và "View1 ↔ View2" cần ký hiệu rõ hơn
- "Ảnh → Ảnh" (Reconstruction) — ý "ảnh đầu vào dự đoán ảnh đầu ra (bị mask hoặc cùng ảnh)" — quá tóm gọn, người mới sẽ hỏi "vì sao học pixel lại tệ?".
- "View1 ↔ View2" — mũi tên 2 chiều gợi đúng ý "agreement", tốt.

- **Cách sửa cho cột Reconstruction:** đổi thành `Ảnh → Pixel` để đối lập ngữ nghĩa với "View ↔ View" (ngữ nghĩa pixel-level vs view-level). Khán giả sẽ "à" ngay.

#### 4. ⚠️ Câu phụ đề trong block không đối xứng độ dài
Đếm số ký tự dưới `\xmark`/`\cmark`:
| Cột | Phụ đề | Độ dài |
|-----|--------|--------|
| Supervised | "Cần annotation" / "Đắt, khan hiếm" / "Không scale" | 14 / 14 / 11 |
| Reconstruction | "Lãng phí vào pixel" / "Không học semantic" / "Compute cao" | 18 / 18 / 11 |
| Self-Supervised | "Tự sinh tín hiệu" / "Không cần nhãn" / "Scale tốt" | 16 / 14 / 9 |

→ Mỗi block có chiều cao **khác nhau** → 3 cột không thẳng hàng nhau ở đáy. Khi screenshot ta thấy block phải hơi "lùn" hơn. Visual không đẹp.

- **Cách sửa:**
  - Dùng `[t]` đã có ở `\begin{columns}[t]` — đã align top, OK.
  - Nhưng để align cả đáy, có thể bọc mỗi block trong `\parbox[c][2.6cm][t]{\linewidth}{...}` cố định chiều cao.
  - Hoặc thêm `\vspace*{\fill}` ở cuối các block ngắn hơn.

#### 5. ⚠️ Symbol `\xmark` / `\cmark` đứng trước text quá sát
Trong [slides_v2.tex:178-180](slides_v2.tex#L178-L180):
```latex
\textcolor{bad}{\xmark}\ Cần annotation
```
Ký tự `\` (escape space) chỉ ra 1 ký tự space — visually quá sát, đọc không thoải mái.
- **Cách sửa:** Thêm `\quad` hoặc `\;`:
  ```latex
  \textcolor{bad}{\xmark}\;Cần annotation
  ```
  Hoặc dùng `itemize` với custom label:
  ```latex
  \begin{itemize}[label=\textcolor{bad}{\xmark}, leftmargin=*]
    \item Cần annotation
    \item Đắt, khan hiếm
    \item Không scale
  \end{itemize}
  ```

#### 6. 💡 Thiếu visual cho từng paradigm
3 cột chỉ có **text**, không có icon/sketch nhỏ. Đây là slide mở đầu, **bắt buộc** phải có visual để "mỏ neo" vào trí nhớ.
- **Cách sửa:** Thêm 1 mini-TikZ ở đầu mỗi block:
  - Supervised: ảnh + nhãn "cat" gắn lên
  - Reconstruction: ảnh bị che một phần + ảnh khôi phục
  - Self-Supervised: cùng ảnh được crop 2 lần (view1, view2)

  Mỗi mini-icon chỉ 1.5cm × 1cm, đặt trên dòng `Ảnh → Nhãn`. Slide sẽ "đời" hơn nhiều.

#### 7. 💡 Takeaway có thể "đắt" hơn
- Hiện: "*SSL: AI học từ cấu trúc dữ liệu — không từ nhãn con người*"
- **Vấn đề:** Đây là câu **mô tả**, không phải câu **hook**. Khán giả nghe xong đã quên.
- **Cách sửa:** Đổi thành câu có "twist":
  - "*Annotation đắt — nhưng cấu trúc dữ liệu thì miễn phí*"
  - "*SSL: học không cần thầy — nhưng cần đúng câu hỏi*" (gợi mở slide tiếp theo về collapse)

#### 8. 🎨 Tiêu đề block bị `\centering` — có thể không render đúng
Trong [slides_v2.tex:175,183,191](slides_v2.tex#L175):
```latex
\begin{block}{\centering Supervised}
```
- **Vấn đề:** `\centering` trong title của Beamer block đôi khi gây glitch (vì title bar dùng `\setbeamertemplate{block begin}` có sẵn `\insertblocktitle` — `\centering` có thể không hoạt động hoặc làm hỏng baseline).
- **Cách sửa:** Bỏ `\centering`, để Beamer tự align. Nếu thật sự muốn center, đổi sang:
  ```latex
  \begin{block}{\hfill Supervised\hfill\null}
  ```

### Tổng điểm slide 2: **6/10**
Layout đúng, màu đúng, ý đúng — nhưng thiếu visual + tiêu đề dài + chưa "đẩy" được Self-Supervised lên vị trí ngôi sao.

---

## TỔNG KẾT 2 SLIDE ĐẦU

### Điểm mạnh chung
1. ✅ Tone màu chuyên nghiệp, đồng bộ.
2. ✅ Cấu trúc TikZ + block đã có template tốt — dễ tái sử dụng.
3. ✅ Tiếng Việt có dấu đầy đủ, đúng tinh thần `SLIDE_PLAN.md`.
4. ✅ Mỗi slide có takeaway ở footer — kỷ luật cao.

### Điểm yếu chung
1. ❌ **Placeholder chưa thay** — lỗi nhỏ nhưng "ám" cả phần còn lại.
2. ❌ **Visual chưa đủ "thoại"** — slide 1 thiếu distribution cue, slide 2 thiếu icon.
3. ❌ **Takeaway còn mô tả, chưa "câu"** — chưa tạo cảm giác "phải nghe tiếp".
4. ❌ **Tiêu đề slide 2 dài** — vi phạm quy tắc 1-message.
5. ⚠️ **Cột chiến thắng trong slide 2 chưa nổi bật** — bị xếp ngang hàng với 2 cột kia.

### Thứ tự ưu tiên sửa (nếu chỉ có 30 phút)
| # | Việc | Slide | Tác động |
|---|------|-------|----------|
| 1 | Thay `[Tên bạn]` thành tên thật | 1 | Cao (lỗi sờ thấy) |
| 2 | Rút gọn tiêu đề slide 2 còn ≤ 5 từ | 2 | Cao |
| 3 | Thêm đường tròn dashed bao đám embedding | 1 | Cao (visual hook) |
| 4 | Thêm 3 mini-icon cho 3 paradigm | 2 | Trung bình–Cao |
| 5 | Đổi takeaway slide 2 thành câu "có twist" | 2 | Trung bình |
| 6 | Đổi `Ảnh → Ảnh` → `Ảnh → Pixel` | 2 | Thấp nhưng hiệu quả |
| 7 | Bỏ `\centering` trong block title | 2 | Thấp (cosmetic) |
| 8 | Đối xứng độ dài bullet trong 3 block | 2 | Thấp |

### Lời khuyên trình bày (delivery)

**Slide 1** (~30 giây nói):
> "Hôm nay tôi giới thiệu LeJEPA — một paper SSL từ Balestriero và LeCun, vừa lên arXiv 2025. Hai điều khiến paper này đáng chú ý: (1) lần đầu tiên SSL có **chứng minh lý thuyết** rõ ràng, và (2) **toàn bộ method gói trong 50 dòng Python**. Nếu bạn từng tune DINO 7 hyperparameter, bạn sẽ thấy đây là một sự nhẹ nhõm."

**Slide 2** (~60 giây nói):
> "Trước khi vào LeJEPA, hãy nhắc lại **vì sao chúng ta cần SSL**. Có 3 cách AI học: Supervised cần label đắt và khan hiếm. Reconstruction học pixel — phí compute vào những thứ không quan trọng. Còn SSL học **bằng cách so khớp các view khác nhau của cùng một ảnh** — không cần nhãn con người. *(Chỉ vào cột phải)* Đây là paradigm mà LeJEPA, DINO, BYOL... đều thuộc về. Nhưng — slide tiếp theo — nó có một vấn đề chí mạng mà mất 5 năm cộng đồng mới giải quyết được lý thuyết."

→ Câu cuối "**slide tiếp theo**" là **bridge** — đừng quên dùng để dẫn dắt.

---

> **Khi bạn cap thêm các slide tiếp theo, tôi sẽ tiếp tục feedback theo cùng độ chi tiết này (mỗi slide ~5–8 điểm + thứ tự ưu tiên + lời khuyên delivery).**

---
---

# ĐỢT 2 — TIKZ TRONG SLIDE 3 & SLIDE 4

> **Vấn đề chung bạn nêu:** *"Các phần TikZ đều thấy không đẹp, khá lộn xộn, không có điểm nhấn."*
>
> Chuẩn xác. Đây là vấn đề **thiết kế thị giác**, không phải vấn đề LaTeX. Tôi sẽ phân tích từng TikZ rồi đưa code thay thế.

## Nguyên tắc thiết kế TikZ cho slide khoa học

Trước khi đi vào từng slide, ghi nhớ 5 nguyên tắc — bạn sẽ áp được cho **toàn bộ deck**:

1. **Focal point rule** — mỗi figure có **1 nhân vật chính**. Nhân vật chính phải lớn nhất / màu đậm nhất / ở vị trí trung tâm thị giác (rule of thirds).
2. **Contrast > Symmetry** — khi so sánh "tệ" vs "tốt", **đừng vẽ đối xứng**. Đối xứng = thông điệp "ngang nhau". Phải khiến bên "tốt" có cảm giác **khác chất** (kích cỡ khác, mật độ khác, không gian thoáng hơn, v.v.).
3. **White space is design** — TikZ kín mít = mệt. Để 30–40% diện tích là trống để mắt "thở".
4. **Arrow as narrative** — mũi tên là người dẫn chuyện. Nếu khán giả không biết đọc từ đâu → mũi tên thiết kế sai.
5. **Color = meaning, not decoration** — đỏ = xấu, xanh lá = tốt, xanh navy = neutral/chính, vàng = highlight. **Không đổi nghĩa giữa các slide.**

---

## SLIDE 3 — "Collapse Là Lý Do SSL Thường Thất Bại"

### Phân tích screenshot — vì sao "lộn xộn, không điểm nhấn"

#### Panel trái — "✗ Nghiệm tầm thường" (collapse)
- 4 box `x_1..x_4` xếp dọc, **4 mũi tên** đỏ phóng vào 1 chấm tròn `0`.
- **Vấn đề 1:** Chấm tròn `0` quá nhỏ so với 4 box nguồn → mất tính "thu hút" của collapse.
- **Vấn đề 2:** 4 mũi tên đỏ đan chéo nhau, tạo cảm giác **rối** chứ không phải **collapse**.
- **Vấn đề 3:** Caption `f(x) = hằng số` đặt **dưới** chấm `0`, font nhỏ — đọc lướt sẽ bỏ qua.
- **Vấn đề 4:** Không có dấu hiệu nào cho biết "đây là điều xấu" ngoài màu đỏ. Không có "nét gạch chéo" hay "biểu cảm tệ" để nhấn.

#### Panel phải — "✓ Mục tiêu thực" (diversity)
- 4 box `x_1..x_4` → 4 chấm xanh `z_1..z_4`.
- **Vấn đề 1:** Đây là **anti-pattern**: vẽ 1-1 mapping → **không phản ánh diversity**! 4 chấm `z` rời rạc trông giống nhau, không cho thấy chúng "phủ không gian".
- **Vấn đề 2:** Ý "đa dạng" cần được thể hiện bằng **phân bố trong không gian 2D** — chứ không phải xếp dọc.
- **Vấn đề 3:** Hai panel quá **đối xứng** về layout → não đọc thành "2 cách làm như nhau", không phải "1 cách hỏng vs 1 cách đúng".

#### Vấn đề tổng thể
| Khiếm khuyết | Hệ quả |
|--------------|--------|
| Hai panel cùng kích thước, cùng cấu trúc | Không tạo contrast |
| Cả hai đều dùng "4 hộp dọc" | Khán giả không phân biệt được nhanh |
| Không có **không gian embedding** vẽ ra | Khán giả không hiểu collapse là **về geometry**, mà tưởng là về **mapping** |
| `f(x) = hằng số` ở dưới — không đủ nhấn | Bỏ lỡ câu chốt |

### Hướng cải thiện — 3 phương án từ nhẹ đến mạnh

#### Phương án A (sửa nhẹ — giữ layout 2-panel)
Giữ 2 panel nhưng:
1. **Vẽ ellipse/region** xung quanh các điểm `z` để gợi "không gian embedding".
2. **Phóng to chấm `0` trên panel trái** + đặt nó vào **giữa một region đỏ nhỏ** (collapse vào 1 điểm).
3. **Phân bố chấm `z` trên panel phải theo 2D** — không xếp dọc nữa.
4. Thêm **biểu cảm**: panel trái có "X to" mờ phía sau, panel phải có "tick to" mờ phía sau.

```latex
% --- Panel trái: collapse ---
\begin{scope}[xshift=-3.0cm]
  % Embedding space (background)
  \draw[dashed, color=neutral!40, fill=lightred] 
    (0,0) circle (1.6cm);
  \node[font=\tiny, color=neutral, above=2pt] at (0, 1.6) 
    {không gian embedding $\mathbb{R}^K$};
  
  % 4 input boxes ở mép trái  
  \foreach \i/\y in {1/0.9, 2/0.3, 3/-0.3, 4/-0.9} {
    \node[stdbox, fill=lightred!50, draw=bad!40, 
          minimum width=0.6cm, minimum height=0.4cm,
          font=\tiny] (x\i) at (-2.6, \y) {$x_\i$};
  }
  
  % Single collapse point — LỚN, ĐẬM
  \node[circle, fill=bad, text=white, 
        minimum size=1.0cm, font=\bfseries,
        drop shadow={opacity=0.3}] (col) at (0, 0) {$\bm{c}$};
  
  % Mũi tên hội tụ (curved để gợi "bị hút vào")
  \foreach \i in {1,2,3,4} {
    \draw[->, thick, color=bad!70, opacity=0.6] 
      (x\i.east) to[bend left=10] (col.west);
  }
  
  % Caption — bự, nổi bật, đặt trên
  \node[font=\small\bfseries, color=bad, above=10pt of col] 
    {$f(x_1) = f(x_2) = \dots = c$};
\end{scope}

% --- Panel phải: diversity ---
\begin{scope}[xshift=3.0cm]
  \draw[dashed, color=neutral!40, fill=lightgreen] 
    (0,0) circle (1.6cm);
  \node[font=\tiny, color=neutral, above=2pt] at (0, 1.6) 
    {không gian embedding $\mathbb{R}^K$};
  
  % 4 z-points phân tán 2D
  \foreach \i/\px/\py in {1/-0.8/0.7, 2/0.9/0.5, 
                          3/-0.6/-0.8, 4/0.7/-0.6} {
    \node[embnode, minimum size=0.55cm] (z\i) at (\px, \py) {$z_\i$};
  }
  
  % Input boxes
  \foreach \i/\y in {1/0.9, 2/0.3, 3/-0.3, 4/-0.9} {
    \node[stdbox, fill=lightgreen!50, draw=good!40, 
          minimum width=0.6cm, minimum height=0.4cm,
          font=\tiny] (y\i) at (-2.6, \y) {$x_\i$};
  }
  
  % Mũi tên 1-1 (mảnh, không cùng màu)
  \foreach \i in {1,2,3,4} {
    \draw[->, thin, color=good!60] (y\i.east) -- (z\i.west);
  }
  
  \node[font=\small\bfseries, color=good, above=10pt of current bounding box.north, yshift=-12pt] 
    {Phân tán đều trong $\mathbb{R}^K$};
\end{scope}
```

**Đặc điểm:**
- Panel trái: vùng đỏ nhỏ + 1 điểm to → **cảm giác bị "bóp chặt"**.
- Panel phải: vùng xanh + chấm phân tán → **cảm giác "thoáng, có cấu trúc"**.
- Caption đặt phía trên (chứ không dưới) — đọc mắt chạm vào nhanh hơn.
- Mũi tên cong (`bend left`) trên panel trái cho cảm giác "hội tụ".

#### Phương án B (cải tổ — đổi layout sang 1-panel)
Bỏ cấu trúc 2-panel đối xứng, đổi thành **1 hình duy nhất** ở giữa, với 2 đường tiến hóa:

```
                    [Encoder f_θ]
                         |
                         v
              ┌──── ✗ Bad path ────┐
              |                     |
        [embedding cluster ----- > [collapse point]
                                    "f = const"
              |
              └──── ✓ Good path ────┐
                                     |
                                  [spread distribution]
                                  "f ~ N(0,I)"
```

Layout này có lợi:
- Không có đối xứng → contrast mạnh hơn.
- Ánh mắt đi theo 1 dòng kể chuyện rõ ràng.

#### Phương án C (mạnh nhất — minh họa "geometric collapse")
Vẽ **không gian embedding như một plane 2D**, với:
- **Trạng thái 1 (xấu):** tất cả `z_i` nằm chồng lên nhau ở 1 điểm (vẽ chấm to + label "$z_1=z_2=z_3=z_4$").
- **Trạng thái 2 (tốt):** `z_i` phân tán trong 1 vùng tròn lớn.

Hiển thị 2 trạng thái **kế tiếp nhau** với mũi tên `\Rightarrow` ở giữa, kèm caption "**Bài toán:** ngăn không cho rơi vào trạng thái trái".

**Khi nào dùng phương án nào?**
- Lớp học cơ bản → A (giữ ngữ cảnh quen).
- Workshop/seminar chuyên sâu → C (đậm geometry).
- Demo nhanh → B.

### Takeaway hiện tại OK, không cần sửa
*"Cần ràng buộc chống collapse — nhưng ràng buộc NÀO là đúng?"* — câu này tốt vì đã **bridge sang slide pivot question**.

---

## SLIDE 4 — "JEPA Học Trạng Thái Trừu Tượng — Không Phải Pixel"

### Phân tích screenshot — vì sao TikZ "lộn xộn"

#### Bố cục pipeline hiện tại
```
view 1 → f_θ → z_1 ────────────→ so sánh
                                     ↑
view 2 → f_θ → z_2 → Dự báo → ẑ_1 ──┘
        (chia sẻ)
```

#### Các vấn đề cụ thể

1. **❌ Mũi tên "ngược chiều đọc":** `ẑ_1` ở góc dưới-phải, đi mũi tên **ngược lên** đến `so sánh` ở góc trên-phải → mắt phải **đảo ngược** hướng đọc. Não diễn giải sai thành "loop".

2. **❌ Box "so sánh" tách biệt khỏi pipeline:** Nó chỉ kết nối với hàng dưới qua mũi tên ngược, không có chỗ neo rõ ràng → trông như **box mồ côi**.

3. **❌ "chia sẻ" label nhỏ + nằm bên trái dấu ngoặc:** Decoration `brace` được dùng nhưng quá nhỏ — khán giả ngồi xa **không đọc được**. Đây là **thông điệp quan trọng** (encoder chia sẻ trọng số) mà bị "giấu".

4. **❌ Không có ảnh gốc:** "view 1", "view 2" được hiểu là 2 crop của **cùng 1 ảnh** — nhưng slide không vẽ ảnh gốc → khán giả mới không hiểu.

5. **❌ Box màu lộn xộn:**
   - `view 1, view 2` — `lightbluebox` (xanh nhạt)
   - `f_θ` — `primarybox` (navy)
   - `z_1, z_2, ẑ_1` — `accentbox` (vàng)
   - `so sánh` — `goodbox` (xanh lá)
   - `Dự báo` — `neutralbox` (xám)
  
   → **5 màu cho 6 loại box** = quá nhiều. Não phải decode "vàng nghĩa là gì? xanh lá nghĩa là gì?" → mệt.

6. **❌ Pipeline bị nén ngang:** Cột TikZ chỉ chiếm 57% slide, nhưng chứa pipeline **7 box + 7 mũi tên** → mọi thứ chen chúc, font `\tiny`.

7. **⚠️ "Dự báo" và "so sánh" đứng riêng:** Hai khái niệm này là **trái tim** của JEPA (predictability + invariance) nhưng đang bị visual treatment **bằng nhau** với encoder/view → mất focal point.

### Hướng cải thiện

#### Bước 1 — Tái cấu trúc layout: thêm "ảnh gốc" + duỗi pipeline

```
            ┌──── view 1 ──── f_θ ──── z_1 ────┐
[ảnh gốc x] ┤                                   ╞══ so sánh ══ Loss
            └──── view 2 ──── f_θ ──── z_2 ──── predictor ──── ẑ
                                ⇡ chia sẻ trọng số ⇡
```

Lợi ích:
- **Ảnh gốc** ở đầu → câu chuyện rõ: "1 ảnh → 2 view → 2 embedding → so sánh".
- Pipeline duỗi ngang, không có mũi tên ngược.
- "so sánh" giờ là **node tổng** ở phải → focal point rõ.

#### Bước 2 — Giảm số màu xuống 3

| Loại node | Màu | Ý nghĩa |
|-----------|-----|---------|
| Input/data (`ảnh`, `view`) | `lightbluebox` | dữ liệu |
| Function (`f_θ`, `predictor`) | `primarybox` | mô hình |
| Output/embedding (`z_1`, `z_2`, `ẑ`) | `accentbox` | latent |
| Loss (`so sánh`) | `goodbox` (đậm hơn các loại trên) | mục tiêu |

Bỏ `neutralbox` cho "Dự báo" — đổi thành `primarybox` để cùng class với encoder.

#### Bước 3 — Code TikZ thay thế

```latex
\begin{tikzpicture}[every node/.style={font=\scriptsize}, scale=0.95]
  % Ảnh gốc — nhân vật mở đầu
  \node[lightbluebox, minimum width=0.9cm, minimum height=0.9cm,
        align=center] (img) at (0, 0) {Ảnh\\gốc $x$};
  
  % 2 views (crop khác nhau)
  \node[lightbluebox, minimum width=0.85cm, minimum height=0.5cm] 
    (v1) at (1.6, 0.7) {view 1};
  \node[lightbluebox, minimum width=0.85cm, minimum height=0.5cm] 
    (v2) at (1.6,-0.7) {view 2};
  
  % Encoder shared — VẼ 1 BOX TO bao 2 encoder
  \node[primarybox, minimum width=0.85cm, minimum height=0.5cm] 
    (e1) at (3.0, 0.7) {$f_\theta$};
  \node[primarybox, minimum width=0.85cm, minimum height=0.5cm] 
    (e2) at (3.0,-0.7) {$f_\theta$};
  
  % Background bao 2 encoder để gợi "shared"
  \begin{pgfonlayer}{background}
    \node[draw=neutral!50, dashed, rounded corners,
          fit=(e1)(e2), inner sep=4pt,
          fill=neutral!8] (shared) {};
  \end{pgfonlayer}
  \node[font=\tiny\itshape, color=neutral, above=1pt of shared.north] 
    {chia sẻ trọng số};
  
  % Embeddings
  \node[accentbox, minimum width=0.7cm, minimum height=0.5cm] 
    (z1) at (4.5, 0.7) {$z_1$};
  \node[accentbox, minimum width=0.7cm, minimum height=0.5cm] 
    (z2) at (4.5,-0.7) {$z_2$};
  
  % Predictor (chỉ trên 1 nhánh)
  \node[primarybox, minimum width=0.9cm, minimum height=0.5cm] 
    (pred) at (5.9,-0.7) {predictor};
  \node[accentbox, minimum width=0.6cm, minimum height=0.5cm] 
    (zh) at (7.1,-0.7) {$\hat{z}_1$};
  
  % Loss — node TO ở giữa-phải, là focal point
  \node[goodbox, minimum width=1.1cm, minimum height=1.0cm,
        font=\small\bfseries, align=center,
        fill=good!60, text=white, draw=good] 
    (loss) at (8.4, 0) {Loss};
  
  % Mũi tên — hàng trên
  \draw[->, thick, primary] (img.east) -- (v1.west);
  \draw[mainarrow] (v1) -- (e1);
  \draw[mainarrow] (e1) -- (z1);
  \draw[mainarrow, color=good] (z1.east) -- (loss.north west);
  
  % Mũi tên — hàng dưới
  \draw[->, thick, primary] (img.east) -- (v2.west);
  \draw[mainarrow] (v2) -- (e2);
  \draw[mainarrow] (e2) -- (z2);
  \draw[mainarrow] (z2) -- (pred);
  \draw[mainarrow] (pred) -- (zh);
  \draw[mainarrow, color=good] (zh.east) -- (loss.south west);
\end{tikzpicture}
```

**Khác biệt chính so với phiên bản cũ:**
- ✅ Pipeline đi **1 chiều** từ trái sang phải, không có mũi tên ngược.
- ✅ "Loss" là **focal point** ở phải (to nhất, đậm nhất, là điểm hội tụ).
- ✅ Box `fit` (background neutral) bao 2 encoder → "shared" được biểu đạt **bằng visual**, không cần label `brace` nhỏ.
- ✅ Ảnh gốc xuất hiện → câu chuyện đầy đủ.
- ✅ Chỉ 4 màu (data / model / latent / loss) — đỡ rối.

#### Bước 4 — Xử lý 2 block bên phải

Hai block `2 Nguyên Tắc` và `JEPA vs LLM` đang đè dọc — OK về thông tin nhưng phía bên phải nhìn **nặng** hơn TikZ.

**Cách sửa:**
- Bỏ block `JEPA vs LLM` ra khỏi slide này → đẩy thành **slide riêng** (so sánh JEPA vs reconstruction model là chủ đề đủ lớn).
- Slide này chỉ giữ block `2 Nguyên Tắc` ở phải — và phóng to lên `\footnotesize` thay vì `\tiny`.
- Hoặc: gộp 2 nguyên tắc vào TikZ luôn (label trên 2 nhánh):
  - Nhánh trên: `Invariance — z_1 ≈ ẑ_1`
  - Nhánh dưới: `Predictability — predictor`

#### Bước 5 — Caption "JEPA vs LLM" nếu giữ lại

Block này hiện viết:
> ✗ LLM: dự báo pixel → lãng phí vào nhiễu  
> ✓ JEPA: dự báo trạng thái → học cấu trúc ngữ nghĩa

**Lỗi học thuật nhỏ:** LLM (Large Language Model) **không** dự báo pixel — LLM dự báo token. Bạn đang nhầm với **AR pixel models** (PixelCNN, ImageGPT) hoặc **diffusion**.

**Sửa lại:**
> ✗ Pixel models (MAE, PixelCNN): dự báo pixel → lãng phí compute  
> ✓ JEPA: dự báo trạng thái latent → học cấu trúc ngữ nghĩa

(Đây là lỗi nội dung, **bắt buộc sửa** — nếu bạn báo cáo cho academic audience, sẽ có người hỏi "LLM dự báo pixel ở đâu?" và bạn lúng túng.)

### Takeaway hiện tại — chấp nhận được nhưng có thể đắt hơn

Hiện: *"JEPA học 'thế giới thay đổi thế nào', không học 'pixel trông như thế nào'"*

**Phân tích:** Câu này dùng đối lập "thế giới thay đổi thế nào" / "pixel trông như thế nào" — hay nhưng dài. Có thể rút:

- *"JEPA: học **ngữ nghĩa**, bỏ qua **pixel**"* (ngắn, đối xứng).
- *"Pixel là rác — cấu trúc latent là vàng"* (mạnh hơn, hơi 'spicy').

---

## TỔNG KẾT TIKZ — CHECKLIST 7 ĐIỂM

Áp dụng cho **mọi TikZ còn lại trong deck** (tôi sẽ check lại khi bạn cap thêm):

| # | Tiêu chí | Slide 3 hiện tại | Slide 4 hiện tại |
|---|----------|------------------|------------------|
| 1 | Có 1 focal point rõ? | ❌ (chấm `0` quá nhỏ) | ❌ (`Loss`/`so sánh` không nổi) |
| 2 | Mũi tên đi 1 chiều? | ✓ | ❌ (`ẑ_1 → so sánh` ngược) |
| 3 | ≤ 4 màu node? | ✓ (3 màu) | ❌ (5 màu) |
| 4 | Khoảng trống ≥ 30%? | ⚠️ (2 panel chen) | ❌ (pipeline dồn) |
| 5 | Contrast giữa "good" và "bad"? | ❌ (đối xứng quá) | N/A |
| 6 | Caption ≥ `\footnotesize`? | ❌ (`\tiny`) | ❌ (`\tiny`) |
| 7 | Tránh decoration nhỏ (`brace`, label cong)? | ✓ | ❌ (brace `chia sẻ` không đọc được) |

### Quy tắc vàng khi vẽ TikZ cho slide

> **"Nếu screenshot slide rồi xem trên điện thoại, mọi thứ phải vẫn đọc được."**

Nếu font `\tiny` thì điện thoại **không đọc nổi**. Quy ước cho deck này:
- Label trong node: **tối thiểu `\scriptsize`**, ưu tiên `\footnotesize`.
- Label trên mũi tên: **tối thiểu `\scriptsize`**.
- Caption dưới figure: **`\footnotesize`** trở lên.
- Chỉ dùng `\tiny` cho **legend/sublabel phụ** (đơn vị trục, chú thích nhỏ).

### Thứ tự ưu tiên sửa (nếu chỉ có 1 buổi sửa TikZ)

| # | Slide | Việc | Tác động |
|---|-------|------|----------|
| 1 | 4 | Xóa mũi tên ngược, gom `Loss` thành focal point | **Rất cao** |
| 2 | 4 | Sửa "LLM dự báo pixel" → "Pixel models dự báo pixel" | **Rất cao** (lỗi học thuật) |
| 3 | 3 | Vẽ ellipse/region làm "không gian embedding" cho 2 panel | Cao |
| 4 | 3 | Phân bố `z_i` 2D thay vì xếp dọc | Cao |
| 5 | 4 | Phóng to label `chia sẻ` + dùng `fit` background thay brace | Cao |
| 6 | 4 | Giảm 5 màu node xuống 4 | Trung bình |
| 7 | 3 | Phóng to chấm collapse + để caption $f=$const phía trên | Trung bình |
| 8 | 3,4 | Đổi mọi label `\tiny` thành `\scriptsize` | Thấp nhưng dễ |

---

> **Cap tiếp các slide còn lại đi — tôi sẽ feedback theo cùng độ chi tiết, đặc biệt soi kỹ TikZ vì đó là điểm yếu lớn nhất hiện tại của deck.**

---
---

# ĐỢT 3 — SLIDE 5 & SLIDE 6 (đặc biệt slide 6: quá nhiều chữ + diagram lan man)

> **Nhận xét của bạn:** *"Slides 6 quá nhiều chữ, còn diagram không cô đọng, các box cũng nhiều nội dung."*
>
> Hoàn toàn chính xác. Bằng chứng kỹ thuật: trong code có `[shrink=5]` ở [slides_v2.tex:329](slides_v2.tex#L329) — đây là **lệnh ép Beamer co text** vì nội dung tràn slide. Đây là **mùi hôi (code smell)** rất rõ — không bao giờ nên dùng `shrink` trong slide đã hoàn thiện.

---

## SLIDE 5 — "Heuristic Stack: Mỗi Phương Pháp Vá Một Lỗ — Không Có Nền Tảng"

### Phân tích screenshot

#### Điểm mạnh
- ✅ Bảng `booktabs` (toprule/midrule/bottomrule) đúng phong cách academic.
- ✅ Cột "Hạn chế" highlight `bad!20` — visual rất rõ, mắt chạy thẳng vào "vấn đề".
- ✅ Mỗi method được tóm gọn 1 dòng — đúng tinh thần "1 message".
- ✅ 5 method = số lẻ, đẹp về thẩm mỹ (không bị "bệnh số chẵn").

#### Vấn đề

##### 1. ⚠️ Tiêu đề slide quá dài — vi phạm quy tắc 1-message
- Hiện: `Heuristic Stack: Mỗi Phương Pháp Vá Một Lỗ — Không Có Nền Tảng`
- **Vấn đề:** 11 từ, 2 mệnh đề (1 trước dấu hai chấm, 2 sau em-dash). Đây là 2-3 message gộp.
- **Cách sửa:**
  - Phương án A: `Vì Sao SSL Trước LeJEPA Là "Whac-A-Mole"` (giữ metaphor từ comment trong code)
  - Phương án B: `Heuristic Stack: Vá Lỗ, Không Có Lý Thuyết`
  - Phương án C: `5 Method, 5 Hạn Chế Khác Nhau` (rất ngắn, dùng số để câu)

##### 2. ⚠️ Bố cục dồn về phía trên — khoảng trắng dưới quá lớn
Trong screenshot: bảng kết thúc ở khoảng giữa slide, takeaway ở đáy → vùng giữa **trống lớn**.
- **Cách sửa:** Phóng `\arraystretch{1.3}` để giãn dòng:
  ```latex
  \renewcommand{\arraystretch}{1.3}
  ```
  Hoặc thêm 1 hàng tổng kết "**LeJEPA**" ở cuối bảng (highlight xanh) để **khẳng định contrast**:
  ```latex
  \midrule
  \rowcolor{good!15}
  \textbf{LeJEPA} & \textbf{1 theorem (iso Gaussian)} & \textcolor{good}{\cmark}\;Provable \\
  \bottomrule
  ```
  → Lúc này bảng có 6 hàng (5 đỏ + 1 xanh), khán giả thấy ngay "đây là kẻ thay thế".

##### 3. ⚠️ Cột "Cơ chế chống collapse" có 2 dòng cho VICReg — không đối xứng
"Làm trắng phương sai (whitening)" bị wrap thành 2 dòng → bảng cao không đều.
- **Cách sửa:** rút gọn còn `Whitening (variance)` hoặc `Decorrelate phương sai` — 1 dòng, đỡ nhảy.

##### 4. 💡 Thêm cột "# Hyperparameters" sẽ tạo punchline mạnh hơn
Hiện chỉ 3 cột, có thể thêm cột thứ 4 đếm số hyperparameter:

| Phương pháp | Cơ chế | # HP | Hạn chế |
|---|---|---|---|
| SimCLR | Negatives | 3 | $\mathcal{O}(N^2)$ |
| BYOL | Asym. arch | 5 | Không lý thuyết |
| DINO | Teacher-student | **7+** | $>$5 hyperparam |
| VICReg | Whitening | 4 | Under-specified |
| I-JEPA | Mask + stop-grad | 5 | Chỉ ViT |
| **LeJEPA** | **Iso Gaussian** | **1** | — |

Cột # HP sẽ làm con số `1` của LeJEPA trở thành **focal point** của slide.

##### 5. 💡 Takeaway ổn nhưng có thể "đắt" hơn
Hiện: *"Không có framework nào từ first principles — chỉ là empirical patches"*

Tốt rồi nhưng dài. Có thể:
- *"5 phương pháp, 5 cách vá — không phương pháp nào có lý thuyết"*
- *"Mỗi heuristic vá 1 lỗ — và tạo lỗ mới"*

### Tổng điểm slide 5: **7.5/10**
Slide đơn giản, hiệu quả. Chỉ cần thêm hàng LeJEPA và rút gọn tiêu đề là lên 9/10.

---

## SLIDE 6 — "Câu Hỏi Thay Đổi Mọi Thứ" 🚨 *Slide có vấn đề lớn nhất tới giờ*

### Chẩn đoán: tại sao slide này "quá nhiều chữ"

Đếm "atom thông tin" trên slide:

| Vùng | Nội dung | Số atom |
|------|----------|---------|
| Block "Cách tiếp cận cũ" | Tiêu đề + 1 câu hỏi + 1 caption + 3 bullet | **6** |
| Block "Câu hỏi LeJEPA" | Tiêu đề + 1 câu hỏi + 1 caption + 3 bullet | **6** |
| TikZ — cột chính | "Prevent Collapse" → "Distribution Tối Ưu?" → "$\mathcal{N}(0,I)$ Optimal" | **3** |
| TikZ — 3 axioms phải | "Giải bài toán dự báo (cũ)", "Enforce iso Gaussian (MỚI)", "Không thêm gì khác" | **3** |
| TikZ — labels mũi tên | "đổi góc nhìn", "Theorem 3.3" | **2** |
| Footer | takeaway | **1** |
| **Tổng** | | **21 atom** |

**Quy tắc thumb:** Một slide nên có **≤ 7 atom** để khán giả xử lý trong 70 giây. Slide này **gấp 3 lần ngưỡng**.

→ Đó là lý do `[shrink=5]` đã được dùng — nhưng shrink chỉ làm slide **đọc khó hơn**, không làm thông tin **ít đi**.

### Vấn đề cụ thể trong screenshot

#### 1. ❌ Hai block bên trái duplicate cấu trúc với TikZ bên phải
Quan sát kỹ:
- Block "Cách tiếp cận cũ" nói: vấn đề cũ ("tránh collapse"), 3 ✗
- Block "Câu hỏi LeJEPA" nói: hướng mới ("distribution tối ưu"), 3 ✓
- TikZ phải nói: vấn đề cũ → câu hỏi mới → kết quả

→ **Cùng 1 thông điệp được kể 2 lần, bằng 2 phương tiện khác nhau (text + diagram).** Đây là lỗi **redundancy** — đáng lẽ chọn 1 trong 2.

#### 2. ❌ TikZ phải vừa là "câu chuyện chính" vừa thêm "3 axiom phụ"
Diagram này cố nhồi:
- **Câu chuyện chuyển paradigm** (Prevent → Pivot → N(0,I))
- **3 nguyên tắc thiết kế** (3 box phải)

Hai chủ đề này khác nhau. 3 axiom là chủ đề của **slide tiếp theo** (slide 7+ về linear probe / theorems) — không phải slide pivot question.

#### 3. ❌ Các box có content quá dài, font phải nhỏ
Box "Prevent Collapse" — chữ trắng trên nền đỏ, font `\footnotesize`.
Box "Distribution Tối Ưu?" — 2 dòng, đặt câu hỏi.
3 box phải — `\tiny` text, mỗi box 2 dòng.

→ Bố cục không có **cấp bậc** rõ. "Distribution Tối Ưu?" lẽ ra là **focal point lớn nhất** của slide, nhưng bị 3 box phụ "ăn theo" làm loãng.

#### 4. ❌ Mũi tên `to[out=0,in=180]` đến 3 axiom — visual rối
3 mũi tên cong từ "$\mathcal{N}(0,I)$ Optimal" sang 3 axiom phải tạo cảm giác **chùm dây điện**.

#### 5. ⚠️ Label "đổi góc nhìn" (font tiny, italic) nằm trên mũi tên dashed — gần như không đọc được

### Hướng cải thiện — 2 phương án

#### Phương án A — TÁCH THÀNH 2 SLIDE (khuyến nghị mạnh)

**Slide 6a — "Đổi câu hỏi" (text-driven, dramatic)**

Layout: full-slide, 2 panel **trên-dưới** (không trái-phải):

```
┌─────────────────────────────────────────────────────┐
│   PANEL TRÊN (đỏ, nhỏ):                             │
│   ✗ Câu hỏi cũ:                                     │
│      "Làm sao TRÁNH collapse?"                      │
│   → 5 năm vá lỗ, không có lý thuyết                 │
│                                                      │
│        ⇩  (mũi tên to ở giữa)                       │
│                                                      │
│   PANEL DƯỚI (xanh, lớn):                           │
│   ✓ Câu hỏi mới:                                    │
│      "Distribution NÀO là tối ưu?"                  │
│   → Giải từ gốc, có theorem                         │
└─────────────────────────────────────────────────────┘
```

Slide này **không có TikZ phức tạp** — chỉ 2 câu hỏi đối lập. Đó mới là tinh thần "*câu hỏi thay đổi mọi thứ*".

**Slide 6b — "3 nguyên tắc của LeJEPA" (diagram-driven)**

Tách phần TikZ + 3 axiom thành slide riêng:

```
                  LeJEPA
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   1. Solve     2. Enforce   3. Add
   prediction   iso          nothing
   (cũ)         Gaussian     else
                (MỚI ★)
```

→ 1 message, 1 diagram, 1 takeaway. Sạch sẽ.

#### Phương án B — GIỮ 1 SLIDE NHƯNG CẮT GỌT MẠNH

Nếu không thể tách (do giới hạn 30 slide), cắt như sau:

**Bỏ:**
- ❌ 3 bullet trong mỗi block (`Không có lý thuyết nền`, `Định lý rõ ràng`, ...) — đã được nói ở slide 5 (heuristic stack) và slide 11 (theory summary). **Trùng lặp**.
- ❌ 3 axiom phụ trong TikZ — đẩy sang slide khác.
- ❌ Label "đổi góc nhìn" trên mũi tên — không cần thiết.

**Giữ:**
- ✅ 2 block đối lập (`Cách tiếp cận cũ` vs `Câu hỏi LeJEPA`) — chỉ giữ **câu hỏi**, bỏ bullet.
- ✅ TikZ chính 3 node (Prevent → Pivot → Optimal) — giữ.

**Code rút gọn:**

```latex
\begin{frame}{Câu Hỏi Thay Đổi Mọi Thứ}
\begin{columns}[c]
\column{0.45\textwidth}
  \begin{alertblock}{Cách tiếp cận cũ (5 năm)}
    \large
    \textcolor{bad}{\xmark}\;\textit{``Làm sao \textbf{tránh} collapse?''}
    \\[8pt]
    \footnotesize\color{neutral}
    → Vá empirically từng method
  \end{alertblock}
  \vspace{12pt}
  \begin{exampleblock}{Câu hỏi LeJEPA (2025)}
    \large
    \textcolor{good}{\cmark}\;\textit{``Distribution \textbf{nào} là tối ưu?''}
    \\[8pt]
    \footnotesize\color{neutral}
    → Giải từ first principles
  \end{exampleblock}
\column{0.50\textwidth}
  \centering
  \begin{tikzpicture}[every node/.style={font=\small}]
    \node[badbox, minimum width=3.6cm, minimum height=1.2cm,
          align=center, font=\footnotesize]
      (old) at (0, 2.0) {Prevent\\Collapse};
    \node[primarybox, minimum width=4.0cm, minimum height=1.4cm,
          align=center, font=\bfseries]
      (pivot) at (0, 0) {Distribution\\Tối Ưu?};
    \node[goodbox, minimum width=3.6cm, minimum height=1.2cm,
          align=center, font=\footnotesize]
      (new) at (0,-2.0) {$\mathcal{N}(\mathbf{0},I)$\\Provably Optimal};
    \draw[->, very thick, dashed, color=neutral] 
      (old) -- (pivot);
    \draw[->, very thick, color=good] 
      (pivot) -- node[right=4pt, font=\scriptsize, color=good]
      {Theorem 3.3} (new);
  \end{tikzpicture}
\end{columns}
\takeaway{Đổi câu hỏi: ``tránh collapse'' $\to$ ``đạt distribution tối ưu''}
\end{frame}
```

**Atom đếm sau khi cắt:** 2 (block) + 3 (TikZ node) + 1 (label theorem) + 1 (takeaway) = **7 atom**. **Đạt ngưỡng**.

**Khác biệt:**
| Trước | Sau |
|-------|-----|
| 21 atom | **7 atom** |
| `[shrink=5]` | Không cần shrink |
| 3 phông cỡ (\tiny/\footnotesize/\large) | 2 phông (\footnotesize/\large) |
| TikZ 7 node + 5 mũi tên | TikZ **3 node + 2 mũi tên** |
| Block dài 5 dòng | Block **2 dòng** (chỉ câu hỏi) |

### Tổng điểm slide 6 hiện tại: **4.5/10** — Cần cải tổ trước khi báo cáo

---

## NHỮNG QUY TẮC RÚT RA TỪ SLIDE 6

### Quy tắc "đếm atom"

> **Trước khi commit 1 slide, đếm số atom (mỗi câu/bullet/node TikZ/label = 1 atom).**
>
> - **≤ 5 atom**: Slide quá thoáng, có thể gộp với slide khác.
> - **6–8 atom**: ✅ Vùng an toàn cho 70 giây nói.
> - **9–12 atom**: ⚠️ Nhiều, cần `\footnotesize` xuyên suốt và kỷ luật khi nói.
> - **13+ atom**: ❌ **Tách slide hoặc cắt nội dung.**

### Quy tắc "không redundancy"

> **Nếu một thông điệp đã được kể bằng diagram, KHÔNG kể lại bằng bullet — và ngược lại.**

Slide 6 vi phạm: 2 block bên trái lặp lại nội dung TikZ bên phải. Khi review slide, hỏi:
> *"Nếu tôi xóa block này, khán giả vẫn hiểu ý không?"*

Nếu **có** → bỏ block đó.

### Quy tắc "shrink = mùi hôi"

> **Bất kỳ slide nào dùng `[shrink]`, `\resizebox`, `\scalebox` để fit content vào slide đều là tín hiệu CONTENT QUÁ NHIỀU — không phải vấn đề kỹ thuật.**

Tìm trong toàn bộ deck:
```bash
grep -n "shrink\|resizebox\|scalebox" slides_v2.tex
```

Mỗi match là 1 slide cần xem xét lại nội dung.

---

## CẬP NHẬT BẢNG ƯU TIÊN SỬA TỔNG THỂ (Slides 1–6)

| # | Slide | Việc | Tác động |
|---|-------|------|----------|
| 1 | 1 | Thay `[Tên bạn]` thành tên thật | Cao |
| 2 | **6** | **Tách slide 6 thành 2 slide HOẶC cắt 14 atom xuống 7** | **Rất cao** |
| 3 | 4 | Sửa "LLM dự báo pixel" → "Pixel models" | **Rất cao** (lỗi học thuật) |
| 4 | 4 | Sửa mũi tên ngược `ẑ_1 → so sánh` | Rất cao |
| 5 | 5 | Thêm hàng "LeJEPA" vào bảng để tạo contrast | Cao |
| 6 | 3 | Vẽ ellipse "không gian embedding" | Cao |
| 7 | 3 | Phân bố `z_i` 2D thay vì xếp dọc | Cao |
| 8 | 1 | Đường tròn dashed bao đám embedding + label `N(0,I)` | Cao |
| 9 | 2 | Rút tiêu đề slide còn ≤ 5 từ + thêm icon | Trung bình |
| 10 | 5 | Rút tiêu đề slide còn ≤ 6 từ | Trung bình |
| 11 | 4 | Bỏ `JEPA vs LLM` block sang slide khác | Trung bình |
| 12 | All | Đổi label `\tiny` thành `\scriptsize` | Thấp nhưng dễ |

---

> **Slide 6 là slide quan trọng nhất của Phần 1 (đặt câu hỏi pivot) — nếu khán giả không "thông" ở đây, toàn bộ Phần 2 (theory) sẽ vô nghĩa.** 
> 
> Phải dành thời gian đầu tư cho slide này nhiều nhất.
> 
> Cap tiếp các slide sau, tôi sẽ tiếp tục feedback.

---
---

# ĐỢT 4 — SLIDE 7 & SLIDE 8 + VẤN ĐỀ HỆ THỐNG: "BOX EVERYWHERE"

> **Nhận xét của bạn (rất chính xác):**
> - Slide 7: *"Box quá nhiều nội dung, đọc dễ choán, 2 box choán slide quá nhiều."*
> - Slide 8: *"Tiêu đề figure lệch phải, legend che figure."*
> - Tổng: ***"Nên hạn chế box không cần thiết xuyên suốt slides."***
>
> **Bằng chứng kỹ thuật:** Đếm số block trong toàn deck:
> ```
> grep -c "begin{block}\|begin{alertblock}\|begin{exampleblock}" slides_v2.tex
> → 38 block trên 30 slide ≈ 1.27 box/slide
> ```
> → Trung bình mỗi slide có hơn 1 box. Nhiều slide có 2-3 box. Đây là **box-driven design** — phong cách phổ biến nhưng đã lỗi thời (thấy trong template Beamer mặc định 2010s). Modern academic decks (Metropolis, Berkeley CS theme) **dùng box rất ít**.

---

## VẤN ĐỀ HỆ THỐNG — VÌ SAO "TOO MANY BOXES" LÀ XẤU?

### 1. Box thêm "frame" thị giác mà không thêm thông tin
Mỗi `\begin{block}{Title}` vẽ:
- 1 thanh tiêu đề (navy đậm)
- 1 vùng nền (xám/xanh nhạt)
- 1 padding ~6pt 4 phía

→ Khán giả phải xử lý: "đây là gì? tiêu đề nói gì? nội dung nói gì?". Mỗi box là **1 đơn vị nhận thức**.

### 2. Khi mọi thứ là box, không có gì là điểm nhấn
Visual hierarchy = **vài thứ nổi bật** trên nền **nhiều thứ phẳng**. Khi mọi định nghĩa, ví dụ, kết luận đều ở trong box → não không biết cái nào quan trọng hơn cái nào.

### 3. Box "ăn" diện tích slide
1 block có padding ~12pt và title bar ~16pt → **mất ~28pt chiều cao** chỉ cho "chrome". Slide 16:9 cao ~430pt. **2 box/slide = 56pt = 13% diện tích đi vào trang trí.**

### 4. Box ép cấu trúc cứng nhắc
Khi đã đặt nội dung vào `\begin{block}`, bạn buộc phải có tiêu đề. Đôi khi nội dung không cần tiêu đề — nhưng box vẫn ép phải có.

### Khi nào DÙNG box, khi nào KHÔNG?

**Dùng box khi:**
- ✅ Nội dung là **theorem/definition/lemma** chính thống → cần "frame" để khán giả biết "đây là statement formal".
- ✅ Cần **highlight 1 cụm thông tin** giữa 1 slide chủ yếu là text/figure.
- ✅ Slide phức tạp cần **chia vùng** rõ ràng (vd: 4-quadrant layout).

**KHÔNG dùng box khi:**
- ❌ Toàn bộ slide chỉ có 2-3 cụm text → không cần box, dùng heading text + bullet.
- ❌ 1 figure + 1 caption — box đè lên figure làm rối.
- ❌ "Tôi muốn slide có cấu trúc" — đó là lý do bạn dùng `\begin{columns}`, không phải `\begin{block}`.
- ❌ Slide đã có TikZ phức tạp — thêm box = tax thị giác.

---

## SLIDE 7 — "Framework: Đánh Giá Qua Linear Probe Ridge Regression"

### Phân tích screenshot

#### Cấu trúc hiện tại
```
┌─ Equation ridge regression (centered) ─┐
└─────────────────────────────────────────┘
┌── alertblock ──┐  ┌── exampleblock ──┐
│ ✗ Anisotropic  │  │ ✓ Isotropic       │
│  - Eigenvalues │  │  - Eigenvalues    │
│  - Formula     │  │  - Formula        │
│  - ⇒ point 1   │  │  - ⇒ point 1      │
│  - ⇒ point 2   │  │  - ⇒ point 2      │
│  - Hệ quả:     │  │  - Hệ quả:        │
│    - Bias cao  │  │    - Bias thấp    │
│    - Var cao   │  │    - Var thấp     │
└────────────────┘  └────────────────────┘
[takeaway]
```

#### Vấn đề (đúng như bạn nhận xét)

##### 1. ❌ Mỗi box có **6 atom** thông tin — quá tải
Mỗi block chứa: tiêu đề + 1 dòng eigenvalues + 1 formula + 2 implications + 2 hệ quả = **6 atom**. Hai block = **12 atom** + equation đỉnh = **13 atom** chỉ cho phần nội dung.

→ Khi khán giả nhìn vào, mắt nhảy giữa 2 box, đọc tới đâu quên tới đó.

##### 2. ❌ Box chiếm ~70% diện tích slide
Equation top + 2 box → push takeaway xuống dưới đáy. Không có "không khí". Slide cảm giác **chật**.

##### 3. ❌ Cấu trúc 2 box đối xứng — đẹp về visual nhưng SAI về thông điệp
Cả 2 box đều `block` với formula + ⇒ + Hệ quả → khán giả nghĩ "anisotropic và isotropic là 2 lựa chọn ngang nhau, đang cân nhắc chọn cái nào".

**Thực tế:** Bạn muốn nói "**isotropic > anisotropic**, và đây là lý do". Box phải **không đối xứng**.

##### 4. ❌ Equation top dùng `\Large` nhưng underbraces `\text{prediction error}` lại nhỏ
Format underbrace `\underbrace{...}_{\text{...}}` thường hiển thị tag dưới cỡ nhỏ — kết hợp với `\Large` thành mismatch font.

### Hướng cải thiện — phương án "ít box hơn"

**Cấu trúc mới:** thay 2 alertblock/exampleblock bằng **layout headline + bullet trực tiếp**, không box.

```latex
\begin{frame}{Framework: Linear Probe Ridge Regression}
% --- Equation ở top, vừa phải, không Large ---
\begin{center}
  \[
  \hat{\beta}
  = \arg\min_\beta\;
    \|\mathbf{y} - \mathbf{Z}\beta\|_2^2
  + \lambda\|\beta\|_2^2
  \]
\end{center}
\vspace{4pt}

\begin{columns}[T]
\column{0.48\textwidth}
  % --- KHÔNG dùng alertblock, chỉ dùng heading + bullet ---
  \begin{center}
    \textcolor{bad}{\textbf{\large \xmark\ Anisotropic}\;\; $\mathbf{Z}_{\text{aniso}}$}
  \end{center}
  \footnotesize
  $\lambda_1 \gg \lambda_2 \gg \cdots \gg \lambda_K$
  \\[6pt]
  \textcolor{bad}{$\Rightarrow$} Một số chiều bị "squished"\\
  \textcolor{bad}{$\Rightarrow$} Estimator lean vào chiều lớn\\[6pt]
  \textbf{\color{bad}Bias \& Variance đều CAO}

\column{0.48\textwidth}
  \begin{center}
    \textcolor{good}{\textbf{\large \cmark\ Isotropic}\;\; $\mathbf{Z}_{\text{iso}}$}
  \end{center}
  \footnotesize
  $\lambda_1 = \lambda_2 = \cdots = \lambda_K$
  \\[6pt]
  \textcolor{good}{$\Rightarrow$} Mọi chiều đều quan trọng như nhau\\
  \textcolor{good}{$\Rightarrow$} Estimator cân bằng\\[6pt]
  \textbf{\color{good}Bias \& Variance đều THẤP}
\end{columns}
\takeaway{Cùng "energy" — hình học khác $\Rightarrow$ hiệu quả khác}
\end{frame}
```

**Khác biệt:**

| Trước | Sau |
|-------|-----|
| 2 box (1 đỏ, 1 xanh) | **0 box** — chỉ heading màu |
| Mỗi box 6 atom | Mỗi cột 4 atom |
| 13 atom tổng | **9 atom tổng** |
| 70% diện tích = box | 100% diện tích = nội dung |
| Equation `\Large` mismatch | Equation default size |
| 2 dòng "Hệ quả: Bias cao / Var cao" | **1 dòng tổng kết bold** |

→ Slide thoáng hơn nhiều, message vẫn nguyên.

### Bonus — đổi 2 hệ quả "Bias cao / Var cao" thành 1 statement
Thay vì:
```
Hệ quả:
Bias(β̂_aniso) cao
tr(Var(β̂_aniso)) cao
```

Viết thẳng:
```
Bias & Variance đều CAO
```

→ Khán giả không cần đọc 2 dòng formula, chỉ cần nhớ "**cao**" vs "**thấp**". Formula chi tiết để dành cho slide 8 (lemma).

### Tổng điểm slide 7 hiện tại: **5.5/10**
Sau khi bỏ box: **8/10**.

---

## SLIDE 8 — "Bằng Chứng 1: Aniso Tệ Hơn Iso Về Cả Bias Và Variance"

### Phân tích screenshot — đúng các vấn đề bạn nêu

#### 1. ❌ Tiêu đề figure lệch phải so với figure

Trong code [slides_v2.tex:437,468](slides_v2.tex#L437):
```latex
\begin{center}\footnotesize\textbf{Bias theo số mẫu $N$}\end{center}
\begin{tikzpicture}
  \begin{axis}[width=5.2cm, height=2.7cm, ...]
```

**Nguyên nhân:** `\begin{center}` căn giữa theo **chiều rộng cột** (`\linewidth` của 0.48\textwidth). Nhưng axis pgfplots có **margin trái lớn** (cho ylabel + tick label). Kết quả: tâm của axis lệch sang phải so với tâm cột.

**Fix:**

**Cách A — căn giữa theo plot:**
Dùng `title` của pgfplots thay vì `\begin{center}` ở ngoài:
```latex
\begin{tikzpicture}
\begin{axis}[
  width=5.2cm, height=2.7cm,
  title={Bias theo số mẫu $N$},
  title style={font=\footnotesize\bfseries},
  xlabel={Số mẫu $N$},
  ...
]
```
→ Title sẽ nằm **căn giữa theo plot area**, không bị lệch.

**Cách B — dịch trái thủ công:**
```latex
\begin{center}\hspace*{-8pt}\footnotesize\textbf{Bias theo số mẫu $N$}\end{center}
```
(Cách A tốt hơn — giải quyết vấn đề ở gốc.)

#### 2. ❌ Legend che figure

Trong code [slides_v2.tex:448](slides_v2.tex#L448):
```latex
legend style={font=\tiny, at={(0.98,0.08)}, anchor=south east, ...}
```

**Vấn đề:** Legend đặt **inside plot area** ở góc dưới-phải. Đường `Iso ✓` (xanh, đường cao) đi qua khu vực này → legend đè lên đường data.

Tương tự [slides_v2.tex:478](slides_v2.tex#L478): legend ở góc trên-trái, đè lên 3 đường aniso.

**Fix:**

**Cách A — đẩy legend ra ngoài plot:**
```latex
legend style={
  font=\tiny,
  at={(1.02,1.0)},        % phải-trên, OUT of plot
  anchor=north west,
  draw=none, fill=none
}
```
Hoặc:
```latex
legend pos=outer north east  % shortcut của pgfplots
```

**Cách B — bỏ legend, dùng inline label trên đường:**
```latex
\addplot[color=bad, thick] coordinates {...} 
  node[pos=0.7, above, font=\tiny, color=bad] {Aniso \xmark};
\addplot[color=good, thick] coordinates {...}
  node[pos=0.7, above, font=\tiny, color=good] {Iso \cmark};
```
→ Không có legend box, label gắn ngay trên đường — sạch hơn nhiều.

(Đây là kỹ thuật thường dùng trong paper — slide cũng nên áp dụng.)

#### 3. ❌ 2 alertblock "Lemma 3.1" và "Lemma 3.2" đè dưới figure — không cần thiết

Quan sát: 2 box `\begin{alertblock}{Lemma 3.X — Bias/Variance}` chiếm 1 dải dọc dưới mỗi figure. Mỗi box chỉ có **1 dòng formula** bên trong.

**Đây là ví dụ điển hình của "box thừa":**
- Box title: "Lemma 3.1 — Bias" (đã đặt trong block title)
- Box body: 1 dòng formula

→ **Có thể viết thẳng dưới figure** mà không mất ý nghĩa:
```latex
\begin{tikzpicture}...\end{tikzpicture}
\begin{center}\scriptsize
  \textbf{Lemma 3.1:} Với $\lambda>0$, $\exists\,\mathbf{y}$:
  $\text{Bias}(\hat\beta_{\text{aniso}}) > \text{Bias}(\hat\beta_{\text{iso}})$
\end{center}
```

→ Bỏ được box, slide thoáng, message vẫn rõ.

#### 4. ⚠️ Variance plot dùng decision boundary — nhưng dữ liệu là illustrative
Trong code [slides_v2.tex:485-494](slides_v2.tex#L485):
```latex
\addplot[color=bad, thin, ...] {0.60*x + 0.15};  % 3 đường aniso
\addplot[color=bad, thin, ...] {0.60*x - 0.30};
\addplot[color=bad, thin, ...] {0.60*x + 0.55};
\addplot[color=good, thick, ...] {-0.55*x + 0.05};  % 1 đường iso
```

**Vấn đề:**
- 3 đường aniso **song song** (cùng slope 0.60) — không thể hiện được "variance".
- 1 đường iso slope khác (`-0.55`) — không cùng "trial" với 3 đường kia.
- Không rõ "variance của decision boundary" có nghĩa gì với khán giả.

**Fix:** Hoặc:
- (a) **Vẽ thêm đường trial** cho cả 2 trường hợp (4-5 đường aniso + 4-5 đường iso) để khán giả thấy "đường iso bám sát nhau, đường aniso nhảy múa".
- (b) **Đổi visual** sang ellipse covariance (1 ellipse aniso dài + 1 ellipse iso tròn) — đơn giản hơn, dễ đọc hơn cho slide.

Tôi đề xuất (b) vì slide không có thời gian giải thích "decision boundary":
```
[ellipse dài + nhọn (aniso)]    [hình tròn (iso)]
σ_β² lớn                          σ_β² nhỏ
```

#### 5. ⚠️ Khoảng cách figure → lemma → takeaway quá dày
Slide có 4 lớp chồng dọc: figure-title → figure → lemma-box → (bên dưới) → takeaway. Quá nhiều "level". 

**Sau khi áp các fix trên:**
- Bỏ alertblock Lemma → 1 dòng text
- Title figure di vào pgfplots → bớt 1 lớp `\begin{center}`

Slide còn 3 lớp: figure → caption + lemma 1 dòng → takeaway. Sạch.

### Tổng điểm slide 8 hiện tại: **5/10** — sửa 4 điểm trên lên 8.5/10.

---

## QUY TẮC RÚT RA — "BOX HYGIENE"

### Audit box xuyên deck

Chạy:
```bash
grep -n "begin{block}\|begin{alertblock}\|begin{exampleblock}" slides_v2.tex
```

Đếm hiện tại: **38 block trên 30 slide**. Mục tiêu hợp lý: **≤ 20 block** (tối đa 2 box trên 1/3 số slide).

### Quy tắc 4 câu hỏi trước khi viết `\begin{block}`

Trước mỗi `\begin{block}{...}`, hỏi:

1. **Nội dung này là theorem/lemma/definition formal?**
   - Có → dùng box (tăng tính "uy quyền")
   - Không → cân nhắc bỏ box

2. **Có > 3 dòng nội dung trong box?**
   - Có → giữ box (cần frame để chia khối)
   - Không → bỏ box, dùng heading + 1-2 dòng text

3. **Slide đã có figure/TikZ chiếm > 50% diện tích?**
   - Có → **bỏ box bên cạnh figure**, dùng caption text thẳng
   - Không → có thể dùng box

4. **Có hơn 1 box khác trên cùng slide?**
   - Có → cân nhắc gộp 2 box hoặc bỏ 1 box
   - Không → có thể dùng box

→ Nếu trả lời **"không"** ≥ 2 câu → **bỏ box, dùng heading + bullet**.

### Pattern thay thế khi bỏ box

Pattern cũ:
```latex
\begin{block}{Tiêu đề}
  Nội dung 1 dòng
\end{block}
```

Pattern mới (3 lựa chọn):

**(a) Heading màu + content:**
```latex
\textcolor{primary}{\textbf{Tiêu đề}} \\[2pt]
Nội dung 1 dòng
```

**(b) Centered statement:**
```latex
\begin{center}\footnotesize
  \textbf{Tiêu đề:} Nội dung 1 dòng
\end{center}
```

**(c) Inline labeling:**
```latex
\textbf{\color{good}\cmark\ Tiêu đề} —\;Nội dung 1 dòng
```

3 pattern này cho cùng thông điệp nhưng KHÔNG có "chrome" của box.

### Bảng các slide có box dày đặc cần audit

Dựa trên đọc code, các slide bạn nên review về box:

| Slide | # Box | Chẩn đoán nhanh |
|-------|-------|-----------------|
| 4 | 3 (block + alertblock + exampleblock-implicit) | TikZ + 2 block — cân nhắc bỏ 1 |
| 6 | 2 alertblock + 1 exampleblock | **3 box + TikZ — đã flag ở đợt trước** |
| **7** | **2 (alertblock + exampleblock)** | **Đã flag ở đợt này** |
| **8** | **2 alertblock + 2 figure title** | **Đã flag ở đợt này** |
| 9 | 1 alertblock to | Nội dung theorem — OK giữ box |
| 11 | 1 block + 1 exampleblock + TikZ | Nhiều — cân nhắc bỏ exampleblock |
| 12 | 1 block + 1 alertblock + TikZ | Box "Vấn Đề" 1 dòng — bỏ |
| 13 | 1 block + 1 alertblock + TikZ | OK nhưng theorem 4.2 không có box (inconsistent) |
| 14 | 1 block + 1 alertblock + plot | OK |
| 15 | 1 block + 1 alertblock + TikZ | OK |
| 17 | 1 block + lstlisting | OK |
| 19 | TikZ + sout text | OK |
| 21 | 1 block + 1 plot + TikZ | "Recommended defaults" 1 dòng — bỏ box |
| 22 | 1 block + 1 alertblock + plot | OK nhưng nhiều |
| 23 | 1 block + 1 alertblock + TikZ tree | OK |
| 24 | 1 block + 1 exampleblock + plot | "Ablation" có thể không cần box |
| 26 | 1 exampleblock dày | "Paradigm Shift" 2 dòng — chuyển thành takeaway |
| 27 | 1 block + 1 alertblock + TikZ | OK |
| 28 | TikZ radial + timeline | OK |
| 29 | 1 block + 1 alertblock + TikZ | OK |

---

## CẬP NHẬT BẢNG ƯU TIÊN SỬA TỔNG THỂ (Slides 1–8)

| # | Slide | Việc | Tác động |
|---|-------|------|----------|
| 1 | **6** | Tách slide hoặc cắt 21→7 atom | **Rất cao** |
| 2 | 4 | Sửa "LLM dự báo pixel" (lỗi học thuật) | **Rất cao** |
| 3 | 4 | Mũi tên ngược + giảm 5 màu xuống 4 | Rất cao |
| 4 | 1 | Thay `[Tên bạn]` | Cao |
| 5 | **8** | **Title figure dùng `title=` của pgfplots, đẩy legend ra ngoài** | **Cao** |
| 6 | **7,8** | **Bỏ 4 box (2 alertblock slide 7 + 2 lemma box slide 8) → heading màu + 1 dòng** | **Cao** |
| 7 | 5 | Thêm hàng "LeJEPA" + cột "# HP" trong bảng | Cao |
| 8 | 3 | Vẽ ellipse "không gian embedding" + phân bố `z` 2D | Cao |
| 9 | 1 | Đường tròn dashed bao đám embedding | Cao |
| 10 | All | **Audit toàn deck — bỏ box thừa (mục tiêu 38 → ≤ 20)** | **Trung bình–Cao** |

---

## LỜI KHUYÊN PHILOSOPHICAL CHO PHẦN CÒN LẠI CỦA DECK

> **"Box là dụng cụ — không phải style."**
> 
> Mỗi lần bạn viết `\begin{block}`, hãy nghĩ: **"Tôi cần frame này để làm gì?"**
> Nếu câu trả lời là *"để slide có cấu trúc"* → sai. Cấu trúc đến từ `columns`, `\vspace`, heading text.
> Nếu câu trả lời là *"để khán giả biết đây là theorem quan trọng"* → đúng, dùng `alertblock`.

Nguyên tắc thiết kế khi tiếp tục với slides 9–30:

| Loại nội dung | Dùng box? |
|---------------|-----------|
| Theorem / Lemma / Definition | ✅ `alertblock` (sparingly) |
| Code listing | ✅ box ngầm của `lstlisting` |
| Quote / câu chốt | ✅ `tcolorbox` 1 lần (slide cuối) |
| Bullet list | ❌ KHÔNG box |
| Definition 1 dòng | ❌ Heading + text |
| Caption figure | ❌ `\begin{center}` hoặc `\caption` |
| "Implication" / "Hệ quả" | ❌ inline `\textbf{Implication:}` |
| "So sánh" 2 phía | ❌ Heading màu, không box (đối xứng nhưng minimal) |

Áp dụng quy tắc này, deck sẽ giảm 38 → ~15 box. Slide thoáng hẳn.

---

> **Cap tiếp đi — đặc biệt là slide 11 (theory summary) và slide 19 (LeJEPA loss formula) — hai slide quan trọng nhất của Phần 2 và 3, cần soi rất kỹ về box hygiene và density.**

---
---

# ĐỢT 5 — SLIDE 9 & SLIDE 10 + BRAINSTORM REDESIGN ANISO/ISO

> **Yêu cầu cụ thể của bạn:** *"Hai hình anisotropic và isotropic không đẹp, hiện tại đơn điệu và không có tính thẩm mỹ — brainstorm ý tưởng vẽ lại."*
>
> Đây là **vấn đề trung tâm** của slide 9 + 10 + 12 + 13 — vì motif "ellipse vs circle" lặp lại nhiều nơi trong deck. Sửa được sẽ kéo lên **chất lượng cả phần lý thuyết**.

---

## SLIDE 9 — "Bằng Chứng 2: Iso Gaussian Tối Ưu Cho kNN Và Kernel Regression"

### Phân tích screenshot

#### Cấu trúc hiện tại
```
┌── alertblock to: Theorem 3.3 ────────────┐
│  Math formula dài 2 dòng                  │
│  arg min p ISB(p) = N(0, κ/K I)           │
└───────────────────────────────────────────┘
[Intuition text — 4 dòng]      [TikZ nhỏ:]
                                ✗ Aniso ellipse
                                ✓ Iso circle
[takeaway]
```

#### Vấn đề

##### 1. ❌ Theorem block chiếm ~50% chiều cao slide
Block "Theorem 3.3" có:
- Tiêu đề: "Theorem 3.3 (Balestriero & LeCun, 2025)"
- Body: 1 dòng setup + 1 công thức ISB to + 1 dòng kết luận

→ Body **3 atom math-heavy**. Khán giả cần ~30 giây để đọc → tốn nửa thời gian slide chỉ cho 1 box.

##### 2. ❌ TikZ phải bị "chật khí"
2 hình (ellipse + circle) mỗi cái chỉ cao ~0.8cm → vô cùng nhỏ. Caption "Aniso: bị lệch" và "Iso: cân bằng" font `\tiny`. **Không đủ visual weight** cho hình minh họa quan trọng nhất.

→ Đáng lẽ TikZ này nên là **focal point** (vì là intuition của theorem), nhưng đang bị Theorem block "ăn" hết spotlight.

##### 3. ❌ Intuition text bên trái lặp lại nội dung TikZ phải
Text trái:
- "Aniso: neighborhood lệch — prediction bị bias"
- "Iso: neighborhood cân bằng — unbiased"

TikZ phải:
- Aniso ellipse với caption "bị lệch"
- Iso circle với caption "cân bằng"

→ **Redundancy**. Đáng lẽ TikZ phải tự nói được, hoặc text phải bổ sung thông tin TikZ không có.

##### 4. ⚠️ Math trong theorem block dùng `\tiny` — đọc không nổi
Trong code [slides_v2.tex:509](slides_v2.tex#L509): `\tiny` cho cả công thức ISB. Math `\tiny` không đọc được trên màn chiếu lớn.

### Hướng cải thiện

**Tái cấu trúc:** đổi từ "theorem-heavy" sang "intuition-heavy", đẩy theorem xuống secondary:

```latex
\begin{frame}{Bằng Chứng 2: Iso Gaussian Tối Ưu Cho kNN \& Kernel}
\begin{columns}[c]
\column{0.50\textwidth}
  % --- Câu hỏi đặt vấn đề ---
  \textcolor{primary}{\textbf{Vì sao $\mathcal{N}(0,I)$?}}
  \\[6pt]
  \footnotesize
  kNN và kernel regression dựa vào \textbf{khoảng cách Euclidean}.\\[8pt]
  
  \textcolor{bad}{\xmark\ Aniso:} neighborhood **lệch** theo trục dài\\
  \quad → kNN bias về 1 phía\\[4pt]
  
  \textcolor{good}{\cmark\ Iso:} neighborhood **đối xứng**\\
  \quad → kNN unbiased mọi hướng\\[8pt]
  
  % --- Theorem rút gọn ---
  \scriptsize\color{neutral}
  \textbf{Theorem 3.3} (Balestriero \& LeCun, 2025)\\
  Với $\text{Tr}(\text{Cov}(Z))=\kappa$ cố định:
  \[
  \arg\min_p \text{ISB}_{k\text{NN}}(p) = \mathcal{N}(\mathbf{0}, \tfrac{\kappa}{K} I)\;\;\text{(unique)}
  \]

\column{0.50\textwidth}
  % --- TikZ TO, là focal point ---
  \centering
  [TikZ — sẽ thiết kế ở phần BRAINSTORM bên dưới]
\end{columns}
\takeaway{Kết quả UNIQUE: không distribution nào khác đạt ISB tối thiểu}
\end{frame}
```

**Khác biệt:**
- Bỏ alertblock to → math thành 3 dòng inline
- Giữ kết luận quan trọng nhất ("unique minimizer at $\mathcal{N}(0, \kappa/K\, I)$")
- Bỏ derivation ISB formula chi tiết (Fisher info, $r_0^4$, $\tau_g$) — **đây là chi tiết technical** không phù hợp cho slide. Để dành cho Q&A nếu ai hỏi.
- TikZ phải được phóng to → focal point đúng nghĩa

---

## SLIDE 10 — "Geometric Intuition: Hình Cầu Là Tối Ưu"

### Phân tích screenshot

#### Vấn đề chính bạn nêu — chính xác từng điểm
1. ❌ **Đơn điệu:** chỉ có 1 ellipse + 1 circle — 2 hình hình học cơ bản.
2. ❌ **Không có thẩm mỹ:** không shading, không depth, không texture.
3. ❌ **Đối xứng đến mức nhàm:** 2 panel cùng kích thước, cùng layout, cùng vị trí caption.
4. ❌ **Random scattered points** không có ý nghĩa — chỉ là "rắc thêm cho có".
5. ⚠️ **Mũi tên eigenvector cơ bản** (đường thẳng có mũi tên) — nhìn như sketch giảng đường, không như slide hội nghị.
6. ⚠️ **Caption dưới đáy quá xa shape** → đứt mạch đọc.

---

## 🎨 BRAINSTORM 8 IDEA REDESIGN ANISO/ISO

Tôi đưa 8 hướng từ "tinh chỉnh nhẹ" tới "phá cách". Bạn có thể pick 1, hoặc combine 2 ideas.

---

### 💡 IDEA 1 — **3D Shaded Sphere/Ellipsoid** (impressive, dễ làm)

**Concept:** Render 2 hình như **thể vật thể vật lý 3D** với shading gradient — không phải đường viền 2D đơn điệu.

```latex
\begin{tikzpicture}
  % --- Aniso: ellipsoid bị bóp dẹt ---
  \begin{scope}[xshift=-3.5cm]
    % Body với shading
    \shade[ball color=bad!50, opacity=0.85] 
      (0,0) ellipse (1.8cm and 0.55cm);
    % Shadow under
    \fill[bad!20, opacity=0.4] 
      (0,-0.7) ellipse (1.6cm and 0.12cm);
    % Highlight reflection
    \fill[white, opacity=0.4] 
      (-0.4,0.2) ellipse (0.3cm and 0.08cm);
    
    % Axes inside (eigenvector arrows)
    \draw[->, thick, white, opacity=0.8] (0,0) -- (1.6, 0);
    \draw[->, thick, white, opacity=0.5] (0,0) -- (0, 0.5);
    \node[font=\scriptsize\bfseries, color=bad] at (0, 1.4) 
      {\xmark\ Anisotropic};
    \node[font=\tiny, color=neutral] at (0,-1.2) 
      {$\lambda_1 \gg \lambda_2$};
  \end{scope}
  
  % --- Iso: sphere hoàn hảo ---
  \begin{scope}[xshift=3.5cm]
    \shade[ball color=good!60, opacity=0.85] 
      (0,0) circle (1.1cm);
    \fill[good!20, opacity=0.4] 
      (0,-1.3) ellipse (1.0cm and 0.15cm);
    \fill[white, opacity=0.45] 
      (-0.3,0.4) ellipse (0.25cm and 0.18cm);
    
    \node[font=\scriptsize\bfseries, color=good] at (0, 1.4) 
      {\cmark\ Isotropic};
    \node[font=\tiny, color=neutral] at (0,-1.5) 
      {$\lambda_1 = \lambda_2 = \cdots$};
  \end{scope}
  
  % --- Mũi tên giữa, không phải dấu => đơn giản ---
  \draw[->, ultra thick, primary] 
    (-1.5, 0) -- (1.5, 0)
    node[midway, above, font=\scriptsize, color=primary]
    {tối ưu hóa};
\end{tikzpicture}
```

**Ưu:** Trông như slide hội nghị Pixar/Apple. Shading + reflection cho cảm giác **hiện đại**.
**Nhược:** Cần thêm package `tikz` + chú ý opacity layering.

---

### 💡 IDEA 2 — **Concentric Iso-Distance Contours** (semantic, đẹp + có ý nghĩa)

**Concept:** Vẽ **contour** khoảng cách Euclidean — đây là **chính xác** điều paper nói (kNN dựa trên Euclidean distance).

```latex
\begin{tikzpicture}
  % --- Aniso: ellipse contours đồng tâm ---
  \begin{scope}[xshift=-3.5cm]
    % 5 ellipse contour với opacity tăng dần
    \foreach \r/\op in {1.8/0.15, 1.4/0.25, 1.0/0.4, 0.6/0.6, 0.3/0.8} {
      \draw[bad, line width=0.6pt, opacity=\op]
        (0,0) ellipse ({\r*1.8cm} and {\r*0.6cm});
    }
    % Query point ở tâm
    \fill[bad] (0,0) circle (3pt);
    \node[font=\tiny, color=bad, above=4pt] at (0,0) {query};
    
    % 3 nearest neighbors — bị lệch về phía trục dài
    \fill[neutral!80] (1.4, 0.25) circle (2pt);
    \fill[neutral!80] (-1.2, -0.15) circle (2pt);
    \fill[neutral!80] (-0.9, 0.3) circle (2pt);
    
    % Caption
    \node[font=\scriptsize\bfseries, color=bad] at (0, 1.6) 
      {\xmark\ Anisotropic};
    \node[font=\tiny, color=neutral, align=center] at (0,-1.5) 
      {Neighbor lệch trục dài\\$d_{\text{Euclid}}$ không phản ánh similarity};
  \end{scope}
  
  % --- Iso: circle contours đồng tâm (target/bullseye) ---
  \begin{scope}[xshift=3.5cm]
    \foreach \r/\op in {1.0/0.15, 0.78/0.25, 0.56/0.4, 0.36/0.6, 0.18/0.8} {
      \draw[good, line width=0.6pt, opacity=\op]
        (0,0) circle (\r cm);
    }
    \fill[good] (0,0) circle (3pt);
    \node[font=\tiny, color=good, above=4pt] at (0,0) {query};
    
    % 3 nearest neighbors — phân tán đều
    \fill[neutral!80] (0.65, 0.4) circle (2pt);
    \fill[neutral!80] (-0.55, 0.45) circle (2pt);
    \fill[neutral!80] (-0.1, -0.7) circle (2pt);
    
    \node[font=\scriptsize\bfseries, color=good] at (0, 1.6) 
      {\cmark\ Isotropic};
    \node[font=\tiny, color=neutral, align=center] at (0,-1.5) 
      {Neighbor đối xứng\\$d_{\text{Euclid}}$ phản ánh đúng similarity};
  \end{scope}
\end{tikzpicture}
```

**Ưu:** 
- Kết nối **trực tiếp** với "kNN dùng khoảng cách Euclidean" → khán giả hiểu **vì sao** iso tối ưu.
- 5 contour layer + opacity gradient → đẹp mắt như topographic map.
- Có query point + neighbors → context kNN rõ ràng.

**Nhược:** Cần khéo chọn vị trí 3 neighbor cho aniso/iso để minh họa đúng "lệch" vs "đối xứng".

→ **Đây là idea tôi recommend nhất** vì vừa đẹp, vừa đúng ngữ nghĩa.

---

### 💡 IDEA 3 — **Voronoi Tessellation** (technical, semantic mạnh)

**Concept:** Vẽ **Voronoi diagram** — partition của không gian theo nearest neighbor. Đây là **bản chất** kNN.

```latex
% --- Pseudo Voronoi cells ---
\begin{tikzpicture}
  % Aniso: cells stretched theo trục x
  \begin{scope}[xshift=-3.5cm]
    \clip (0,0) ellipse (1.8cm and 0.6cm);
    % 7 cell stretched
    \foreach \px/\py/\clr in 
      {-1.5/0.1/bad!20, -0.8/0.3/bad!30, 0/0.2/bad!40,
       0.8/-0.1/bad!30, 1.5/-0.2/bad!20, -0.4/-0.3/bad!50,
       0.5/0.4/bad!25} {
      \draw[fill=\clr, draw=bad!50, line width=0.4pt] 
        (\px,\py) ellipse (0.5cm and 0.18cm);
      \fill[bad] (\px,\py) circle (1.5pt);
    }
  \end{scope}
  
  % Iso: cells hexagon đều
  \begin{scope}[xshift=3.5cm]
    \clip (0,0) circle (1.0cm);
    \foreach \px/\py/\clr in 
      {0/0.6/good!40, 0/-0.6/good!40,
       0.5/0.3/good!30, -0.5/0.3/good!30,
       0.5/-0.3/good!30, -0.5/-0.3/good!30,
       0/0/good!50} {
      \draw[fill=\clr, draw=good!50, line width=0.4pt] 
        (\px,\py) circle (0.3cm);
      \fill[good] (\px,\py) circle (1.5pt);
    }
  \end{scope}
\end{tikzpicture}
```

**Ưu:** Nhìn rất "technical" và đẹp như paper figure thật.
**Nhược:** Vẽ Voronoi đúng trong TikZ phức tạp — phải fake bằng hexagons/ellipses.

---

### 💡 IDEA 4 — **Distance Ruler Comparison** (super clear)

**Concept:** Vẽ **các thanh đo** từ query đến 4 hướng → cho thấy "khoảng cách không bằng nhau" (aniso) vs "khoảng cách bằng nhau" (iso).

```
[Aniso]                       [Iso]
   ↑                              ↑
   |─0.8─|                        |───1───|
   ←──1.5──→ query ←──1.5──→     ←──1───→ query ←──1───→
   |─0.8─|                        |───1───|
   ↓                              ↓

  ⚠ 4 hướng KHÔNG bằng         ✓ 4 hướng đều bằng nhau
```

```latex
% Aniso
\begin{scope}[xshift=-3.5cm]
  \fill[bad] (0,0) circle (3pt) node[above right=2pt, font=\tiny] {query};
  % 4 rulers với kích thước khác nhau
  \draw[<->, color=bad, thick] (-1.6,0) -- (1.6,0);
  \draw[<->, color=bad!50, thick] (0,-0.5) -- (0,0.5);
  % Tick marks + numbers
  \node[font=\scriptsize, color=bad, above] at (1.3,0) {$1.6$};
  \node[font=\scriptsize, color=bad, right] at (0,0.4) {$0.5$};
  \node[font=\tiny, color=bad, align=center] at (0,-1.3) 
    {Khoảng cách \textbf{khác}\\theo từng hướng};
\end{scope}

% Iso
\begin{scope}[xshift=3.5cm]
  \fill[good] (0,0) circle (3pt) node[above right=2pt, font=\tiny] {query};
  \draw[<->, color=good, thick] (-1,0) -- (1,0);
  \draw[<->, color=good, thick] (0,-1) -- (0,1);
  \draw[<->, color=good, thick] (-0.7,-0.7) -- (0.7,0.7);
  \draw[<->, color=good, thick] (0.7,-0.7) -- (-0.7,0.7);
  \node[font=\scriptsize, color=good, above] at (0.8,0) {$1$};
  \node[font=\scriptsize, color=good, right] at (0,0.7) {$1$};
  \node[font=\tiny, color=good, align=center] at (0,-1.3) 
    {Khoảng cách \textbf{bằng}\\mọi hướng};
\end{scope}
```

**Ưu:** Cực kỳ clear cho khán giả non-technical. Mỗi hướng có **số đo** cụ thể.
**Nhược:** Less aesthetic hơn idea 1, 2.

---

### 💡 IDEA 5 — **Density Heatmap** (đẹp, hiện đại)

**Concept:** Dùng `pgfplots` colormap để render density 2D.

```latex
\begin{axis}[
  width=4cm, height=3cm,
  view={0}{90},                 % top-down view
  colormap/viridis,
  hide axis,
]
  \addplot3[surf, shader=interp]
    {exp(-(x*x)/0.1 - (y*y)/2)};   % Aniso: stretched
\end{axis}
```

So với:

```latex
\addplot3[surf, shader=interp]
  {exp(-(x*x)/1 - (y*y)/1)};       % Iso: symmetric
```

**Ưu:** Cực kỳ aesthetic. Nhìn như nhiệt đồ khoa học chuyên nghiệp.
**Nhược:** 
- pgfplots 3D `surf` render chậm khi compile.
- Cần colormap đồng bộ với palette deck (viridis có thể clash với navy/sage).

---

### 💡 IDEA 6 — **Map Metaphor: Distorted vs Flat Earth Projection**

**Concept:** Dùng metaphor "**bản đồ phẳng**" trực tiếp (đã có trong takeaway hiện tại của bạn).

- **Aniso:** một mảnh bản đồ Mercator bị kéo dài (Greenland to khổng lồ).
- **Iso:** bản đồ với equal-area projection (mọi nước có kích thước tương đối đúng).

```latex
% Aniso "world map" với grid bị méo
\begin{scope}[xshift=-3.5cm]
  \draw[bad!50] (-1.8,-0.7) rectangle (1.8,0.7);
  % Vertical gridlines stretched
  \foreach \x in {-1.5,-1,-0.5,0,0.5,1,1.5} {
    \draw[bad!30, line width=0.3pt] (\x,-0.7) -- (\x,0.7);
  }
  % Horizontal gridlines bị wrap
  \foreach \y/\stretch in {-0.5/1.3, 0/1, 0.5/1.3} {
    \draw[bad!30, line width=0.3pt, domain=-1.8:1.8, samples=20] 
      plot (\x, {\y + 0.05*sin(\x*180/1.8)});
  }
  \node[font=\scriptsize\bfseries, color=bad] at (0, 1.1) 
    {\xmark\ Bản đồ méo (Aniso)};
\end{scope}

% Iso "flat map" với grid đều  
\begin{scope}[xshift=3.5cm]
  \draw[good!50] (-1,-1) rectangle (1,1);
  \foreach \x in {-0.75,-0.5,...,0.75} 
    \draw[good!30, line width=0.3pt] (\x,-1) -- (\x,1);
  \foreach \y in {-0.75,-0.5,...,0.75} 
    \draw[good!30, line width=0.3pt] (-1,\y) -- (1,\y);
  \node[font=\scriptsize\bfseries, color=good] at (0, 1.4) 
    {\cmark\ Bản đồ đều (Iso)};
\end{scope}
```

**Ưu:** Metaphor rất sticky — khán giả nhớ lâu.
**Nhược:** Hơi xa với toán học của paper. Phù hợp slide intuition (slide 10) hơn slide proof (slide 9).

---

### 💡 IDEA 7 — **Eigenvalue Bar Chart + Shape Combo** (clean, dual-info)

**Concept:** Mỗi panel có **2 visualization stack dọc**:
1. Trên: bar chart eigenvalues
2. Dưới: shape tương ứng

```
ANISO                    ISO
[█████]                  [██]
[██]                     [██]
[█]                      [██]
[ ]                      [██]
   ↓                        ↓
[ellipse]                [circle]
```

**Ưu:** Khán giả thấy **mối liên hệ trực tiếp** giữa "eigenvalue spectrum" và "shape".
**Nhược:** Cần 2 hình stack → cao hơn so với 1 hình.

---

### 💡 IDEA 8 — **Animated/Reveal Sequence** (cho slide 10 nếu có thời gian)

**Concept:** Dùng `\onslide<1->` của Beamer để **reveal từng layer**:
1. Layer 1: vẽ shape gốc (ellipse vs circle)
2. Layer 2: thêm query point + 3 neighbors
3. Layer 3: highlight neighbors → "đây là kNN"
4. Layer 4: thêm caption "biased" vs "unbiased"

```latex
\begin{tikzpicture}
  \draw[bad] ...ellipse;       % Always
  \onslide<2->{ \fill[bad] (0,0) circle (3pt); }   % Reveal slide 2
  \onslide<3->{ \fill[neutral] (1.4,0.2) circle (2pt); ... }
  \onslide<4->{ \node ... {biased}; }
\end{tikzpicture}
```

**Ưu:** Khán giả không bị overwhelm — thông tin nhả dần.
**Nhược:** Cần 4 click chỉ cho 1 slide. Quản lý timing phức tạp.

---

## 🏆 KHUYẾN NGHỊ COMBINE

**Cho slide 9** (proof slide, technical): **Idea 2 (Iso-Distance Contours)**
- Lý do: đúng ngữ nghĩa nhất với "kNN dựa Euclidean distance"
- Có query point + neighbors → khán giả thấy ngay cơ chế

**Cho slide 10** (intuition slide, aesthetic): **Idea 1 (3D Shaded) + Idea 7 (Bar chart combo)**
- Lý do: slide 10 là slide "drama" — cần wow factor
- 3D shading cho hai shape → đẹp visual
- Bar chart eigenvalue ở dưới mỗi shape → thông tin định lượng

**Layout đề xuất cho slide 10:**

```
┌──────────────── Slide 10 ────────────────┐
│  Geometric Intuition: Hình Cầu Là Tối Ưu │
│                                           │
│   ANISO                  ISO              │
│   [bar:█████]            [bar: ██]        │
│   [bar:██]               [bar: ██]        │
│   [bar:█]                [bar: ██]        │
│         ↓                       ↓         │
│   ┌──ellipsoid 3D──┐    ┌──sphere 3D──┐  │
│   │ stretched      │    │ symmetric   │  │
│   │ shaded body    │    │ shaded ball │  │
│   └────────────────┘    └─────────────┘  │
│                                           │
│   ✗ Bias mọi hướng       ✓ Unbiased      │
│                                           │
│  N(0,I): "bản đồ phẳng" — unbiased mọi   │
│  hướng                                    │
└───────────────────────────────────────────┘
```

→ Mỗi panel có **3 layer** (bar / shape / caption) → contrast aniso↔iso rõ rệt.

---

## CODE HOÀN CHỈNH — IDEA 2 (RECOMMENDED CHO SLIDE 9)

```latex
\begin{frame}{Bằng Chứng 2: Iso Tối Ưu Cho kNN \& Kernel}
\begin{columns}[c]
\column{0.45\textwidth}
  \textcolor{primary}{\textbf{Vì sao $\mathcal{N}(0,I)$?}}\\[6pt]
  \footnotesize
  kNN \& kernel regression dựa trên\\\textbf{khoảng cách Euclidean}.
  \\[8pt]
  \textcolor{bad}{\xmark\ Aniso:} neighborhood lệch trục dài → bias\\[3pt]
  \textcolor{good}{\cmark\ Iso:} neighborhood đối xứng → unbiased\\[10pt]
  \scriptsize\color{neutral}
  \textbf{Theorem 3.3:} $\arg\min_p \text{ISB}(p) = \mathcal{N}(\mathbf{0}, \tfrac{\kappa}{K} I)$
  \quad (\textbf{unique})

\column{0.50\textwidth}
\centering
\begin{tikzpicture}
  % --- Aniso ---
  \begin{scope}[xshift=-1.8cm]
    \foreach \r/\op in {1.0/0.12, 0.8/0.22, 0.6/0.36, 0.4/0.55, 0.2/0.85} {
      \draw[bad, line width=0.6pt, opacity=\op]
        (0,0) ellipse ({\r*1.6cm} and {\r*0.55cm});
    }
    \fill[bad] (0,0) circle (2.5pt);
    \node[font=\tiny, color=bad, above=3pt] at (0,0) {query};
    
    \fill[neutral!80] (1.25, 0.18) circle (2pt);
    \fill[neutral!80] (-1.05, -0.12) circle (2pt);
    \fill[neutral!80] (-0.85, 0.25) circle (2pt);
    
    \node[font=\scriptsize\bfseries, color=bad] at (0, 1.0) 
      {\xmark\ Aniso};
    \node[font=\tiny, color=neutral] at (0,-0.95) 
      {neighbors lệch};
  \end{scope}

  % --- Iso ---
  \begin{scope}[xshift=1.8cm]
    \foreach \r/\op in {1.0/0.12, 0.8/0.22, 0.6/0.36, 0.4/0.55, 0.2/0.85} {
      \draw[good, line width=0.6pt, opacity=\op]
        (0,0) circle (\r cm);
    }
    \fill[good] (0,0) circle (2.5pt);
    \node[font=\tiny, color=good, above=3pt] at (0,0) {query};
    
    \fill[neutral!80] (0.65, 0.4) circle (2pt);
    \fill[neutral!80] (-0.55, 0.45) circle (2pt);
    \fill[neutral!80] (-0.1, -0.7) circle (2pt);
    
    \node[font=\scriptsize\bfseries, color=good] at (0, 1.3) 
      {\cmark\ Iso};
    \node[font=\tiny, color=neutral] at (0,-1.2) 
      {neighbors đối xứng};
  \end{scope}
\end{tikzpicture}
\end{columns}
\takeaway{Kết quả UNIQUE: không distribution nào khác đạt ISB tối thiểu}
\end{frame}
```

## CODE HOÀN CHỈNH — IDEA 1 + 7 (RECOMMENDED CHO SLIDE 10)

```latex
\begin{frame}{Geometric Intuition: Hình Cầu Là Tối Ưu}
\centering
\begin{tikzpicture}
  % ============================================================
  % --- ANISO PANEL ---
  % ============================================================
  \begin{scope}[xshift=-3.8cm]
    % Bar chart eigenvalue (trên cùng)
    \fill[bad!70] (-0.6, 1.7) rectangle (-0.45, 2.5);   % λ1 lớn
    \fill[bad!50] (-0.35, 1.7) rectangle (-0.20, 2.0);  % λ2
    \fill[bad!30] (-0.10, 1.7) rectangle (0.05, 1.85);  % λ3
    \fill[bad!20] (0.15, 1.7) rectangle (0.30, 1.78);   % λ4
    \node[font=\tiny, color=bad, anchor=west] at (0.45, 2.1) 
      {Eigenvalues:\\$\lambda_1 \gg \lambda_2 \gg \cdots$};

    % 3D ellipsoid shaded
    \shade[ball color=bad!50, opacity=0.85] 
      (0,0) ellipse (1.8cm and 0.55cm);
    \fill[bad!15, opacity=0.5] 
      (0,-0.75) ellipse (1.6cm and 0.10cm);   % shadow
    \fill[white, opacity=0.45] 
      (-0.5,0.18) ellipse (0.32cm and 0.08cm);  % highlight

    % Caption
    \node[font=\footnotesize\bfseries, color=bad] at (0, 3.0) 
      {\xmark\ Anisotropic};
    \node[font=\scriptsize, color=bad, align=center] at (0,-1.3) 
      {Bias mọi hướng\\$d_{\text{Euclid}}$ \emph{méo}};
  \end{scope}

  % ============================================================
  % --- ARROW GIỮA ---
  % ============================================================
  \draw[->, ultra thick, primary] 
    (-1.5, 0.5) -- (1.5, 0.5)
    node[midway, above, font=\scriptsize, color=primary]
    {tối ưu};

  % ============================================================
  % --- ISO PANEL ---
  % ============================================================
  \begin{scope}[xshift=3.8cm]
    % Bar chart eigenvalue đều
    \foreach \i in {0,1,2,3} {
      \fill[good!60] ({-0.6+\i*0.25}, 1.7) rectangle ({-0.45+\i*0.25}, 2.3);
    }
    \node[font=\tiny, color=good, anchor=west] at (0.5, 2.0) 
      {Eigenvalues:\\$\lambda_1 = \lambda_2 = \cdots$};

    % 3D sphere shaded
    \shade[ball color=good!60, opacity=0.9] 
      (0,0) circle (1.0cm);
    \fill[good!15, opacity=0.5] 
      (0,-1.2) ellipse (0.9cm and 0.13cm);
    \fill[white, opacity=0.5] 
      (-0.3,0.35) ellipse (0.22cm and 0.16cm);

    \node[font=\footnotesize\bfseries, color=good] at (0, 3.0) 
      {\cmark\ Isotropic};
    \node[font=\scriptsize, color=good, align=center] at (0,-1.5) 
      {Unbiased mọi hướng\\$d_{\text{Euclid}}$ \emph{đều}};
  \end{scope}
\end{tikzpicture}

\vspace{8pt}
\takeaway{$\mathcal{N}(0,I)$: ``bản đồ phẳng'' — unbiased mọi hướng}
\end{frame}
```

**Đặc điểm code này:**
1. **3D shading** với `\shade[ball color=...]` → cho cảm giác **vật thể vật lý**
2. **Drop shadow** mờ dưới mỗi shape → cảm giác "vật thật trên mặt phẳng"
3. **Highlight reflection** trên-trái shape → giả light source
4. **Bar chart eigenvalues** ở trên → **dual visualization** (number + shape)
5. **Caption ngắn 2 dòng** → không lan man
6. **Mũi tên giữa thay cho `⇒`** → narrative driven, không hình học cứng
7. **Bỏ axes labels (λ1, λ2)** vì đã có bar chart → bớt clutter
8. **Bỏ random scattered dots** → vì không thêm thông tin gì

---

## TIPS CHUNG ĐỂ TIKZ ĐẸP HƠN

### 1. Dùng `\shade[ball color=...]` cho mọi "object 3D"
Thay vì:
```latex
\draw[fill=good!8, color=good] (0,0) circle (1cm);   % phẳng
```
Dùng:
```latex
\shade[ball color=good!60] (0,0) circle (1cm);       % 3D
```

### 2. Thêm shadow + highlight cho mọi shape lớn
- Shadow dưới: `\fill[neutral!10, opacity=0.5] (0,-h) ellipse (w and 0.1);`
- Highlight trên-trái: `\fill[white, opacity=0.4] (-x,y) ellipse (a and b);`

### 3. Ưu tiên `opacity` gradient thay vì màu cứng
5 contour với `opacity={0.15, 0.25, 0.4, 0.6, 0.85}` đẹp hơn 5 contour với `color={bad!10, !25, !50, !70, !90}`.

### 4. Bỏ axes thừa khi đã có bar chart riêng
Eigenvalue arrow trong shape (như slide 10 hiện tại) **trùng** với bar chart bên cạnh. Chọn 1.

### 5. Caption 2 dòng max, dạng "**ngắn**\\**ngắn**"
Tránh caption 1 dòng dài hoặc 3+ dòng.

### 6. `every node/.style={font=\scriptsize}` thay vì rải rác `\tiny`
Thiết lập 1 lần ở `\begin{tikzpicture}` cho consistency.

---

## CẬP NHẬT BẢNG ƯU TIÊN SỬA TỔNG THỂ (Slides 1–10)

| # | Slide | Việc | Tác động |
|---|-------|------|----------|
| 1 | **6** | Tách slide / cắt 21→7 atom | **Rất cao** |
| 2 | 4 | Lỗi học thuật "LLM dự báo pixel" | **Rất cao** |
| 3 | 4 | Mũi tên ngược + 5 màu xuống 4 | Rất cao |
| 4 | **9** | **Bỏ alertblock Theorem to → 3 dòng inline + TikZ phóng to** | **Rất cao** |
| 5 | **10** | **Redesign aniso/iso bằng 3D shading + bar chart (Idea 1+7)** | **Rất cao (về aesthetic)** |
| 6 | 1 | Thay `[Tên bạn]` | Cao |
| 7 | 8 | Title figure + legend pos + bỏ lemma block | Cao |
| 8 | 7 | Bỏ 2 alertblock/exampleblock → heading | Cao |
| 9 | 5 | Thêm hàng "LeJEPA" + cột # HP | Cao |
| 10 | 3 | Vẽ ellipse "không gian embedding" + 2D scatter | Cao |
| 11 | All | Audit box (38 → ≤ 20) | Trung bình–Cao |
| 12 | All | Áp dụng `\shade[ball color]` cho mọi shape lớn | Trung bình |

---

> **Slides 9-10 là cặp slide "bằng chứng + intuition" — tỷ lệ thành công của phần proof phụ thuộc cặp này. Đầu tư 30-40 phút redesign aniso/iso bằng Idea 1+7 sẽ nâng deck lên hẳn.**
> 
> **Cap tiếp slide 11-13 (theory wrap-up + thách thức high-dim + random slicing) đi — đây là transition vào Phần 3 (SIGReg).**

---
---

# ĐỢT 6 — SLIDE 11 (URGENT) & SLIDE 12

> **Nhận xét của bạn:**
> - Slide 11: *"Quá nhiều nội dung, diagram bị nén lại rất xấu, nhiều box và có box lớn — brainstorm cách minimize visual."*
> - Slide 12: *"Tạm ổn, nhưng vẫn nên feedback và cải thiện thêm."*

---

## SLIDE 11 — "Kết Luận Lý Thuyết: Design Principle Cho LeJEPA" 🚨

### Chẩn đoán: vì sao slide này là "tệ thứ 2" của deck (chỉ sau slide 6)

#### Đếm atom thông tin
| Vùng | Nội dung | Atom |
|------|----------|------|
| TikZ trái | Task → 3 probes → Optimal → Design (5 node + 6 mũi tên + 1 label theorem) | **6** |
| Block "So sánh với Prior SSL" | Title + bảng 4 hàng × 3 cột | **5** |
| exampleblock "Ý nghĩa" | Title + 1 câu | **2** |
| Footer takeaway | | **1** |
| **Tổng** | | **14 atom** |

→ Vượt ngưỡng "an toàn" 6-8 atom. **Gấp 2 lần ngưỡng.**

#### Vấn đề cụ thể trong screenshot

##### 1. ❌ Diagram bị nén theo chiều dọc — kết quả: text trong node bị wrap xấu
Quan sát:
- Node "Bất kỳ downstream task" — 2 dòng wrap
- Node "Optimal khi $Z \sim \mathcal{N}(0,I)$" — 2 dòng
- Node "Design: $f_\theta(x) \sim \mathcal{N}(0,I)$" — 2 dòng (có label "Theorem 3.3" đè ngang)

→ 5 node + 6 mũi tên + 1 label phụ phải gò vào cột 0.50\textwidth, chiều dọc giới hạn → **mọi node đều 2 dòng + font tiny**.

##### 2. ❌ Slide này là **slide kết luận lý thuyết** — nhưng đang đóng vai **slide so sánh**
Title: *"Kết Luận Lý Thuyết: Design Principle Cho LeJEPA"* → **kết luận** = đáng lẽ phải có **1 thông điệp lớn duy nhất**.

Nhưng nội dung gồm:
- (a) Diagram derivation (nhắc lại logic)
- (b) Bảng so sánh với prior SSL  
- (c) "Ý nghĩa" — nhắc lại ý nghĩa

→ **3 chủ đề khác nhau trên 1 slide kết luận**. Slide kết luận phải **đơn giản hóa**, không **tổng hợp thêm**.

##### 3. ❌ Bảng so sánh "Prior SSL vs LeJEPA" trùng với slide 5 (Heuristic Stack) và slide 20 (LeJEPA vs DINO/I-JEPA)
Bạn đã có:
- Slide 5: bảng 5 method × 3 cột → Prior SSL các vấn đề
- Slide 20: bảng 3 method × 7 tiêu chí → so sánh chi tiết

→ Bảng ở slide 11 (4 tiêu chí × 2 cột) là **redundant**. Khán giả đã thấy rồi.

##### 4. ❌ Block "Ý nghĩa" (1 câu) là ví dụ "box thừa" tiêu biểu
Nội dung: *"Lần đầu tiên SSL có **lý do lý thuyết** cho việc chọn distribution — không phải thử nghiệm."*

→ Đây chính là **takeaway** của slide. Đặt trong exampleblock và lặp lại trong takeaway footer = **kể 2 lần**.

##### 5. ⚠️ Label "Theorem 3.3" trong TikZ đè lệch
Code [slides_v2.tex:644](slides_v2.tex#L644):
```latex
\node[right=3pt of opt.south, font=\tiny, color=neutral, xshift=2pt, yshift=-8pt] {Theorem 3.3};
```
→ `xshift` + `yshift` thủ công = sign of fight với layout. Không stable khi font/size thay đổi.

---

## 🎨 BRAINSTORM 6 PHƯƠNG ÁN MINIMIZE VISUAL CHO SLIDE 11

Tôi đưa 6 hướng từ "ít drama" tới "rất tối giản". Mỗi phương án có atom-count và mức "wow" khác nhau.

---

### 💡 PHƯƠNG ÁN A — **"Hero Equation" minimal** (recommended cho slide kết luận)

**Concept:** Chỉ có **1 phương trình lớn ở giữa** + 3 dòng annotation nhỏ. Bỏ TikZ, bỏ table, bỏ block.

```latex
\begin{frame}{Kết Luận Lý Thuyết}
\vfill
\begin{center}
  {\footnotesize\color{neutral}\itshape Theorem 3.3 implies:}\\[12pt]
  
  % Hero equation
  \Huge\color{primary}
  $f_\theta(\mathbf{x}) \;\sim\; \mathcal{N}(\mathbf{0}, I)$
  \\[20pt]
  
  \large\color{neutral}
  Đây là design principle \textbf{duy nhất} cần đạt
\end{center}
\vfill

% 3 cột nhỏ phía dưới — KHÔNG box
\begin{columns}[t]
\column{0.32\textwidth}
  \centering\footnotesize
  \textcolor{good}{\cmark}\;\textbf{Linear probe}\\
  optimal
\column{0.32\textwidth}
  \centering\footnotesize
  \textcolor{good}{\cmark}\;\textbf{kNN probe}\\
  optimal
\column{0.32\textwidth}
  \centering\footnotesize
  \textcolor{good}{\cmark}\;\textbf{Kernel probe}\\
  optimal
\end{columns}
\vfill
\takeaway{Lần đầu tiên: biết \textbf{chính xác} embeddings nên phân phối thế nào}
\end{frame}
```

**Atom-count:** 1 equation + 3 mini-block + 1 takeaway = **5 atom**. Tối thiểu.

**Visual ưu điểm:**
- **1 focal point khổng lồ** — equation $\mathcal{N}(0,I)$ là "hero"
- Khoảng trắng `\vfill` ở 2 phía → slide thở
- Không box, không TikZ phức tạp
- 3 cột bullet ở dưới chỉ để **enumerate**, không phải compare

**Nhược:** Mất phần "so sánh với Prior SSL" — nhưng đã có ở slide 5/20.

---

### 💡 PHƯƠNG ÁN B — **Single Horizontal Flow** (semantic, cô đọng)

**Concept:** Thay 5-node 2D flow bằng **1 chuỗi ngang đơn giản** giống flow diagram của paper.

```
[Bất kỳ probe] ──→ [optimal khi Z ~ N(0,I)] ──→ [Design: f_θ ~ N(0,I)]
   3 loại                Theorem 3.3
```

```latex
\begin{frame}{Kết Luận Lý Thuyết: Design Principle}
\vspace{20pt}
\centering
\begin{tikzpicture}[every node/.style={font=\footnotesize}]
  \node[lightbluebox, minimum width=2.8cm, minimum height=1.2cm, 
        align=center] (probe) at (0, 0) 
    {Linear / kNN /\\Kernel probe};
  
  \node[goodbox, minimum width=2.8cm, minimum height=1.2cm,
        align=center] (opt) at (5, 0)
    {Optimal khi\\$Z \sim \mathcal{N}(\mathbf{0}, I)$};
  
  \node[primarybox, minimum width=2.8cm, minimum height=1.2cm,
        align=center, font=\footnotesize\bfseries] (design) at (10, 0)
    {Design Principle:\\$f_\theta(\mathbf{x}) \sim \mathcal{N}(\mathbf{0}, I)$};
  
  \draw[->, very thick, primary] (probe) -- 
    node[above, font=\scriptsize, color=neutral]{Theorem 3.3} 
    (opt);
  \draw[->, very thick, primary] (opt) -- 
    node[above, font=\scriptsize, color=neutral]{$\Rightarrow$}
    (design);
\end{tikzpicture}
\vspace{30pt}

% Inline annotation — không box
\begin{center}
  \footnotesize\color{neutral}
  Đây là principle \textbf{tổng quát}: bất kỳ downstream task dùng probe đều hưởng lợi.
\end{center}
\takeaway{Lần đầu tiên: biết chính xác embeddings nên phân phối thế nào}
\end{frame}
```

**Atom:** 3 node + 2 mũi tên + 1 caption + 1 takeaway = **6 atom**.

**Ưu:** Vẫn giữ "narrative flow" (probe → optimal → design) nhưng **đi ngang**, không **phân nhánh dọc**. Đơn giản hơn nhiều.

---

### 💡 PHƯƠNG ÁN C — **Theorem Card** (academic, formal)

**Concept:** Treat slide như "**theorem card**" trong sách giáo khoa — 1 box chính chứa theorem + corollary, không gì khác.

```latex
\begin{frame}{Kết Luận Lý Thuyết}
\vfill
\begin{center}
\begin{tcolorbox}[
  colback=primary!5, colframe=primary, 
  width=0.85\textwidth, arc=4pt, boxrule=1pt,
  title={\bfseries Design Principle (Theorem 3.3 corollary)}
]
\centering
\large
$f_\theta(\mathbf{x}) \;\sim\; \mathcal{N}(\mathbf{0}, I)$
\\[12pt]
\footnotesize\color{neutral}
là phân phối \textbf{duy nhất tối ưu} cho mọi downstream task dùng:\\
linear probe, kNN, kernel regression
\end{tcolorbox}
\end{center}
\vfill
\takeaway{Lần đầu tiên: biết chính xác embeddings nên phân phối thế nào}
\end{frame}
```

**Atom:** 1 box + 1 takeaway = **2 atom**. Cực tối giản.

**Ưu:** Phong cách **textbook** — rất formal, phù hợp với slide kết luận lý thuyết.
**Nhược:** Có thể "quá ít" cho 70 giây nói. Bạn cần kéo dài bằng narrative voice.

---

### 💡 PHƯƠNG ÁN D — **"Convergence Diagram"** (visual metaphor)

**Concept:** Vẽ **3 mũi tên hội tụ** từ 3 probe types về 1 điểm $\mathcal{N}(0,I)$. Visual driven.

```
   Linear probe ─────╮
                      ╲
   kNN probe ────────→ N(0,I)  →  Design: f_θ ~ N(0,I)
                      ╱
   Kernel probe ─────╯
```

```latex
\begin{tikzpicture}[every node/.style={font=\footnotesize}]
  % 3 probe sources
  \node[lightbluebox, minimum width=2.0cm] (lp) at (0, 1.5) {Linear probe};
  \node[lightbluebox, minimum width=2.0cm] (kn) at (0, 0)   {kNN probe};
  \node[lightbluebox, minimum width=2.0cm] (kp) at (0,-1.5) {Kernel probe};
  
  % Convergence target — TO, là focal point
  \node[primarybox, minimum width=2.5cm, minimum height=1.5cm, 
        font=\large\bfseries, align=center, fill=primary,
        text=white, drop shadow={opacity=0.3}] 
    (target) at (5, 0) {$\mathcal{N}(\mathbf{0}, I)$};
  
  % Mũi tên hội tụ — màu khác nhau cho 3 nguồn nhưng cùng đích
  \draw[->, thick, color=primary]   (lp.east) -- (target.west);
  \draw[->, thick, color=good]      (kn.east) -- (target.west);
  \draw[->, thick, color=accent]    (kp.east) -- (target.west);
  
  % Label trên cụm mũi tên
  \node[font=\scriptsize, color=neutral, above=4pt] at (3, 0.8) {Theorem 3.3};
  
  % Mũi tên ra design
  \node[goodbox, minimum width=3.2cm, minimum height=1.0cm,
        align=center, font=\footnotesize\bfseries] 
    (design) at (10, 0) {Design:\\$f_\theta \sim \mathcal{N}(\mathbf{0}, I)$};
  \draw[->, very thick, primary] (target) -- (design);
\end{tikzpicture}
```

**Atom:** 3 probe + 1 target (focal) + 1 design + 1 takeaway = **6 atom**.

**Ưu:** Visual metaphor "hội tụ" rất mạnh — **3 cách khác nhau, cùng 1 đích**. Phù hợp với thông điệp.
**Nhược:** Cần khéo placement để 3 mũi tên không bị chồng.

---

### 💡 PHƯƠNG ÁN E — **Tách thành 2 slide** (an toàn nhất)

Nếu bạn muốn giữ cả 3 chủ đề (diagram + comparison + ý nghĩa):

**Slide 11a:** "Design Principle" → dùng phương án A hoặc D
**Slide 11b:** "So Sánh: Prior SSL vs LeJEPA" → bảng chi tiết, có thể merge với slide 5

→ Mỗi slide chỉ 1 message. Không bị nén.

---

### 💡 PHƯƠNG ÁN F — **"3 column = 3 probe" với card style** (information-dense)

**Concept:** Giữ thông tin nhưng layout thành 3 card đối xứng:

```
┌────────────┬────────────┬────────────┐
│  Linear    │   kNN      │  Kernel    │
│  probe     │   probe    │  probe     │
│            │            │            │
│  Lemma 3.1 │  Theorem   │  Theorem   │
│  Lemma 3.2 │  3.3       │  3.3       │
│            │            │            │
│  ✓ N(0,I)  │  ✓ N(0,I)  │  ✓ N(0,I)  │
└────────────┴────────────┴────────────┘

         ⬇  All converge to:  ⬇

       Design: f_θ(x) ~ N(0,I)
```

**Ưu:** Mỗi probe có ngữ cảnh đầy đủ.
**Nhược:** Atom-count tương đương slide hiện tại — không thực sự minimize. Skip.

---

## 🏆 KHUYẾN NGHỊ CHO SLIDE 11

**Lựa chọn 1 (recommended):** **Phương án A (Hero Equation)** + bỏ bảng comparison
- Slide kết luận **phải** có 1 hero element
- Bảng đã có ở slide 5/20 → không lặp
- Atom-count: 5 → vùng an toàn

**Lựa chọn 2 (nếu muốn giữ flow diagram):** **Phương án D (Convergence Diagram)**
- Visual metaphor mạnh
- Vẫn có "narrative" cho người present
- Atom-count: 6

**KHÔNG nên:** Giữ layout 2-column hiện tại + bảng + 2 block. Atom-count 14 quá tải, diagram bị nén — không thể fix bằng tinh chỉnh nhỏ.

---

## SLIDE 12 — "Thách Thức: Kiểm Tra Distribution Trong Không Gian Cao Chiều"

### Đánh giá tổng quan
Bạn nhận xét "tạm ổn" — đúng. Slide này có:
- ✅ Title rõ, 1 message
- ✅ Bar chart trái có comparison rõ (4 method, SIGReg là duy nhất xanh)
- ✅ Block phải (3 yêu cầu) đúng cấu trúc bullet
- ✅ Takeaway đắt: "**Không thể test trực tiếp — cần sketching**"

Điểm 7/10. Có thể lên 8.5/10 với một số tinh chỉnh.

### Vấn đề và hướng cải thiện

#### 1. ⚠️ Bar chart **vẽ thủ công** bằng `\fill[bad!80] (0,-1.2) rectangle (3,-0.8);`

Trong code [slides_v2.tex:691-712](slides_v2.tex#L691):
```latex
\fill[bad!80] (0,-1.2) rectangle (3,-0.8);    % MMD bar
\fill[bad!80] (0,-2.2) rectangle (1.5,-1.8);  % KL bar
...
```

**Vấn đề:**
- Tọa độ pixel-level → fragile (đổi font hoặc width là vỡ)
- Không có axis ticks → khán giả không hiểu "scale" của các bar
- "Complexity" axis chỉ có mũi tên, không có giá trị → khá giả lập

**Fix:** Dùng `pgfplots ybar` thực sự:

```latex
\begin{tikzpicture}
\begin{axis}[
  xbar,                    % horizontal bar chart
  width=6cm, height=4cm,
  bar width=10pt,
  symbolic y coords={SIGReg, Direct, KL, MMD},
  ytick=data,
  xlabel={Complexity},
  xlabel style={font=\tiny},
  yticklabel style={font=\scriptsize},
  xtick style={draw=none},
  axis line style={-, color=neutral!50},
  enlarge y limits=0.2,
  nodes near coords,
  nodes near coords style={font=\scriptsize, color=primary},
  every node near coord/.append style={anchor=west},
  point meta=explicit symbolic,
]
  \addplot+[fill=bad!70, draw=none] coordinates {
    (3, MMD)        [$\mathcal{O}(N^2)$]
    (1.5, KL)       [Unstable]
    (3, Direct)     [$\mathcal{O}(N^2)$]
  };
  \addplot+[fill=good!80, draw=none] coordinates {
    (0.8, SIGReg)   [$\mathcal{O}(N)$]
  };
\end{axis}
\end{tikzpicture}
```

→ Layout sạch, axis có nghĩa, label tự động.

#### 2. ⚠️ Block `Vấn Đề` (alertblock) chỉ chứa 1 câu

Code [slides_v2.tex:727-729](slides_v2.tex#L727):
```latex
\begin{alertblock}{Vấn Đề}
  \footnotesize Mọi multivariate normality test chuẩn (BHEP, Mardia) đều $\mathcal{O}(N^2)$.
\end{alertblock}
```

→ **1 dòng + box overhead** = vi phạm box hygiene.

**Fix:** Viết thành caption dưới bar chart:
```latex
\begin{tikzpicture} ... \end{tikzpicture}
\begin{center}
  \scriptsize\color{neutral}
  \textbf{Vấn đề:} Mọi multivariate normality test chuẩn (BHEP, Mardia) đều $\mathcal{O}(N^2)$
\end{center}
```

→ Bỏ được 1 box, slide thoáng hơn.

#### 3. 💡 SIGReg bar nên **nổi bật hơn** vì là kết luận

Hiện tại: SIGReg bar chỉ khác màu (xanh) — bằng kích cỡ với 3 bar đỏ kia.

**Cách nhấn:**
- Bold tên "SIGReg" (đã có)
- Thêm **icon ⭐** kế bên SIGReg
- Thêm **annotation arrow** chỉ vào SIGReg với caption "← LeJEPA chọn cái này"
- Hoặc làm SIGReg bar **dày hơn** (`bar width=14pt` thay vì 10pt)

Code:
```latex
\addplot+[fill=good!80, draw=good, line width=1pt] 
  coordinates {(0.8, SIGReg)};
\node[font=\scriptsize\bfseries, color=good, anchor=west] 
  at (axis cs:1.0, SIGReg) {$\star$ chosen};
```

#### 4. 💡 Block "3 Yêu Cầu" có thể bỏ box, dùng inline

Hiện:
```latex
\begin{block}{3 Yêu Cầu Bắt Buộc}
  \begin{itemize}
    \item[\cmark] Differentiable: ...
    \item[\cmark] $\mathcal{O}(N)$ complexity: ...
    \item[\cmark] Provably correct: ...
  \end{itemize}
\end{block}
```

Có thể đơn giản hóa:
```latex
\textcolor{primary}{\textbf{\large 3 Yêu Cầu Bắt Buộc}}
\\[8pt]
\textcolor{good}{\cmark}\;\textbf{Differentiable}\\
\quad Cho gradient-based training\\[6pt]
\textcolor{good}{\cmark}\;\textbf{$\mathcal{O}(N)$ complexity}\\
\quad Scale lên millions samples\\[6pt]
\textcolor{good}{\cmark}\;\textbf{Provably correct}\\
\quad Guarantee convergence đến $\mathcal{N}(0, I)$
```

→ Cùng nội dung, không có box overhead.

#### 5. 💡 Title slide có thể rút ngắn

Hiện: `Thách Thức: Kiểm Tra Distribution Trong Không Gian Cao Chiều` (10 từ)

Rút thành:
- `Thách Thức: Test Phân Phối High-Dim`
- Hoặc: `Vì Sao Test $\mathcal{N}(0,I)$ Khó?`

#### 6. 💡 Takeaway có thể đối lập mạnh hơn

Hiện: *"Không thể test $\mathcal{N}(0,I)$ trực tiếp trong high-dim — cần sketching"*

Đề xuất: *"High-dim chặn đường thẳng — cần đường vòng (sketching)"* (giàu hình ảnh hơn)

### Tổng điểm slide 12 hiện tại: **7/10** — sửa 4 điểm trên lên 8.5/10.

---

## CẬP NHẬT BẢNG ƯU TIÊN SỬA TỔNG THỂ (Slides 1–12)

| # | Slide | Việc | Tác động |
|---|-------|------|----------|
| 1 | **6** | Tách slide / cắt 21→7 atom | **Rất cao** |
| 2 | **11** | **Cải tổ — phương án A (Hero Equation) hoặc D (Convergence)** | **Rất cao** |
| 3 | 4 | Lỗi học thuật "LLM dự báo pixel" | Rất cao |
| 4 | 4 | Mũi tên ngược + 5 màu xuống 4 | Rất cao |
| 5 | 9 | Bỏ alertblock Theorem to → 3 dòng inline | Rất cao |
| 6 | 10 | Redesign aniso/iso (Idea 1+7: 3D shading + bar) | Rất cao |
| 7 | 1 | Thay `[Tên bạn]` | Cao |
| 8 | 8 | Title figure + legend pos + bỏ lemma block | Cao |
| 9 | 7 | Bỏ 2 alertblock/exampleblock → heading | Cao |
| 10 | **12** | **Bar chart pgfplots + bỏ alertblock "Vấn Đề"** | **Trung bình** |
| 11 | 5 | Thêm hàng "LeJEPA" + cột # HP | Cao |
| 12 | 3 | Vẽ ellipse "không gian embedding" + 2D scatter | Cao |
| 13 | All | Audit box (38 → ≤ 20) | Trung bình–Cao |

---

## NGUYÊN TẮC RÚT RA TỪ SLIDE 11

> **"Slide kết luận = ít hơn, không phải nhiều hơn."**
> 
> Khi viết slide kết luận của 1 phần (theory wrap-up, method wrap-up, results wrap-up), hỏi:
> 1. Khán giả vừa xem 5-7 slide trước. Họ đã hiểu chi tiết chưa?
> 2. Slide này nên là **đọng lại** điều gì sau khi họ quên hết chi tiết?
> 3. Nếu slide này là **slide duy nhất họ chụp ảnh**, thì nội dung gì cần xuất hiện?
> 
> → Câu trả lời thường là: **1 phương trình + 1 câu**. Không phải bảng + diagram + ý nghĩa.

### Quy tắc "Hero Element" cho slide tổng kết

Slide tổng kết phải có **1 hero element**:
- Phương trình (như slide 11 nên có $f_\theta \sim \mathcal{N}(0,I)$)
- 1 con số ấn tượng (slide 25 đã làm tốt: `79.0%` to)
- 1 quote (slide 30 đã làm tốt: "*If 2024 was scaling, 2025...*")
- 1 figure đặc biệt (rare cho conclusion)

→ **Không bao giờ là 1 bảng + 1 diagram + 1 block + 1 caption.**

---

> **Slide 11 đang ở mức 4/10. Cải tổ theo phương án A → 8/10. Dùng 30 phút cho slide này.**
> 
> **Cap tiếp slide 13-15 (Random Slicing + Moment + CDF tests) — đây là phần nền tảng cho SIGReg ở slide 16-17.**

---
---

# ĐỢT 7 — SLIDE 13 (BRAINSTORM REDESIGN) & SLIDE 14

> **Yêu cầu:**
> - Slide 13: *"Brainstorm cải thiện idea cho hình vẽ — hiện tại không đẹp."*
> - Slide 14: *"Tạm ổn nhưng nên feedback để cải thiện thêm."*

---

## SLIDE 13 — "Giải Pháp: Sketch Qua Random 1D Projections"

### Phân tích figure hiện tại — vì sao "không đẹp"

#### Quan sát từ screenshot
TikZ hiện tại có 3 phần:
1. **"Cloud điểm" $\mathbb{R}^K$**: 1 ellipse + 5 chấm bên trong
2. **3 mũi tên $u_1, u_2, u_M$**: phóng từ ellipse sang phải
3. **3 "histogram"**: vẽ bằng `\draw sin/cos` — bất kỳ ai biết toán nhìn đều thấy đây là **đường sin**, không phải histogram/Gaussian

#### Vấn đề cụ thể

##### 1. ❌ "Cloud" không trông giống cloud
- 1 ellipse + 5 chấm ngẫu nhiên nằm bên trong
- 5 chấm = ít, không cảm giác "cloud điểm $K$ chiều"
- Không có depth, không có shading

##### 2. ❌ "Histogram" thực ra là sin curves
Code [slides_v2.tex:756-770](slides_v2.tex#L756):
```latex
\draw[good, fill=good!20, thick] (-1,0) sin (0,1) cos (1,0);     % "Khớp"
\draw[bad, fill=bad!20, thick] (-1,0) sin (-0.5,0.8) cos (0,0) sin (0.5, 0.5) cos (1,0);  % "Không khớp"
\draw[good, fill=good!20, thick] (-1,0) sin (0,1) cos (1,0);     % "Khớp"
```

→ Đây là sin curves vẽ bằng path operators — **không phải distribution**. Khán giả có thể nhầm là "wave functions" hoặc "spectra".

##### 3. ❌ Hai histogram "Khớp N(0,1)" giống hệt nhau, ở 2 vị trí khác nhau
Cùng path `(-1,0) sin (0,1) cos (1,0)` được vẽ 2 lần (cho $u_1$ và $u_M$). 
→ Khán giả tưởng "$u_1$ và $u_M$ tạo ra cùng 1 histogram" — sai ngữ nghĩa! Các projection khác nhau cho cùng 1 distribution N(0,1) **về mặt distribution**, nhưng **mẫu (sample histogram) phải khác nhau**.

##### 4. ❌ Mũi tên $u_1, u_2, u_M$ phóng ra **từ ellipse** — sai về toán
Trong projection: $u$ là **vector hướng**, nó **không đến từ cloud**, nó tồn tại độc lập trong $\mathbb{S}^{K-1}$. Mỗi $u$ tạo ra 1 phép chiếu $\langle u, X \rangle$.

→ Hình hiện tại gợi ý "$u$ là một thành phần của cloud" — **diễn giải sai**.

##### 5. ❌ Layout "horizontal sprawl" — không cân
Cloud bên trái (chiếm ~30%) + mũi tên giữa (~30%) + 3 histogram bên phải (~30%) → cả 3 phần đều nhỏ. Cảm giác "lan man".

##### 6. ⚠️ Block phải có 3 atom: Cramér-Wold + Phiên bản thực tế + Theorem 4.2
2 box + theorem inline = 3 element thông tin → cũng nhiều.

---

## 🎨 BRAINSTORM 7 IDEA REDESIGN HÌNH SLIDE 13

---

### 💡 IDEA 1 — **3D Cloud + Projection Onto Axes** (semantic chính xác)

**Concept:** Vẽ **3D scatter cloud** (fake 3D bằng TikZ) với 3 axis projections, mỗi axis là 1 vector $u$. Dưới mỗi axis là histogram thật.

```
        z↑
        |    ●  ●
        |   ●●  ●●
        | ●● ●● ●● ●
        |●●●●●●●●●●●●  ←─── cloud 3D
        |  ●●●● ●●
        |________________→ x  (u_1)
       /
      /
    y (u_2)

  Project lên u_1:  histogram đẹp ~ N(0,1)  ✓
  Project lên u_2:  histogram lệch          ✗
  Project lên u_M:  histogram đẹp ~ N(0,1)  ✓
```

```latex
\begin{tikzpicture}[scale=0.9]
  % --- 3D cloud, fake bằng cách scatter nhiều chấm ---
  \begin{scope}
    % Bounding box mờ
    \draw[neutral!30, dashed, thin] 
      (-1.5,-1) -- (1.5,-1) -- (2,0.3) -- (-1,0.3) -- cycle;
    % ~30 chấm ngẫu nhiên trong bounding
    \foreach \px/\py/\opp in 
      {-0.8/-0.5/0.7, 0.3/-0.4/0.9, 0.7/-0.7/0.6,
       -0.5/-0.2/0.8, 0.5/-0.1/0.85, 1.0/-0.3/0.7,
       -1.2/-0.6/0.6, 0.0/-0.8/0.7, 1.3/-0.5/0.5,
       -0.3/0.0/0.9, 0.6/-0.55/0.85, -0.9/-0.3/0.7,
       0.2/-0.2/0.8, 1.1/-0.6/0.6, -0.5/-0.7/0.7,
       0.8/0.0/0.7, -0.2/-0.5/0.85, 0.4/-0.65/0.7,
       1.4/-0.2/0.5, -1.0/-0.1/0.6, 0.0/0.1/0.7} {
      \fill[primary, opacity=\opp] (\px,\py) circle (1.5pt);
    }
    \node[font=\footnotesize, color=primary, above=2pt] at (0, 0.5) 
      {Cloud điểm $\mathbb{R}^K$};
  \end{scope}

  % --- 3 axis projections ---
  \draw[->, thick, accent] (0, -1.3) -- (3.5, -1.3) 
    node[right, font=\scriptsize, color=accent] {$u_1$};
  \draw[->, thick, accent] (0, -2.3) -- (3.5, -2.3) 
    node[right, font=\scriptsize, color=accent] {$u_2$};
  \draw[->, thick, accent] (0, -3.3) -- (3.5, -3.3) 
    node[right, font=\scriptsize, color=accent] {$u_M$};
\end{tikzpicture}
```

**Ưu:** Kết nối trực quan giữa cloud → axis → histogram.
**Nhược:** Nhiều chi tiết, có thể vẫn phức tạp.

---

### 💡 IDEA 2 — **"Shadow" Metaphor** (đẹp + dễ nhớ)

**Concept:** Cloud điểm chiếu **bóng** xuống 3 trục khác nhau, tạo ra 3 "histogram bóng" khác nhau. Đây là cách hình dung kinh điển cho projection.

```
     [3D point cloud]
          |
   ┌──────┼──────┐
   ↓      ↓      ↓
  ░░    ▒▒▒▒▒    ░░
 (shadow on u_1, u_2, u_M)
```

```latex
\begin{tikzpicture}
  % Cloud — 3D shape có shading (như 1 quả bóng)
  \shade[ball color=primary!50, opacity=0.7] (0,0) circle (1.0cm);
  \node[font=\scriptsize, color=primary, above=4pt] at (0,1.0) 
    {Cloud $\mathbb{R}^K$};
  
  % "Light beams" hướng xuống 3 hướng
  \draw[->, thick, color=accent, opacity=0.5] (0,-0.3) -- (-2.5,-2);
  \draw[->, thick, color=accent, opacity=0.7] (0,-0.5) -- (0,-2);
  \draw[->, thick, color=accent, opacity=0.5] (0,-0.3) -- (2.5,-2);
  
  % 3 "shadow" histograms
  \begin{scope}[xshift=-2.5cm, yshift=-2.5cm]
    [pgfplots N(0,1) — fit good]
    \node[font=\tiny, color=good, above] {$u_1$: \cmark\ Khớp};
  \end{scope}
  
  \begin{scope}[xshift=0cm, yshift=-2.5cm]
    [pgfplots — bimodal — bad fit]
    \node[font=\tiny, color=bad, above] {$u_2$: \xmark\ Không khớp};
  \end{scope}
  
  \begin{scope}[xshift=2.5cm, yshift=-2.5cm]
    [pgfplots N(0,1) — fit good]  
    \node[font=\tiny, color=good, above] {$u_M$: \cmark\ Khớp};
  \end{scope}
\end{tikzpicture}
```

**Ưu:** Metaphor "bóng" rất dễ hiểu cho non-expert. Visual mạnh.
**Nhược:** Hơi xa với toán formal.

---

### 💡 IDEA 3 — **Real Histograms with pgfplots** (đẹp + technical)

**Concept:** Thay sin curves bằng **histogram thật** (bar chart) với normal curve overlay.

```latex
% Histogram cho N(0,1) — fit good
\begin{tikzpicture}
\begin{axis}[
  width=3cm, height=2cm,
  hide axis,
  ymin=0, ymax=0.5,
]
  % Bars histogram
  \addplot+[ybar interval, fill=good!30, draw=good, line width=0.3pt] 
    coordinates {
      (-3,0.02) (-2,0.06) (-1.5,0.13) (-1,0.24) 
      (-0.5,0.35) (0,0.40) (0.5,0.35) (1,0.24) 
      (1.5,0.13) (2,0.06) (3,0.02) (3.5,0)
    };
  % Normal curve overlay
  \addplot[domain=-3:3, samples=50, color=primary, thick] 
    {0.4*exp(-x*x/2)};
\end{axis}
\end{tikzpicture}

% Histogram bimodal (bad fit) — clearly không phải Gaussian
\begin{axis}[...]
  \addplot+[ybar interval, fill=bad!30] coordinates {
    (-2,0.05) (-1.5,0.20) (-1,0.32) (-0.5,0.18)
    (0,0.10) (0.5,0.20) (1,0.30) (1.5,0.18)
    (2,0.05) (3,0)
  };
  % Cùng N(0,1) curve (target) để show mismatch
  \addplot[domain=-2.5:2.5, samples=50, color=primary, thick, dashed] 
    {0.4*exp(-x*x/2)};
\end{axis}
```

**Ưu:** Histograms thật (bar) → khán giả thấy ngay "đây là distribution sample". Có Normal curve overlay (đường liền vs đường gạch) → so sánh **trực quan** good vs bad.
**Nhược:** Dùng pgfplots → compile chậm hơn TikZ thuần.

→ **Tôi recommend nhất Idea 3** vì sửa đúng vấn đề số 2 (sin ≠ histogram).

---

### 💡 IDEA 4 — **Slicing Knife / Cookie Cutter** (metaphor lạ + memorable)

**Concept:** Cloud là khối "bánh", các vector $u$ là "dao cắt" tạo ra slice 1D.

```
          ┌──────────┐
          │  bánh K-d │
          │  (cloud)  │
          └──────────┘
              ║║║
              ▼▼▼  (3 dao cắt khác hướng)
          ┌──┐ ┌──┐ ┌──┐
          │∩∩│ │~∼│ │∩∩│
          └──┘ └──┘ └──┘
            u_1   u_2   u_M
```

**Ưu:** Memorable, ai cũng hiểu "cắt bánh".
**Nhược:** Hơi childish — phù hợp seminar lab hơn hội nghị formal.

---

### 💡 IDEA 5 — **Layered Reveal: Cloud → Sphere of Directions → Histograms** (3-stage)

**Concept:** 3 stage liên tiếp (đọc từ trái sang phải):

```
[Stage 1]              [Stage 2]              [Stage 3]
Cloud K-dim            Sphere S^(K-1)          Histograms 1D
●●●                     u_1 ↑                  u_1: ∩∩
●●●●●          →       u_2 →           →       u_2: ~∼
●●●                     u_M ↘                  u_M: ∩∩
```

```latex
\begin{tikzpicture}[scale=0.85]
  % --- Stage 1: cloud ---
  \shade[ball color=primary!40, opacity=0.7] (0,0) circle (0.9cm);
  \node[font=\scriptsize, below=4pt] at (0,-0.9) {Cloud $\mathbb{R}^K$};
  
  \draw[->, ultra thick, neutral] (1.2, 0) -- (2.4, 0);
  
  % --- Stage 2: sphere với 3 directions ---
  \begin{scope}[xshift=3.5cm]
    \draw[primary, thick, dashed] (0,0) circle (0.9cm);
    \draw[primary, thick, dashed] (0,0) ellipse (0.9cm and 0.3cm);
    \node[font=\scriptsize, below=4pt] at (0,-0.9) {$\mathbb{S}^{K-1}$};
    
    \draw[->, accent, thick] (0,0) -- (0.7, 0.5) 
      node[right, font=\tiny, color=accent] {$u_1$};
    \draw[->, accent, thick] (0,0) -- (-0.6, -0.4) 
      node[left, font=\tiny, color=accent] {$u_2$};
    \draw[->, accent, thick] (0,0) -- (0.5, -0.6) 
      node[right, font=\tiny, color=accent] {$u_M$};
  \end{scope}
  
  \draw[->, ultra thick, neutral] (4.7, 0) -- (5.9, 0);
  
  % --- Stage 3: 3 histograms thực ---
  \begin{scope}[xshift=7cm]
    [3 mini pgfplots stacked, mỗi cái với 1 distribution]
  \end{scope}
\end{tikzpicture}
```

**Ưu:** 3-stage rõ ràng, có sphere $\mathbb{S}^{K-1}$ (đúng với theorem Cramér-Wold).
**Nhược:** Cần horizontal space lớn → có thể không vừa cột.

---

### 💡 IDEA 6 — **Spotlight / Radar Visualization**

**Concept:** Cloud ở trung tâm, 3 "spotlight beam" từ 3 hướng chiếu vào, mỗi beam tạo 1 histogram ở rìa.

```
         ╭───── spotlight u_1 ─────╮
                      │
               ▓▓▓▓▓▓▓
              ░░░░cloud░░░░
               ▓▓▓▓▓▓▓
                      │
         ╰───── spotlight u_M ─────╯
```

**Ưu:** Visual giàu, có sense of "scanning từ nhiều góc".
**Nhược:** Phức tạp về layout.

---

### 💡 IDEA 7 — **Minimal: 1 Clean Diagram** (tối giản)

Nếu muốn đơn giản hết mức:

```
[Cloud K-dim] ───u_1───→ [N(0,1) ✓]
              ───u_2───→ [Bimodal ✗]
              ───u_M───→ [N(0,1) ✓]
```

Chỉ 1 cloud + 3 mũi tên + 3 box-result. Atom = 7. Vừa đủ.

---

## 🏆 KHUYẾN NGHỊ CHO SLIDE 13

**Recommend:** **IDEA 3 (Real Histograms via pgfplots)** + giữ layout horizontal hiện tại

**Lý do:**
- Sửa **lỗi gốc** (sin ≠ histogram)
- Vẫn dùng layout cloud + arrows + histograms — không phải re-architect
- Khán giả nhìn **histogram thật** sẽ hiểu ngay

**Combine với cải thiện cloud:** thay `\draw ellipse` + 5 chấm bằng `\shade[ball color]` + ~25 chấm scatter → cloud trông "đậm đặc" hơn, có 3D feel.

### Code đề xuất hoàn chỉnh

```latex
\begin{frame}{Giải Pháp: Sketch Qua Random 1D Projections}
\begin{columns}[c]
\column{0.55\textwidth}
\centering
\begin{tikzpicture}[every node/.style={font=\scriptsize}]
  % --- Cloud 3D-feel ---
  \shade[ball color=primary!50, opacity=0.55] 
    (0,0) ellipse (1.3cm and 0.8cm);
  \foreach \px/\py in 
    {-0.6/0.2, 0.3/0.4, 0.1/-0.3, -0.6/-0.1, 0.5/-0.2,
     -0.3/0.5, 0.7/0.1, -0.9/0.3, 0.4/-0.5, -0.5/-0.4} {
    \fill[primary, opacity=0.85] (\px,\py) circle (1.5pt);
  }
  \node[font=\footnotesize, color=primary, above=4pt] at (0, 0.8) 
    {Cloud $\mathbb{R}^K$};
  
  % --- 3 mũi tên ra 3 histogram ---
  \draw[->, thick, accent] (1.3, 0.3) -- (2.6, 1.2)
    node[midway, above, font=\tiny, color=accent] {$u_1$};
  \draw[->, thick, accent] (1.3, 0)   -- (2.6, 0)
    node[midway, above, font=\tiny, color=accent] {$u_2$};
  \draw[->, thick, accent] (1.3, -0.3) -- (2.6, -1.2)
    node[midway, below, font=\tiny, color=accent] {$u_M$};
  
  % --- 3 histogram thật bằng pgfplots ---
  \begin{scope}[xshift=4.0cm, yshift=1.2cm]
    \begin{axis}[
      width=3.0cm, height=1.5cm, hide axis,
      ymin=0, ymax=0.5, xmin=-3, xmax=3,
      enlargelimits=false, clip=false
    ]
      \addplot+[ybar interval, fill=good!30, draw=good!60, 
                line width=0.3pt, mark=none] 
        coordinates {(-3,0.04)(-2,0.10)(-1,0.24)(0,0.40)
                     (1,0.24)(2,0.10)(3,0.04)(3.5,0)};
      \addplot[domain=-3:3, samples=40, color=primary, thick]
        {0.4*exp(-x*x/2)};
    \end{axis}
    \node[font=\tiny, color=good, right=2pt] 
      at (1.6, 0.7) {\cmark\ Khớp $\mathcal{N}(0,1)$};
  \end{scope}
  
  \begin{scope}[xshift=4.0cm, yshift=0cm]
    \begin{axis}[
      width=3.0cm, height=1.5cm, hide axis,
      ymin=0, ymax=0.5, xmin=-3, xmax=3,
    ]
      \addplot+[ybar interval, fill=bad!30, draw=bad!60, mark=none]
        coordinates {(-2,0.08)(-1,0.30)(-0.5,0.15)(0,0.10)
                     (0.5,0.18)(1.5,0.32)(2,0.10)(2.5,0)};
      \addplot[domain=-3:3, samples=40, color=primary, thick, dashed]
        {0.4*exp(-x*x/2)};
    \end{axis}
    \node[font=\tiny, color=bad, right=2pt] 
      at (1.6, 0.7) {\xmark\ Không khớp};
  \end{scope}
  
  \begin{scope}[xshift=4.0cm, yshift=-1.2cm]
    \begin{axis}[
      width=3.0cm, height=1.5cm, hide axis,
      ymin=0, ymax=0.5, xmin=-3, xmax=3,
    ]
      \addplot+[ybar interval, fill=good!30, draw=good!60, mark=none]
        coordinates {(-3,0.03)(-2,0.12)(-1,0.22)(0,0.38)
                     (1,0.26)(2,0.08)(3,0.05)(3.5,0)};
      \addplot[domain=-3:3, samples=40, color=primary, thick]
        {0.4*exp(-x*x/2)};
    \end{axis}
    \node[font=\tiny, color=good, right=2pt] 
      at (1.6, 0.7) {\cmark\ Khớp $\mathcal{N}(0,1)$};
  \end{scope}
\end{tikzpicture}

\column{0.42\textwidth}
  % --- Bỏ alertblock và block, dùng heading + text ---
  \textcolor{primary}{\textbf{Hyperspherical Cramér-Wold}}
  \\[4pt]
  \footnotesize
  $X \stackrel{d}{=} Y \;\iff\; \langle u, X\rangle \stackrel{d}{=} \langle u, Y\rangle, \;\forall u \in \mathbb{S}^{K-1}$
  \\[12pt]
  \textcolor{primary}{\textbf{Phiên bản thực tế}}
  \\[4pt]
  \footnotesize
  Không cần \textbf{tất cả} hướng — chỉ cần $M$ hướng ngẫu nhiên, tái sử dụng qua nhiều bước training.
  \\[10pt]
  \scriptsize\color{neutral}
  \textbf{Theorem 4.2:} Test consistent nếu $M \to \infty$ cùng training.
\end{columns}
\takeaway{Bài toán $K$-chiều $\to$ $M$ bài toán 1-chiều độc lập}
\end{frame}
```

**Đặc điểm:**
1. ✅ Cloud có **shade** + **10 chấm density** — đậm đặc hơn
2. ✅ 3 histogram **THẬT** với bar + Normal curve overlay
3. ✅ Bad fit dùng **dashed** Normal curve → so sánh trực quan với histogram thực tế
4. ✅ Bỏ 2 box phải → heading màu inline (áp dụng "box hygiene")
5. ✅ Theorem 4.2 → 1 dòng inline, không box

---

## SLIDE 14 — "Test 1D Họ Moment: Mạnh Nhưng Không Stable"

### Đánh giá tổng quan
Bạn nói "tạm ổn" — đúng. **Điểm 7/10**. Slide có:
- ✅ Title rõ
- ✅ Math formula EJB chi tiết (cho audience technical)
- ✅ Theorem 4.3 cô đọng
- ✅ Plot "gradient explosion" right side trực quan
- ✅ Takeaway sắc: "*identifiability vs stability — không thể có cả hai*"

### Cải thiện đề xuất

#### 1. ⚠️ Formula EJB dài, dùng `\resizebox` để fit
Code [slides_v2.tex:799-805](slides_v2.tex#L799):
```latex
\resizebox{0.95\linewidth}{!}{$
\text{EJB}(\mathbf{u}) = \frac{N\hat\mu^2}{\hat\sigma^2} 
+ \frac{(N-1)(\hat\sigma^2 - 1)^2}{2} 
+ \frac{N}{6}\left(\text{skew}^2 + \frac{(\text{kurt}-3)^2}{4}\right)
$}
```

**Vấn đề:** `\resizebox` co toàn bộ formula → font math bị nén. Đọc trên màn chiếu xa = ácquá.

**Fix A — break thành 2 dòng:**
```latex
\begin{align*}
\text{EJB}(\mathbf{u}) &= \underbrace{\tfrac{N\hat\mu^2}{\hat\sigma^2}}_{\text{mean}} 
+ \underbrace{\tfrac{(N-1)(\hat\sigma^2-1)^2}{2}}_{\text{variance}}\\
&+ \tfrac{N}{6}\left(\underbrace{\text{skew}^2}_{m_3} 
+ \tfrac{(\text{kurt}-3)^2}{4}_{m_4}\right)
\end{align*}
```

**Fix B — đơn giản hóa formula:**
```latex
\text{EJB}(\mathbf{u}) = \sum_{k=1}^{4} c_k \cdot (m_k - m_k^{\mathcal{N}})^2
```
Sau đó nói thêm: "*4 moment đầu tiên (mean, var, skew, kurt) so với chuẩn*".

→ Khán giả không cần thấy 4 hệ số $c_k$ chi tiết — chỉ cần ý "**đo theo các moment**".

#### 2. ⚠️ Theorem 4.3 đặt trong `alertblock` — cùng lúc với block EJB → 2 box stack dọc

Code [slides_v2.tex:808-811](slides_v2.tex#L808):
```latex
\begin{alertblock}{Theorem 4.3}
  \footnotesize
  Minimize $\sum c_k(m_k(P) - m_k(Q))^2$ với $K$ hữu hạn \textbf{không} imply $P = Q$.
\end{alertblock}
```

**Vấn đề:** 2 box stack → tốn space. Block EJB đã 1 box, alertblock Theorem là box thứ 2.

**Fix:** Đổi alertblock thành caption nhỏ dưới formula:
```latex
\begin{block}{Extended Jarque-Bera (EJB)}
  ... formula ...
\end{block}
\vspace{4pt}
\centering\scriptsize
\textcolor{bad}{\textbf{Theorem 4.3:}} 
Minimize finite moments \textbf{KHÔNG} imply $P = Q$
\\(tồn tại shortcut solutions)
```

#### 3. 💡 2 bullet "K nhỏ / K lớn" có thể chuyển thành **table compact**

Hiện:
```
- K nhỏ: shortcut solutions tồn tại.
- K lớn: gradient explode.
```

Đổi thành table 2 hàng:
```latex
\centering\footnotesize
\begin{tabular}{l l}
\toprule
$K$ \textbf{nhỏ} & shortcut solutions tồn tại \\
$K$ \textbf{lớn} & gradient explode \\
\bottomrule
\end{tabular}
```

→ Cấu trúc rõ hơn — 2 mặt của trade-off được trình bày song song.

#### 4. 💡 Plot "Gradient Explosion" có thể nhấn mạnh hơn

Hiện code [slides_v2.tex:822-838](slides_v2.tex#L822):
```latex
\addplot[color=bad, thick, domain=1:6, samples=100] {2^(x)};
```

Plot $y = 2^x$ from x=1 to 6: y range = [2, 64]. Nhưng `ymax=100` → chỉ 64% chiều cao plot có data → trên có khoảng trắng.

**Fix:**
- Đổi `ymax=80` để curve "chạm trần" → cảm giác explode mạnh hơn
- Thêm dashed line ngang ở `y = stable threshold` (ví dụ y=10) để show "ngưỡng an toàn"
- Có thể thêm 1 plot iso (constant gradient) để contrast

```latex
\addplot[color=bad, thick, domain=1:6, samples=100] {2^(x)};
\addplot[color=good, thick, domain=1:6, samples=2] {1};   % Iso constant
\addlegendentry{EJB (moment)};
\addlegendentry{Epps-Pulley (CF)};
```

→ Khán giả thấy **2 đường so sánh** — không chỉ "explode đỏ" mà còn "stable xanh".

#### 5. 💡 Có thể thêm 1 visual "shortcut solution" để minh họa Theorem 4.3

Theorem nói "moments khớp ≠ distribution khớp". Có thể thêm 1 mini-figure:

```
[Histogram A: bimodal]   [Histogram B: Gaussian]
   ●●  ●●                   ●●●●●●
  ●●●●●●●                  ●●●●●●●●●
 ●●● ●● ●●●               ●●●●●●●●●●●

 mean=0, var=1, skew=0, kurt=3      mean=0, var=1, skew=0, kurt=3
       ↑ moments giống nhau ↑
       nhưng distribution khác hoàn toàn
```

→ Demonstrate **trực quan** Theorem 4.3 — đây là "**hai distributions khác nhau cùng moments**".

Nếu thêm visual này → slide có 3 figure: formula + plot explosion + bimodal vs gaussian. **Quá nhiều**. Trade-off: nếu thêm visual này thì **bỏ 1 trong 2 figure khác** (recommend bỏ block formula EJB chi tiết, dùng formula đơn giản hơn).

#### 6. 💡 Takeaway có thể đơn giản hóa

Hiện: *"Moment-based: identifiability vs stability — không thể có cả hai"*

**Đắt:** *"Moment đầy đủ → gradient explode. Moment hữu hạn → không identifiable. Bí."*

→ Diễn đạt được "cái trade-off" tốt hơn.

### Tổng điểm slide 14 hiện tại: **7/10** — sửa 3-4 điểm trên lên 8.5/10.

---

## CẬP NHẬT BẢNG ƯU TIÊN SỬA TỔNG THỂ (Slides 1–14)

| # | Slide | Việc | Tác động |
|---|-------|------|----------|
| 1 | **6** | Tách slide / cắt 21→7 atom | Rất cao |
| 2 | **11** | Cải tổ Hero Equation hoặc Convergence | Rất cao |
| 3 | 4 | Lỗi học thuật "LLM dự báo pixel" | Rất cao |
| 4 | 4 | Mũi tên ngược + 5 màu xuống 4 | Rất cao |
| 5 | 9 | Bỏ alertblock Theorem to → 3 dòng inline | Rất cao |
| 6 | 10 | Redesign aniso/iso (3D shading + bar) | Rất cao |
| 7 | **13** | **Thay sin curves bằng pgfplots histogram thật + Normal overlay** | **Rất cao** |
| 8 | 1 | Thay `[Tên bạn]` | Cao |
| 9 | 8 | Title figure + legend pos | Cao |
| 10 | 7 | Bỏ 2 alertblock/exampleblock → heading | Cao |
| 11 | **14** | **Bỏ resizebox, gộp Theorem 4.3 vào caption** | **Trung bình** |
| 12 | 12 | Bar chart pgfplots + bỏ alertblock "Vấn Đề" | Trung bình |
| 13 | 5 | Thêm hàng "LeJEPA" + cột # HP | Cao |
| 14 | 3 | Vẽ ellipse "không gian embedding" + 2D scatter | Cao |
| 15 | All | Audit box (38 → ≤ 20) | Trung bình–Cao |

---

## NGUYÊN TẮC RÚT RA

### 1. **"Histogram thật ≠ sin curve"**
Nếu vẽ distribution, **đừng dùng `\draw sin/cos`** — phải dùng `pgfplots ybar` hoặc Gaussian curve $e^{-x^2/2}$. Sin curve **đối xứng tuần hoàn** — không phải distribution.

### 2. **"Resizebox = mùi hôi" (đã nêu)**
Slide 14 có `\resizebox` cho EJB formula → **tín hiệu công thức quá dài**. Hoặc:
- Break thành multi-line
- Đơn giản hóa notation (dùng $\sum$ thay vì spell-out 4 term)
- Bỏ chi tiết không cần thiết

### 3. **"Compare visual ≠ side-by-side text"**
Slide 14 nói "moment có shortcut" — nếu **chỉ nói bằng theorem**, khán giả không tin. Nếu vẽ **2 histogram cùng moments** → khán giả thấy ngay.

→ **Bất kỳ khi nào claim một negative result, hãy có 1 visual minh chứng.**

---

> **Slide 13 sau redesign sẽ là 1 trong các slide đẹp nhất của Phần 3 (SIGReg construction).**
> 
> **Cap tiếp slide 15-17 (CDF tests + Epps-Pulley + SIGReg) — đây là core method của paper, cần soi rất kỹ.**

---
---

# ĐỢT 8 — SLIDE 15 (BRAINSTORM SORT VIZ) & SLIDE 16

> **Yêu cầu:**
> - Slide 15: *"Sort operation visualization không được đẹp, nghĩ cách cải thiện. Box choán quá."*
> - Slide 16: *"Tạm ổn nhưng nên feedback để cải thiện thêm."*

---

## SLIDE 15 — "Test 1D Họ CDF: Chính Xác Nhưng Không Differentiable"

### Phân tích screenshot

#### Atom-count
| Vùng | Atom |
|------|------|
| block "Công Thức CDF Test" (formula + 2 bullets) | 4 |
| alertblock "2 Hạn Chế Chính" (2 bullets) | 3 |
| TikZ "Sort Operation" (8 box + arrow + caption) | 4 |
| Takeaway | 1 |
| **Tổng** | **12 atom** |

→ Trên ngưỡng 7-8. Cần cắt.

### Vấn đề figure "Sort Operation Visualization"

#### 1. ❌ Visualization hiện tại không **show vấn đề** — chỉ show "có sort"
8 box + 1 arrow "Sort" + 2 caption (`O(N log N), non-parallel`, `∂(sort)/∂x = undefined`).

→ Khán giả thấy **kết quả sort** (đúng → đẹp), không thấy **tại sao sort là vấn đề**. 

Visual phải chứng minh: sort làm cho (a) **không parallel** và (b) **không differentiable**. Hiện tại chỉ có **caption text** nói điều đó — không có visual proof.

#### 2. ❌ Box plain, không shading — không có hierarchy
4 box `lightgray` left + 4 box `lightgreen` right + 1 mũi tên text "Sort". Quá đơn điệu.

#### 3. ⚠️ Caption "$\partial(\text{sort})/\partial x = \text{undefined}$" technically sai
Sort function khả vi a.e. (almost everywhere), gradient = 0 ngoại trừ tại các điểm tying. Đúng hơn là: "*gradient là step function với jumps tại tied values*" hoặc "*sub-differential, không smooth*".

→ Đối với academic audience, đây là điểm dễ bị challenge.

---

## 🎨 BRAINSTORM 6 IDEA REDESIGN SORT VISUALIZATION

---

### 💡 IDEA 1 — **"GPU Breakdown" Visualization** (show non-parallel)

**Concept:** Vẽ 2 GPU đang xử lý 1 nửa data, sau đó **cần synchronize** để sort toàn bộ. So sánh với operation parallel-friendly.

```
┌──── Sort (XẤU) ────┐         ┌──── Sum (TỐT) ────┐
│                     │         │                     │
│  GPU1: [4.2, 1.1]   │         │  GPU1: [4.2, 1.1]   │
│  GPU2: [3.5, 2.8]   │         │  GPU2: [3.5, 2.8]   │
│                     │         │                     │
│      ⇩ MUST MERGE   │         │   ⇩ INDEPENDENT     │
│      ⛔ bottleneck   │         │   ✓ parallel        │
│                     │         │                     │
│  [1.1,2.8,3.5,4.2]  │         │  GPU1: 5.3          │
│                     │         │  GPU2: 6.3          │
│                     │         │  reduce: 11.6       │
└─────────────────────┘         └─────────────────────┘
```

**Ưu:** Visual chứng minh **trực tiếp** "non-parallel". Có comparison sum (parallel-friendly) → contrast.
**Nhược:** Rộng theo chiều ngang.

---

### 💡 IDEA 2 — **"Discontinuity Demo" Visualization** (show non-differentiable)

**Concept:** Show **3 input arrays** chỉ khác nhau 1 chút, nhưng output sort thay đổi đột ngột tại 1 ngưỡng → minh chứng **gradient jump**.

```
Input:        [4.2, 1.1, 3.5, 2.8]
                          ↑
              x_2 thay đổi nhẹ:
                          
x_2 = 1.1:    Sort → [1.1, 2.8, 3.5, 4.2]
                       ▲ position 1
                       
x_2 = 3.0:    Sort → [2.8, 3.0, 3.5, 4.2]
                            ▲ position 2  ← JUMP!
                       
x_2 = 3.6:    Sort → [2.8, 3.5, 3.6, 4.2]
                                 ▲ position 3 ← JUMP again!

   Position(x_2) = step function
   ∂(sort)/∂x_2 = ∞ tại jumps
```

**Plot bên cạnh:**
```
y = position of x_2 in sorted output
^
|       ┌──── 3
|       │
|   ┌───┘
|   │   2
| ──┘   1
|________________→ x_2
   1.1   3.0   3.6
```

→ Step function với 2 jump → khán giả **thấy** non-differentiable.

**Ưu:** Chứng minh trực quan và toán học. Đẹp về visual (step function).
**Nhược:** Phức tạp về layout — cần 2 panel (input changes + step function).

---

### 💡 IDEA 3 — **"Sorting Network Diagram"** (technical, đẹp)

**Concept:** Vẽ sorting network thực sự — các "wire" với **compare-and-swap** operations. Đây là cách CS classic visualize sort.

```
4.2 ─┬─×──────── 1.1
     │ ╱
1.1 ─┴─×─┬────── 2.8
         │ ╱
3.5 ─×───┴─┬──── 3.5
     │ ╱   │
2.8 ─┴─────┴──── 4.2

Mỗi × = 1 compare-swap operation
Tổng N log N operations theo dependency dọc
```

```latex
\begin{tikzpicture}[every node/.style={font=\tiny}]
  % 4 wires
  \foreach \i in {1,2,3,4} {
    \draw[color=neutral, thick] (0, -\i*0.5) -- (5, -\i*0.5);
  }
  % Input labels
  \node at (-0.4, -0.5) {4.2};
  \node at (-0.4, -1.0) {1.1};
  \node at (-0.4, -1.5) {3.5};
  \node at (-0.4, -2.0) {2.8};
  
  % Comparators (vertical bars connecting 2 wires)
  \draw[primary, very thick] (1.0, -0.5) -- (1.0, -1.0);
  \fill[primary] (1.0, -0.5) circle (3pt);
  \fill[primary] (1.0, -1.0) circle (3pt);
  
  \draw[primary, very thick] (1.5, -1.5) -- (1.5, -2.0);
  \fill[primary] (1.5, -1.5) circle (3pt);
  \fill[primary] (1.5, -2.0) circle (3pt);
  
  \draw[primary, very thick] (2.5, -0.5) -- (2.5, -1.5);
  \fill[primary] (2.5, -0.5) circle (3pt);
  \fill[primary] (2.5, -1.5) circle (3pt);
  
  \draw[primary, very thick] (3.0, -1.0) -- (3.0, -2.0);
  \fill[primary] (3.0, -1.0) circle (3pt);
  \fill[primary] (3.0, -2.0) circle (3pt);
  
  \draw[primary, very thick] (3.8, -1.0) -- (3.8, -1.5);
  \fill[primary] (3.8, -1.0) circle (3pt);
  \fill[primary] (3.8, -1.5) circle (3pt);
  
  % Output
  \node at (5.4, -0.5) {1.1};
  \node at (5.4, -1.0) {2.8};
  \node at (5.4, -1.5) {3.5};
  \node at (5.4, -2.0) {4.2};
  
  % Annotation
  \node[font=\scriptsize, color=bad, align=center] 
    at (2.5, -2.7) {5 compare-swaps\\sequential dependency};
\end{tikzpicture}
```

**Ưu:** Chuyên nghiệp như paper hardware/CS. Show cụ thể "sequential dependency".
**Nhược:** Hơi technical cho audience SSL.

---

### 💡 IDEA 4 — **"Gradient Flow Diagram"** (forward + backward)

**Concept:** Show forward + backward pass cho sort, với **dấu X to** trên backward arrow → không có gradient.

```
Forward:  x_1, x_2, x_3, x_4  ──sort──→  z_1, z_2, z_3, z_4  ──→ Loss
                                                                    
Backward: ∂L/∂x ← ─[ 🚫 ]─── ∂L/∂z                              
                  no gradient
                  flow
```

```latex
\begin{tikzpicture}
  % Forward
  \node[neutralbox] (in) at (0, 0.5) {$x_1, x_2, x_3, x_4$};
  \node[primarybox] (sort) at (3, 0.5) {sort};
  \node[goodbox] (out) at (6, 0.5) {$z_1 \le z_2 \le z_3 \le z_4$};
  
  \draw[->, thick, primary] (in) -- (sort);
  \draw[->, thick, primary] (sort) -- (out);
  \node[font=\scriptsize, color=primary, above=2pt] at (1.5, 0.5) 
    {Forward};
  
  % Backward — dotted, broken
  \draw[<-, dashed, thick, bad] (in.south) -- (1.5, -0.5);
  \node[font=\Huge, color=bad] (block) at (3, -0.5) {⊘};   % 🚫
  \draw[<-, dashed, thick, bad, opacity=0.5] (3.5, -0.5) -- (5.0, -0.5);
  \draw[<-, dashed, thick, bad] (out.south) -- (6, -0.5);
  
  \node[font=\scriptsize, color=bad, below=4pt] at (3, -1.0) 
    {Gradient không lan truyền — sub-gradient = 0 a.e.};
\end{tikzpicture}
```

**Ưu:** Chứng minh **trực tiếp** "sort breaks backprop". Phù hợp với deep learning audience.
**Nhược:** Cần thấy diff với operation differentiable (như mean) để có context.

---

### 💡 IDEA 5 — **"Sequential Timeline"** (show O(N log N))

**Concept:** Visualize **timeline** của các operation với 2 tracks:
- Track parallel (mean/sum): tất cả operation done in 1 step
- Track sort: N log N steps sequential

```
Time:  0       1       2       3       4       5
       │       │       │       │       │       │
Sum:   ████████                                       (1 step)
                                                      
Sort:  █▓ ━━ ▓█ ━━ ▓█ ━━ ▓█ ━━ ▓█ ━━ █▓             (5 steps)
       step1   step2   step3   step4   step5
```

**Ưu:** Direct visualization của "sort tốn thời gian hơn".
**Nhược:** Không show non-differentiable.

---

### 💡 IDEA 6 — **"Permutation as Step Function"** (đẹp + math precise)

**Concept:** Plot **permutation index** $\sigma(x)$ là step function — chứng minh discontinuous nature.

```latex
% pgfplots step function
\begin{axis}[
  width=5.5cm, height=3cm,
  xlabel={$x$ value},
  ylabel={Sorted position $\sigma(x)$},
  ymin=0, ymax=5, xmin=0, xmax=5,
]
  % Step function
  \addplot[bad, thick, const plot mark left] coordinates {
    (1.1, 1) (2.8, 2) (3.5, 3) (4.2, 4)
  };
  
  % Highlight discontinuities
  \draw[bad, dashed] (axis cs:1.1, 1) -- (axis cs:1.1, 0);
  \draw[bad, dashed] (axis cs:2.8, 2) -- (axis cs:2.8, 1);
  \draw[bad, dashed] (axis cs:3.5, 3) -- (axis cs:3.5, 2);
  
  % Annotation
  \node[bad, font=\tiny] at (axis cs:2.5, 4.5) 
    {Step function\\$\Rightarrow$ no smooth gradient};
\end{axis}
```

**Ưu:** **Mathematically precise** — show đúng bản chất "discontinuous step function". Phù hợp audience formal.
**Nhược:** Hơi abstract — cần explain.

---

## 🏆 KHUYẾN NGHỊ CHO SLIDE 15

**Recommend:** Combine **IDEA 1 (GPU Breakdown)** + **IDEA 4 (Gradient Flow)** vào **2 mini-panel stack dọc**.

**Lý do:**
- Slide cần show **2 vấn đề khác nhau** (non-parallel + non-differentiable)
- 2 mini-panel mỗi panel address 1 vấn đề rõ ràng
- Vẫn vừa cột phải

```
┌─── Sort Operation: 2 Vấn Đề ───────────┐
│                                          │
│  Vấn đề 1: Non-parallel                  │
│  ┌────────────────┐                      │
│  │ GPU1   GPU2    │                      │
│  │ ████   ████    │                      │
│  │   ⇩ MUST SYNC  │                      │
│  │ Combined sort  │                      │
│  └────────────────┘                      │
│                                          │
│  Vấn đề 2: Non-differentiable            │
│  ┌────────────────┐                      │
│  │ x → sort → z   │                      │
│  │ ∂L/∂x ← ⊘ ←    │                      │
│  └────────────────┘                      │
└──────────────────────────────────────────┘
```

### Audit box bên trái — bỏ box

Hiện 2 box stack: `block` (formula) + `alertblock` (2 hạn chế).

**Đề xuất:** Giữ 1 box (formula) — chuyển 2 hạn chế thành **caption inline** dưới figure phải:

```latex
\column{0.50\textwidth}
% --- 1 box duy nhất bên trái ---
\begin{block}{Công Thức CDF Test}
  \footnotesize
  \[
  T_w = N\int_{-\infty}^{\infty}(F_N(x) - F(x))^2 w(x)\, dF(x)
  \]
  \begin{itemize}\setlength\itemsep{2pt}
    \item $w(x) = 1 \implies$ Cramér-von Mises
    \item $w(x) = [F(x)(1-F(x))]^{-1} \implies$ Anderson-Darling
  \end{itemize}
\end{block}

\column{0.46\textwidth}
% --- Figure thay thế (idea 1+4) ---
\begin{tikzpicture}...\end{tikzpicture}

% --- 2 hạn chế dưới figure, NO BOX ---
\centering\footnotesize
\textcolor{bad}{\xmark\ Non-parallel} (Multi-GPU sync)\\
\textcolor{bad}{\xmark\ Non-differentiable} (cần relaxation)
```

→ Slide còn 1 box thay vì 2. Visual thoáng.

### Code cho figure đề xuất (Idea 1+4 combined)

```latex
\begin{tikzpicture}[every node/.style={font=\scriptsize}, scale=0.9]
  % ============================================
  % --- VẤN ĐỀ 1: Non-parallel ---
  % ============================================
  \node[font=\footnotesize\bfseries, color=bad] at (0, 1.7) 
    {\xmark\ Non-parallel};
  
  % 2 GPU boxes
  \node[stdbox, fill=neutral!15, draw=neutral!50, 
        minimum width=1.2cm, minimum height=0.5cm] 
    (gpu1) at (-1, 1.0) {GPU 1};
  \node[stdbox, fill=neutral!15, draw=neutral!50,
        minimum width=1.2cm, minimum height=0.5cm] 
    (gpu2) at (1, 1.0) {GPU 2};
  
  % "MUST SYNC" arrow
  \draw[<->, thick, bad] (-0.4, 0.7) -- (0.4, 0.7);
  \node[font=\tiny, color=bad, above=1pt] at (0, 0.7) {sync};
  
  % Bottleneck box
  \node[stdbox, fill=lightred, draw=bad, 
        minimum width=2.5cm, minimum height=0.4cm,
        font=\tiny\bfseries, color=bad]
    at (0, 0.3) {bottleneck};
  
  % ============================================
  % --- VẤN ĐỀ 2: Non-differentiable ---
  % ============================================
  \node[font=\footnotesize\bfseries, color=bad] at (0, -0.6) 
    {\xmark\ Non-differentiable};
  
  % Forward
  \node[lightbluebox, minimum width=0.8cm, minimum height=0.4cm] 
    (x) at (-1.6, -1.2) {$x$};
  \node[primarybox, minimum width=0.8cm, minimum height=0.4cm] 
    (s) at (0, -1.2) {sort};
  \node[goodbox, minimum width=0.8cm, minimum height=0.4cm] 
    (z) at (1.6, -1.2) {$z$};
  
  \draw[->, thick, primary] (x) -- (s);
  \draw[->, thick, primary] (s) -- (z);
  
  % Backward — broken
  \draw[<-, dashed, thick, bad] (x.south) -- ++(0, -0.4) -- (-0.4, -1.8);
  \node[font=\Large, color=bad] at (0, -1.8) {$\oslash$};
  \draw[<-, dashed, thick, bad, opacity=0.4] 
    (0.4, -1.8) -- (1.6, -1.8) -- (z.south);
  \node[font=\tiny, color=bad, below=2pt] at (0, -2.1) 
    {gradient = 0 a.e.};
\end{tikzpicture}
```

### Tổng điểm slide 15 hiện tại: **6/10** — sửa figure + bỏ 1 box → 8/10.

---

## SLIDE 16 — "Epps-Pulley: Stable, Scalable, Provable"

### Đánh giá tổng quan
Bạn nói "tạm ổn" — đúng. Slide quan trọng nhất Phần 3 (introduce method chính), điểm 7/10.

### Vấn đề và cải thiện

#### 1. ⚠️ Math top quá dày — formula EP + 2 định nghĩa = 3 dòng math

Code [slides_v2.tex:899-906](slides_v2.tex#L899):
```latex
\[
EP = N \int_{-\infty}^{\infty} \underbrace{|\hat\phi_X(t) - \phi(t)|^2}_{\text{ECF vs target CF}} 
\underbrace{w(t)}_{\text{Gaussian window}} dt
\]
với $\hat\phi_X(t) = \frac{1}{N}\sum_{j=1}^N e^{itX_j}, \quad \phi(t) = e^{-t^2/2}$
```

→ 1 formula chính + 2 definition phụ = mất ~20% chiều cao slide cho math.

**Fix:** Đặt 2 definition vào **side caption nhỏ** thay vì dòng math thứ hai:

```latex
\begin{center}
  \[
  EP = N \int_{-\infty}^{\infty} \underbrace{|\hat\phi_X(t) - \phi(t)|^2}_{\text{ECF vs CF}} 
  \, \underbrace{e^{-t^2/2}}_{\text{Gaussian window}} \, dt
  \]
  \tiny\color{neutral}
  $\hat\phi_X(t) = \tfrac{1}{N}\sum e^{itX_j}$ (empirical CF)\quad
  $\phi(t) = e^{-t^2/2}$ (CF của $\mathcal{N}(0,1)$)
\end{center}
```

→ Định nghĩa nhỏ hơn, đặt dưới formula chính, đỡ tốn vertical space.

#### 2. ❌ Plot "CF Value" — Empirical CF và Target CF nhìn **giống hệt nhau**

Code [slides_v2.tex:924-925](slides_v2.tex#L924):
```latex
\addplot[color=primary, thick, ...] {exp(-x^2/2)};               % Target
\addplot[color=good, thin, ...] {exp(-x^2/2) + 0.1*sin(deg(5*x))*exp(-x^2/4)};  % Empirical
```

→ 2 đường gần như chồng nhau (sai khác chỉ 0.1·sin·exp).

**Vấn đề:** Khán giả nhìn plot → thấy 1 đường Gaussian → không thấy được "**Empirical noisy quanh Target**" — đây là **toàn bộ ý của slide**.

**Fix A — Tăng noise của Empirical:**
```latex
% Empirical với noise lớn hơn + dot markers
\addplot[color=good, only marks, mark=*, mark size=0.8pt, samples=30, domain=-5:5] 
  {exp(-x^2/2) + 0.05*sin(deg(8*x)) + 0.03*rand};
```

**Fix B — Show 2 plot stack: Empirical histogram + Target curve:**
```latex
% Layer 1: histogram của |ECF|² 
\addplot+[ybar interval, fill=good!30] coordinates {...};
% Layer 2: smooth target curve overlay
\addplot[domain=-5:5, samples=50, color=primary, thick] 
  {exp(-x^2/2)};
```

**Fix C — Thay plot ECF bằng plot khác có ý nghĩa:**
Hiện tại plot CF không add value lắm — bạn có thể thay bằng:
- **Plot |φ(t)| ≤ 1**: minh họa "ECF bị chặn" — đây là core của theorem 4.5.
- **Plot gradient comparison**: EJB (slide 14) gradient explode vs Epps-Pulley gradient bounded.

→ **Recommend Fix C** với plot gradient comparison — cực mạnh cho narrative.

#### 3. ⚠️ alertblock "Bounded Gradient" với 2 inequalities — chiếm cột phải

Code [slides_v2.tex:937-946](slides_v2.tex#L937):
```latex
\begin{alertblock}{Bounded Gradient (Theorem 4.5)}
  \footnotesize
  \[\resizebox{0.9\linewidth}{!}{$
  \left|\frac{\partial EP}{\partial z_i}\right| \leq \frac{4\sigma^2}{N}, \qquad
  \left|\frac{\partial^2 EP}{\partial z_i^2}\right| \leq \frac{C\sqrt{\pi}\sigma^3}{2N}
  $}\]
\end{alertblock}
```

**Vấn đề:**
- `\resizebox` (mùi hôi)
- 2 inequalities phức tạp — chỉ ý "**bounded**" cần communicate

**Fix:** Đơn giản hóa:
```latex
\begin{block}{Theorem 4.5: Bounded Gradient}
  \footnotesize
  $\left|\dfrac{\partial EP}{\partial z_i}\right| \leq \dfrac{4\sigma^2}{N}$
  \\[4pt]
  Gradient bị chặn $O(1/N)$ — **bất kể** distribution của data.
\end{block}
```

Hoặc **bỏ box, đặt inline** dưới plot:
```latex
\textcolor{primary}{\textbf{Theorem 4.5:}} 
$\left|\partial EP / \partial z_i\right| \leq 4\sigma^2/N$
\\
\footnotesize Gradient \& curvature đều \textbf{BỊ CHẶN}.
```

#### 4. 💡 3 bullet "Differentiable / O(N) / DDP-friendly" — có thể visual hơn

Hiện chỉ là 3 dòng text:
```latex
\item[\cmark] Differentiable (ECF là trung bình của $e^{itx}$)
\item[\cmark] $\mathcal{O}(N)$ tính toán (tổng hợp, không cần sort)
\item[\cmark] DDP-friendly (chỉ cần all_reduce)
```

**Fix:** Đổi thành **3 mini-card** ngang (đã làm tốt ở slide 17):
```latex
\begin{tikzpicture}[every node/.style={font=\tiny}, scale=0.85]
  \node[goodbox, minimum width=2.0cm, align=center] (p1) at (0,0) 
    {\cmark\ Differentiable\\(ECF = avg)};
  \node[goodbox, minimum width=2.0cm, align=center] (p2) at (2.6,0) 
    {\cmark\ $\mathcal{O}(N)$ Scale\\(no sort)};
  \node[goodbox, minimum width=2.0cm, align=center] (p3) at (5.2,0) 
    {\cmark\ DDP-friendly\\(\texttt{all\_reduce})};
\end{tikzpicture}
```

→ Visual hơn, dễ scan.

#### 5. ⚠️ Page number "16/3" trong screenshot — possibly bug rendering

Quan sát góc dưới-phải: số trang hiển thị "16/3" thay vì "16/30". Có thể:
- Render bug do `[shrink]` ở slide khác làm vỡ page counter
- Hoặc footer template bị clip

**Check:** chạy `pdflatex slides_v2.tex` 2 lần và xem trang 16 — nếu vẫn "16/3" → có vấn đề frame.

#### 6. 💡 Takeaway có thể đắt hơn

Hiện: *"ECF bị chặn trong $[-1,1] \implies$ gradient không bao giờ explode"*

Đề xuất:
- *"$|e^{itx}| = 1$ — đó là lý do Epps-Pulley bao giờ cũng ổn"*
- *"Trick toán cổ điển (1983) cứu deep learning hiện đại"* (bridge tới timeline thú vị)

### Tổng điểm slide 16 hiện tại: **7/10** — sửa 3 điểm chính lên 8.5/10.

---

## CẬP NHẬT BẢNG ƯU TIÊN SỬA TỔNG THỂ (Slides 1–16)

| # | Slide | Việc | Tác động |
|---|-------|------|----------|
| 1 | 6 | Tách slide / cắt 21→7 atom | Rất cao |
| 2 | 11 | Cải tổ Hero Equation hoặc Convergence | Rất cao |
| 3 | 4 | Lỗi học thuật "LLM dự báo pixel" | Rất cao |
| 4 | 4 | Mũi tên ngược + 5 màu xuống 4 | Rất cao |
| 5 | 9 | Bỏ alertblock Theorem to → 3 dòng | Rất cao |
| 6 | 10 | Redesign aniso/iso (3D shading + bar) | Rất cao |
| 7 | 13 | Histogram thật via pgfplots | Rất cao |
| 8 | **15** | **Sort viz: combine IDEA 1+4 (GPU + Gradient) + bỏ alertblock** | **Cao** |
| 9 | **16** | **Plot ECF noisy hơn HOẶC thay bằng plot gradient comparison** | **Cao** |
| 10 | 1 | Thay `[Tên bạn]` | Cao |
| 11 | 8 | Title figure + legend pos | Cao |
| 12 | 7 | Bỏ 2 alertblock/exampleblock → heading | Cao |
| 13 | 14 | Bỏ resizebox EJB | Trung bình |
| 14 | 12 | Bar chart pgfplots + bỏ alertblock "Vấn Đề" | Trung bình |
| 15 | 5 | Thêm hàng "LeJEPA" + cột # HP | Cao |
| 16 | 3 | Vẽ ellipse "không gian embedding" + 2D scatter | Cao |
| 17 | All | Audit box (38 → ≤ 20) | Trung bình–Cao |

---

## NGUYÊN TẮC RÚT RA TỪ SLIDE 15-16

### "Visualize the **problem**, not the **operation**"

Slide 15 hiện tại: vẽ **sort operation** (input → output array). 
**Tốt hơn:** vẽ **vì sao sort là vấn đề** (GPU sync break, gradient flow break).

→ Quy tắc: **Khi giảng vấn đề, vẽ vấn đề, không vẽ giải pháp.** 

Áp dụng cho mọi slide còn lại:
- Slide 14 (moment unstable): vẽ **gradient explosion plot** (đã làm)
- Slide 12 (high-dim challenge): vẽ **complexity bar chart** (đã làm)
- Slide 18 (curse of dim): vẽ **error bound theorems** (đã làm)

### "Plot phải show diff, không show similarity"

Slide 16: 2 đường CF gần như chồng nhau → **không show được vấn đề**. Plot chỉ value khi 2 đường **khác nhau rõ rệt**:
- 1 đường smooth + 1 đường jagged (nếu so sánh ideal vs noisy)
- 1 đường flat + 1 đường spike (nếu so sánh stable vs unstable)

→ Quy tắc: **Trước khi vẽ plot, hỏi: "Khán giả thấy gì khác nhau giữa 2 curves?"** Nếu không trả lời được → đổi plot.

---

> **Slide 15-16 là core method slides — sau khi cải thiện sẽ là 2 slide đẹp nhất Phần 3.**
> 
> **Cap tiếp slide 17-19 — đây là LeJEPA loss + curse of dim → method climax.**
