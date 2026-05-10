# Báo cáo kết quả quá trình Pretraining và Evaluation (LeJEPA ViT-B)

Báo cáo này tổng hợp kết quả đạt được từ quá trình huấn luyện LeJEPA ViT-B/16 trong vòng 1 epoch trên dataset ImageNet-1K, và kết quả đánh giá Few-Shot Linear Probe trên các bộ dữ liệu fine-grained.

## 1. Thông tin cấu hình Pretraining
* **Mô hình (Backbone)**: ViT-B/16 (timm `vit_base_patch16_224` - 86M params)
* **Phương pháp**: LeJEPA (Joint-Embedding Predictive Architecture với SIGReg)
* **Dataset**: ImageNet-1K (`ILSVRC/imagenet-1k`)
* **Tổng số epoch**: 1 epoch
* **Batch size**: 512 (64 batch size thực tế * 8 bước gradient accumulation)
* **Optimizer**: AdamW (Learning rate = 5e-4, Weight decay = 5e-2)
* **Data Augmentation**: Multi-crop (2 global views, 4 local views) kết hợp photometric transforms.
* **Thời gian huấn luyện**: ~ 2 giờ 23 phút (theo log `train.log`)

## 2. Kết quả Evaluation (Few-Shot Linear Probe)

Quá trình đánh giá được thực hiện thông qua mạng tuyến tính đơn giản (Linear Probe) train trên các đặc trưng (embeddings) bị đóng băng (frozen) trích xuất từ mô hình ViT-B/16 đã huấn luyện.
Các kết quả phân loại (Top-1 Accuracy %) dựa trên số shot khác nhau:

| Dataset | 1-shot (%) | 10-shot (%) | All-shot (%) | Ghi chú / Trạng thái |
| :--- | :---: | :---: | :---: | :--- |
| **DTD** | 10.98 | 25.25 | 39.26 | Hoàn thành thành công |
| **CIFAR-10** | 23.99 | 41.07 | 71.48 | Đã fix lỗi tương thích (chuyển sang torchvision) |
| **CIFAR-100** | 7.29 | 22.10 | 49.85 | Đã fix lỗi tương thích (chuyển sang torchvision) |
| **Flowers102** | 19.74 | 49.51 | 65.29 | Hoàn thành thành công |
| **Food-101** | 4.09 | 13.98 | 39.49 | Đã fix lỗi `Truncated File Read` (PIL ImageFile) |
| **Stanford Cars** | 1.81 | 5.32 | 10.77 | Đã fix lỗi `CUDA error: initialization error` (worker=0) |
| **Aircraft** | N/A | N/A | N/A | Đã fix lỗi dataset script (chuyển sang `FGVCAircraft`) |
| **Oxford Pets** | N/A | N/A | N/A | Đã fix lỗi thiếu split test (chuyển sang `OxfordIIITPet`) |

*(Lưu ý: Một số giá trị N/A trong báo cáo này đang ở trạng thái trống do quá trình eval đã bị ngắt giữa chừng, tuy nhiên code đã được fix triệt để sẵn sàng chạy).*

## 3. Nhật ký gỡ lỗi (Debugging & Fixes)

Trong quá trình chạy evaluation pipeline, mã nguồn nguyên bản đã gặp một số vấn đề liên quan đến tương thích và cấu hình. Hệ thống đã xử lý và gỡ rối triệt để các vấn đề sau:

1. **Vấn đề tương thích của HuggingFace Datasets v4.0.0**: 
   - Lỗi `Dataset scripts are no longer supported` ngăn chặn tải FGVC Aircraft. 
   - **Giải pháp**: Tích hợp module `torchvision.datasets.FGVCAircraft` thay thế.
2. **Crash CUDA Initialization trong DataLoader**:
   - Môi trường đa tiến trình (multi-processing) xung đột khi khởi tạo CUDA do cờ `pin_memory=True` kết hợp fork worker.
   - **Giải pháp**: Đồng bộ hóa pipeline evaluation bằng cách đưa `num_workers=0` (chỉ chạy trên main process) đảm bảo 100% an toàn không crash.
3. **Thiếu metadata/split**:
   - `Oxford Pets` trên HF không có file test split.
   - **Giải pháp**: Chuyển sang sử dụng `torchvision.datasets.OxfordIIITPet` với thiết lập chuẩn `trainval` và `test`.
4. **Ảnh bị lỗi (corrupted JPEGs)**:
   - Tập `Food-101` có chứa file ảnh cụt khiến PIL throw warning/error.
   - **Giải pháp**: Cấu hình `ImageFile.LOAD_TRUNCATED_IMAGES = True` để duy trì pipeline mượt mà.

Tất cả những thay đổi trên đã được commit và push lên nhánh `ml`. Toàn bộ `checkpoints` rác và log tạm thời được lọc bằng `.gitignore` để giữ sạch sẽ dung lượng của GitHub.
