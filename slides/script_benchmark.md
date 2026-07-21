# Script thuyết trình — "Kết quả" + "Nghiên cứu mở rộng"

**Tổng thời lượng mục tiêu: ~6 phút** (Kết quả ~2:45, Nghiên cứu mở rộng ~3:15).
---

## PHẦN A — KẾT QUẢ (~2 phút 45)

### A0. Câu mở phần (nói trước khi vào slide đầu)

"Phần lý thuyết vừa rồi cho ta một mục tiêu duy nhất là SIGReg. Bây giờ ta kiểm chứng bằng thực nghiệm: **(1)** pipeline có tái lập được đúng như paper không, và **(2)** LeJEPA có thật sự *ổn định trên mọi siêu tham số* như tác giả tuyên bố không — đây là 3 ablation A, B, C của nhóm."

---

### A1. Frame "Reproduce — ViT-B/16, 5 epoch trên ImageNet-1K"

Chuyển sang phần thực nghiệm. Đầu tiên, nhóm tái lập lại pipeline gốc: huấn luyện ViT-B/16 from scratch trên ImageNet-1K, 5 epoch, với  đúng cấu hình paper: $\lambda=0.05$, 1024 slices, 2 global và 4 local view, AdamW ở bf16.

Đánh giá bằng **linear probe trên backbone đóng băng**: đóng băng encoder, chỉ huấn luyện một lớp tuyến tính phía trên, rồi transfer sang **8 bộ dữ liệu**.
Ở mức few-shot (1/10 sample mỗi lớp) và full (toàn bộ tập train), hành vi khớp đúng paper: loss hội tụ mượt, các lớp thô như Flower, CIFAR học được sớm còn fine-grained cần pretrain lâu hơn.

`[chuyển slide]`

---

### A2. Câu OVERVIEW cho cả A, B, C (nói trước khi vào Ablation A)

**Settings baseline của ablation:**
- Dữ liệu: Imagenette (imagenet10)

- Backbone: ViT-S/16 · 100 epoch · batch 512 · AdamW lr 5e-4, wd 0.05 · bf16.
- Mục tiêu: Epps-Pulley 1000 slice, t_max 3.0, 17 điểm; λ = 0.05; projector MLP (phi tuyến) dim 512; không predictor, không teacher-student; 8 view (2 global 224 + 6 local 96).
- Eval: đúng recipe paper — frozen backbone, concat CLS 2 block cuối + LayerNorm, linear probe AdamW lr 1e-3 wd 1e-6, 100 epoch.

Nhóm chạy 8 ablation, gộp thành A/B/C. Do **giới hạn tài nguyên**, nhóm không chạy hết bảng ablation của paper — register token thì timm trong môi trường này không hỗ trợ, batch size và embedding-dim thì chưa chạy.

**Nhưng những cái bỏ qua đều là các nút mà paper chỉ dùng để chứng minh "nút này không quan trọng".** Còn 8 ablation đã chạy thì **phủ trọn những kết luận cốt lõi mà paper deliver**:
- **Siêu tham số nội tại của SIGReg có thật sự trung tính không** → Epps-Pulley (integration range, quadrature points, slices) và số view.
- **Các nguyên tắc thiết kế** → SIGReg đặt ở đâu, projector có cần phi tuyến không, có cần predictor không, gộp token thế nào.

Ngoài ra nhóm còn **mở rộng thêm vài nút paper chưa đụng**: patch-masking, drop-path, aggregator. 



---

### A3. Frame "Ablation A — Siêu tham số của mục tiêu học"

Câu hỏi ở đây là: SIGReg nhạy đến đâu với lưới tích phân của Epps-Pulley, và cần bao nhiêu view để huấn luyện tốt?

Nhóm quét toàn bộ 27 cấu hình Epps-Pulley — ba mức integration range, ba mức số slices, ba mức số quadrature points. 

Cấu hình tốt nhất đạt 70.1%, nhưng điều thú vị là chỉ có **số slices** thực sự tạo khác biệt: cứ tăng từ 512 lên 4096 slices là top1 tăng đều, bất kể các tham số khác. 

Còn integration range hay số quadrature points thì gần như ổn định - khớp paper.

Về số view, kết quả ngược với trực giác thông thường: càng ít view lại càng tốt trong setup này — 4 view đạt 72.8%, rồi giảm dần khi tăng lên 6, 8, 10 view.

**Takeaway**: chỉ `num_slices` là đòn bẩy thật sự; số quadrature points hay integration range gần như trung tính. Một số khác biệt về tính ổn định của tham số là do nhóm ablation trên dữ liệu và backbone nhỏ hơn. 

`[chuyển slide]`

---

### A4. Frame "Ablation B — Thành phần kiến trúc"

Trả lời các câu hỏi: "SIGReg đặt trên projection hay embedding, projector tuyến tính hay phi tuyến, có cần predictor không?"

Kết quả rất dứt khoát. Áp SIGReg lên projection cho 59.5%, nhưng áp thẳng lên embedding thô thì collapse. 

Với projector, nếu dùng projector tuyến tính đơn giản thì mô hình sụp hẳn xuống hơn 23%. 

Thêm predictor cũng không giúp gì — không dùng predictor vẫn là lựa chọn tốt nhất - trùng với phát hiện của paper.

Và cách gộp token cũng đơn giản: dùng CLS token một mình đã tốt ngang việc kết hợp CLS với mean pooling, còn chỉ dùng mean thì kém hơn hẳn.

**Takeaway**: đặt SIGReg đúng chỗ, cộng với projector phi tuyến, là tự nó đã đủ chống collapse — không cần thêm predictor.

`[chuyển slide]`

---

### A5. Frame "Ablation C — Regularization kiểu augmentation"

Câu hỏi cuối trong loạt ablation này: tỉ lệ patch-masking nào là tối ưu, và LeJEPA có nhạy với stochastic depth không? — **hai nút này paper KHÔNG ablate; đây là phần nhóm mở rộng thêm.**"

Patch masking — ngẫu nhiên che/bỏ đi một tỉ lệ patch token trước khi đưa vào ViT (vd ratio=0.3 = giấu 30% số patch), ép model đoán nội dung ảnh từ phần còn lại.

Stochastic depth (drop-path) — ngẫu nhiên bỏ qua nguyên một residual block lúc train (vd rate=0.1 = mỗi block có 10% khả năng bị nhảy cóc), khiến mạng train với độ sâu hiệu dụng ngẫu nhiên.

Kết quả khá bất ngờ — cả hai kỹ thuật đều đạt đỉnh khi **tắt hoàn toàn**. Patch-mask ratio bằng 0 cho kết quả tốt nhất, càng tăng tỉ lệ mask thì top1 càng giảm nhẹ. Drop-path cũng vậy: rate 0 là tốt nhất, tăng dần rate thì hiệu năng giảm dần, thấp nhất khi drop-path ở mức cao.

Lý do nằm ở quy mô dữ liệu: trong chế độ low-data như Imagenette, mô hình chưa hề rơi vào tình trạng overfit, nên các kỹ thuật regularization vốn được thiết kế để chống overfit lại chỉ làm mất thông tin một cách vô ích.

**Takeaway**: trái với kỳ vọng, tắt mask và drop-path lại tốt nhất — vì ở quy mô dữ liệu này mô hình chưa bao giờ overfit.

---

## PHẦN B — NGHIÊN CỨU MỞ RỘNG: LEO BENCHMARK IMAGENETTE (~3 phút 15)


### B1. Frame "Câu hỏi nghiên cứu: headroom còn nằm ở đâu?"

Sang phần cuối: đây là phần nghiên cứu mở rộng của riêng nhóm, thử leo benchmark Imagenette hơn nữa.

Câu hỏi đặt ra là: còn dư địa cải thiện ở đâu?

Nhóm đặt song song hai giả thuyết, cả hai cùng xuất phát từ baseline 89.5% đó. Giả thuyết thứ nhất là cải thiện nằm ở objective hoặc representation head — thêm tín hiệu hình học, hoặc đổi cách thiết kế projector, có thể giúp SIGReg tốt hơn.

Giả thuyết thứ hai là nút nghẽn thực ra không nằm ở mục tiêu huấn luyện, mà ở dynamics của optimizer hoặc ở phần stem đầu vào của ViT.

Baseline: ViT-S - 100 epochs 

Tất cả kết quả sau đây đều dùng chung một giao thức đánh giá: đóng băng encoder, ghép CLS token của hai block cuối cùng rồi chuẩn hóa bằng LayerNorm, train linear probe bằng AdamW, rồi so top1 và mức chênh lệch so với baseline.


`[chuyển slide]`

---

### B2. Frame "Hướng 1: Objective và projection head"

Hướng 1 — nhóm thử thêm tín hiệu hình học vào mục tiêu: một số **uniformity loss**, đổi normalization bằng **DynTanh**, và thêm **coding-rate** (log-det)."
- DynTanh là...
- coding-rate là ...
- uniformity loss là ...
**Đọc kết quả:**
"Kết quả: **không idea nào vượt baseline rõ ràng.**

Uniformity (Wang & Isola) — chuẩn hóa các vector về mặt cầu đơn vị rồi phạt khi chúng nằm chụm lại (log E[exp(−t·‖zᵢ−zⱼ‖²)]), tức đẩy các điểm ra xa nhau cho trải đều trên mặt cầu.

Coding-rate (MCR2) — đo "thể tích" mà biểu diễn chiếm trong không gian bằng log-det của ma trận hiệp phương sai (0.5·logdet(I + d/ε²·Cov(Z))), rồi cộng dấu âm của nó vào loss để ép model trải rộng, chiếm nhiều chiều nhất có thể.

Cả hai đều là cách chống collapse bằng hình học — một cái đẩy điểm ra xa trên mặt cầu, một cái phình thể tích của đám mây điểm — và đó chính là lý do chúng thất bại: SIGReg vốn đã ép phân phối về N(0,I), tức đã làm sẵn cả hai việc đó rồi. Uniformity thành thừa (≈ baseline), còn coding-rate thì log-det quá mạnh, lấn át SIGReg và gây collapse.

DynTanh (Dynamic Tanh) — một lớp normalization "giả" không dùng thống kê batch, chỉ bóp giá trị qua hàm tanh với biên độ học được: γ · tanh(α · x) + β, dùng để thay thẳng BatchNorm/LayerNorm (Zhu et al., CVPR 2025).

Ý tưởng: thay vì chuẩn hóa bằng cách đo mean/variance của batch rồi chia (như BatchNorm), thì cứ ép giá trị vào khoảng bão hòa của tanh — α học độ dốc, γ/β học lại thang đo. Rẻ hơn, không phụ thuộc batch.

Trong LeJEPA nó thất bại đúng vì lý do đó: SIGReg cần phân phối đầu vào đã được chuẩn hóa thật sự (mean 0, var 1) — thứ mà BatchNorm cung cấp miễn phí. tanh chỉ bóp giá trị chứ không chuẩn hóa, nên interface projector–SIGReg bị hỏng → hội tụ chậm ~8 lần và không bao giờ đuổi kịp baseline.

`[chuyển slide]`

---

### B3. Frame "Insight hướng 1: SIGReg + MLP projector là điểm cân bằng"

Cả hai cách can thiệp thất bại ở Hướng 1 đều nhắm đúng vào điểm nút projector này: đổi normalization thì DynTanh thất bại, còn thêm geometry phụ quá mạnh thì coding-rate gây collapse. Điều đó cho thấy cấu hình hiện tại — SIGReg cộng MLP projector — không phải ngẫu nhiên mà đã ở một điểm cân bằng khá mong manh.

**Takeaway**: objective và projector phải được thiết kế cùng nhau, không thể coi loss phụ trợ là một thành phần rời rạc rồi lắp vào tùy ý.

`[chuyển slide]`

---

### B4. Frame "Hướng 2: Optimizer và training geometry"


Hướng thứ hai: giữ nguyên kiến trúc ViT-S, chỉ đổi optimizer và training dynamics.

Nhìn chung bức tranh khá ảm đạm. Vài phương pháp nhích nhẹ trên baseline nhưng phần lớn các can thiệp còn lại đều sụt: SWA, QK-Norm, deep-supervision sụt nhẹ; còn nhóm thay hẳn optimizer — Schedule-Free, LLRD, Muon — thì sụt rất mạnh, có phương pháp mất tới hơn 3 điểm phần trăm so với baseline.

**Takeaway**: trên một ViT-S cố định, các can thiệp vào dynamics không mở ra headroom ổn định nào cả; công thức AdamW cộng cosine schedule vẫn là một cái neo rất khó đánh bại.

`[chuyển slide]`

---

### B5. Frame "Conv-stem: architecture co-design riêng"

Và đây là kết quả đáng chú ý nhất của toàn bộ phần mở rộng. 
Thay vì đổi objective hay optimizer, nhóm thử đổi hẳn kiến trúc đầu vào: 

Nhóm thay **patchify stride-16** bằng một **stem 4 lớp conv** — trick 'early convolutions help transformers' của Xiao 2021 — giữ nguyên phần ViT body."

Kết quả: top1 nhảy từ 89.49% với patchify lên 92.08% với conv-stem — tăng gần 2.6 điểm phần trăm, mức cải thiện lớn nhất trong toàn bộ phần mở rộng.

Nhưng cải thiện này đến từ inductive bias của backbone, chứ chưa phải bằng chứng rằng objective LeJEPA tốt hơn.

**Takeaway**: headroom thật sự đang nằm ở kiến trúc đầu vào (input architecture) — không phải ở objective hay optimizer.

