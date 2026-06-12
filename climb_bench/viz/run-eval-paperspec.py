# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Paper-spec frozen linear-probe eval — Kaggle GPU runner (ALL BATCHES)

# Unified runner: set `BATCH` and run. Calls `eval-frozen-paperspec.py` on each
# checkpoint over the FULL dataset, paper recipe (concat CLS last-2 + LN, AdamW
# lr1e-3 wd1e-6). Loads the full Lightning `.ckpt` DIRECTLY (weights_only=True works,
# no `stable_pretraining` needed) — so there is NO separate extract-backbone step.

# **Self-locating + pre-flight checked:**
#   * eval script taken from NEXT TO this runner (single source of truth);
#   * checkpoints found by globbing the `lejepa-ckpts` dataset by exp folder name;
#   * imagenet10 found by globbing `/kaggle/input`;
#   * verifies the eval script supports `--qk_norm` / `--conv_stem` before running.

# **Arch flags (must match training):** exp2 QK-Norm → `--qk_norm`; exp6 conv-stem
# → `--conv_stem`; exp7 SWA → eval `swa_avg.ckpt`; everything else = vanilla ViT-S.

# Kaggle inputs: (1) `climb_bench` (runner + eval script), (2) `lejepa-ckpts`
# (extracted ckpt tree), (3) a dataset holding `data/imagenet10`.

# %% Config
BATCH = "batch_2"   # <-- set me: batch_1 | batch_2 | ...

# tag -> (exp folder name, ckpt filename glob, extra eval flags)
PLANS = {
    "batch_1": {
        "baseline_100": ("exp_baseline-vits",    "*epoch=099.ckpt", ""),
        "idea3_100":    ("exp3-codingrate-vits", "*epoch=099.ckpt", ""),
        "idea4_100":    ("exp4-uniformity-vits", "*epoch=099.ckpt", ""),
        "idea7_100":    ("exp7-dyntanh-vits",    "*epoch=099.ckpt", ""),
    },
    "batch_2": {
        "baseline_100":     ("exp_baseline-vits",      "*epoch=099.ckpt", ""),
        "convstem_100":     ("exp6-convstem-vits",     "*epoch=099.ckpt", "--conv_stem"),
        "qknorm_100":       ("exp2-qknorm-vits",       "*epoch=099.ckpt", "--qk_norm"),
        "pcgrad_100":       ("exp5-pcgrad-vits",       "*epoch=099.ckpt", ""),
        "sam_100":          ("exp1-sam-vits",          "*epoch=099.ckpt", ""),
        "swa_100":          ("exp7-swa-vits",          "swa_avg.ckpt",    ""),
        "sdschedule_100":   ("exp9-sdschedule-vits",   "*epoch=099.ckpt", ""),
        "schedulefree_100": ("exp4-schedulefree-vits", "*epoch=099.ckpt", ""),
        "deepsup_100":      ("exp10-deepsup-vits",     "*epoch=099.ckpt", ""),
        "llrd_100":         ("exp8-llrd-vits",         "*epoch=099.ckpt", ""),
        "muon_100":         ("exp3-muon-vits",         "*epoch=099.ckpt", ""),
    },
}
PLAN = PLANS[BATCH]
TAGS = list(PLAN)   # eval all; trim this list to skip some

# %% Setup + auto-locate
import os, glob, subprocess

INPUT = "/kaggle/input"


def find_one(pattern, what):
    hits = sorted(glob.glob(pattern, recursive=True))
    if not hits:
        raise FileNotFoundError(f"could not locate {what}: no match for {pattern}")
    if len(hits) > 1:
        print(f"  [note] {what}: {len(hits)} matches, using {hits[0]}")
    return hits[0]


try:  # eval script: prefer the copy next to THIS runner
    HERE = os.path.dirname(os.path.abspath(__file__))
    SCRIPT = os.path.join(HERE, "eval-frozen-paperspec.py")
    assert os.path.exists(SCRIPT)
except (NameError, AssertionError):
    SCRIPT = find_one(f"{INPUT}/**/climb_bench/viz/eval-frozen-paperspec.py", "eval script")

CKPT_ROOT = find_one(f"{INPUT}/**/lejepa-ckpts", "lejepa-ckpts dataset")
DATA = os.path.dirname(find_one(f"{INPUT}/**/data/imagenet10/validation", "imagenet10 dataset"))
OUT = f"/kaggle/working/eval_results/{BATCH}"
os.makedirs(OUT, exist_ok=True)
print("BATCH    ", BATCH)
print("SCRIPT   ", SCRIPT)
print("CKPT_ROOT", CKPT_ROOT)
print("DATA     ", DATA)
print("OUT      ", OUT)

# %% GPU check
import torch
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"   # CPU works too, just slower
print(f"PyTorch {torch.__version__} | device={DEVICE} | "
      f"{torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU (~15-40min/ckpt)'}")

# %% locate ckpts
CKPT_PATH = {}
for tag in TAGS:
    exp_dir, ckpt_glob, _ = PLAN[tag]
    hits = sorted(glob.glob(f"{CKPT_ROOT}/**/{exp_dir}/{ckpt_glob}", recursive=True))
    if not hits:
        print(f"[MISS] {tag:16s} no match for **/{exp_dir}/{ckpt_glob}"); continue
    CKPT_PATH[tag] = hits[0]
    print(f"{tag:16s} -> {hits[0]}  ({os.path.getsize(hits[0])//2**20} MB)"
          + ("  [+more]" if len(hits) > 1 else ""))

# %% preflight (stale eval script would crash on --qk_norm/--conv_stem)
_src = open(SCRIPT).read()
for tag in list(CKPT_PATH):
    flag = PLAN[tag][2].strip()
    if flag and flag not in _src:
        print(f"[DROP] {tag}: eval script has no '{flag}' -> RE-UPLOAD climb_bench. Skipping.")
        CKPT_PATH.pop(tag)
print("will eval:", [t for t in TAGS if t in CKPT_PATH])

# %% eval-loop
for tag in [t for t in TAGS if t in CKPT_PATH]:
    flags = PLAN[tag][2]
    cmd = ["python", SCRIPT, "--ckpt", CKPT_PATH[tag], "--tag", tag,
           *flags.split(), "--data_local_path", DATA, "--device", DEVICE,
           "--max_train", "0", "--max_val", "0", "--probe_epochs", "100",
           "--batch_size", "256", "--out", f"{OUT}/{tag}.json"]
    print("\n$", " ".join(cmd))
    print(f"[{tag}] returncode={subprocess.run(cmd).returncode}")

# %% visualize + summary
# # !python {os.path.dirname(SCRIPT)}/viz_paperspec.py --results {OUT} --out /kaggle/working

# %% inline summary
import json
rows = [json.load(open(f)) for f in sorted(glob.glob(f"{OUT}/*.json"))]
base = next((r["top1"] for r in rows if "baseline" in r["tag"].lower()), None)
print(f"{'idea':16s} {'top1':>7s} {'top5':>7s} {'Δtop1':>8s}")
for r in sorted(rows, key=lambda r: -r["top1"]):
    d = f"{r['top1']-base:+.4f}" if base and "baseline" not in r["tag"].lower() else "—"
    print(f"{r['tag']:16s} {r['top1']:.4f} {r['top5']:7.4f} {d:>8s}")
