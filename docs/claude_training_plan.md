# Plan Chi Tiết — Sửa `train_eval_vit_l.py` và Training LeJEPA ViT-B/16

> **Mục tiêu**: Sửa file `train_eval_vit_l.py` để chạy trên RunPod server với ViT-B/16, train 1 epoch, chạy test trước khi train.
>
> **Cách dùng**: Copy từng prompt trong mỗi Task → paste vào Claude Sonnet 3.6 Antigravity → verify kết quả → chuyển Task tiếp.

---

## Tổng quan các thay đổi cần làm

| # | Thay đổi | File | Chi tiết |
|---|----------|------|----------|
| 1 | Đường dẫn data | `train_eval_vit_l.py` | `KAGGLE_IMAGENET` → `/workspace/imagenet` |
| 2 | `CLONE_DIR` | `train_eval_vit_l.py` | `/kaggle/working/...` → `/workspace/lejepa-MLProject` |
| 3 | Backbone | `train_eval_vit_l.py` | `vit_large_patch16_224` → `vit_base_patch16_224` |
| 4 | Epochs | `train_eval_vit_l.py` | `MAX_EPOCHS = 100` → `MAX_EPOCHS = 1` |
| 5 | Batch size | `train_eval_vit_l.py` | Giảm nếu cần (ViT-B nhỏ hơn ViT-L) |
| 6 | Bỏ bootstrap Kaggle | `train_eval_vit_l.py` | Bỏ/skip git clone, shm remount |
| 7 | UI text | `train_eval_vit_l.py` | Cập nhật print messages ViT-L → ViT-B |
| 8 | Test trước train | `test_before_train.py` | Chạy trước khi train |

---

## TASK 1 — Đọc hiểu codebase

### Prompt (copy vào Claude Sonnet 3.6):

```
Đọc và tóm tắt cấu trúc của các file sau trong project /workspace/lejepa-MLProject:

1. train_eval_vit_l.py — file training chính
2. test_before_train.py — file test trước khi train
3. CLAUDE.md — hướng dẫn project

Tôi cần bạn liệt kê:
- Tất cả các hardcoded paths (đường dẫn cứng) trong train_eval_vit_l.py
- Tất cả chỗ reference đến backbone name "vit_large_patch16_224"
- Tất cả chỗ reference đến MAX_EPOCHS
- Tất cả chỗ reference đến BATCH_SIZE
- Cấu trúc data flow: data load → model → train → eval

KHÔNG sửa gì, chỉ đọc và báo cáo.
```

### Kết quả mong đợi:
- Danh sách tất cả hardcoded paths
- Danh sách tất cả references đến backbone, epochs, batch size
- Hiểu rõ flow trước khi sửa

---

## TASK 2 — Sửa đường dẫn data và bỏ bootstrap Kaggle

### Bối cảnh
Server RunPod có ImageNet tại `/workspace/imagenet/` với cấu trúc:
```
/workspace/imagenet/
├── train/    (1000 class subfolders)
└── val/      (1000 class subfolders)
```

File hiện tại hardcode đường dẫn Kaggle:
- Line 59: `CLONE_DIR = "/kaggle/working/lejepa-MLProject"`
- Line 238: `KAGGLE_IMAGENET = "/kaggle/input/imagenet-object-localization-challenge/ILSVRC/Data/CLS-LOC"`

### Prompt (copy vào Claude Sonnet 3.6):

```
Sửa file /workspace/lejepa-MLProject/train_eval_vit_l.py với các thay đổi sau:

## 1. Sửa CLONE_DIR (line 59)
Đổi:
CLONE_DIR = "/kaggle/working/lejepa-MLProject"
Thành:
CLONE_DIR = "/workspace/lejepa-MLProject"

## 2. Sửa KAGGLE_IMAGENET (line 238)
Đổi:
KAGGLE_IMAGENET = "/kaggle/input/imagenet-object-localization-challenge/ILSVRC/Data/CLS-LOC"
Thành:
IMAGENET_ROOT = "/workspace/imagenet"

Đồng thời đổi tên biến KAGGLE_IMAGENET → IMAGENET_ROOT ở tất cả nơi reference nó:
- Line 238: khai báo
- Line 386: trong build_pretrain_datamodule(), dòng train_root = os.path.join(KAGGLE_IMAGENET, "train") → os.path.join(IMAGENET_ROOT, "train")

## 3. Bỏ/Comment out block remount /dev/shm (lines 39-50)
Comment out block try...except remount /dev/shm vì trên RunPod không cần và không có quyền.
Giữ nguyên phần tạo cache dir (/dev/shm/hf_cache) và set env vars (lines 34-37).

## 4. Sửa build_pretrain_datamodule() (line 380-411)
Vì server có cả train/ và val/ riêng biệt (val có class subfolders), sửa hàm để:
- train dùng IMAGENET_ROOT + "/train"
- val dùng IMAGENET_ROOT + "/val" (thay vì lấy 50k cuối của train làm val proxy)

Cụ thể, thay toàn bộ nội dung hàm build_pretrain_datamodule() thành:

def build_pretrain_datamodule() -> DataModule:
    """DataModule dùng ImageNet-1K trên RunPod server."""
    train_root = os.path.join(IMAGENET_ROOT, "train")
    val_root   = os.path.join(IMAGENET_ROOT, "val")
    print(f"[data] ImageNet-1K train: {train_root}")
    print(f"[data] ImageNet-1K val:   {val_root}")

    train_ds = KaggleImageNetDataset(train_root, transform=make_train_transform())
    val_ds   = KaggleImageNetDataset(val_root,   transform=make_val_transform())

    print(f"[data] train={len(train_ds):,}  val={len(val_ds):,}")

    return DataModule(
        train=DataLoader(
            train_ds,
            batch_size=BATCH_SIZE, shuffle=True,
            num_workers=NUM_WORKERS, drop_last=True,
            pin_memory=True, persistent_workers=True,
        ),
        val=DataLoader(
            val_ds,
            batch_size=BATCH_SIZE, shuffle=False,
            num_workers=NUM_WORKERS,
            pin_memory=True, persistent_workers=True,
        ),
    )

KHÔNG sửa gì khác ngoài các điểm trên. Giữ nguyên tất cả comments và docstrings không liên quan.
```

### Checklist verify sau Task 2:
- [ ] `CLONE_DIR` đã đổi thành `/workspace/lejepa-MLProject`
- [ ] `KAGGLE_IMAGENET` đã đổi thành `IMAGENET_ROOT = "/workspace/imagenet"`
- [ ] Tất cả references đến `KAGGLE_IMAGENET` đã đổi thành `IMAGENET_ROOT`
- [ ] Block remount /dev/shm đã được comment out
- [ ] `build_pretrain_datamodule()` dùng val/ riêng thay vì proxy
- [ ] Không có lỗi syntax

---

## TASK 3 — Đổi backbone ViT-L → ViT-B/16

### Bối cảnh
ViT-B/16 có 86M params (vs ViT-L/16 304M params). Tên timm: `vit_base_patch16_224`.
`embed_dim` của ViT-B = 768 (vs ViT-L = 1024).
LeJEPA tự lấy `embed_dim` từ backbone nên KHÔNG cần sửa thủ công embed_dim.

### Prompt (copy vào Claude Sonnet 3.6):

```
Sửa file /workspace/lejepa-MLProject/train_eval_vit_l.py — đổi backbone từ ViT-L/16 sang ViT-B/16.

## Thay đổi cần làm:

### 1. BACKBONE_NAME (line 195)
Đổi:
BACKBONE_NAME = "vit_large_patch16_224"   # ViT-L/16, 304M params
Thành:
BACKBONE_NAME = "vit_base_patch16_224"    # ViT-B/16, 86M params

### 2. Cập nhật tất cả comments/print messages chứa "ViT-L" hoặc "vit_large"
Tìm và sửa TẤT CẢ chỗ sau:
- Line 132-138: markdown header "ViT-L/16 (304M params)" → "ViT-B/16 (86M params)"
- Line 135: "vit_large_patch16_224" trong comment → "vit_base_patch16_224"
- Line 415: docstring "ViT-L" → "ViT-B"
- Line 499: docstring "ViT-L" → "ViT-B"
- Line 560: print "Best checkpoint" (OK giữ nguyên)
- Line 697: print chứa BACKBONE_NAME (OK giữ nguyên vì dùng biến)
- Line 764: print "ViT-L/16" → "ViT-B/16"
- Line 777: print "ViT-L (100ep IN-1K)" → "ViT-B (1ep IN-1K)"
- Line 791: argparse description "ViT-L" → "ViT-B"

### 3. Checkpoint filename pattern (line 517)
Đổi:
filename="lejepa-vitl-ep{epoch:03d}"
Thành:
filename="lejepa-vitb-ep{epoch:03d}"

### 4. Giữ nguyên các tham số LeJEPA
KHÔNG sửa SIGREG_LAMBDA, SIGREG_SLICES, SIGREG_N_POINTS — các tham số này independent với backbone size.

Tìm bằng grep tất cả "vit_large", "ViT-L", "vitl", "304M" trong file và sửa hết. KHÔNG bỏ sót.
```

### Checklist verify sau Task 3:
- [ ] `BACKBONE_NAME = "vit_base_patch16_224"`
- [ ] Không còn reference nào đến `vit_large`, `ViT-L`, `304M`, `vitl` trong file
- [ ] Checkpoint filename chứa `vitb` thay vì `vitl`
- [ ] Các hyperparameters SIGReg giữ nguyên

---

## TASK 4 — Đổi MAX_EPOCHS = 1 và điều chỉnh liên quan

### Prompt (copy vào Claude Sonnet 3.6):

```
Sửa file /workspace/lejepa-MLProject/train_eval_vit_l.py — đổi MAX_EPOCHS từ 100 xuống 1 và điều chỉnh các tham số liên quan.

## Thay đổi cần làm:

### 1. MAX_EPOCHS (line 199)
Đổi:
MAX_EPOCHS = 100
Thành:
MAX_EPOCHS = 1

### 2. BATCH_SIZE (line 200)
Giảm xuống 256 để an toàn hơn cho VRAM:
Đổi:
BATCH_SIZE = 512
Thành:
BATCH_SIZE = 256

### 3. NUM_WORKERS (line 241)
Giữ nguyên NUM_WORKERS = 8 — phù hợp cho server.

### 4. Cập nhật print messages
- Line 777: nếu còn chứa "100ep" → sửa thành "1ep"

### 5. val_check_interval (line 551)
Vì chỉ có 1 epoch, giữ val_check_interval=1.0 (validate 1 lần cuối epoch).

KHÔNG sửa gì khác.
```

### Checklist verify sau Task 4:
- [ ] `MAX_EPOCHS = 1`
- [ ] `BATCH_SIZE = 256`
- [ ] Print messages phản ánh đúng "1ep"

---

## TASK 5 — Chạy test trước khi train

### Prompt (copy vào Claude Sonnet 3.6):

```
Chạy file test trước khi training để kiểm tra môi trường, dataset, model.

## Bước 1: Cài đặt dependencies
Chạy lệnh:
cd /workspace/lejepa-MLProject && SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0 pip install -e stable-pretraining/

## Bước 2: Chạy test
Chạy lệnh:
cd /workspace/lejepa-MLProject && python test_before_train.py --imagenet-root /workspace/imagenet

## Bước 3: Đọc output
Báo cáo lại cho tôi:
1. Tổng số check PASS / FAIL
2. Liệt kê tất cả FAIL (nếu có) kèm chi tiết
3. GPU detected: tên, VRAM
4. Dataset: số lượng images, classes
5. Forward pass: OK hay lỗi?
6. Dry-run training: loss values, VRAM usage
7. Kết luận: an toàn để train hay cần sửa gì?

Nếu có FAIL critical (GPU, import, model, dataset), DỪNG LẠI và báo cho tôi. KHÔNG chạy training.
```

### Kết quả mong đợi:
- Tất cả checks PASS
- GPU detected với đủ VRAM cho ViT-B/16
- Dataset ImageNet có 1000 classes, ~1.28M images
- Forward pass OK, loss hợp lệ (không NaN/Inf)
- Dry-run 3 steps thành công

---

## TASK 6 — Chạy Training

> **CHỈ CHẠY SAU KHI TASK 5 PASS TOÀN BỘ**

### Prompt (copy vào Claude Sonnet 3.6):

```
Chạy training LeJEPA ViT-B/16 trên ImageNet-1K, 1 epoch.

## Bước 1: Verify file đã sửa đúng
Chạy các lệnh kiểm tra nhanh:
cd /workspace/lejepa-MLProject
grep "BACKBONE_NAME" train_eval_vit_l.py
grep "MAX_EPOCHS" train_eval_vit_l.py
grep "IMAGENET_ROOT\|KAGGLE_IMAGENET" train_eval_vit_l.py
grep "BATCH_SIZE" train_eval_vit_l.py

Xác nhận:
- BACKBONE_NAME = "vit_base_patch16_224"
- MAX_EPOCHS = 1
- IMAGENET_ROOT = "/workspace/imagenet"
- BATCH_SIZE = 256 (hoặc 512)

Nếu KHÔNG đúng, DỪNG LẠI và báo cho tôi.

## Bước 2: Chạy training
cd /workspace/lejepa-MLProject && python train_eval_vit_l.py

## Bước 3: Monitor
Trong khi chạy, theo dõi:
1. Data loading OK? (print "[data] train=..., val=...")
2. Model init OK? (không error khi tạo LeJEPA)
3. Training bắt đầu? (loss values xuất hiện)
4. Loss giảm dần hay NaN?
5. Validation chạy OK?
6. Checkpoint được save?

## Bước 4: Báo cáo kết quả
Sau khi training xong (hoặc lỗi), báo cáo:
1. Training thành công hay lỗi?
2. Final loss value
3. Validation metrics
4. Checkpoint path
5. Thời gian training
6. Evaluation results (few-shot accuracy trên 8 datasets)

Nếu lỗi, copy TOÀN BỘ error traceback.
```

### Kết quả mong đợi:
- Training 1 epoch hoàn tất (~20-40 phút tùy GPU)
- Checkpoint được save tại `/workspace/lejepa-MLProject/checkpoints/`
- Few-shot evaluation chạy trên 8 datasets
- Bảng accuracy được in ra

---

## TASK 7 — Kiểm lỗi tổng thể

### Prompt (copy vào Claude Sonnet 3.6):

```
Kiểm tra tổng thể sau khi hoàn thành tất cả các task sửa code và training.

## Checklist kiểm tra:

### A. Kiểm tra file đã sửa đúng
Chạy các lệnh:
cd /workspace/lejepa-MLProject

# 1. Không còn reference Kaggle
grep -n "kaggle\|KAGGLE" train_eval_vit_l.py

# 2. Không còn reference ViT-L
grep -n "vit_large\|ViT-L\|vitl\|304M" train_eval_vit_l.py

# 3. Backbone đúng
grep -n "vit_base\|ViT-B\|vitb" train_eval_vit_l.py

# 4. Epochs = 1
grep -n "MAX_EPOCHS" train_eval_vit_l.py

# 5. Data path đúng
grep -n "IMAGENET_ROOT\|/workspace/imagenet" train_eval_vit_l.py

### B. Kiểm tra syntax Python
python -c "import ast; ast.parse(open('train_eval_vit_l.py').read()); print('Syntax OK')"

### C. Kiểm tra checkpoint tồn tại
ls -la checkpoints/

### D. Kiểm tra logs
ls -la logs/

### E. Báo cáo tổng hợp
Tạo bảng tóm tắt:

| Mục | Trước | Sau | Status |
|-----|-------|-----|--------|
| Backbone | vit_large_patch16_224 | vit_base_patch16_224 | ? |
| Data path | /kaggle/input/... | /workspace/imagenet | ? |
| CLONE_DIR | /kaggle/working/... | /workspace/lejepa-MLProject | ? |
| MAX_EPOCHS | 100 | 1 | ? |
| BATCH_SIZE | 512 | 256 | ? |
| Kaggle refs | Có | Không | ? |
| Test passed | - | Yes/No | ? |
| Training done | - | Yes/No | ? |
| Checkpoint saved | - | path | ? |

Nếu có bất kỳ lỗi nào, liệt kê cách sửa cụ thể.
```

---

## Thứ tự thực hiện

```
Task 1 (Đọc codebase)
  │
  ▼
Task 2 (Sửa đường dẫn data)
  │
  ▼
Task 3 (Đổi backbone ViT-B/16)
  │
  ▼
Task 4 (Đổi epochs = 1)
  │
  ▼
Task 5 (Chạy test_before_train.py)
  │
  ├── ALL PASS ──► Task 6 (Chạy training)
  │                    │
  │                    ▼
  │               Task 7 (Kiểm lỗi tổng thể)
  │
  └── HAS FAIL ──► Sửa lỗi ──► Quay lại Task 5
```

---

## Lưu ý quan trọng

### WARNING
- **KHÔNG chạy Task 6 (training) nếu Task 5 (test) có FAIL critical**
- Luôn verify bằng `grep` sau mỗi Task sửa code
- Nếu VRAM không đủ cho BATCH_SIZE=256, giảm xuống 128

### TIP
- Task 2, 3, 4 có thể gộp thành 1 prompt duy nhất nếu muốn nhanh hơn
- Nhưng tách ra giúp dễ debug nếu có lỗi

### QUAN TRỌNG
- File `test_before_train.py` đã dùng `vit_base_patch16_224` sẵn — không cần sửa
- File `test_before_train.py` đã dùng `--imagenet-root /workspace/imagenet` làm default — không cần sửa
- Comment `# ── Kaggle local ImageNet-1K` ở line 234-237 nên được cập nhật thành `# ── RunPod local ImageNet-1K`
