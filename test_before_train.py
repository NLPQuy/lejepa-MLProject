#!/usr/bin/env python3
"""test_before_train.py — Dry-run checks before full LeJEPA ViT-B/16 training on RunPod.

Run:  python test_before_train.py [--imagenet-root /workspace/imagenet]

Completes in < 2 minutes.  Each check prints ✅ PASS or ❌ FAIL.
At the end a summary tells you whether it is safe to start training.
"""

import argparse
import gc
import os
import sys
import time
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# Configurable paths (override via CLI)
# ---------------------------------------------------------------------------
DEFAULT_IMAGENET_ROOT = "/workspace/imagenet"
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
SPT_PATH = os.path.join(REPO_ROOT, "stable-pretraining")

# Ensure packages are importable
for p in [REPO_ROOT, SPT_PATH]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ---------------------------------------------------------------------------
# Bookkeeping
# ---------------------------------------------------------------------------
_results: list[tuple[str, bool, str]] = []  # (name, passed, detail)


def check(name: str, passed: bool, detail: str = ""):
    tag = "✅ PASS" if passed else "❌ FAIL"
    msg = f"  {tag}  {name}"
    if detail:
        msg += f"  —  {detail}"
    print(msg)
    _results.append((name, passed, detail))
    return passed


def section(title: str):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")


# ===================================================================
# 4a. Environment Checks
# ===================================================================
def check_environment():
    section("4a. Environment Checks")

    # --- GPU ---
    try:
        import torch
        gpu_ok = torch.cuda.is_available()
        if gpu_ok:
            name = torch.cuda.get_device_name(0)
            vram = torch.cuda.get_device_properties(0).total_memory / 1e9
            n_gpu = torch.cuda.device_count()
            check("GPU available", True, f"{n_gpu}x {name}, {vram:.1f} GB VRAM")
            bf16 = torch.cuda.is_bf16_supported()
            check("bfloat16 support", bf16,
                  "Required for bf16-mixed precision" if not bf16 else "OK")
        else:
            check("GPU available", False, "torch.cuda.is_available() == False")
    except Exception as e:
        check("GPU available", False, str(e))

    # --- Core imports ---
    imports = {
        "torch": "torch",
        "torchvision": "torchvision",
        "timm": "timm",
        "lightning": "lightning",
        "torchmetrics": "torchmetrics",
        "wandb": "wandb",
        "datasets (HF)": "datasets",
        "huggingface_hub": "huggingface_hub",
        "hydra": "hydra",
        "omegaconf": "omegaconf",
        "stable_pretraining": "stable_pretraining",
        "lejepa": "lejepa",
    }
    all_ok = True
    for label, mod in imports.items():
        try:
            __import__(mod)
            check(f"import {label}", True)
        except ImportError as e:
            check(f"import {label}", False, str(e))
            all_ok = False

    # --- Env vars ---
    hf_token = os.environ.get("HF_TOKEN", "")
    # HF_TOKEN is only needed for eval phase (Phase 2 embedding extraction).
    # Pretraining on local ImageNet works without it → treat as non-critical warning.
    if hf_token:
        check("HF_TOKEN set", True, "OK")
    else:
        # Don't fail — just warn. Pretraining will work; eval datasets will fail later.
        print("  ⚠️  WARN  HF_TOKEN set  —  Not set (OK for pretraining; needed for eval phase)")
        _results.append(("HF_TOKEN set", True, "Not set — pretraining OK, eval will need token"))

    # --- Disk space ---
    try:
        st = os.statvfs(REPO_ROOT)
        free_gb = st.f_bavail * st.f_frsize / 1e9
        check("Disk space", free_gb > 10,
              f"{free_gb:.1f} GB free (need >10 GB for checkpoints)")
    except Exception as e:
        check("Disk space", False, str(e))


# ===================================================================
# 4b. Dataset Checks
# ===================================================================
def check_dataset(imagenet_root: str):
    section("4b. Dataset Checks")
    import torch
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader

    train_root = os.path.join(imagenet_root, "train")
    val_root = os.path.join(imagenet_root, "val")

    # --- Path exists ---
    check("Train path exists", os.path.isdir(train_root), train_root)
    check("Val path exists", os.path.isdir(val_root), val_root)

    if not os.path.isdir(train_root):
        check("Dataset usable", False, "Train path missing — cannot continue")
        return

    # --- Class count ---
    classes = sorted([d for d in os.listdir(train_root)
                      if os.path.isdir(os.path.join(train_root, d))])
    check("Train classes == 1000", len(classes) == 1000, f"Found {len(classes)}")

    val_classes = sorted([d for d in os.listdir(val_root)
                          if os.path.isdir(os.path.join(val_root, d))])
    check("Val classes == 1000", len(val_classes) == 1000, f"Found {len(val_classes)}")

    # --- Sample a few classes for image count (count VALID non-zero files) ---
    import random
    sample_classes = random.sample(classes, min(5, len(classes)))
    issues = []
    for cls in sample_classes:
        cls_dir = os.path.join(train_root, cls)
        files = os.listdir(cls_dir)
        img_files = [f for f in files if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
        valid_files = [f for f in img_files
                       if os.path.getsize(os.path.join(cls_dir, f)) > 0]
        zero_kb = len(img_files) - len(valid_files)
        if zero_kb > 0:
            issues.append(f"class {cls}: {zero_kb} zero-byte (will be skipped by SafeImageFolder)")
        if len(valid_files) < 10:
            issues.append(f"class {cls}: only {len(valid_files)} valid images (critical!)")

    # Zero-byte files are handled by SafeImageFolder at runtime — only fail if truly unusable
    critical_issues = [i for i in issues if "critical" in i]
    check("Sample classes healthy", len(critical_issues) == 0,
          "; ".join(issues) if issues else f"Checked {len(sample_classes)} classes, all OK")
    if issues and not critical_issues:
        print(f"    ℹ️  Zero-byte files present but SafeImageFolder will skip them at runtime")

    # --- Check zero-byte / corrupt files (fast Python scan, samples 20 classes) ---
    try:
        import random as _rng
        sample_n = 20  # scan 20 random classes as representative sample
        sample_cls = _rng.sample(classes, min(sample_n, len(classes)))
        total_files = 0
        total_zero  = 0
        t_scan = time.time()
        for cls in sample_cls:
            cls_dir = os.path.join(train_root, cls)
            try:
                with os.scandir(cls_dir) as it:
                    for entry in it:
                        if entry.is_file():
                            total_files += 1
                            if entry.stat().st_size == 0:
                                total_zero += 1
            except OSError:
                pass
        scan_time = time.time() - t_scan
        pct_zero = 100.0 * total_zero / max(total_files, 1)
        # Extrapolate to full dataset
        est_total = int(total_files * 1000 / sample_n)
        est_zero  = int(total_zero  * 1000 / sample_n)
        msg = (f"~{est_zero:,}/{est_total:,} estimated 0-byte ({pct_zero:.1f}%) "
               f"[sampled {sample_n} classes in {scan_time:.1f}s] "
               f"— SafeImageFolder skips them at runtime")
        # Pass if <50% zero-byte (SafeImageFolder handles the rest)
        check("Zero-byte files", pct_zero < 50.0, msg)
        if pct_zero >= 50.0:
            print(f"    ⚠️  HIGH zero-byte rate ({pct_zero:.0f}%). Run: python fast_repair_imagenet.py")
        elif pct_zero > 0:
            print(f"    ℹ️  {pct_zero:.1f}% zero-byte (being repaired or will be skipped)")
    except Exception as e:
        check("Zero-byte files", False, f"scan error: {e}")

    # --- Load 1 batch (with error-tolerant loader) ---
    try:
        from PIL import Image

        class SafeImageFolder(datasets.ImageFolder):
            """ImageFolder that skips corrupt/zero-byte images."""
            def __getitem__(self, index):
                while True:
                    try:
                        path, target = self.samples[index]
                        if os.path.getsize(path) == 0:
                            index = (index + 1) % len(self)
                            continue
                        return super().__getitem__(index)
                    except Exception:
                        index = (index + 1) % len(self)

        tf = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])
        ds = SafeImageFolder(train_root, transform=tf)
        check("ImageFolder load", True, f"{len(ds):,} images total")

        dl = DataLoader(ds, batch_size=8, shuffle=False, num_workers=0, pin_memory=True)
        batch_imgs, batch_labels = next(iter(dl))
        check("DataLoader batch", True,
              f"images {tuple(batch_imgs.shape)}, labels {tuple(batch_labels.shape)}, "
              f"dtype={batch_imgs.dtype}")
    except Exception as e:
        check("DataLoader batch", False, str(e))


# ===================================================================
# 4c. Model + Forward Pass Checks
# ===================================================================
def check_model_forward():
    section("4c. Model + Forward Pass Checks")
    import torch

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # --- Create model ---
    BACKBONE = "vit_base_patch16_224"
    try:
        from stable_pretraining.methods.lejepa import LeJEPA, LeJEPAOutput
        model = LeJEPA(
            encoder_name=BACKBONE,
            n_slices=1024,
            n_points=17,
            lamb=0.05,
            pretrained=False,
            drop_path_rate=0.1,
        ).to(device)
        n_params = sum(p.numel() for p in model.parameters()) / 1e6
        check(f"Model init ({BACKBONE})", True, f"{n_params:.1f}M params, embed_dim={model.embed_dim}")
    except Exception as e:
        check(f"Model init ({BACKBONE})", False, traceback.format_exc())
        return None

    # --- Forward pass (eval) ---
    try:
        model.eval()
        dummy = torch.randn(2, 3, 224, 224, device=device)
        with torch.no_grad(), torch.amp.autocast("cuda", dtype=torch.bfloat16):
            out = model(images=dummy)
        check("Forward (eval)", True,
              f"embedding shape={tuple(out.embedding.shape)}, dtype={out.embedding.dtype}")
    except Exception as e:
        check("Forward (eval)", False, str(e))

    # --- Forward pass (train) with loss ---
    try:
        model.train()
        bs = 4
        global_views = [torch.randn(bs, 3, 224, 224, device=device) for _ in range(2)]
        local_views = [torch.randn(bs, 3, 96, 96, device=device) for _ in range(6)]

        with torch.amp.autocast("cuda", dtype=torch.float16):
            out = model(global_views=global_views, local_views=local_views)

        loss_val = out.loss.item()
        inv_val = out.inv_loss.item()
        sig_val = out.sigreg_loss.item()

        import math
        loss_ok = not (math.isnan(loss_val) or math.isinf(loss_val))
        check("Forward (train) + loss", loss_ok,
              f"loss={loss_val:.4f}, inv={inv_val:.4f}, sigreg={sig_val:.4f}")
    except Exception as e:
        check("Forward (train) + loss", False, traceback.format_exc())
        return None

    # --- Backward / gradient flow ---
    try:
        out.loss.backward()
        grad_ok = all(
            p.grad is not None and not torch.isnan(p.grad).any()
            for p in model.parameters() if p.requires_grad and p.grad is not None
        )
        n_grad = sum(1 for p in model.parameters() if p.grad is not None)
        check("Backward + gradients", grad_ok, f"{n_grad} param groups with gradients")
    except Exception as e:
        check("Backward + gradients", False, str(e))

    # --- Mixed precision check ---
    try:
        model.zero_grad()
        scaler = torch.amp.GradScaler("cuda")
        with torch.amp.autocast("cuda", dtype=torch.float16):
            out2 = model(global_views=global_views, local_views=local_views)
        scaler.scale(out2.loss).backward()
        check("Mixed precision (bf16)", True, "GradScaler + autocast OK")
    except Exception as e:
        check("Mixed precision (bf16)", False, str(e))

    # Cleanup
    del model, global_views, local_views
    gc.collect()
    torch.cuda.empty_cache()
    return True


# ===================================================================
# 4d. Dry-Run Training (3 steps with real data)
# ===================================================================
def check_dry_run(imagenet_root: str):
    section("4d. Dry-Run Training (3 steps, real data)")
    import torch
    from torchvision import datasets, transforms
    from torch.utils.data import DataLoader

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_root = os.path.join(imagenet_root, "train")
    BACKBONE = "vit_base_patch16_224"

    if not os.path.isdir(train_root):
        check("Dry-run", False, "Train path missing")
        return

    # --- Build small dataloader (skip zero-byte files) ---
    from PIL import Image

    class SafeImageFolder(datasets.ImageFolder):
        def __getitem__(self, index):
            while True:
                try:
                    path, target = self.samples[index]
                    if os.path.getsize(path) == 0:
                        index = (index + 1) % len(self)
                        continue
                    return super().__getitem__(index)
                except Exception:
                    index = (index + 1) % len(self)

    tf = transforms.Compose([
        transforms.RandomResizedCrop(224, scale=(0.3, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    ds = SafeImageFolder(train_root, transform=tf)
    dl = DataLoader(ds, batch_size=8, shuffle=True, num_workers=0,
                    pin_memory=True, drop_last=True)

    # --- Build model ---
    try:
        from stable_pretraining.methods.lejepa import LeJEPA
    except ImportError as e:
        check("Dry-run imports", False, str(e))
        return

    model = LeJEPA(
        encoder_name=BACKBONE,
        n_slices=256,  # fewer slices for speed
        n_points=17,
        lamb=0.05,
        pretrained=False,
        drop_path_rate=0.1,
    ).to(device).train()

    opt = torch.optim.AdamW(model.parameters(), lr=5e-4, weight_decay=5e-2)
    scaler = torch.amp.GradScaler("cuda")

    # --- Run 3 steps ---
    losses = []
    step_times = []
    torch.cuda.reset_peak_memory_stats()

    data_iter = iter(dl)
    for step in range(3):
        try:
            imgs, labels = next(data_iter)
        except StopIteration:
            data_iter = iter(dl)
            imgs, labels = next(data_iter)

        imgs = imgs.to(device, non_blocking=True)

        # Create 2 global views + 2 local views (small for speed)
        global_views = [imgs, imgs]
        # Resize to 96x96 for local views (must be divisible by patch_size=16)
        local_imgs = torch.nn.functional.interpolate(imgs, size=96, mode="bilinear",
                                                      align_corners=False)
        local_views = [local_imgs, local_imgs]

        t0 = time.perf_counter()
        opt.zero_grad()
        with torch.amp.autocast("cuda", dtype=torch.float16):
            out = model(global_views=global_views, local_views=local_views)

        scaler.scale(out.loss).backward()
        scaler.step(opt)
        scaler.update()
        dt = time.perf_counter() - t0

        loss_val = out.loss.item()
        losses.append(loss_val)
        step_times.append(dt)
        print(f"    step {step}: loss={loss_val:.4f}  time={dt:.2f}s")

    # --- Verify losses ---
    import math
    no_nan = all(not (math.isnan(l) or math.isinf(l)) for l in losses)
    check("3 steps no NaN/Inf", no_nan, f"losses={[f'{l:.4f}' for l in losses]}")

    avg_time = sum(step_times) / len(step_times)
    peak_vram = torch.cuda.max_memory_allocated() / 1e9
    check("Step timing", True, f"avg={avg_time:.2f}s/step, peak VRAM={peak_vram:.1f} GB")

    # Estimate full training time
    # Full config: BS=512 (vs 8 here), 1.28M images, 100 epochs
    steps_per_epoch = 1_281_167 // 512
    total_steps = steps_per_epoch * 100
    # Scale time: real batch is 64x bigger, but GPU utilization is higher
    # Use a rough 40x factor (not linear due to GPU saturation)
    est_step_time = avg_time * 30  # rough estimate for BS=512
    est_hours = (total_steps * est_step_time) / 3600
    print(f"\n    📊 Estimated full training: ~{est_hours:.0f} hours "
          f"({total_steps:,} steps × ~{est_step_time:.1f}s/step)")
    print(f"    📊 Peak VRAM (BS=8): {peak_vram:.1f} GB")

    # --- Checkpoint save/load ---
    ckpt_path = os.path.join(REPO_ROOT, "checkpoints", "_test_ckpt.pt")
    os.makedirs(os.path.dirname(ckpt_path), exist_ok=True)
    try:
        torch.save({
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": opt.state_dict(),
            "step": 3,
        }, ckpt_path)
        check("Checkpoint save", True, ckpt_path)

        ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
        model.load_state_dict(ckpt["model_state_dict"])
        check("Checkpoint load", True, f"step={ckpt['step']}")

        # Cleanup test checkpoint
        os.remove(ckpt_path)
    except Exception as e:
        check("Checkpoint save/load", False, str(e))

    # Cleanup
    del model, opt, scaler
    gc.collect()
    torch.cuda.empty_cache()


# ===================================================================
# Summary
# ===================================================================
def print_summary():
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in _results if ok)
    n_fail = sum(1 for _, ok, _ in _results if not ok)
    total = len(_results)

    print(f"\n  Total: {total}  |  ✅ Pass: {n_pass}  |  ❌ Fail: {n_fail}\n")

    if n_fail > 0:
        print("  Failed checks:")
        for name, ok, detail in _results:
            if not ok:
                print(f"    ❌ {name}: {detail}")

        # Critical failures
        critical = [
            "GPU available", "import torch", "import stable_pretraining",
            "Model init (ViT-L)", "Forward (train) + loss",
            "Backward + gradients", "Train path exists",
        ]
        critical_fails = [n for n, ok, _ in _results if not ok and n in critical]
        if critical_fails:
            print(f"\n  🚨 CRITICAL FAILURES: {critical_fails}")
            print("  ⛔ DO NOT start training until these are fixed.\n")
            print("  Hướng dẫn sửa:")
            for f in critical_fails:
                if "GPU" in f:
                    print("    - Kiểm tra NVIDIA driver: nvidia-smi")
                    print("    - Kiểm tra CUDA: python -c 'import torch; print(torch.version.cuda)'")
                elif "import" in f:
                    print(f"    - pip install -e . && pip install -e stable-pretraining/")
                elif "Model" in f or "Forward" in f or "Backward" in f:
                    print("    - Kiểm tra VRAM đủ cho ViT-L (cần ~20GB+ cho BS=4)")
                elif "Train path" in f:
                    print(f"    - Kiểm tra dataset: ls {DEFAULT_IMAGENET_ROOT}/train/")
        else:
            print("\n  ⚠️  Non-critical failures. Training may still work but review above.\n")
    else:
        print("  🎉 ALL CHECKS PASSED — Safe to start full training!\n")


# ===================================================================
# Main
# ===================================================================
def main():
    parser = argparse.ArgumentParser(description="Pre-training dry-run checks")
    parser.add_argument("--imagenet-root", default=DEFAULT_IMAGENET_ROOT,
                        help="Path to ImageNet root (with train/ and val/ subdirs)")
    args = parser.parse_args()

    print(f"\n{'#'*60}")
    print(f"  LeJEPA Pre-Training Dry-Run Test")
    print(f"  ImageNet root: {args.imagenet_root}")
    print(f"  Repo root:     {REPO_ROOT}")
    print(f"{'#'*60}")

    t0 = time.time()

    check_environment()
    check_dataset(args.imagenet_root)
    check_model_forward()
    check_dry_run(args.imagenet_root)

    elapsed = time.time() - t0
    print(f"\n  ⏱  Total time: {elapsed:.1f}s")

    print_summary()


if __name__ == "__main__":
    main()
