# Prompt cho Claude Sonnet — LeJEPA ViT-B/16 Training Pipeline

## Mục đích
File này chứa toàn bộ context và các lệnh cụ thể để:
1. Re-extract ImageNet val set bị hỏng
2. Audit + fix `train_eval_vit_l.py`
3. Kiểm tra GPU state
4. Khởi động lại training an toàn

---

## CONTEXT TỔNG QUAN

**Server**: RunPod GPU — NVIDIA RTX PRO 4500 Blackwell (32 GB VRAM)  
**Project dir**: `/workspace/lejepa-MLProject/`  
**Python venv**: `/workspace/jepa/bin/python`  
**Dataset parquet**: `/workspace/imagenet-hf/data/` (train + validation parquet files)  
**Dataset extracted**: `/workspace/imagenet/` (train/ OK, val/ toàn bộ 0-byte vì crashed)

**Vấn đề đã phát hiện**:
- Val set `/workspace/imagenet/val/` có 50,000 files, tất cả 0-byte (crash khi extract)
- Parquet gốc `/workspace/imagenet-hf/data/validation-*.parquet` (14 files, ~6.5GB) vẫn tốt
- Training script trước đây crash tại validation vì đọc 0-byte → `UnidentifiedImageError`
- Training epoch 0 đã hoàn tất 2 lần nhưng checkpoint không được lưu vì crash ở val

---

## TASK 1: Fix `prepare_imagenet.py` và re-extract val

File `/workspace/prepare_imagenet.py` đã được sửa để:
- Check `img_path.stat().st_size > 0` (không chỉ `img_path.exists()`)
- Xóa file 0-byte trước khi ghi lại
- Hỗ trợ `--val-only` flag

### Lệnh cần chạy:
```bash
cd /workspace
/workspace/jepa/bin/python prepare_imagenet.py --val-only
```

**Thời gian ước tính**: 30-60 phút (14 parquet files × ~3572 rows = 50K ảnh)

**Verify sau khi xong**:
```bash
find /workspace/imagenet/val -name "*.JPEG" -size 0 | wc -l
# Expected: 0

find /workspace/imagenet/val -name "*.JPEG" | wc -l
# Expected: ~50000

ls /workspace/imagenet/val | wc -l
# Expected: 1000 (classes)
```

---

## TASK 2: Audit `train_eval_vit_l.py`

File chính: `/workspace/lejepa-MLProject/train_eval_vit_l.py`

### Checklist audit (tất cả đã được verify/fix):

| Item | Line | Status | Chi tiết |
|------|------|--------|----------|
| Backbone ViT-B/16 | 204 | ✅ | `BACKBONE_NAME = "vit_base_patch16_224"` |
| MAX_EPOCHS = 1 | 208 | ✅ | Đúng 1 epoch |
| save_on_train_epoch_end | 529 | ✅ | Lưu checkpoint sau train, trước val |
| monitor=None | 527 | ✅ | Không phụ thuộc val metric |
| limit_val_batches=0 | 560 | ✅ | Tắt val (val set hỏng) |
| HF_TOKEN try/except | 62-71 | ✅ | Không crash nếu token thiếu |
| GITHUB_TOKEN hardcoded | 57 | ⚠️ | Security: xóa sau khi xong project |
| __getitem__ try/except | 380-389 | ✅ | Skip ảnh hỏng trong train |
| Label dtype .long() | 666,674,678 | ✅ | Tránh cross_entropy crash |
| Empty embs guard | 615-616 | ✅ | torch.cat([]) không crash |
| Empty train probe guard | 660-661 | ✅ | Probe train không crash |
| Per-dataset try/except | 750-752 | ✅ | 1 dataset fail không crash toàn bộ |
| Checkpoint file guard | 797-801 | ✅ | Không gọi eval với ckpt=None |
| model_state empty guard | 714-718 | ✅ | Rõ ràng khi key sai |
| Local view size 96x96 | 288 | ✅ | Chia hết cho patch size 16 |
| CUDA expandable_segments | 50 | ✅ | Giảm memory fragmentation |
| BATCH_SIZE=64 | 209 | ✅ | Tránh OOM 32GB VRAM |
| N_LOCAL_VIEWS=4 | 214 | ✅ | Tránh OOM |

> [!WARNING]
> **Sau khi training xong**, hãy xóa/rotate GITHUB_TOKEN ở line 57.
> Token `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` đang hardcode trong file.

---

## TASK 3: Kiểm tra GPU state

Script `/workspace/lejepa-MLProject/check_gpu_state.py` đã được tạo.

```bash
# Chỉ kiểm tra:
/workspace/jepa/bin/python /workspace/lejepa-MLProject/check_gpu_state.py

# Kill zombie processes nếu có:
/workspace/jepa/bin/python /workspace/lejepa-MLProject/check_gpu_state.py --kill --yes
```

**Expected output khi GPU sạch**:
```
GPU 0: NVIDIA RTX PRO 4500 Blackwell
  Used  : 2 MiB
  Free  : 32124 MiB
✓ Không có process nào đang dùng GPU.
✓ Không có zombie training process.
```

---

## TASK 4: Khởi động training

Chỉ chạy sau khi:
- [ ] Val set đã được re-extract (Task 1) — hoặc confirm `limit_val_batches=0` (đã set)
- [ ] GPU sạch (Task 3)
- [ ] `train_eval_vit_l.py` syntax OK

```bash
cd /workspace/lejepa-MLProject

# Verify syntax
/workspace/jepa/bin/python -c "import ast; ast.parse(open('train_eval_vit_l.py').read()); print('OK')"

# Start training (nohup → chạy ngầm kể cả khi mất kết nối SSH)
nohup /workspace/jepa/bin/python train_eval_vit_l.py > logs/training_run4.log 2>&1 &
echo "Training PID: $!"
```

**Monitor training**:
```bash
# Real-time log
tail -f /workspace/lejepa-MLProject/logs/training_run4.log

# Metrics (sau vài step)
VERSION=$(ls -t /workspace/lejepa-MLProject/logs/lightning_logs/ | head -1)
tail -5 /workspace/lejepa-MLProject/logs/lightning_logs/$VERSION/metrics.csv

# GPU usage
watch -n 5 nvidia-smi
```

**Checkpoint location**:
```
/workspace/lejepa-MLProject/checkpoints/lejepa-vitb-ep000.ckpt   ← saved after epoch 0
/workspace/lejepa-MLProject/checkpoints/last.ckpt                ← always latest
```

---

## TASK 5: Chạy eval riêng (nếu muốn re-eval sau training)

```bash
source /workspace/.env
/workspace/jepa/bin/python train_eval_vit_l.py \
  --skip-pretrain \
  --checkpoint /workspace/lejepa-MLProject/checkpoints/last.ckpt
```

---

## Lệnh debug nhanh

```bash
# Đếm file 0-byte trong val
find /workspace/imagenet/val -name "*.JPEG" -size 0 | wc -l

# Xem checkpoints đã có
ls -lh /workspace/lejepa-MLProject/checkpoints/

# Top training loss trong metrics
VERSION=$(ls -t /workspace/lejepa-MLProject/logs/lightning_logs/ | head -1)
awk -F',' 'NR>1 && $3!=""' \
  /workspace/lejepa-MLProject/logs/lightning_logs/$VERSION/metrics.csv \
  | awk -F',' '{printf "Step: %-6s | Loss: %-8s\n", $10, $3}' | tail -10
```
