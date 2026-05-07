"""
extract_imagenet.py
===================
Giải nén ImageNet-1K từ định dạng Parquet (HuggingFace) sang ImageFolder.

Yêu cầu:  pyarrow  Pillow  tqdm
Cài đặt:  pip install -r requirements_extract.txt

Cấu trúc INPUT (đã có sẵn trên Network Volume):
  /workspace/imagenet-hf/
      data/
          train-00000-of-00256.parquet
          train-00001-of-00256.parquet
          ...
          validation-00000-of-00016.parquet
          ...
      classes.py

Cấu trúc OUTPUT (dùng được với torchvision.ImageFolder):
  /workspace/imagenet/
      train/
          n01440764/   ← synset ID
              n01440764_00000001.JPEG
              ...
          n01443537/
          ...   (1000 class folders)
      val/
          n01440764/
          ...

Sau khi xong, sửa train_eval_vit_l.py dòng 238:
  KAGGLE_IMAGENET = "/workspace/imagenet"
"""

import io
import sys
from pathlib import Path

import pyarrow.parquet as pq
from PIL import Image
from tqdm import tqdm

# ─── CẤU HÌNH ────────────────────────────────────────────────────────────────
SOURCE_DIR  = Path("/workspace/imagenet-hf")   # thư mục đã tải về
DATA_DIR    = SOURCE_DIR / "data"               # nơi chứa file .parquet
EXTRACT_DIR = Path("/workspace/imagenet")       # thư mục đích

# Các split cần giải nén: train và validation (bỏ test vì không có label)
SPLITS = {
    "train":      "train",       # parquet prefix → tên thư mục output
    "validation": "val",
}
# ─────────────────────────────────────────────────────────────────────────────


def load_label_map() -> dict[int, str]:
    """
    Đọc mapping label_index → synset_id từ classes.py của repo HuggingFace.
    Trả về dict {0: 'n01440764', 1: 'n01443537', ...}.
    Nếu không đọc được, trả về dict rỗng (sẽ dùng số nguyên làm tên thư mục).
    """
    classes_file = SOURCE_DIR / "classes.py"
    if not classes_file.exists():
        print("⚠  classes.py không tìm thấy → dùng label index làm tên thư mục.")
        return {}

    namespace: dict = {}
    try:
        exec(classes_file.read_text(encoding="utf-8"), namespace)
    except Exception as e:
        print(f"⚠  Không parse được classes.py: {e}")
        return {}

    # Thử các tên biến phổ biến trong repo ILSVRC/imagenet-1k
    for key in ["IMAGENET_CLASSES", "classes", "CLASS_INDEX", "idx_to_class", "CLASSES"]:
        val = namespace.get(key)
        if val is None:
            continue
        if isinstance(val, dict):
            result = {}
            for k, v in val.items():
                synset = v[0] if isinstance(v, (list, tuple)) else v
                result[int(k)] = str(synset)
            print(f"✓  Label map: {len(result)} classes từ biến '{key}'.")
            return result
        if isinstance(val, (list, tuple)):
            result = {}
            for i, v in enumerate(val):
                synset = v[0] if isinstance(v, (list, tuple)) else v
                result[i] = str(synset)
            print(f"✓  Label map: {len(result)} classes từ biến '{key}'.")
            return result

    print("⚠  Không tìm thấy biến label map trong classes.py → dùng label index.")
    return {}


def get_parquet_files(split_prefix: str) -> list[Path]:
    """Trả về danh sách file parquet theo thứ tự cho split nhất định."""
    files = sorted(DATA_DIR.glob(f"{split_prefix}-*.parquet"))
    if not files:
        # fallback: khớp bất kỳ file bắt đầu bằng split_prefix
        files = sorted(DATA_DIR.glob(f"{split_prefix}*.parquet"))
    return files


def decode_image(raw_value) -> Image.Image | None:
    """
    Decode giá trị parquet thành PIL Image.
    Hỗ trợ 2 định dạng:
      - struct {'bytes': <bytes>, 'path': <str>}  (HuggingFace Image feature)
      - binary thuần (<bytes>)
    """
    raw_py = raw_value.as_py() if hasattr(raw_value, "as_py") else raw_value

    if isinstance(raw_py, dict):
        img_bytes = raw_py.get("bytes") or raw_py.get("data")
    elif isinstance(raw_py, bytes):
        img_bytes = raw_py
    else:
        img_bytes = bytes(raw_py)

    if not img_bytes:
        return None
    return Image.open(io.BytesIO(img_bytes))


def extract_split(split_prefix: str, out_subdir: str, label_map: dict[int, str]):
    """Giải nén toàn bộ một split."""
    parquet_files = get_parquet_files(split_prefix)
    if not parquet_files:
        print(f"\n⚠  Không tìm thấy file parquet nào cho split '{split_prefix}'. Bỏ qua.")
        return

    out_path = EXTRACT_DIR / out_subdir
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Split: {split_prefix}  →  {out_path}")
    print(f"  Số file parquet: {len(parquet_files)}")
    print(f"{'='*60}")

    global_idx = 0   # index ảnh toàn cục (dùng cho tên file)
    skipped    = 0   # số ảnh đã tồn tại, bỏ qua

    for pq_file in parquet_files:
        table     = pq.read_table(pq_file)
        n_rows    = table.num_rows
        img_col   = table.column("image")
        label_col = table.column("label")

        for i in tqdm(range(n_rows), desc=pq_file.stem, leave=True, file=sys.stdout):
            label  = int(label_col[i].as_py())
            synset = label_map.get(label, str(label))

            save_dir = out_path / synset
            save_dir.mkdir(exist_ok=True)

            img_path = save_dir / f"{synset}_{global_idx:08d}.JPEG"
            global_idx += 1

            if img_path.exists():
                skipped += 1
                continue

            try:
                img = decode_image(img_col[i])
                if img is None:
                    print(f"\n  ⚠  Ảnh rỗng tại index {global_idx - 1}, bỏ qua.")
                    continue
                img.convert("RGB").save(img_path, "JPEG", quality=95)
            except Exception as e:
                print(f"\n  ⚠  Lỗi ảnh {global_idx - 1}: {e}")

    saved = global_idx - skipped
    print(f"\n  ✓  {split_prefix}: lưu {saved:,} ảnh mới, bỏ qua {skipped:,} ảnh đã có.")


def sanity_check():
    """Kiểm tra nhanh kết quả sau khi giải nén."""
    print("\n=== KIỂM TRA KẾT QUẢ ===")
    for subdir in ["train", "val"]:
        p = EXTRACT_DIR / subdir
        if not p.exists():
            print(f"  ❌  {p} không tồn tại")
            continue
        n_classes = len(list(p.iterdir()))
        print(f"  {subdir}: {n_classes} thư mục class")
    print(f"\nSau khi xong, sửa train_eval_vit_l.py dòng 238:")
    print(f'  KAGGLE_IMAGENET = "{EXTRACT_DIR}"')


def main():
    print("=" * 60)
    print("  ImageNet-1K: Parquet → ImageFolder")
    print("=" * 60)
    print(f"  Source : {DATA_DIR}")
    print(f"  Target : {EXTRACT_DIR}")

    if not DATA_DIR.exists():
        sys.exit(f"\n❌  Không tìm thấy {DATA_DIR}. Kiểm tra lại đường dẫn SOURCE_DIR.")

    # In danh sách file parquet tìm được
    all_parquets = sorted(DATA_DIR.glob("*.parquet"))
    print(f"\n  Tổng số file parquet: {len(all_parquets)}")
    for f in all_parquets[:5]:
        print(f"    {f.name}")
    if len(all_parquets) > 5:
        print(f"    ... và {len(all_parquets) - 5} files khác")

    label_map = load_label_map()

    for split_prefix, out_subdir in SPLITS.items():
        extract_split(split_prefix, out_subdir, label_map)

    sanity_check()
    print("\n✅  XONG! Dataset sẵn sàng để train.")


if __name__ == "__main__":
    main()
