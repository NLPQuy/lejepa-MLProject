===============================================================================
 LeJEPA — Kiến trúc cốt lõi + Các hướng "leo benchmark"
 (tài liệu đọc hiểu, viết theo code thực tế trong repo)
===============================================================================

Mục tiêu của file này:
  PHẦN 1 — Giải thích thật kỹ kiến trúc cốt lõi của LeJEPA (từng khối làm gì,
           nối với nhau ra sao, loss tính thế nào).
  PHẦN 2 — Giải thích từng can thiệp (architecture + optimizer/dynamics) mà
           nhóm dùng để cố cải thiện LeJEPA trên benchmark Imagenette:
           conv-stem, DynTanh, coding-rate, uniformity, SAM, Muon, PCGrad,
           SWA, Schedule-Free, LLRD, QK-Norm, deep-supervision, prog-drop-path.

Nguồn code: stable-pretraining/stable_pretraining/methods/lejepa.py
            climb_bench/batch1/_variants.py, climb_bench/batch2/_variants.py
            climb_bench/batch2/_common.py


===============================================================================
 PHẦN 1 — KIẾN TRÚC CỐT LÕI CỦA LeJEPA
===============================================================================

-------------------------------------------------------------------------------
 1.1  Bức tranh lớn: một loss, một siêu tham số
-------------------------------------------------------------------------------

LeJEPA là một phương pháp Self-Supervised Learning (học không nhãn). Ý tưởng:
cho model xem nhiều "view" (phiên bản cắt/biến đổi) của cùng một ảnh, và ép:

  (1) INVARIANCE  — các view của cùng ảnh phải cho biểu diễn GIỐNG nhau.
  (2) SIGReg      — toàn bộ biểu diễn của cả batch phải phân bố theo một
                    Gaussian đẳng hướng N(0, I) (hình cầu, mọi hướng đều nhau).

Toàn bộ hàm loss chỉ gồm hai số hạng:

      loss = Invariance  +  λ · SIGReg

  - λ (lambda) là SIÊU THAM SỐ DUY NHẤT cần chỉnh (mặc định 0.02–0.05).
  - Không cần EMA, không stop-gradient, không predictor, không teacher-student.

Vì sao chỉ hai số hạng này là đủ (trực giác chống "collapse"):
  - Nếu chỉ có Invariance, model sẽ gian lận bằng cách cho MỌI ảnh ra cùng một
    vector (mọi thứ giống nhau => invariance = 0). Đó gọi là "collapse".
  - SIGReg chặn đứng điều đó: nó bắt phân phối biểu diễn phải trải đều thành
    hình cầu N(0, I). Một điểm duy nhất thì không thể là hình cầu => collapse
    bị phạt nặng. Hai lực kéo ngược nhau tạo ra biểu diễn vừa gom-cụm-theo-ngữ-
    nghĩa vừa trải-đều-toàn-không-gian.


-------------------------------------------------------------------------------
 1.2  Luồng dữ liệu (rất quan trọng — ba khái niệm hay bị lẫn)
-------------------------------------------------------------------------------

  ảnh
   │
   ▼
 [ BACKBONE / ENCODER ]      <- mạng chính (ViT-S, ResNet...), thứ ta GIỮ LẠI
   │                            để dùng downstream
   ▼
  EMBEDDING  (features, D chiều, vd 384)   <- "biểu diễn" của ảnh
   │
   ▼
 [ PROJECTOR ]               <- mạng head phụ, CHỈ dùng lúc train
   │
   ▼
  PROJECTION  (proj, K chiều, vd 512)      <- nơi hai loss tác động
   │
   ▼
 [ PREDICTOR ]  (tùy chọn, mặc định TẮT = Identity)
   │
   ▼
  predicted    <- chỉ dùng cho nhánh invariance

Phân biệt ba thứ hay lẫn:

  * PROJECTOR  = một MẠNG (module). Biến embedding -> projection.
                 "tuyến tính / phi tuyến" là nói về mạng NÀY.
  * PROJECTION = một TENSOR (đầu ra của projector). Đây là nơi SIGReg và
                 invariance được tính (mặc định).
  * PREDICTOR  = một MẠNG phụ, chỉ trên nhánh invariance, thường TẮT.

Câu để nhớ:
  "Projector là cái máy, projection là sản phẩm nó tạo ra,
   predictor là máy phụ (thường tắt)."

LƯU Ý CỐT TỬ: thứ ta thực sự dùng để đánh giá (linear probe, kNN) là EMBEDDING
(đầu ra backbone), KHÔNG phải projection. Projector "gánh" ràng buộc phân phối
để embedding giữ được thông tin phong phú. Đây là "projector-head trick" kinh
điển của SSL (giống SimCLR/BYOL/VICReg).


-------------------------------------------------------------------------------
 1.3  Backbone / Encoder
-------------------------------------------------------------------------------

- Là mạng thị giác bất kỳ từ thư viện timm (LeJEPA "agnostic" với kiến trúc):
  ViT, ResNet, ConvNeXt... Benchmark của nhóm ghim cứng vit_small_patch16_224.
- Với ViT: ảnh 224x224 được cắt thành các patch 16x16 -> 14x14 = 196 patch
  token, cộng 1 CLS token ở đầu -> chuỗi 197 token đi qua các transformer block.
- "aggregator" quyết định lấy gì làm embedding từ chuỗi token:
    cls       -> chỉ lấy CLS token           (mặc định)
    mean      -> trung bình các patch token
    cls_mean  -> ghép CLS + mean (2*D chiều)
- embed_dim = số chiều embedding (vit_small = 384).


-------------------------------------------------------------------------------
 1.4  Projector — build_projector()
-------------------------------------------------------------------------------

Biến embedding (D) -> projection (K=512). Các lựa chọn kiến trúc:

  "Linear"  : chỉ một nn.Linear(D, 512).  => PROJECTOR TUYẾN TÍNH
              (một phép nhân ma trận, KHÔNG có phi tuyến)

  "MLP2"    : Linear -> BN -> ReLU -> Linear         (2 lớp)
  "MLP"     : Linear(D,512) rồi MLP(512->2048->2048->512)  <- MẶC ĐỊNH
              mỗi lớp ẩn có BatchNorm + ReLU            => PHI TUYẾN
  "MLP4"    : như trên nhưng 4 lớp

"Tuyến tính vs phi tuyến":
  - Linear = ánh xạ thẳng, không bẻ cong không gian.
  - MLP = có ReLU + BatchNorm xen giữa => biểu diễn được biến đổi phi tuyến.

Vai trò: projector là nơi loss "đổ" vào. Nhờ có projector, ràng buộc Gaussian
không ép trực tiếp lên embedding => embedding sạch, giàu thông tin hơn.

Kết quả ablation của nhóm: projector PHẢI phi tuyến. Đặt Linear -> collapse.


-------------------------------------------------------------------------------
 1.5  Projection và hai số hạng loss
-------------------------------------------------------------------------------

Gọi:
  all_features  = embedding của mọi view      [V, N, D]
  all_projected = projection của mọi view     [V, N, K]
  all_predicted = đầu ra predictor            [V, N, K]  (=projection nếu tắt)
  n_global      = số global view (mặc định 2)

(A) INVARIANCE LOSS
    center = trung bình projection của các GLOBAL view:
        centers = all_projected[:n_global].mean(0)          # [N, K]
    inv_loss = ( centers - all_predicted )^2 . mean()

    Ý nghĩa: mỗi view (kể cả local crop nhỏ) phải dự đoán được "tâm" chung
    tính từ các global view. Đây là phần "Predictive" trong JEPA.
    (Chú ý: tâm chỉ lấy từ GLOBAL view vì chúng thấy toàn ảnh, đáng tin hơn
     local crop 96x96.)

(B) SIGReg LOSS  (mặc định áp lên projection)
    sigreg_target = "proj"  -> tính trên all_projected      (mặc định, tốt nhất)
                  = "embed" -> tính trên all_features       (-> collapse!)
                  = "both"  -> trung bình cả hai

    loss = inv_loss + λ · sigreg_loss


-------------------------------------------------------------------------------
 1.6  SIGReg = Sliced Isotropic Gaussian Regularization (trái tim của LeJEPA)
-------------------------------------------------------------------------------

Bài toán: làm sao KIỂM TRA xem một đám vector K chiều (K=512) có phân bố theo
N(0, I) hay không, một cách (a) khả vi để backprop, (b) rẻ, (c) ổn định số học?
Kiểm tra trực tiếp trong 512 chiều là "curse of dimensionality". Giải pháp gồm
hai tầng:

  TẦNG 1 — SLICING (chiếu ngẫu nhiên xuống 1 chiều)
    Định lý Cramér–Wold: nếu MỌI hình chiếu 1 chiều của một phân phối đều là
    Gaussian chuẩn, thì phân phối gốc là Gaussian đẳng hướng.
    => Thay vì test trong 512D, ta:
       - Sinh ngẫu nhiên `num_slices` hướng đơn vị (mặc định 1024), gom thành
         ma trận A cỡ [K, num_slices].
       - proj = x @ A   -> mỗi cột là một "lát cắt" 1 chiều của dữ liệu.
       - Test từng lát cắt 1D xem có ~ N(0,1) không, rồi lấy trung bình.
    (num_slices càng lớn = test càng chặt, càng tốn. Seed được đồng bộ giữa các
     GPU để mọi rank chiếu cùng hướng.)

  TẦNG 2 — EPPS-PULLEY (test 1 chiều bằng hàm đặc trưng - ECF)
    Với mỗi lát cắt 1D, so "hàm đặc trưng thực nghiệm" (Empirical Characteristic
    Function) của dữ liệu với hàm đặc trưng của N(0,1) = exp(-t^2/2).
      - Hàm đặc trưng = biến đổi Fourier của phân phối; "chính xác quanh gốc t=0"
        nên nắm tốt các moment (mean, variance...) dù chỉ tích phân trong miền
        hẹp.
      - Đo khoảng cách L2 giữa hai hàm này, tích phân số trên [0, t_max] bằng
        `n_points` điểm quadrature (mặc định 17, phải lẻ). Khai thác tính đối
        xứng của hàm đặc trưng để chỉ tích phân nửa miền.
    Ba nút của Epps-Pulley:
      integration range (t_max), n_points (số điểm quadrature), num_slices.

    Vì sao chọn ECF (Epps-Pulley) thay vì các test khác:
      - Test dựa trên MOMENT (skew/kurtosis): gradient dễ nổ (bùng nổ số học).
      - Test dựa trên CDF (Kolmogorov, Anderson-Darling): không khả vi mượt.
      - Test ECF: vừa ỔN ĐỊNH, vừa RẺ, vừa có bảo chứng lý thuyết. Đó là lý do
        LeJEPA chọn nó.

Tóm tắt SIGReg bằng một câu:
  "Chiếu embedding xuống hàng nghìn hướng 1D ngẫu nhiên; lát nào lệch khỏi
   Gaussian chuẩn thì phạt lát đó."


-------------------------------------------------------------------------------
 1.7  Predictor — build_predictor() (thường TẮT)
-------------------------------------------------------------------------------

- Một head phụ chỉ trên nhánh invariance: projection -> predicted (cùng chiều).
- Lựa chọn: "none" (nn.Identity, MẶC ĐỊNH) / "linear" / "mlp".
- Ở BYOL, I-JEPA... predictor bất đối xứng là thứ CHỐNG COLLAPSE. Nhưng LeJEPA
  đã có SIGReg lo việc đó => predictor thành THỪA. Ablation xác nhận: "none"
  tốt nhất. Đây là một điểm bán hàng của LeJEPA: bỏ được predictor.


-------------------------------------------------------------------------------
 1.8  Train vs Eval (hai chế độ forward khác nhau)
-------------------------------------------------------------------------------

  TRAIN:  model(global_views=[g1,g2], local_views=[l1..l6])
          -> chạy backbone trên mọi view -> projector -> loss (inv + λ·sigreg)
          global view 224x224, local view 96x96 (multi-crop kiểu DINO).

  EVAL:   model(images=X)  -> chỉ chạy backbone -> trả embedding [N, D].
          Backbone được ĐÓNG BĂNG, ta gắn linear probe / kNN lên embedding.


-------------------------------------------------------------------------------
 1.9  Các siêu tham số mặc định (benchmark Imagenette của nhóm)
-------------------------------------------------------------------------------

  backbone        vit_small_patch16_224   (embed_dim 384)
  λ (lamb)        0.02        (paper khuyến nghị 0.05)
  num_slices      1024
  n_points        17          (điểm quadrature Epps-Pulley, lẻ)
  projector       MLP (phi tuyến), proj_dim 512, hidden 2048, BatchNorm
  predictor       none
  views           2 global (224) + 6 local (96) = 8
  optimizer       AdamW, lr 4e-4, wd 0.05, warmup 10ep + cosine
  precision       16-mixed
  epochs          400 (batch-1) / 100 (batch-2)


===============================================================================
 PHẦN 2 — CÁC HƯỚNG "LEO BENCHMARK"
===============================================================================

Bối cảnh: baseline LeJEPA trên Imagenette đã rất mạnh (~89.5% frozen top1).
Nhóm thử cải thiện theo hai họ can thiệp:

  HỌ 1 (objective / representation head)  -> đụng vào LOSS hoặc PROJECTOR.
  HỌ 2 (optimizer / training geometry)    -> đụng vào cách TỐI ƯU, giữ nguyên loss.
  + một track riêng: ARCHITECTURE co-design (đổi backbone -> conv-stem).

NGUYÊN TẮC IMPLEMENT (quan trọng để đọc code):
  Mỗi can thiệp có một "công tắc tắt" đưa nó về ĐÚNG baseline (weight=0 hoặc
  flag off). Ba cơ chế swap:
    (a) model.sigreg = ...            (đổi test)
    (b) subclass LeJEPA, override _compute_loss   (thêm số hạng loss)
    (c) LeJEPA(projector=...)         (thay projector)
  Logic biến thể nằm trong _variants.py; runner chỉ import + nối dây.

CÁCH ĐỌC KẾT QUẢ (đọc kỹ, tránh hiểu sai):
  - Metric ONLINE (linear probe lr 0.03, kNN, RankMe) = RẺ, dùng để xếp hạng
    nhanh trong lúc train. KHÔNG phải recipe của paper.
  - Metric PAPER-SPEC (frozen, concat CLS 2 block cuối + LayerNorm, AdamW
    lr 1e-3 wd 1e-6) = recipe chuẩn để so sánh.
  - BÀI HỌC LỚN: online ranking KHÔNG sống sót qua recipe paper. Chỉ can thiệp
    có biên đủ lớn (>~2 điểm) mới trụ được. Online chỉ để LOẠI cái dở.


===============================================================================
 HỌ 1 — OBJECTIVE / REPRESENTATION HEAD  (batch-1)
===============================================================================

-------------------------------------------------------------------------------
 2.1  Coding-rate (MCR2)   — class LeJEPACodingRate
-------------------------------------------------------------------------------
LÀ GÌ:
  Thêm một số hạng "thể tích" vào loss để chống collapse mạnh hơn:
      loss = inv + λ·sigreg + coding_beta · (−coding_rate(Z))
  coding_rate(Z) = 0.5·logdet( I + (d/eps^2)·Cov(Z) )   [MCR2, Yu et al.]
  Trực giác: logdet của ma trận hiệp phương sai = "thể tích" mà biểu diễn
  chiếm trong không gian. Thể tích lớn = trải rộng = ít collapse. Ta muốn TĂNG
  coding_rate nên cộng dấu ÂM của nó vào loss (để minimize).

CHI TIẾT:
  - Tính trên projection Z (cùng tensor SIGReg thấy).
  - PHẢI tính bằng fp32 vì logdet ở bf16/16-mixed rất mất ổn định.
  - coding_beta = 0 => đúng baseline.

KẾT QUẢ: HỎNG. Học nhanh lúc đầu (đỉnh ~ep10) rồi SỤP xuống ~0.22, RankMe
  crash. => log-det quá mạnh, "nuốt" mất SIGReg, over-regularize. Là ví dụ
  điển hình: geometry phụ có thể XUNG ĐỘT với chính SIGReg.

-------------------------------------------------------------------------------
 2.2  Uniformity (Wang & Isola)   — class LeJEPAUniformity
-------------------------------------------------------------------------------
LÀ GÌ:
  Thêm số hạng "trải đều trên mặt cầu đơn vị":
      loss = inv + λ·sigreg + gamma · uniformity(Z)
  uniformity(Z) = log E[ exp(−t·||zi − zj||^2) ]   trên Z đã L2-normalize.
  Thấp = các điểm nằm cách đều nhau trên hình cầu.

KẾT QUẢ: ≈ baseline (gần sát, hơn ~0.8pp trong nhiễu), nhưng RankMe cao hơn
  (244 vs 209) = trải đặc trưng rộng hơn thật. Là biến thể DUY NHẤT không làm
  hại. Insight: SIGReg vốn đã ép phân phối tốt rồi; thêm uniformity chỉ lặp lại
  điều SIGReg đang làm, spread tăng nhưng chưa đủ thành lợi thế accuracy.

-------------------------------------------------------------------------------
 2.3  DynTanh projector   — class LeJEPADynTanhProj
-------------------------------------------------------------------------------
LÀ GÌ:
  Thay BatchNorm trong projector bằng "Dynamic Tanh" (Zhu et al., CVPR 2025):
      DynTanh(x) = gamma · tanh(alpha · x) + beta
  Đây là một normalization KHÔNG dùng thống kê batch (không cần mean/var của
  batch), được đề xuất để thay LayerNorm/BatchNorm trong transformer.

CHI TIẾT: chỉ thay self.projector; loss/SIGReg/invariance giữ nguyên.

KẾT QUẢ: KÉM. Hội tụ chậm ~8 lần (đạt 0.80 mãi ep264 vs baseline ep34), không
  bao giờ đuổi kịp. => bỏ BatchNorm làm HỎNG interface projector–SIGReg (SIGReg
  dựa vào phân phối chuẩn hóa mà BatchNorm cung cấp). Bài học: normalization
  trong projector không phải thứ "tháo ra tùy tiện".

CHỐT HỌ 1:
  SIGReg + MLP projector (có BatchNorm) là một ĐIỂM CÂN BẰNG MONG MANH. Cả ba
  can thiệp — thêm coding-rate, thêm uniformity, đổi normalization — đều không
  tạo winner. Objective và projector phải CO-DESIGN, không "bolt-on" rời rạc.


===============================================================================
 HỌ 2 — OPTIMIZER / TRAINING GEOMETRY  (batch-2)
===============================================================================

Tất cả giữ NGUYÊN loss LeJEPA; chỉ đổi cách tối ưu. Xếp theo cơ chế:

-------------------------------------------------------------------------------
 NHÓM "minima phẳng / trung bình trọng số"
-------------------------------------------------------------------------------

 2.4  SAM — Sharpness-Aware Minimization      (kết quả: +0.23pp, trong nhiễu)
   LÀ GÌ: mỗi bước làm HAI lần forward/backward. Bước 1 đi lên đỉnh xấu nhất
     trong bán kính rho quanh điểm hiện tại (w + rho·grad/||grad||); bước 2 tính
     gradient TẠI điểm xấu đó rồi mới cập nhật. => tìm minima "phẳng" (ít nhạy
     nhiễu) thay vì minima nhọn. Kỳ vọng: minima phẳng ít overfit trên data ít.
   CHI TIẾT: cần manual optimization (SAMModule), vì có 2 optimizer (SSL + probe).
     --sam_rho điều khiển bán kính; --sam_late = chỉ bật SAM ở 30% epoch cuối
     (tiết kiệm, vì SAM đắt gấp đôi).
   KẾT QUẢ: chạm baseline, không mở headroom.

 2.5  SWA — Stochastic Weight Averaging       (kết quả: −0.38pp)
   LÀ GÌ: từ một mốc epoch (vd 75%) trở đi, GIỮ TRUNG BÌNH đều các trọng số qua
     các epoch cuối => một điểm ở "trung tâm" vùng phẳng. Nhắm thẳng vào bệnh
     "đỉnh rồi tụt" (peak-then-decay) của baseline.
   CHI TIẾT: bản Lightning gốc đòi đúng 1 optimizer nên nhóm tự viết
     RankMeGatedSWA (tự trung bình param + buffer, không cần update_bn riêng;
     lúc validation swap trọng số trung bình vào để đo, xong trả lại; cuối train
     ghi swa_avg.ckpt cho eval paper-spec).
   KẾT QUẢ: dưới baseline theo recipe paper.

 2.6  Progressive stochastic depth (drop-path) (kết quả: +0.01pp)
   LÀ GÌ: "drop-path" = ngẫu nhiên bỏ qua cả một residual block lúc train
     (stochastic depth). "Progressive" = TĂNG DẦN tỉ lệ drop theo tiến trình
     (đầu train 0, cuối train tới max). Ý: regularize mạnh hơn khi nguy cơ
     overfit tăng dần.
   CHI TIẾT: callback DropPathScheduler quét mọi module có .drop_prob và set
     rate = max · (epoch/max_epoch).
   KẾT QUẢ: gần như 0 thay đổi.

-------------------------------------------------------------------------------
 NHÓM "hình học gradient"
-------------------------------------------------------------------------------

 2.7  PCGrad — Projected Conflicting Gradients (kết quả: −0.05pp)
   LÀ GÌ: LeJEPA có 2 gradient (từ invariance và từ SIGReg). Nếu chúng "cãi
     nhau" (tích vô hướng < 0, tức góc > 90 độ), PCGrad CHIẾU BỎ thành phần xung
     đột: mỗi gradient bỏ đi hình chiếu của nó lên gradient kia, rồi mới cộng.
     "Gradient surgery" để hai mục tiêu bớt phá nhau.
   CHI TIẾT: pcgrad_combine() tính cosine hai gradient; nếu conflict thì
     ga -= (ga·gb/|gb|^2)·gb và ngược lại. Cần custom training step.
   KẾT QUẢ: ≈ baseline. (Ngụ ý: hai gradient của LeJEPA vốn ít xung đột.)

-------------------------------------------------------------------------------
 NHÓM "thay hẳn optimizer"  (đều THUA rõ)
-------------------------------------------------------------------------------

 2.8  Muon                                    (kết quả: −3.75pp, tệ nhất)
   LÀ GÌ: optimizer mới thay AdamW cho các trọng số MA TRẬN (2D). Nó
     "orthogonalize" bản cập nhật gradient bằng lặp Newton-Schulz (đẩy các giá
     trị suy biến về gần 1) trước khi bước. Rất mạnh ở LLM pretraining.
   KẾT QUẢ: đỉnh sớm rồi tụt, thua sâu. Không hợp regime này.

 2.9  LLRD — Layer-wise LR Decay              (kết quả: −3.33pp)
   LÀ GÌ: đặt learning-rate GIẢM DẦN theo độ sâu — lớp gần input học chậm (lr
     nhỏ), lớp gần output học nhanh. Kinh điển khi FINE-TUNE model đã pretrain.
   CHI TIẾT: build_llrd_param_groups() gán scale = gamma^(depth − layer_id);
     patch_embed/pos_embed/cls = layer 0 (chậm nhất). gamma=0 tắt.
   KẾT QUẢ: thua sâu. Lý do: đây là pretrain TỪ ĐẦU, không phải fine-tune —
     làm chậm lớp thấp = bỏ đói phần lớn mạng.

 2.10 Schedule-Free AdamW                     (kết quả: −0.77pp)
   LÀ GÌ: biến thể AdamW bỏ luôn LR schedule (không cần cosine), dùng trung bình
     kiểu Polyak nội tại để tự ổn định. Bớt một thứ phải chỉnh.
   CHI TIẾT: cần callback ScheduleFreeModeCallback để chuyển optimizer giữa chế
     độ train-iterate và eval-averaged-iterate quanh mỗi lần validation.
   KẾT QUẢ: dưới baseline. Cosine gốc vẫn hơn.

-------------------------------------------------------------------------------
 NHÓM "attention / depth"
-------------------------------------------------------------------------------

 2.11 QK-Norm                                 (kết quả: −0.40pp)
   LÀ GÌ: thêm LayerNorm cho Query và Key TRƯỚC khi tính attention (cờ timm
     qk_norm=True). Giúp ổn định attention, phổ biến ở ViT lớn / train dài.
   CHI TIẾT: phải bật lúc TẠO backbone => build_lejepa() tạm monkey-patch hàm
     _create_timm_backbone để chèn qk_norm=True. Lưu ý: đây thực chất ĐỔI KIẾN
     TRÚC nhẹ (thêm tham số norm), nên eval phải rebuild đúng arch.
   KẾT QUẢ: online +0.010 nhưng paper-spec −0.004 => ví dụ điển hình "online
     thổi phồng".

 2.12 Deep supervision                        (kết quả: −0.55pp)
   LÀ GÌ: áp THÊM loss (invariance + SIGReg) lên các lớp TRUNG GIAN của ViT
     (vd block 6, 9), không chỉ ở lớp cuối. Ý: ép biểu diễn giữa mạng cũng tốt.
   CHI TIẾT: class LeJEPADeepSup dùng get_intermediate_layers(), mỗi lớp phụ có
     projector Linear riêng; deepsup_mu=0 tắt.
   KẾT QUẢ: dưới baseline. Ràng buộc lớp giữa gây nhiễu hơn là giúp.

CHỐT HỌ 2:
  Trên fixed ViT-S, KHÔNG can thiệp optimizer/dynamics nào mở ra headroom ổn
  định. Baseline AdamW + cosine đã là một cái neo rất mạnh. "Thay hẳn optimizer"
  (Muon/LLRD/Schedule-Free) đều thua — vì đây là pretrain SSL từ đầu, không phải
  regime mà các optimizer đó được thiết kế cho. Đây là KẾT QUẢ ÂM CÓ GIÁ TRỊ:
  chỉnh optimizer là ngõ cụt => nên dồn sức vào loss/data/kiến trúc.


===============================================================================
 TRACK RIÊNG — ARCHITECTURE CO-DESIGN: CONV-STEM  (điểm sáng duy nhất)
===============================================================================

 2.13 Conv-stem   — class ConvStem + apply_conv_stem
   LÀ GÌ:
     ViT chuẩn "patchify" ảnh bằng MỘT conv lớn stride-16 (cắt phịch thành patch
     16x16). Conv-stem thay khối đó bằng một CHỒNG 4 conv nhỏ stride-2
     (3->emb/4->emb/2->emb->emb), mỗi lớp có BatchNorm + GELU. Đây là trick
     "Early Convolutions Help Transformers See Better" (Xiao et al., NeurIPS
     2021): vài conv nhỏ ở đầu cho ViT "inductive bias" thị giác tốt hơn, học
     ổn định hơn.
   CHI TIẾT:
     - Giữ NGUYÊN hình học token (vẫn 14x14=196 patch) để phần ViT body và CLS
       không đổi -> tương thích pos_embed.
     - Với timm dynamic_img_size, patch_embed trả NHWC và để ViT tự flatten.
     - CHỈ đổi backbone.patch_embed; loss LeJEPA (SIGReg + invariance) KHÔNG đổi.
   KẾT QUẢ: +2.59pp (89.49% -> 92.08%). Winner THẬT SỰ duy nhất, sống sót qua
     recipe paper.

   NHƯNG — cảnh báo trung thực (rất quan trọng khi báo cáo):
     - Đây KHÔNG phải cải tiến của LeJEPA (objective). Nó là cải tiến của
       BACKBONE, giúp MỌI phương pháp SSL/supervised, không riêng LeJEPA.
     - Nó PHÁ luật chơi benchmark "frozen vit_small chuẩn": backbone không còn
       là vit_small nữa => +2.59pp lẫn lộn giữa "objective tốt hơn" và "encoder
       mạnh hơn / nhiều param hơn / inductive bias tốt hơn".
     - Muốn quy công đúng: phải re-baseline cùng conv-stem cho phương pháp khác,
       và báo params/FLOPs. Nếu mọi method đều lợi như nhau => đó là "free lunch
       kiến trúc", không phải công của LeJEPA.
   => Báo cáo conv-stem như một TRACK RIÊNG "architecture co-design", KHÔNG xếp
      cùng cột "ý tưởng cải tiến LeJEPA".


===============================================================================
 TỔNG KẾT ĐỂ NHỚ
===============================================================================

1. LeJEPA = Invariance + λ·SIGReg. SIGReg = slicing (Cramér–Wold) + Epps-Pulley
   (test ECF 1 chiều). Chống collapse bằng LÝ THUYẾT, nên bỏ được predictor,
   EMA, teacher-student.

2. Ba khái niệm: projector (mạng) -> projection (tensor, nơi loss tác động) ->
   predictor (mạng phụ, thường tắt). Embedding (đầu ra backbone) mới là thứ
   dùng để eval.

3. Leo benchmark, hai họ đều là NGÕ CỤT trên fixed ViT-S:
   - Objective/head (coding-rate, uniformity, DynTanh): SIGReg+projector là cân
     bằng mong manh, add-on dễ xung đột.
   - Optimizer/dynamics (SAM, Muon, PCGrad, SWA, LLRD, SF, QK-Norm, deep-sup):
     baseline AdamW+cosine quá mạnh; thay optimizer còn hại.

4. Điểm sáng duy nhất = conv-stem (+2.59pp) — nhưng là ARCHITECTURE, không phải
   objective; phải tách track và kiểm soát confound.

5. Bài học phương pháp luận: metric ONLINE (rẻ) KHÁC recipe PAPER-SPEC. Online
   chỉ để loại cái dở; đừng tin số dương nhẹ của online — kiểm lại bằng recipe
   paper trước khi kết luận.
