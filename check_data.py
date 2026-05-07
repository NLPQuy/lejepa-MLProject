import argparse
import os
import random
from pathlib import Path

def check_imagenet_data(data_dir: str):
    """
    Checks if the ImageNet data is ready in the specified directory.
    Expects ImageFolder format:
    data_dir/
      train/
        n01440764/
          *.JPEG
        ... (1000 folders)
      val/
        (either flat or with 1000 folders, but train must have 1000)
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"[FAIL] Data directory does not exist: {data_dir}")
        return False

    print(f"[INFO] Checking data directory: {data_dir}")

    train_dir = data_path / "train"
    val_dir = data_path / "val"

    # 1. Check train/ and val/ existence
    if not train_dir.exists():
        print(f"[FAIL] 'train' subdirectory not found in {data_dir}")
        return False
    print(f"[OK] 'train' subdirectory exists.")

    # In Kaggle local, val is not strictly required if we use last 50k of train,
    # but let's just warn if it doesn't exist.
    if not val_dir.exists():
        print(f"[WARN] 'val' subdirectory not found in {data_dir}. LeJEPA Kaggle script might use the last 50k of train instead.")
    else:
        print(f"[OK] 'val' subdirectory exists.")

    # 2. Check for 1000 classes in train
    train_subdirs = [d for d in train_dir.iterdir() if d.is_dir()]
    num_classes = len(train_subdirs)
    if num_classes != 1000:
        print(f"[FAIL] 'train' directory should have exactly 1000 class subfolders, found {num_classes}")
        return False
    print(f"[OK] 'train' directory contains exactly 1000 class subdirectories.")

    # 3. Check for actual images in some random class folders
    random_classes = random.sample(train_subdirs, min(5, num_classes))
    all_good = True
    for c_dir in random_classes:
        # Check if there are any files with image extensions
        files = list(c_dir.glob("*.JPEG")) + list(c_dir.glob("*.jpg")) + list(c_dir.glob("*.png"))
        if not files:
            print(f"[FAIL] No images found in {c_dir}")
            all_good = False
        else:
            if len(files) < 10:
                print(f"[WARN] Only {len(files)} images found in {c_dir}, expected much more for ImageNet.")
    
    if all_good:
        print(f"[OK] Random sampling of class folders shows images exist.")
    else:
        return False

    print("\n[SUCCESS] ImageNet data structure looks valid and ready for training!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify ImageNet Data Structure")
    parser.add_argument("--data-dir", type=str, default="/workspace/data/imagenet", 
                        help="Path to the root of the ImageNet data (contains train/ and val/)")
    args = parser.parse_args()
    
    check_imagenet_data(args.data_dir)
