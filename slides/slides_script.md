# Script Trình Bày — LeJEPA
*Provable & Scalable Self-Supervised Learning — Without the Heuristics*
*Balestriero & LeCun, arXiv:2511.08544*

---

## Slide 1 — Title

Xin chào mọi người. Hôm nay mình sẽ trình bày về bài báo **LeJEPA** của Randall Balestriero và Yann LeCun, công bố năm 2025.

Tiêu đề đầy đủ là *"Provable & Scalable Self-Supervised Learning — Without the Heuristics"*. Câu "without the heuristics" — không cần heuristic — là điểm nhấn trung tâm của toàn bộ bài báo.

Ở bên phải là sơ đồ minh họa ý tưởng cốt lõi: ảnh đầu vào được đưa qua encoder $f_\theta$, và các embedding đầu ra nằm trên một vòng tròn — đại diện cho phân phối Gaussian đẳng hướng $\mathcal{N}(0, I)$. Đây chính là mục tiêu mà LeJEPA hướng tới.

---

## Slide 2 — Nội Dung Trình Bày

Bài trình bày được chia làm 4 phần chính theo cấu trúc **WHAT → WHY → HOW → RESULTS**.

- **Phần 1 — WHAT**: định nghĩa bài toán học biểu diễn là gì.
- **Phần 2 — WHY**: tại sao JEPA và các phương pháp SSL hiện tại thất bại — cụ thể là vấn đề collapse.
- **Phần 3 — HOW**: LeJEPA giải quyết từ gốc rễ như thế nào, thông qua lý thuyết và SIGReg.
- **Phần 4 — RESULTS**: kết quả thực nghiệm trên nhiều benchmark và kiến trúc.

Một câu tóm tắt cho toàn bộ bài: *"LeJEPA tối giản hóa self-supervised learning bằng nền tảng lý thuyết vững chắc."*

---

## Slide 3 — Thuật Ngữ Trọng Tâm

Trước khi đi vào nội dung, mình dành một phút để giới thiệu 5 thuật ngữ sẽ xuất hiện thường xuyên.

**Anisotropic / Isotropic** — bất đẳng hướng có nghĩa là dữ liệu trải dài không đều theo các hướng; đẳng hướng có nghĩa là phân bố đều mọi hướng. Phân biệt này là chìa khóa lý thuyết của bài báo.

**SSL** — Self-Supervised Learning, học tự giám sát, không cần nhãn.

**Random projection** — chiếu dữ liệu nhiều chiều xuống 1 chiều theo một hướng ngẫu nhiên. SIGReg dùng kỹ thuật này là nền tảng.

**Decision boundary** — ranh giới phân tách các lớp dữ liệu khi ta áp dụng một classifier. Phân phối embedding ảnh hưởng trực tiếp đến độ ổn định của ranh giới này.

**Exploding gradients** — bùng nổ đạo hàm khiến model không huấn luyện được. Đây là lý do tại sao họ test Moments bị loại.

---

## Slide 4 — [WHAT] Mục Tiêu: Encoder Ánh Xạ Thế Giới Vào Không Gian Có Ý Nghĩa

Bài toán trung tâm của self-supervised representation learning là tìm một ánh xạ $f_\theta : \mathbb{R}^D \to \mathbb{R}^K$ — trong đó $D$ là chiều dữ liệu thô và $K$ là chiều không gian embedding — sao cho vector biểu diễn $\mathbf{z} = f_\theta(\mathbf{x})$ **có ích cho đa dạng downstream task** mà không cần nhãn trong quá trình huấn luyện.

Nói chính xác hơn: ta muốn $f_\theta$ tốt theo nghĩa *universal* — tức là một lớp tuyến tính đơn giản phủ lên $\mathbf{z}$ là đủ để giải quyết bất kỳ task nào, không cần thay đổi $\theta$.

Sơ đồ bên trái minh họa điều này: encoder $f_\theta$ nhận đầu vào thô — ảnh, video, văn bản — và ánh xạ vào không gian $\mathbb{R}^K$ sao cho các điểm có cùng ngữ nghĩa tụ thành cụm riêng biệt. Ví dụ: "cat" hội tụ về một vùng, "dog" hội tụ về vùng khác, "sky" về vùng khác nữa.

Một encoder $f_\theta$ đạt chất lượng này có thể phục vụ nhiều downstream task — phân loại, segmentation, few-shot learning, retrieval — chỉ bằng cách gắn thêm một đầu tuyến tính phía trên mà không cần fine-tune tham số $\theta$.

Đây chính là định nghĩa của **foundation model**: *"một hệ thống giải được nhiều downstream task sau khi huấn luyện một lần, không thay đổi tham số $\theta$."* Câu hỏi căn bản của bài báo là: $f_\theta$ cần thỏa mãn điều kiện gì để đạt tính chất đó theo nghĩa *provably optimal*?

---

## Slide 5 — JEPA: Dự Đoán Trạng Thái Trừu Tượng — Không Phải Pixel

JEPA — Joint-Embedding Predictive Architecture — là cơ chế SSL mà LeJEPA xây dựng lên.

Ý tưởng: từ một ảnh gốc, ta tạo ra hai "view" — ví dụ crop khác nhau, mask, blur, hoặc frame liền kề trong video. Cả hai view đi qua cùng một encoder $f_\theta$ để ra hai latent vector $z_1$ và $z_2$. Sau đó, một "predictor" cố gắng dự đoán $\hat{z}_1$ từ $z_2$. Loss là khoảng cách giữa $z_1$ và $\hat{z}_1$.

Điểm khác biệt căn bản so với auto-encoder nằm ở **không gian mà loss được tính**. Auto-encoder tối thiểu hóa $\|\mathbf{x} - \hat{\mathbf{x}}\|^2$ — tức là buộc model phải tái tạo từng pixel, bao gồm cả texture, nhiễu, ánh sáng — những thứ không liên quan đến ngữ nghĩa. JEPA thay vào đó tối thiểu hóa $\|z_1 - \hat{z}_1\|^2$ **hoàn toàn trong không gian latent**: predictor nhận $z_2$ và phải dự đoán $z_1$ — tức là dự đoán *cấu trúc ngữ nghĩa mà view 1 mã hóa*, không phải *view 1 trông ra sao*. Điều này buộc encoder $f_\theta$ phải học các đặc trưng bất biến với augmentation — danh tính lớp, cấu trúc hình học, quan hệ đối tượng — trong khi được tự do bỏ qua các chi tiết pixel-level không có giá trị dự đoán.

Tuy nhiên, bài toán dự đoán này có một **nghiệm tầm thường nguy hiểm** mà ta sẽ thấy ngay sau đây.

---

## Slide 6 — [WHY] Collapse — Khi Encoder Học Cách "Gian Lận"

Vấn đề nan giải nhất của JEPA là **collapse** — encoder học cách gian lận để giảm loss mà không học được gì thực sự.

Tại sao? Vì cực tiểu hóa $\|z_1 - \hat{z}_1\|^2$ có nghiệm hiển nhiên: ánh xạ **mọi input** về cùng một điểm. Loss về 0, nhưng encoder hoàn toàn vô dụng.

Có hai dạng collapse:

- **Complete collapse** — bên trái: mọi ảnh đều cho ra cùng một vector $\mathbf{c}$, tức là $f_\theta(\mathbf{x}) = \mathbf{c}$ với mọi $\mathbf{x}$. Loss về 0 tầm thường, nhưng mọi thông tin về input bị xóa hoàn toàn.

- **Dimensional collapse** — bên phải: embedding không về một điểm, nhưng toàn bộ dữ liệu bị dồn vào một **vùng chỉ chiếm $r$ chiều** bên trong không gian $K$ chiều ($r \ll K$). Hình dung cụ thể: ta có không gian 1024 chiều, nhưng encoder chỉ thực sự sử dụng 10 chiều — 1014 chiều còn lại luôn bằng 0 với mọi input. Về mặt đại số tuyến tính, điều này có nghĩa là covariance matrix $\Sigma = \mathbb{E}[\mathbf{z}\mathbf{z}^\top]$ **rank-deficient**: chỉ có $r$ trị riêng dương, còn $K - r$ trị riêng bằng 0. Encoder "lười" theo nghĩa tối ưu — nó tìm ra $r$ hướng đủ để minimize loss và không bao giờ đẩy thông tin ra ngoài $r$ hướng đó, vì loss không phạt điều này. Hệ quả: hai ảnh rất khác nhau về ngữ nghĩa — ví dụ một con mèo và một chiếc xe — có thể có embedding gần hệt nhau nếu sự khác biệt giữa chúng nằm ở chiều thứ 11 trở đi vốn đã bị encoder bỏ qua. Linear probe hay kNN nhìn vào toàn bộ $K$ chiều đó sẽ không phân biệt được hai ảnh này — không phải vì classifier yếu, mà vì thông tin phân biệt không tồn tại trong embedding ngay từ đầu.

Vấn đề sâu hơn: không có lý thuyết nào chỉ ra *chính xác* rank mục tiêu phải là bao nhiêu, hay phân phối nào trên $\mathbb{R}^K$ là tối ưu cho downstream task. Đây là câu hỏi mà LeJEPA sẽ trả lời.

---

## Slide 7 — Literature: Mỗi Phương Pháp Vá Một Lỗ Hổng Mới

Năm năm qua, cộng đồng liên tục đề xuất giải pháp cho collapse — nhưng mỗi giải pháp chỉ vá một lỗ hổng rồi tạo ra lỗ hổng khác. Không ai dừng lại để hỏi: *tại sao collapse lại là vấn đề? Embedding nên trông như thế nào?*

- **SimCLR (2020)** — negative pairs ngăn collapse, nhưng cần batch $\mathcal{O}(N^2)$ — không scale lên millions of samples.

- **BYOL (2020)** — loại bỏ negative pairs bằng kiến trúc bất đối xứng (EMA). Hoạt động thực nghiệm, nhưng **không ai biết tại sao** — sau nhiều năm phân tích vẫn không có lý thuyết hoàn chỉnh. Không biết tại sao → không biết khi nào sẽ thất bại.

- **DINO (2021)** — kết quả ấn tượng trên ViT, nhưng để đạt được đó cần tune ≥7 hyperparameter tương tác lẫn nhau. Transfer sang domain mới là một grid search tốn kém.

- **VICReg (2022)** — cố gắng có lý thuyết: ép covariance gần identity. Nhưng **chỉ ràng buộc 2 moment đầu** — encoder có thể shortcut bằng phân phối non-Gaussian miễn là mean và variance đúng, mà vẫn cho downstream performance kém.

- **I-JEPA (2023)** — JEPA thuần túy trong latent space, stop-gradient ngăn collapse. Kết quả tốt trên ViT, nhưng stop-gradient là heuristic không có lý thuyết bảo đảm, và kiến trúc phụ thuộc vào attention của ViT — kết quả kém hơn đáng kể trên ResNet hay ConvNeXt.

Mỗi dòng trên đều là một **empirical patch** — giải quyết triệu chứng chứ không trả lời câu hỏi gốc.

**Đây chính là khoảng trống mà LeJEPA lấp đầy**: lần đầu tiên, thay vì thiết kế thêm một trick mới để tránh collapse, LeJEPA hỏi ngược lại — *"embedding tối ưu phải phân phối như thế nào?"* — và chứng minh câu trả lời bằng toán học. Từ đó, collapse không còn là thứ cần "vá" mà là hệ quả tự nhiên của việc tối ưu đúng mục tiêu.

---

## Slide 8 — [HOW] Phân Phối Nào Là Tối Ưu Cho Foundation Model?

Đây là slide trung tâm về lý thuyết. LeJEPA đặt câu hỏi: với downstream task dạng linear probe — ridge regression — thì embedding nào cho kết quả tốt nhất?

Nhìn vào hai hình minh họa:

**Bên trái — anisotropic**: embedding trải dài chủ yếu theo một hướng, các trị riêng $\lambda_1 \gg \lambda_2 \approx \lambda_3$. Ridge estimator sẽ co mạnh những hướng yếu, gây ra bias và variance cao.

**Bên phải — isotropic**: embedding là một hình cầu, tất cả các hướng đều bằng nhau, bias và variance đều thấp nhất.

Bài báo chứng minh hai bổ đề: anisotropy làm tăng cả bias lẫn variance. Và từ đó suy ra **Định lý 1**: $\mathcal{N}(0, I)$ là điểm cực tiểu **duy nhất** của worst-case downstream risk — không chỉ cho linear probe mà còn cho kNN và kernel regression.

Đây là lần đầu tiên trong lịch sử SSL có một kết quả lý thuyết chỉ ra chính xác target distribution.

---

## Slide 9 — Bổ Đề 1: Anisotropy Làm Tăng Bias

Bổ đề 1 giải thích tại sao anisotropy gây ra bias cao hơn.

Khi ridge regularizer co các hướng theo công thức $(\Lambda + \lambda I)^{-1}$, hướng nào có trị riêng $\lambda_k$ nhỏ — tức là hướng "yếu" — bị co mạnh hơn. Bias theo hướng đó là $\frac{\lambda}{\lambda_{\min} + \lambda}$.

Với embedding isotropic, tất cả các hướng đều có cùng trị riêng $\bar{\lambda}$, nên bias được phân bổ đều và nhỏ nhất có thể.

Biểu đồ xác nhận: dù tăng số mẫu lên bao nhiêu, bias của anisotropic (đỏ) luôn cao hơn isotropic (xanh).

**Trực giác**: embedding isotropic đồng nghĩa với mọi hướng đều quan trọng như nhau — regularizer không tạo ra thiên vị có hại.

---

## Slide 10 — Bổ Đề 2: Anisotropy Làm Tăng Variance

Bổ đề 2 bổ sung chiều còn lại: không chỉ bias mà variance cũng xấu hơn khi embedding anisotropic.

Mỗi lần ta resample tập huấn luyện, linear probe sẽ cho ra một decision boundary khác. Biểu đồ minh họa: các đường đỏ — anisotropic — dao động rất nhiều, các đường xanh — isotropic — ổn định quanh một đường duy nhất.

Lý do toán học: tổng phương sai $\mathrm{tr}(\mathrm{Var}(\hat\beta))$ được cực tiểu hóa khi tất cả các trị riêng của covariance matrix bằng nhau — tức là isotropic.

Kết hợp hai bổ đề: embedding isotropic tối thiểu hóa đồng thời cả bias lẫn variance, với cùng "năng lượng" $\sum\lambda_k$.

---

## Slide 11 — Định Lý 1: Isotropic Gaussian Là Điểm Cực Tiểu Duy Nhất

Slide này kết hợp hai bổ đề thành một kết quả hoàn chỉnh qua ba bước suy luận.

**Bước 1 — Cramér–Rao**: với bất kỳ phân phối $p$ nào, Fisher information thỏa mãn $J(p) \geq \mathrm{tr}(\Sigma^{-1})$. Vì vậy phân phối Gaussian luôn đạt cận dưới này.

**Bước 2 — Jensen**: trong số các Gaussian $\mathcal{N}(0, \Sigma)$, bất đẳng thức Jensen suy ra $\mathrm{tr}(\Sigma^{-1}) \geq K^2/\kappa$ — đẳng thức xảy ra khi và chỉ khi $\Sigma = \frac{\kappa}{K}I$, tức là isotropic.

**Kết luận — Định lý 1**: trong số mọi phân phối với $\mathrm{Tr}(\mathrm{Cov}) = \kappa$, điểm cực tiểu duy nhất của worst-case downstream risk là $p^* = \mathcal{N}\!\left(0, \frac{\kappa}{K}I\right)$.

Quan trọng: kết quả này là **duy nhất** — không phân phối nào khác, kể cả Student-$t$, Laplace, hay Uniform, đạt được minimum này.

---

## Slide 12 — Kết Luận Lý Thuyết: Design Principle Cho LeJEPA

Slide này tóm tắt thông điệp lý thuyết thành một dòng duy nhất:

$$f_\theta(\mathbf{x}) \;\sim\; \mathcal{N}(\mathbf{0},\, I)$$

Đây là **design principle duy nhất** cần đạt. Không cần thêm điều kiện phụ, không cần heuristic, không cần stop-gradient hay EMA.

Ba probe family đều xác nhận: linear probe, kNN probe, và kernel probe — cả ba đều tối ưu khi embedding có phân phối isotropic Gaussian.

Lần đầu tiên ta biết **chính xác** embeddings nên phân phối thế nào. Bước tiếp theo: cần công cụ để đưa embedding đến đó — đó là SIGReg.

---

## Slide 13 — Tại Sao Hình Cầu: Biến Đổi Không Gian Latent

Lý thuyết vừa nói "hãy đưa embedding về $\mathcal{N}(0,I)$". Nhưng tại sao lại là hình cầu? Tại sao không phải một ellipsoid bẹp hay một phân phối nào khác?

Hãy tưởng tượng bạn đứng tại một điểm query $q$ trong không gian embedding và hỏi: *"5 người hàng xóm gần nhất của tôi là ai?"* Câu trả lời phụ thuộc hoàn toàn vào hình dạng của đám mây điểm xung quanh.

**Bên trái — anisotropic (ellipsoid)**: Đám mây bị kéo dài theo một trục. kNN tìm gần theo khoảng cách Euclidean, nên nó vô tình ưu tiên những điểm nằm dọc theo trục dài — dù chúng ở rất xa về mặt ngữ nghĩa. Một con mèo đen có thể trở thành "hàng xóm" của một con chó đen chỉ vì màu sắc chiếm trục dài. Neighborhood bị lệch, và mỗi lần resample tập huấn luyện thì nó lại lệch theo hướng khác — bias và variance đều cao.

**Bên phải — isotropic (hình cầu)**: Đám mây đồng đều mọi hướng. kNN neighborhood là một quả cầu thực sự, không lệch về phía nào. Khoảng cách Euclidean giờ phản ánh đúng sự tương đồng ngữ nghĩa — điểm gần là điểm thực sự giống nhau.

Mũi tên giữa là SIGReg — nó không thay đổi *nội dung* của embedding mà chỉ biến dạng hình học của đám mây: từ ellipsoid về hình cầu, từ $\Sigma$ về $I$.

---

## Slide 14 — Ý Tưởng: Dùng Statistical Test Như Một Hàm Loss

Bây giờ ta có target distribution. Câu hỏi là: làm sao ép phân phối của embedding $P_\theta$ về $Q = \mathcal{N}(0, I)$?

LeJEPA frame lại bài toán này như một hypothesis test:
$$H_0 : P_\theta = Q \quad \text{vs} \quad H_1 : P_\theta \neq Q$$

Test statistic $T$ đo lường bằng chứng thực nghiệm chống lại $H_0$. Khi $T$ nhỏ, embedding gần với Gaussian; khi $T$ lớn, embedding xa.

Chiến lược: **minimize $T$ như một loss** — thu thập ít bằng chứng chống lại $H_0$ nhất có thể, tức là ép embedding về $\mathcal{N}(0, I)$.

Câu hỏi tiếp theo: chọn test $T$ nào? Cần $T$ vừa differentiable, vừa $\mathcal{O}(N)$, vừa provably correct. Ba họ test sẽ được xét lần lượt.

---

## Slide 15 — Thách Thức: Kiểm Tra Phân Phối Trong Không Gian Cao Chiều

Một regularizer tốt cần ba tính chất: **differentiable** (huấn luyện gradient-based), **$\mathcal{O}(N)$** (scale lên millions samples), và **provably correct** (hội tụ về đúng distribution).

Các phương pháp chuẩn đều thất bại ít nhất một tiêu chí:
- **MMD**: chứng minh được nhưng $\mathcal{O}(N^2)$ — không scale.
- **KL Divergence**: gradient không ổn định khi $p \approx 0$.
- **Test multivariate chuẩn** (BHEP, Mardia): đều $\mathcal{O}(N^2)$ — không dùng được với mini-batch.

**Giải pháp của LeJEPA**: phân rã bài toán $K$-chiều thành $M$ bài toán 1D độc lập qua random projection. Ta sẽ xét ba họ test 1D lần lượt để xem cái nào phù hợp.

---

## Slide 16 — Họ Test 1: Moments — Mạnh Nhưng Gradient Explode

Họ test đầu tiên là dựa trên **moments** — đo lường phân phối qua trung bình, phương sai, skewness, kurtosis. Extended Jarque-Bera gom 4 thống kê này thành một score duy nhất.

Vấn đề: để nhận diện tốt hơn, ta cần thêm nhiều moment bậc cao. Nhưng gradient của moment bậc $k$ tăng theo hàm mũ $2.5^k$.

Từ bậc 4 trở lên: gradient explode — mô hình không thể huấn luyện được.

Hơn nữa, **Định lý 3** trong paper chứng minh: dùng $K$ moment hữu hạn không đủ để xác định duy nhất phân phối Gaussian — nhiều phân phối khác nhau có thể có cùng $K$ moment đầu. Tức là VICReg — vốn dùng chỉ 2 moment đầu — dễ bị shortcut.

**Kết luận**: họ Moments có fundamental trade-off không thể giải quyết được — tăng $K$ để nhận diện tốt hơn thì gradient bùng nổ.

---

## Slide 17 — Họ Test 2: CDF — Chính Xác Nhưng Không Differentiable

Họ test thứ hai dựa trên **CDF** — so sánh hàm phân bố tích lũy thực nghiệm với CDF của Gaussian chuẩn. Về lý thuyết là chính xác, nhưng có hai vấn đề chí mạng với deep learning.

**Vấn đề 1 — Non-parallel**: tính CDF thực nghiệm cần phải sắp xếp dữ liệu trước. Trong môi trường multi-GPU, điều này đòi hỏi đồng bộ hóa toàn bộ dữ liệu giữa các GPU trước khi sort — tạo ra bottleneck nghiêm trọng, phá vỡ DDP.

**Vấn đề 2 — Non-differentiable**: phép sort không có gradient thực sự. Dù có thể dùng differentiable sort relaxation, điều này sinh thêm hyperparameter và sai số xấp xỉ.

**Takeaway**: phép toán sắp xếp bẻ gãy tính toán song song và triệt tiêu luồng gradient — họ CDF bị loại.

---

## Slide 18 — Họ Test 3: ECF — Stable, Scalable, Provable

Họ test thứ ba là **Empirical Characteristic Function** — và đây là giải pháp được chọn.

Ý tưởng: thay vì so sánh CDF trong miền không gian, ta so sánh trong **miền tần số** qua hàm đặc trưng $\phi(t) = \mathbb{E}[e^{itx}]$. ECF thực nghiệm là $\hat\phi_X(t) = \frac{1}{N}\sum e^{itX_j}$.

Chìa khóa: vì $|e^{itx}| = 1$, ECF luôn nằm trong $[-1, 1]$. Gradient tự nhiên từ phép trung bình — không cần sort.

Ba tính chất:
- **Differentiable**: gradient xuất phát từ average, không cần sort.
- **$\mathcal{O}(N)$ và DDP-friendly**: song song hóa qua `all_reduce` dễ dàng.
- **Định lý 4 — Bounded Gradient**: gradient luôn bị chặn $\leq 4\sigma^2/N$ — loại bỏ hoàn toàn rủi ro exploding gradient.

**Takeaway**: $|e^{itx}| = 1$ là chìa khóa cho một loss 100% song song hóa và siêu ổn định.

---

## Slide 19 — SIGReg: Đưa Embedding Về $\mathcal{N}(0,I)$ Ở Chi Phí $\mathcal{O}(N)$

Bây giờ ta kết hợp Epps-Pulley test với Cramér-Wold theorem để có SIGReg.

**Cramér-Wold theorem** nói rằng: $X \stackrel{d}{=} Y$ nếu và chỉ nếu mọi phép chiếu 1D $\langle \mathbf{u}, X\rangle \stackrel{d}{=} \langle \mathbf{u}, Y\rangle$ cho mọi hướng $\mathbf{u}$.

Vì vậy, thay vì kiểm tra phân phối trong $K$ chiều — tốn $\mathcal{O}(N^2)$ — ta chiếu embedding xuống $M$ hướng ngẫu nhiên và áp dụng Epps-Pulley test cho mỗi hướng 1D. Mỗi test $\mathcal{O}(N)$, tổng cộng vẫn $\mathcal{O}(N)$.

Biểu đồ minh họa: hướng $\mathbf{u}_1$ và $\mathbf{u}_M$ — histogram khớp với Gaussian. Hướng $\mathbf{u}_2$ — mismatch, EP test cho điểm cao, gradient đẩy embedding về Gaussian theo hướng đó.

$M = 16$ hướng mỗi bước là đủ nhờ tính trơn của DNN và SGD resampling tích lũy.

---

## Slide 20 — SIGReg: Định Nghĩa Chính Thức và Cài Đặt

**Định nghĩa chính thức của SIGReg**:
$$\mathrm{SIGReg}_T(\mathbb{A}, \{f_\theta(\mathbf{x}_n)\}) = \frac{1}{|\mathbb{A}|}\sum_{\mathbf{a}\in\mathbb{A}} T\!\left(\{\mathbf{a}^\top f_\theta(\mathbf{x}_n)\}_{n=1}^N\right)$$

$\mathbb{A}$ là tập $M$ hướng ngẫu nhiên trên mặt cầu đơn vị, $T$ là Epps-Pulley test.

Tại sao dùng **average** thay vì max? Max cho gradient sparse — chỉ 1 hướng được update mỗi bước. Average cho gradient dense, quá trình huấn luyện ổn định hơn nhiều.

Code PyTorch chỉ ~15 dòng thực sự:
- Seed được đồng bộ giữa các GPU qua `global_step` — đảm bảo mọi GPU dùng cùng hướng chiếu.
- ECF tính bằng cosine và sine trung bình — không có sort, không có non-differentiable op.
- Loss là tổng bình phương khoảng cách giữa ECF thực nghiệm và ECF của $\mathcal{N}(0,1)$.

---

## Slide 21 — LeJEPA: Một Công Thức, Một Siêu Tham Số

Và đây là toàn bộ LeJEPA:
$$\mathcal{L}_{\rm LeJEPA} = (1-\lambda)\cdot\mathcal{L}_{\rm pred} + \lambda\cdot\text{SIGReg}$$

Hai thành phần:
- **Invariance loss** $\mathcal{L}_{\rm pred}$: ép các view của cùng một ảnh phải cho ra embedding giống nhau.
- **SIGReg**: ép embedding về $\mathcal{N}(0, I)$.

$\lambda$ là siêu tham số duy nhất cân bằng giữa hai mục tiêu. Khuyến nghị: $\lambda = 0.05$.

So sánh với các phương pháp khác:

| | DINO | I-JEPA | **LeJEPA** |
|---|---|---|---|
| Lý thuyết | ✗ | ✗ | **✓** |
| # hyperparams | ≥7 | ≥5 | **1 ($\lambda$)** |
| Architecture | ViT | ViT | **Any** |
| Stop-gradient | cần | cần | **không** |
| Teacher-student | cần | cần | **không** |
| Core code | 1000+ | 500+ | **~50** |

**Takeaway**: 1 loss · 1 hyperparameter · 0 heuristic · lý thuyết từ first principles.

---

## Slide 22 — SIGReg Vượt Qua Curse of Dimensionality

Một lo ngại tự nhiên: với $M$ hướng ngẫu nhiên trong không gian $K$ chiều, liệu ta có đủ "coverage" không?

**Định lý 5** trả lời: sai số giảm theo $\mathcal{O}(M^{-\frac{2\alpha}{K-1}})$ với $\alpha$ là Sobolev smoothness của dữ liệu.

Hai lý do SIGReg vượt qua curse of dimensionality:

**1. Sobolev smoothness $\alpha$**: các DNN tự nhiên tạo ra hàm trơn (BatchNorm, Dropout, weight decay tạo ra $\alpha$ lớn). Smoothness cao làm tốc độ hội tụ nhanh, nên $M = \mathcal{O}(K)$ là đủ.

**2. SGD resampling**: mỗi mini-batch lấy mẫu lại $M$ hướng mới. Sau $T$ bước, số hướng tích lũy là $M \times T$ — coverage tăng miễn phí trong quá trình huấn luyện.

Biểu đồ xác nhận: resampling (đường xanh) hội tụ nhanh hơn rất nhiều so với fixed directions (đường đỏ). $M = 16$ hướng mỗi bước là đủ cho $K = 2048$-dim embedding.

---

## Slide 23 — $\lambda$: Nút Điều Chỉnh Duy Nhất

Sơ đồ trên cùng minh họa spectrum của $\lambda$:

- **$\lambda = 0$**: chỉ có prediction loss → pure collapse, encoder vô dụng.
- **$\lambda = 1$**: chỉ có SIGReg → embedding uniform nhưng không có invariance giữa các view, encoder không học được semantic.
- **Sweet spot $\lambda \approx 0.05$**: cân bằng tốt, embedding vừa isotropic Gaussian vừa invariant với augmentation.

Biểu đồ dưới cho thấy linear probe accuracy theo $\lambda$ trên log-scale: đường cong có đỉnh rõ ràng tại $\lambda = 0.05$, với vùng ổn định rộng $[0.01, 0.1]$.

**Thiết lập mặc định khuyên dùng**: $\lambda = 0.05$, 2 global views + 6 local views, batch size ≥ 128, $M = 1024$ slices, 17 quadrature points.

Một điểm thực tế: $\lambda$ robust trên dải rộng — không cần grid search tỉ mỉ.

---

## Slide 24 — LeJEPA Generalizes VICReg

Slide này làm rõ mối quan hệ giữa LeJEPA và các phương pháp trước.

LeJEPA là một **framework tổng quát**: bằng cách thay $T$ trong SIGReg bằng các hàm test khác nhau, ta thu được các phương pháp khác nhau:

- $T$ = Epps-Pulley → **LeJEPA** (khuyên dùng)
- $T$ = Moments (chỉ mean và variance) → **VICReg**
- $T$ = Jarque-Bera → không ổn định (gradient explode)

**Tại sao VICReg không đủ?** Định lý 3 chứng minh: VICReg chỉ đối chiếu 2 moment đầu, nên nhiều phân phối khác nhau đều có thể thỏa mãn — dễ bị shortcut. Vì vậy VICReg phải chắp vá thêm heuristic để tránh sụp đổ.

SIGReg dùng ECF — ràng buộc **toàn bộ** đặc trưng phân phối. Cramér-Wold đảm bảo hội tụ tuyệt đối về $\mathcal{N}(0, I)$.

**Kết luận**: VICReg thực chất là một phiên bản giới hạn và thiếu chặt chẽ của LeJEPA.

---

## Slide 25 — [RESULTS] Hai Kết Quả Nổi Bật

Phần kết quả bắt đầu với hai phát hiện nổi bật.

**Kết quả 1 — Loss tương quan với accuracy**: biểu đồ scatter cho thấy training loss của LeJEPA tương quan 94% (Spearman) với linear probe accuracy. Đây là lần đầu tiên trong SSL: có thể chọn model tốt nhất chỉ dựa trên training loss, không cần chạy linear probe riêng.

**Kết quả 2 — In-domain SSL đánh bại frontier models**: trên Galaxy10 (11K ảnh thiên hà), LeJEPA huấn luyện trực tiếp trên domain chuyên biệt vượt qua DINOv2 và DINOv3 ở mọi mức số mẫu. Ngay cả với chỉ 1 sample mỗi lớp, LeJEPA đạt 31% so với 21% và 25% của DINOv2/v3.

Ý nghĩa: với dữ liệu đặc thù (y tế, khoa học, vệ tinh), huấn luyện LeJEPA từ đầu trên domain đó có thể tốt hơn transfer từ ImageNet foundation model.

---

## Slide 26 — Scale: 60+ Kiến Trúc, Không Collapse, SOTA

LeJEPA được test trên hơn 50 models thuộc 8 architecture family trên ImageNet-10.

**Điểm đáng chú ý nhất**: không có collapse nào trong tất cả 50 models. Không cần tune hyperparameter theo kiến trúc — cùng một $\lambda = 0.05$ hoạt động cho ResNet, ViT, ConvNeXt, và nhiều kiến trúc khác.

**Kết quả SOTA trên ImageNet-1K**:

| Method | Params | Acc |
|---|---|---|
| I-JEPA ViT-H (300ep) | 632M | 77.3% |
| LeJEPA ViT-L (100ep) | 304M | 78.2% |
| **LeJEPA ConvNeXt-H** | 660M | **79.0%** |

LeJEPA ViT-L dùng chỉ một nửa tham số và 1/3 số epoch so với I-JEPA ViT-H, nhưng vẫn vượt qua. Đây là bằng chứng rõ ràng rằng lý thuyết đúng dẫn đến thực nghiệm tốt hơn.

---

## Slide 27 — Ablation: LeJEPA Ổn Định Trên Mọi Siêu Tham Số

Ablation study xác nhận tính robust của LeJEPA.

**Các hyperparameter của Epps-Pulley**: tất cả các cấu hình — integration range, số quadrature points, số slices — đều cho kết quả gần nhau. Hiệu suất không nhạy cảm với các lựa chọn này.

**Register tokens**: không cần thiết. Kết quả với 0, 2, hay 8 register tokens gần như bằng nhau.

So sánh tổng hợp với DINO và I-JEPA: LeJEPA là phương pháp duy nhất có lý thuyết đảm bảo anti-collapse, chỉ có 1 hyperparameter, hoạt động với mọi kiến trúc, và có training loss tương quan 94% với accuracy downstream.

---

## Slide 28 — Emergent Semantics: Không Supervision — Vẫn Học Được Cấu Trúc

Một kết quả định tính ấn tượng: khi chiếu 3 principal component đầu tiên của last-layer patch features của ViT-L ra RGB, ta thấy màu "warm" (đỏ/cam) tương ứng với foreground objects (con chó, mặt, đối tượng chính), và màu "cool" (xanh lam/lục) tương ứng với background (cỏ, trời, nền).

Điều này xảy ra mà **không có bất kỳ annotation nào** trong quá trình huấn luyện.

Ứng dụng: dùng attention map của CLS token để tự động segment đối tượng trong video với temporal coherence rất mượt.

**Lý do cốt lõi**: mục tiêu $\mathcal{N}(0, I)$ ép mọi hướng trong không gian embedding đều phải chứa thông tin — maximum entropy. Điều này triệt tiêu dimensional collapse, buộc encoder phải phân bổ semantic information ra đều các chiều, và cấu trúc ngữ nghĩa tự nhiên nổi lên.

---

## Slide 29 — Tác Động Thực Tế: Từ Lý Thuyết Đến LeWorldModel

Slide này là bằng chứng cụ thể nhất cho impact của LeJEPA: khi có lý thuyết đúng, cả một field có thể được đơn giản hóa triệt để.

Bài toán world model (JEPA-based) trước đây bị ám ảnh bởi collapse — mọi phương pháp đều phải chọn một trong ba con đường không hoàn hảo: (1) dùng stop-gradient hay EMA như heuristic không có lý thuyết, (2) freeze một pre-trained encoder để tránh collapse nhưng từ bỏ end-to-end learning, hoặc (3) thêm reconstruction loss để buộc encoder giữ thông tin — nhưng reconstruction kéo model khỏi latent prediction và làm tăng chi phí tính toán đáng kể.

**LeWorldModel** (arXiv:2603.19312) phá vỡ thế bế tắc này bằng cách dùng SIGReg từ LeJEPA làm anti-collapse regularizer:

- **Chỉ 2 loss terms**: prediction loss + SIGReg — không reconstruction, không contrastive, không multi-objective phức tạp.
- **Chỉ 1 hyperparameter thực sự cần tune** ($\lambda$) — $M$ số random projections có ảnh hưởng không đáng kể, và $\lambda$ có thể tìm bằng bisection search với độ phức tạp logarithmic.
- **Không stop-gradient, không EMA** — gradient propagate qua toàn bộ hệ thống, end-to-end thực sự từ pixel.
- **15M parameters, 1 GPU** — competitive với foundation model-based world models vốn cần encoder pre-train riêng.
- **Nhanh hơn 48×** trong planning so với foundation world models.

Điều này chỉ khả thi vì LeJEPA đã chứng minh $\mathcal{N}(0,I)$ là target distribution tối ưu — SIGReg không phải một trick thêm vào, mà là một đảm bảo lý thuyết rằng collapse không thể xảy ra miễn là loss được tối ưu. Đây là lần đầu tiên một JEPA world model có **provable anti-collapse guarantee** mà không cần bất kỳ heuristic nào.

---

## Slide 30 — Kết Luận

Nhìn lại toàn bộ hành trình: từ Prior SSL với chắp vá thực nghiệm, LeJEPA đã dịch chuyển paradigm sang "từ nguyên lý nền tảng".

Bốn đóng góp chính:

1. **Lý thuyết**: Isotropic Gaussian là unique minimizer cho worst-case downstream risk — lần đầu tiên biết chính xác target distribution.

2. **Phương pháp**: SIGReg — $\mathcal{O}(N)$, differentiable, bounded gradient, không cần sort hay EMA.

3. **Thực nghiệm**: SOTA trên 60+ architectures, đánh bại DINOv2 in-domain, training loss tương quan 94% với accuracy.

4. **Tối giản**: 1 hyperparameter $\lambda$, ~50 dòng code, không cần stop-gradient hay teacher-student.

Tôi muốn kết thúc bằng câu quote của các tác giả:

> *"If 2024 was the year of scaling laws, 2025 may be the year we rediscover structure."*

Cảm ơn mọi người. Mình sẵn sàng cho câu hỏi.

---

## Phụ Lục — Bảng Tra Cứu Thuật Ngữ

*(Dùng khi được hỏi về thuật ngữ)*

| Thuật ngữ | Giải thích |
|---|---|
| JEPA / LeJEPA | Joint-Embedding Predictive Architecture / Latent Epps-Pulley JEPA |
| SSL | Self-Supervised Learning |
| Foundation model | Mô hình huấn luyện một lần, dùng cho nhiều task |
| Linear probe | Đánh giá bằng cách thêm một lớp tuyến tính |
| Anisotropic / Isotropic | Phân bố không đều / đều mọi hướng |
| Embedding / Latent space | Vector biểu diễn / Không gian tiềm ẩn |
| Downstream task | Tác vụ cụ thể sau khi huấn luyện SSL |
| Random projection | Chiếu nhiều chiều xuống 1 chiều |
| Decision boundary | Ranh giới phân tách lớp dữ liệu |
| Bounded gradient | Gradient bị chặn trên, không bùng nổ |
| Curse of dimensionality | Hiệu quả giảm ở không gian nhiều chiều |
| Emergent semantics | Cấu trúc ngữ nghĩa tự nổi lên không cần nhãn |
| Sweet spot | Điểm cân bằng hyperparameter tối ưu |
| DDP | Distributed Data Parallel — huấn luyện song song đa GPU |
| ECF | Empirical Characteristic Function |
| SGD resampling | Lấy mẫu lại hướng chiếu mỗi bước SGD |
