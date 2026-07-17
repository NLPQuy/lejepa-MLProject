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
# # LeJEPA Batch-7 Experiments — Kaggle Offline Runner
#
# T3 cross-domain objectives: score matching, game theory, flow matching, neural
# collapse, RL. Commands are inert by default; delete one leading `# ` to run.
#
# **Phase 0 already settled four questions on CPU (0 GPU-h)** — see
# `climb_bench/tracker/batch7-analysis.md`:
#
# | exp | verdict |
# |---|---|
# | exp1 KL score | SHIPS (rewritten; the original `HyvarienSIGReg` drives the encoder the WRONG way) |
# | exp2 adversarial | SHIPS but ~50–100x slower — the M=1-random control arm is mandatory |
# | exp3 FM-SIGReg | SHIPS as form **b** on the OT path, band [0.3,0.7]. Form **a** (the as-written spec) FAILS |
# | exp6 rotation projector | DEAD — dropped, no exp file |
#
# No extra wheels needed: every mechanism is pure-torch.

# %% Setup paths and offline mode
import os, sys

SOURCE = "/kaggle/input/datasets/phamphuhoa/lejepa7/lejepa-MLProject"
DATA = f"{SOURCE}/data/imagenet10"
CKPT = "/kaggle/working/checkpoints"
BATCH = f"{SOURCE}/climb_bench/batch7"
WHEELS = f"{SOURCE}/wheels"

os.makedirs(CKPT, exist_ok=True)
os.environ["SPT_LIGHT_IMPORT"] = "0"
os.environ["PYTHONPATH"] = f"{SOURCE}/stable-pretraining:{BATCH}:" + os.environ.get("PYTHONPATH", "")
sys.path.insert(0, f"{SOURCE}/stable-pretraining")
sys.path.insert(0, BATCH)

try:
    import requests_cache
except ImportError:
    import types, requests
    _m = types.ModuleType("requests_cache")
    class _CachedSession(requests.Session):
        def __init__(self, *a, **kw): super().__init__()
    _m.CachedSession = _CachedSession
    sys.modules["requests_cache"] = _m

print(f"SOURCE : {SOURCE}")
print(f"DATA   : {DATA}")
print(f"BATCH  : {BATCH}")
print(f"CKPT   : {CKPT}")

# %% Install wheels
# # !pip install {WHEELS}/*.whl --no-deps -q && echo "Wheels installed OK"

# %% GPU check
import torch
print(f"PyTorch : {torch.__version__}  |  CUDA: {torch.cuda.is_available()}")
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    print(f"  GPU {i}: {p.name}  {p.total_memory // 2**20} MB")

# %% [markdown]
# ---
# ## Phase 0 — statistic sanity harness (CPU, ~30 s)
#
# Re-runs the gates that chose exp1's and exp3's forms. Cheap; run it if anything in
# `_variants.py` changed. `scipy` presence matters here: exp3's Hungarian coupling
# falls back to identity on ImportError, which silently disables upgrade (C).

# %% Phase 0 harness
# # !python {BATCH}/test_statistics.py --n 256 --steps 1500 --eval_every 500

# %% [markdown]
# ---
# ## CPU smoke tests
#
# Every exp must reduce to baseline when its knob is off, and pass 3 steps.

# %% Smoke exp1 CPU
# # !python {BATCH}/exp1.py --accelerator cpu --num_gpus 1 --precision 32 \
# #     --max_steps 3 --batch_size 4 --num_workers 0 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/smoke-exp1 --no_wandb

# %% Smoke exp5 off-switch parity CPU
# # !python {BATCH}/exp5.py --accelerator cpu --num_gpus 1 --precision 32 \
# #     --max_steps 3 --batch_size 4 --num_workers 0 --etf_w 0.0 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/smoke-exp5-off --no_wandb

# %% Smoke exp7 CPU
# # !python {BATCH}/exp7.py --accelerator cpu --num_gpus 1 --precision 32 \
# #     --max_steps 3 --batch_size 4 --num_workers 0 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/smoke-exp7 --no_wandb

# %% [markdown]
# ---
# ## Baseline

# %% Baseline ViT-S 400 ep
# # !python {BATCH}/exp_baseline.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp_baseline-vits --no_wandb

# %% [markdown]
# ## Idea 2 — KL score-matching SIGReg (exp1)
#
# The batch's best-motivated mechanism once corrected: a real KL(P_z || N(0,I))
# divergence rather than a goodness-of-fit statistic. Phase 0: ep 51 -> 0.48.
#
# Do NOT set `--aux_lr_mult < 1` — the score net must not be slower than the encoder,
# or the encoder briefly inflates ||z|| before the score net catches up (measured:
# peak std 1.378 and worse final ep at 0.1x).

# %% exp1 KL-score ViT-S 400 ep
# # !python {BATCH}/exp1.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp1-klscore-vits --no_wandb

# %% [markdown]
# ## Idea 3 — adversarial max-sliced SIGReg (exp2)
#
# Phase 0 flagged that idea 3's headline claim ("M=1 suffices / 1000x cheaper") is
# unsupported: per-step cost falls but step count rises ~50-100x. The M=1-RANDOM
# control below is what makes the comparison meaningful — run all three.

# %% exp2 adversarial (M=1 adversarial) ViT-S 400 ep
# # !python {BATCH}/exp2.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp2-adversarial-vits --no_wandb

# %% exp2 CONTROL: M=1 random slice (mandatory arm)
# # !python {BATCH}/exp_baseline.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --n_slices 1 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp2-ctrl-m1random-vits --no_wandb

# %% [markdown]
# ## Idea 7 — FM-SIGReg (exp3)
#
# Ships form **b** (two-player) on the OT path with the KL surrogate averaged over
# t in [0.3, 0.7]. The t-band IS the mechanism — Phase 0: [0.1,0.3] diverges (1/t
# noise amplification), [0.5,0.9] collapses (p_t -> N(0,I), no signal), [0.3,0.7]
# converges to ep 0.59.

# %% exp3 FM-SIGReg form-b OT ViT-S 400 ep
# # !python {BATCH}/exp3.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --fm_form b --fm_path ot \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp3-fmb-ot-vits --no_wandb

# %% exp3 FALSIFICATION ARM: form-a = the as-written spec (fails Phase 0)
# # !python {BATCH}/exp3.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --fm_form a \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp3-fma-ot-vits --no_wandb

# %% [markdown]
# ## Idea 1 — flow-matching invariance (exp4)
#
# Replaces the per-pair MSE alignment; SIGReg untouched. Alignment-axis A/B against
# the b6 Sinkhorn arm (batch-7.md cross-idea consistency) — do not stack them.

# %% exp4 FM-invariance ViT-S 400 ep
# # !python {BATCH}/exp4.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp4-fminv-vits --no_wandb

# %% [markdown]
# ## Idea 5 — simplex-ETF prototypes (exp5)
#
# Prototypes are the exact closed-form ETF and FROZEN, so there is no L_ETF term and
# no alpha weight — one knob, `--etf_w`. Prior-art gate cleared: SIGReg constrains
# the marginal law, ETF constrains class-conditional means; independent.
#
# Falsification is the 3-arm below. Watch `fit/etf_usage_entropy` — it should stay
# near log(K)=2.996 for K=20; a drop means the assignment collapsed onto few prototypes.

# %% exp5 ETF prototypes ViT-S 400 ep
# # !python {BATCH}/exp5.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --etf_w 0.1 --etf_k 20 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp5-etf-vits --no_wandb

# %% exp5 ARM: L_NC only (lamb=0 isolates the ETF contribution)
# # !python {BATCH}/exp5.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --etf_w 0.1 --etf_k 20 --lamb 0.0 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp5-etfonly-vits --no_wandb

# %% [markdown]
# ## Idea 4 — RL crop policy (exp7)
#
# Heaviest and most fragile. TWO GUARDS ARE MANDATORY before committing 400 epochs —
# check them on a short run first:
#   * `fit/rl_entropy` must DECREASE from its init (~4.26). Flat => not learning, reject.
#   * `fit/rl_reward` must stay positive and rise. ~0 => reward too noisy, reject.
#
# `--rl_reward hard` follows the idea's rationale and arXiv:2310.03940; the spec's
# literal formula is `easy` and contradicts its own rationale. Both arms below.

# %% exp7 RL policy — SHORT run first, to read the guards
# # !python {BATCH}/exp7.py --backbone vit_small_patch16_224 --max_epochs 20 \
# #     --batch_size 128 --num_workers 4 --rl_reward hard \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp7-guardcheck --no_wandb

# %% exp7 RL policy (hard views) ViT-S 400 ep
# # !python {BATCH}/exp7.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --rl_reward hard --rl_warmup_steps 2000 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp7-rl-hard-vits --no_wandb

# %% exp7 RL policy (easy views = the spec's literal formula) ViT-S 400 ep
# # !python {BATCH}/exp7.py --backbone vit_small_patch16_224 --max_epochs 400 \
# #     --batch_size 128 --num_workers 4 --rl_reward easy --rl_warmup_steps 2000 \
# #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp7-rl-easy-vits --no_wandb

# %% [markdown]
# ---
# ## Zip results
#
# NB the online probe is NOT the paper recipe (single CLS, no LN, lr 0.03). Use it to
# KILL losers only; re-run `viz/eval-frozen-paperspec.py` on survivors before quoting
# any number as paper-comparable.

# %% Zip checkpoints
# # !cd /kaggle/working && zip -qr batch7-results.zip checkpoints -x "*.ckpt" && echo "zipped"
