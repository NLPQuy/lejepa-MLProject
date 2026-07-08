"""Paper-spec frozen linear-probe evaluation for LeJEPA checkpoints.

Reproduces the README/paper linear-probe protocol so numbers are comparable to
the paper (NOT the online-probe used during training):
  * features = concat of the CLS token from the **last two** ViT blocks
  * LayerNorm on the concatenated CLS, then a linear classifier
  * AdamW, lr 1e-3, weight_decay 1e-6, warmup + cosine
  * backbone is FROZEN (loaded from checkpoint, no grad)

It deliberately avoids the `stable_pretraining` data pipeline (which needs
torchvision 0.26; local env is 0.20) by loading the HF arrow dataset directly
and using plain torchvision v1 transforms.

Usage:
    python eval-frozen-paperspec.py --ckpt <path.ckpt> --data_local_path data/imagenet10 \
        --tag baseline_100 --probe_epochs 100 --out eval_results/batch_1/baseline_100.json

Features are extracted ONCE with a deterministic center-crop (no train aug) and
cached, so every checkpoint is probed under an identical, reproducible protocol.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import timm
import torch
import torch.nn as nn
from datasets import load_from_disk
from torchvision import transforms

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


class ConvStem(nn.Module):
    """Self-contained copy of climb_bench.batch2._variants.ConvStem (exp6).

    Stride-16 conv patch-embed matching ViT-S token geometry. Returns NHWC
    because the backbone is built with dynamic_img_size=True (timm flattens).
    Replicated here so the eval rebuilds the exp6 architecture without importing
    stable_pretraining.
    """

    def __init__(self, img_size: int = 224, in_chans: int = 3, embed_dim: int = 384):
        super().__init__()
        self.img_size = (img_size, img_size)
        self.patch_size = (16, 16)
        self.grid_size = (img_size // 16, img_size // 16)
        self.num_patches = self.grid_size[0] * self.grid_size[1]
        self.flatten = False
        self.proj = nn.Sequential(
            nn.Conv2d(in_chans, embed_dim // 4, 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(embed_dim // 4),
            nn.GELU(),
            nn.Conv2d(embed_dim // 4, embed_dim // 2, 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(embed_dim // 2),
            nn.GELU(),
            nn.Conv2d(embed_dim // 2, embed_dim, 3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(embed_dim),
            nn.GELU(),
            nn.Conv2d(embed_dim, embed_dim, 3, stride=2, padding=1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.proj(x)
        return x.permute(0, 2, 3, 1)


def _load_state_dict(ckpt_path: str) -> dict:
    """Load either a plain backbone .pt (pure tensors) or a full Lightning ckpt.

    Tries weights_only=True first (works for the extracted backbone .pt and needs
    NO stable_pretraining on path — ideal for Kaggle); falls back to the full
    unpickle for raw Lightning checkpoints.
    """
    try:
        ck = torch.load(ckpt_path, map_location="cpu", weights_only=True)
    except Exception:
        ck = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    return ck.get("state_dict", ck) if isinstance(ck, dict) and "state_dict" in ck else ck


def build_backbone(ckpt_path: str, backbone: str, device: str,
                   qk_norm: bool = False, conv_stem: bool = False) -> nn.Module:
    sd = _load_state_dict(ckpt_path)
    bsd = None
    for prefix in ("model.backbone.", "backbone.", ""):
        cand = {k[len(prefix):]: v for k, v in sd.items() if k.startswith(prefix)}
        if any(kk.startswith(("blocks.", "cls_token", "pos_embed", "patch_embed")) for kk in cand):
            bsd = cand
            break
    if not bsd:
        raise ValueError(f"no recognizable backbone keys in {ckpt_path}")
    kwargs = {"num_classes": 0, "dynamic_img_size": True}
    if qk_norm:  # exp2: timm builds the q/k LayerNorms only when asked
        kwargs["qk_norm"] = True
    model = timm.create_model(backbone, **kwargs)
    if conv_stem:  # exp6: swap the patch embed for the trained conv stem
        embed_dim = int(getattr(model, "embed_dim", 384))
        model.patch_embed = ConvStem(embed_dim=embed_dim)
    missing, unexpected = model.load_state_dict(bsd, strict=False)
    if missing or unexpected:
        print(f"  [warn] backbone load missing={len(missing)} unexpected={len(unexpected)}")
    model.eval().to(device)
    for p in model.parameters():
        p.requires_grad_(False)
    return model


def eval_transform() -> transforms.Compose:
    return transforms.Compose([
        transforms.Lambda(lambda im: im.convert("RGB")),
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])


@torch.no_grad()
def extract_features(model, split_path, tfm, device, batch_size, feat_dim_blocks=2, max_n=0, seed=0):
    """Return (features [N, 384*feat_dim_blocks], labels [N]) using last-2 CLS concat.

    ``max_n>0`` selects a deterministic random subset (same indices across all
    checkpoints, since the seed is fixed) so CPU-only runs stay tractable.
    """
    ds = load_from_disk(split_path)
    indices = list(range(len(ds)))
    if max_n and max_n < len(ds):
        g = torch.Generator().manual_seed(seed)
        indices = torch.randperm(len(ds), generator=g)[:max_n].tolist()

    def collate(idxs):
        imgs = torch.stack([tfm(ds[int(i)]["image"]) for i in idxs])
        labels = torch.tensor([int(ds[int(i)]["label"]) for i in idxs])
        return imgs, labels

    loader = torch.utils.data.DataLoader(
        indices, batch_size=batch_size, num_workers=8, collate_fn=collate
    )
    feats, labs = [], []
    for imgs, labels in loader:
        imgs = imgs.to(device, non_blocking=True)
        outs = model.get_intermediate_layers(
            imgs, n=feat_dim_blocks, return_prefix_tokens=True, norm=True
        )
        cls = torch.cat([o[1][:, 0] for o in outs], dim=1)  # [B, 384*n]
        feats.append(cls.float().cpu())
        labs.append(labels)
    return torch.cat(feats), torch.cat(labs)


def train_probe(tr_x, tr_y, va_x, va_y, device, epochs, lr, wd, bs=1024):
    dim = tr_x.shape[1]
    probe = nn.Sequential(nn.LayerNorm(dim), nn.Linear(dim, 10)).to(device)
    opt = torch.optim.AdamW(probe.parameters(), lr=lr, weight_decay=wd)
    warmup = max(1, epochs // 10)
    sched = torch.optim.lr_scheduler.SequentialLR(
        opt,
        [torch.optim.lr_scheduler.LinearLR(opt, 0.01, 1.0, warmup),
         torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs - warmup)],
        [warmup],
    )
    tr_x, tr_y = tr_x.to(device), tr_y.to(device)
    va_x, va_y = va_x.to(device), va_y.to(device)
    crit = nn.CrossEntropyLoss()
    n = tr_x.shape[0]
    best = {"top1": 0.0, "top5": 0.0, "epoch": -1}
    for ep in range(epochs):
        probe.train()
        perm = torch.randperm(n, device=device)
        for i in range(0, n, bs):
            idx = perm[i:i + bs]
            opt.zero_grad()
            loss = crit(probe(tr_x[idx]), tr_y[idx])
            loss.backward()
            opt.step()
        sched.step()
        probe.eval()
        with torch.no_grad():
            logits = probe(va_x)
            top1 = (logits.argmax(1) == va_y).float().mean().item()
            top5 = (logits.topk(5, 1).indices == va_y[:, None]).any(1).float().mean().item()
        if top1 > best["top1"]:
            best = {"top1": top1, "top5": top5, "epoch": ep}
    return best


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True)
    p.add_argument("--data_local_path", default="data/imagenet10")
    p.add_argument("--backbone", default="vit_small_patch16_224")
    p.add_argument("--qk_norm", action="store_true", help="exp2: build backbone with timm qk_norm=True")
    p.add_argument("--conv_stem", action="store_true", help="exp6: replace patch_embed with the conv stem")
    p.add_argument("--tag", required=True)
    p.add_argument("--probe_epochs", type=int, default=100)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight_decay", type=float, default=1e-6)
    p.add_argument("--batch_size", type=int, default=128)
    p.add_argument("--max_train", type=int, default=0, help="0=all; else deterministic subset")
    p.add_argument("--max_val", type=int, default=0, help="0=all; else deterministic subset")
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    p.add_argument("--out", default=None)
    args = p.parse_args()
    torch.set_num_threads(8)

    print(f"[{args.tag}] loading backbone from {args.ckpt} on {args.device}")
    model = build_backbone(args.ckpt, args.backbone, args.device,
                           qk_norm=args.qk_norm, conv_stem=args.conv_stem)
    tfm = eval_transform()
    dp = Path(args.data_local_path)
    print(f"[{args.tag}] extracting frozen features (concat CLS last-2)...")
    tr_x, tr_y = extract_features(model, str(dp / "train"), tfm, args.device, args.batch_size, max_n=args.max_train)
    va_x, va_y = extract_features(model, str(dp / "validation"), tfm, args.device, args.batch_size, max_n=args.max_val)
    print(f"[{args.tag}] train {tuple(tr_x.shape)} val {tuple(va_x.shape)} | probing {args.probe_epochs} ep")
    best = train_probe(tr_x, tr_y, va_x, va_y, args.device, args.probe_epochs, args.lr, args.weight_decay)

    result = {
        "tag": args.tag, "ckpt": args.ckpt, "backbone": args.backbone,
        "feature": "concat_cls_last2_layernorm", "probe": "AdamW lr1e-3 wd1e-6 cosine",
        "probe_epochs": args.probe_epochs, "n_train": int(tr_x.shape[0]), "n_val": int(va_x.shape[0]),
        "top1": round(best["top1"], 4), "top5": round(best["top5"], 4), "best_probe_epoch": best["epoch"],
    }
    print(f"[{args.tag}] PAPER-SPEC frozen linear-probe top1={result['top1']} top5={result['top5']}")
    out = Path(args.out) if args.out else Path(__file__).parent / "eval_results" / f"{args.tag}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(f"[{args.tag}] saved {out}")


if __name__ == "__main__":
    main()
