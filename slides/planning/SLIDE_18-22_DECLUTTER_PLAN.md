# Plan giảm tải text cho Slides 18–22

> Mục tiêu: cắt số chữ ~40–60% mỗi slide nhưng **giữ nguyên 100% nội dung cần truyền đạt**.
> Nguyên tắc chung: chữ trên slide chỉ giữ *từ khoá + công thức + hình*, phần diễn giải chuyển sang lời nói (speaker notes). Mỗi slide chỉ nên có **1 thông điệp chính**.

Mapping (PDF 34 trang, không có overlay → frame ≈ trang):

| Slide | Frame (dòng .tex) | Tiêu đề hiện tại |
|-------|-------------------|------------------|
| 18 | 1279 | Họ Test 3: ECF — Stable, Scalable, Provable |
| 19 | 1344 | SIGReg: Đưa Embedding Về N(0,I) Ở Chi Phí O(N) |
| 20 | 1440 | SIGReg: Định Nghĩa Chính Thức và Cài đặt |
| 21 | 1519 | LeJEPA: Một Công Thức, Một Siêu Tham Số |
| 22 | 1662 | λ: Nút Điều Chỉnh Duy Nhất |

---

## Vấn đề xuyên suốt (chẩn đoán)

1. **Trùng lặp giữa slide 18 và 19.** Cả hai đều giải thích ECF, công thức EP, "Định lý 4 / bounded gradient", và "Differentiable + O(N) + DDP". Định lý 4 xuất hiện **2 lần** (slide 18 ở primarybox, slide 19 ở goodbox). Đây là nguồn dư thừa lớn nhất.
2. **Quá nhiều box văn xuôi.** Mỗi slide có 3–4 box (`primarybox`/`goodbox`/`accentbox`) chứa câu hoàn chỉnh — nên rút thành gạch đầu dòng/từ khoá.
3. **Diễn giải "tại sao" nằm trên slide** thay vì trong lời nói (vd "Tại sao average thay vì max?", "Hai lý do thắng curse", phần scaling law).
4. **Chú thích lặp ý của hình** (vd mô tả lại histogram khớp/không khớp đã thể hiện bằng ✓/✗).

---

## Slide 18 — Họ Test 3: ECF

**Thông điệp duy nhất giữ lại:** `|e^{itx}| = 1` ⇒ loss bị chặn, differentiable, O(N), song song hoá.

**Cắt:**
- Bỏ `primarybox` "Định lý 4: Bounded Gradient" — **dời sang slide 19** (nơi có công thức EP đầy đủ), tránh lặp 2 lần.
- Câu "Gradient tự nhiên từ trung bình, không cần phép sort" → rút còn `Differentiable (không cần sort)`.
- Câu "Song song hoá dễ dàng qua all_reduce" → rút còn `O(N) · DDP qua all_reduce`.
- Câu mở đầu "so sánh phân phối qua miền tần số… tính trung bình các sóng" → 1 dòng: `EP so khớp phân phối trên miền tần số (ECF)`.

**Giữ:** biểu đồ TikZ CF vs ECF (đắt giá, trực quan) + 3 bullet ✓ ngắn + takeaway.

**Layout đề xuất:** trái = hình; phải = 3 dòng ✓ (Differentiable / O(N)+DDP / Bounded gradient → forward sang slide sau). Takeaway giữ nguyên.

**Speaker notes (chuyển khỏi slide):** vì sao `|e^{itx}|=1` cho ổn định; cơ chế all_reduce; ý nghĩa exploding gradient.

---

## Slide 19 — SIGReg O(N) (Cramér-Wold sketching)

**Thông điệp duy nhất:** Test K-chiều O(N²) → chiếu xuống M hướng 1D ngẫu nhiên (Cramér-Wold) → trung bình EP. O(N).

**Cắt mạnh (cột phải đang lặp slide 18):**
- Bỏ goodbox "Định lý 4" trùng (chỉ giữ ở 1 slide — đề xuất giữ tại đây vì có công thức EP).
- Bỏ box "SIGReg = trung bình EP… O(N)·differentiable·DDP" — 3 tính chất này đã/đang nói ở slide 18; ở đây chỉ cần 1 dòng định nghĩa.
- accentbox "M=16 đủ nhờ tính trơn DNN + SGD resampling" → **dời sang lời nói** (hoặc gộp vào slide 22 phần default config); không cần ở đây.
- Dòng "φ̂_X(t) = … luôn nằm trong [−1,1]" → giữ ngắn dạng chú thích công thức.

**Giữ:** công thức Cramér-Wold + hình blob→3 projection→histogram (ngôi sao của slide) + 1 dòng công thức EP.

**Layout đề xuất:** trái = công thức Cramér-Wold + hình; phải chỉ còn 2 thứ: công thức EP (kèm chú thích [−1,1]) và 1 box "Định lý 4: gradient ≤ 4σ²/N".

> **Quyết định gộp (khuyến nghị):** Slide 18 và 19 chồng lấn ~50%. Cân nhắc **gộp thành 1 slide** "ECF → SIGReg": hình ECF nhỏ + công thức EP + hình sketching + 3 tính chất. Nếu giữ 2 slide riêng thì phải phân vai rõ: **18 = vì sao ECF tốt (tính chất)**, **19 = mở rộng lên K-chiều (sketching)**, tuyệt đối không lặp Định lý 4 / bộ ba tính chất.

---

## Slide 20 — SIGReg: Định nghĩa chính thức + code

**Thông điệp duy nhất:** Định nghĩa hình thức + "50 dòng PyTorch" là toàn bộ implementation.

**Cắt:**
- Sơ đồ 3 box "Differentiable / O(N) / Provably" → **bỏ** (đã xuất hiện ở slide 18–19; ở đây thừa).
- Đoạn "Tại sao average thay vì max? Max ⇒ gradient sparse… Average ⇒ dense, ổn định hơn" → **dời sang speaker notes**, trên slide chỉ để 1 chú thích nhỏ: `dùng average → gradient dense`.
- Code: giữ nguyên (code là điểm nhấn "đơn giản"), nhưng **xoá khối comment LaTeX chết** (dòng 1500–1511) cho file sạch.

**Giữ:** accentbox Định nghĩa 2 (công thức SIGReg) + code 50 dòng.

**Layout đề xuất:** trái = Định nghĩa 2 + 1 dòng "average → dense gradient"; phải = code. Gọn, 2 khối lớn.

---

## Slide 21 — LeJEPA: Một công thức, một siêu tham số

**Thông điệp duy nhất:** 1 loss = (1−λ)·Invariance + λ·SIGReg; so với DINO/I-JEPA cực kỳ đơn giản.

**Nhận xét:** slide này tương đối ổn (chủ yếu là hình + bảng). Chỉ tinh chỉnh nhẹ:
- Bảng so sánh: giữ nguyên (đây là phần "đắt" nhất, truyền tải mạnh).
- Sơ đồ pipeline: giữ.
- Không cần thêm chữ. Có thể bỏ chú thích nhỏ trùng nếu có.

**Speaker notes:** giải thích từng dòng bảng (stop-gradient, teacher-student) bằng lời.

> Slide này **ưu tiên thấp** — đã gần đạt mục tiêu, đụng vào ít.

---

## Slide 22 — λ: Nút điều chỉnh duy nhất

**Thông điệp duy nhất:** λ là siêu tham số duy nhất, robust trong [0.01, 0.1], sweet spot ≈ 0.05.

**Cắt:**
- primarybox "Thiết lập mặc định" (5 dòng config) → nén thành **1 dòng** hoặc bảng mini: `λ=0.05 · V=2g+6l · bs≥128 · M=1024 · 17 pts, t∈[−5,5]`.
- goodbox "λ robust… Figure 8… không cần grid search" → rút còn `Robust: λ∈[0.01, 0.1] (Fig.8)`.
- Đoạn "Scaling law với số views: peak λ tỉ lệ thuận với V…" → **dời sang speaker notes** (đây là chi tiết phụ, không phải thông điệp chính).

**Giữ:** hình spectrum (0 → sweet spot → 1) + đồ thị parabol accuracy vs λ (rất trực quan).

**Layout đề xuất:** trái = 2 hình; phải chỉ còn: 1 dòng config + 1 dòng robustness. Thoáng hẳn.

---

## Tổng kết hành động (ưu tiên)

| Ưu tiên | Việc | Tác động |
|---------|------|----------|
| ★★★ | Khử trùng lặp 18↔19 (Định lý 4 + bộ ba tính chất chỉ xuất hiện 1 lần) | Giảm text nhiều nhất; cân nhắc gộp 2 slide |
| ★★★ | Slide 22: nén config box + dời scaling law sang notes | Slide thoáng rõ rệt |
| ★★ | Slide 20: bỏ sơ đồ 3-box thừa + dời "average vs max" sang notes + xoá comment chết | Gọn, đỡ nhiễu |
| ★★ | Đổi mọi box văn xuôi → gạch đầu dòng/từ khoá | Đồng bộ toàn deck |
| ★ | Slide 21: chỉ tinh chỉnh nhẹ | Đã gần đạt |

**Quy ước áp dụng cho cả 5 slide:**
- Mỗi box tối đa 1 dòng; câu giải thích "tại sao" → speaker notes.
- Không lặp lại thông tin đã nói ở slide trước (đặc biệt bộ ba *differentiable / O(N) / provable*).
- Chú thích hình không mô tả lại điều hình đã thể hiện.
- Giữ toàn bộ TikZ/đồ thị/bảng — đó là phần "đậm đặc thông tin mà ít chữ".
