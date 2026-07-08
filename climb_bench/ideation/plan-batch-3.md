# Implementation Plan — Batch 3 (Imagenette / LeJEPA anti-overfit objective + data signal)

**Source ideas**: [batch-3.md](batch-3.md) (10 ideas, all `enhance-existing`, OBJECTIVE / PROJECTOR / DATA-SIGNAL only — encoder identity preserved)
**Target**: jupytext experiment files `exp<x>.py` under `climb_bench/batch3/`, uploaded to Kaggle, run **offline** (torchvision 0.26 pinned wheels).
**Hard rule (same as batch-1/2)**: variant/mechanism logic goes in a **batch-local** `climb_bench/batch3/_variants.py`; the official `stable_pretraining/methods/lejepa_variants.py` is **NOT** touched. Runners only import + wire. `_common.py` is reused/extended from batch-1/2.

> **Do not implement yet — await user approval of this plan.**

---

## 0. Key difference from batch-2: back to model/loss/data surfaces (no optimizer changes)

Batch-2 wired mostly at the **optimizer/trainer** (SAM, Muon, Schedule-Free, PCGrad, SWA, LLRD, stochastic-depth). Batch-3 returns to the **three batch-1 swap surfaces** plus a data-pipeline surface — every idea targets the *measured overfit* (probe peaks ~ep80–150 then decays −2.4pp), none touch the optimizer or the frozen `vit_small_patch16_224` body:

- **`subclass`** (override `_compute_loss`) — i-Mix, Input-Jacobian, MMCR, Whitening, R-Drop (double projector forward).
- **`sigreg-swap`** (`model.sigreg = …`) — Robust/Huberized Epps–Pulley.
- **`ctor-inject`** (`LeJEPA(projector=…)`) — Narrow projector bottleneck (+ the dropout projector that R-Drop needs).
- **`callback`** (`pl.Callback` in `_common.py` stack) — Gen-gap λ controller.
- **`data/transform`** (epoch-indexed transform schedule in `_common.py`) — Crop/aug curriculum, ContrastiveCrop sampler.

So `_common.py` gains, on top of the batch-1/2 contract:
- an **epoch-indexed transform schedule** hook (transform builder reads `current_epoch`) for the curriculum (exp6) and ContrastiveCrop sampler (exp10),
- a **callback registry** entry for `GenGapLambdaController` (exp4),
- a `--projector {mlp,narrow,dropout}` switch feeding `LeJEPA(projector=…)` (exp3, exp2),
- a `--manual_loss`-free path: all loss-side variants stay in **automatic optimization** (no manual-opt needed this batch) **except** exp7 (Jacobian) which needs `create_graph=True` inside an otherwise-normal `training_step`.

Everything keeps an **off-switch == exact baseline** (weight-0 / α=0 / δ→∞ / identity-schedule reproduces stock LeJEPA), verified by identical 1-epoch loss, per the batch-1/2 convention.

---

## 1. Per-idea implementation map

Legend — **Surface**: `subclass` | `sigreg-swap` | `ctor-inject` | `callback` | `data/transform`.
All "new code" lands in `climb_bench/batch3/_variants.py` (mechanism) or `_common.py` (wiring), never in official source.

| exp | Idea (batch-3 #) | Surface | New thing in `batch3/_variants.py` (or `_common.py`) | Runner does |
|-----|------------------|---------|------------------------------------------------------|-------------|
| exp1 | #1 i-Mix embedding mixup | subclass | `LeJEPAiMix(LeJEPA)` — Beta(α,α) mix of projections + interpolated-center invariance; SIGReg on clean | instantiate subclass, `--mix_alpha 1.0 --mix_w 0.5` |
| exp3 | #3 Narrow projector bottleneck | ctor-inject | `build_narrow_projector(in_dim,out_dim,hidden)` (+ optional low-rank linear) in `_common.py` | `LeJEPA(projector=…)`, `--proj_dim 8 --proj_bottleneck 0` |
| exp5 | #5 Robust/Huberized Epps–Pulley | sigreg-swap | `HuberSlicedEppsPulley(nn.Module)` — Huber(δ)/top-k-trim integrand, copy of `SlicedEppsPulley` | `model.sigreg = HuberSlicedEppsPulley(…)`, `--huber_delta 1.0` |
| exp2 | #2 R-Drop dual-mask consistency | ctor-inject + subclass | `DropoutMLP` projector + `LeJEPARDrop(LeJEPA)` (2 projector forwards, `rdrop_w·MSE`) | instantiate subclass w/ dropout projector, `--rdrop_w 1.0 --proj_dropout 0.1` |
| exp6 | #6 Crop/aug curriculum | data/transform | epoch→aug-params schedule in `_common.py` transform builder | `--aug_curriculum linear --aug_ramp_frac 0.5` |
| exp4 | #4 Gen-gap λ / early-freeze controller | callback | `GenGapLambdaController(pl.Callback)` — watch kNN/coding-rate vs train-loss, ramp `model.lamb` | add callback, `--gap_control [--gap_lambda_mult 2.0]` |
| exp9 | #9 Whitening invariance (W-MSE) | subclass | `LeJEPAWhitenInv(LeJEPA)` — batch-sliced Cholesky whitening before invariance MSE | instantiate subclass, `--whiten_subset 0` (0=off) |
| exp8 | #8 MMCR nuclear-norm aux | subclass | `LeJEPAMMCR(LeJEPA)` — `−mmcr_w·‖C‖_*` of per-image centroids (fp32 SVD) | instantiate subclass, `--mmcr_w 0.0` |
| exp7 | #7 Input-Jacobian penalty | subclass | `LeJEPAJacobian(LeJEPA)` — 1-probe Hutchinson `‖∂(v·z)/∂x‖²`, `create_graph=True` | instantiate subclass, `--jac_w 0.0` |
| exp10 | #10 ContrastiveCrop semantic crop | data/transform + callback | `ContrastiveCropSampler` + periodic encoder-heatmap/box pass | swap crop sampler, `--ccrop [--ccrop_warmup_ep 50]` |

**Notes / risks baked into the plan**
- **exp1 i-Mix** — the one correctness trap: mix the **projections** for the *invariance* target only; **keep SIGReg on the clean projections** (mixtures of Gaussians ≠ Gaussian, so pushing mixtures to N(0,I) fights the test). Off-switch `mix_w=0` (or `mix_alpha=0`) ⇒ bit-for-bit baseline.
- **exp3 narrow projector** — pure `ctor-inject`, no subclass. Sweep `proj_dim∈{8,16,32,64}` + a low-rank-bottleneck variant; the *current* width must reproduce 0.8949. Cheapest probe of the overfit lever → build/smoke first.
- **exp5 robust EP** — copy the **batch-3-local** `SlicedEppsPulley` (the self-contained one in `stable_pretraining.methods.lejepa`, NOT the `lejepa/` package class — see CLAUDE.md "dual EppsPulley"); wrap the squared ECF deviation in Huber(δ) before the trapezoid sum. **Verify δ→∞ ⇒ identical statistic AND gradient** as baseline. Two sub-variants (Huber vs top-k slice-trim) behind one flag. Watch RankMe for under-regularization/collapse.
- **exp2 R-Drop** — needs a **dropout-enabled projector** (`DropoutMLP`, p≈0.1) injected via ctor; the subclass runs the projector **twice** under independent masks and adds `rdrop_w·MSE(z¹,z²)`. ⚠️ devil's-advocate warning from the batch: ViT-S SSL usually runs dropout=0, so with `proj_dropout=0` the term is identically 0 — the idea **only exists** if dropout is deliberately enabled. Off-switch = `rdrop_w=0` OR `proj_dropout=0` ⇒ baseline.
- **exp6 curriculum** — epoch-indexed schedule of local-crop `scale_min` and color/blur strength (mild→aggressive over first `aug_ramp_frac` of training). Constant schedule == paper aug ⇒ baseline. Confound with LR warmup — isolate by keeping warmup fixed. Needs the transform builder to know `current_epoch` (pass via callback-set attribute or DataModule hook).
- **exp4 controller** — ⚠️ must beat **passive best-ckpt selection** (already a free +2.4pp), not just last-epoch. The callback reads the existing `OnlineKNN`/`RankMe` logged metrics + train-loss slope; at the divergence point it ramps `module.model.lamb` (and/or starts weight averaging). Keep the control law a 1-line rule. Falsification = controller-on vs passive best-ckpt.
- **exp9 whitening** — batch-sliced Cholesky whitening of projections, then invariance MSE in whitened space; **views of the same image must not share a whitening subset**. Identity whitening ⇒ baseline invariance. ⚠️ potential redundancy/conflict with SIGReg (both touch covariance) — evaluate independently before combining; small-batch whitening is unstable (enough samples per subset).
- **exp8 MMCR** — `−mmcr_w·nuclear_norm(C)` of the per-image view-centroid matrix, **fp32 SVD**. ⚠️ HIGH risk (flagged in batch): spectral term can over-regularize/collapse exactly as batch-1 coding-rate did — **start tiny + warmup + RankMe guard**. `mmcr_w=0` ⇒ baseline.
- **exp7 Jacobian** — 1-probe Hutchinson estimate `‖∂(v·z)/∂x‖²` needs `create_graph=True` (double-backward) inside `training_step`. ⚠️ bf16 second-order instability — **may need an fp32 probe**; bounds per-step cost at ~+1 backward. `jac_w=0` ⇒ baseline.
- **exp10 ContrastiveCrop** — heaviest (L-effort). Periodic (every few ep) coarse object heatmap from encoder CLS-attention → box → center-suppressed crop sampling. ⚠️ heatmap from an early/random encoder is unreliable → **warmup with plain RandomResizedCrop first** (`ccrop_warmup_ep`). Off-switch reverts to RandomResizedCrop ⇒ baseline. Multi-crop (global/local) integration is fiddly — gate behind `/idea-vetting`.

---

## 2. Shared runner contract (`_common.py` additions)

Reuse the batch-1/2 `_common.py` (transforms, dataset, `lejepa_forward`, OnlineProbe+OnlineKNN+RankMe, `run()`). Add:
- `build_narrow_projector(...)` / a `--projector {mlp,narrow,dropout}` dispatch feeding `LeJEPA(projector=…)` (exp3, exp2).
- An **epoch-aware transform builder**: the global/local transforms read a `current_epoch` set each epoch (curriculum exp6, ContrastiveCrop exp10). Default schedule = constant = paper aug ⇒ baseline.
- Callback-registry flags appended to the existing OnlineProbe/OnlineKNN/RankMe stack: `GenGapLambdaController` (`--gap_control`), ContrastiveCrop heatmap refresher (`--ccrop`).
- A shared `get_args()` superset adding per-exp knobs (`--mix_alpha`, `--mix_w`, `--rdrop_w`, `--proj_dropout`, `--huber_delta`, `--whiten_subset`, `--mmcr_w`, `--jac_w`, `--aug_curriculum`, `--gap_control`, `--ccrop`, …), all defaulting to the **baseline/off value**.

All loss-side variants stay in **automatic optimization** — no manual-opt branch this batch. exp7's `create_graph=True` lives inside the normal `training_step` (subclass-local), so the shared module is untouched.

Each `exp<x>.py` stays ~30 lines: `get_args()` (+ exp knob) → build model (stock `LeJEPA` for exp5/sigreg-swap and exp3/ctor-inject; subclass for exp1/2/7/8/9) → optional `model.sigreg = …` → `run(model, args, tag)`.

```python
# exp1.py (i-Mix) example
from _common import get_args, run
from _variants import LeJEPAiMix
def main():
    args = get_args()
    model = LeJEPAiMix(encoder_name=args.backbone, lamb=args.lamb,
                       n_slices=args.n_slices, projector_dim=args.proj_dim,
                       mix_alpha=args.mix_alpha, mix_w=args.mix_w)
    run(model, args, tag="exp1-imix")
if __name__ == "__main__": main()
```

```python
# exp5.py (robust Epps–Pulley) example — sigreg-swap, stock LeJEPA
from _common import get_args, run
from stable_pretraining.methods.lejepa import LeJEPA
from _variants import HuberSlicedEppsPulley
def main():
    args = get_args()
    model = LeJEPA(encoder_name=args.backbone, lamb=args.lamb,
                   n_slices=args.n_slices, projector_dim=args.proj_dim)
    model.sigreg = HuberSlicedEppsPulley(num_slices=args.n_slices,
                                         n_points=17, huber_delta=args.huber_delta)
    run(model, args, tag="exp5-huber-ep")
if __name__ == "__main__": main()
```

---

## 3. Evaluation consistency (frozen ViT-S linear probe)

- **Primary ranking metric across all exps = the online callbacks already in `run()`** (`linear_probe/top1`, `knn_probe/top1`, `rankme`), **identical config for every exp** → apples-to-apples. Do **not** vary probe settings between exps. The loss/projector/data changes must not touch probe settings.
- ⚠️ **The online `OnlineProbe` is NOT the paper recipe** (single CLS, no LN, lr 0.03). Use it only to KILL losers; **re-run `eval-frozen-paperspec.py` on survivors** (concat CLS last-2 + LN + AdamW lr1e-3 wd1e-6). Batch-2 proved online ranking does **not** survive the paper recipe — require ≥~0.02 margin before trusting a pre-eval result.
- **Report every number best-ckpt, not last** — the baseline demonstrably overfits (−2.4pp post-peak). Checkpoint every `max_epochs//2`; the controller (exp4) must beat **passive best-ckpt** to count.
- 400-epoch pretrain; resume across Kaggle ≤12 h sessions.

---

## 4. Kaggle offline runbook (`run-batch3.py`)

Clone `climb_bench/batch2/run-batch2.py` (itself derived from `batch1/run-batch1.py` → `lejepa-nointernet-setup.py`). Per [[kaggle-jupytext-convention]]:
- **Double-`#`** every `!python …`/`!pip …` block (`# # !python …`) so "Run All" stays inert; user deletes one `# ` per session.
- No `[...]` in `# %%` cell titles.
- Set `PYTHONPATH` to both `stable-pretraining` and `climb_bench/batch3`; `SPT_LIGHT_IMPORT=0`; stub `requests_cache`.
- **No extra wheels needed** this batch (no Muon/Schedule-Free) — all mechanisms are pure-torch. Reuse the batch-2 `--no-deps` wheel cell as-is.
- One run-block per exp pointing at `climb_bench/batch3/exp<x>.py`, `--no_wandb` (CSV) offline.

---

## 5. Build & verification order (goal-driven)

1. **Extend `_common.py`** (`--projector` dispatch, epoch-aware transform hook, callback flags) → smoke: `exp_baseline.py` (stock LeJEPA, all knobs off) reproduces the batch-1/2 baseline on 1 epoch. *Verify*: probe metric logged, loss matches.
2. **Cheap, low-risk first (S-effort, target the measured overfit directly)**: exp3 (narrow projector — ctor-inject, no new loss path), exp5 (robust EP — δ→∞ parity), exp1 (i-Mix — `mix_w=0` parity). *Verify*: 1-epoch / `max_steps=3` smoke, off-switch == baseline loss.
3. **Data-side & control**: exp6 (curriculum — constant schedule == baseline), exp4 (gen-gap controller — fires the trigger once, beats passive best-ckpt in a short run). *Verify*: transform schedule toggles, callback mutates `model.lamb` without NaN.
4. **Subclass loss terms**: exp2 (R-Drop — dropout projector double-forward), exp9 (whitening — identity-whitening parity). *Verify*: forward/backward, off-switch parity, RankMe logged.
5. **Heavier / risk-flagged** (gate behind `/idea-vetting` before full 400-ep runs): exp8 (MMCR — tiny `mmcr_w` + warmup + fp32 SVD + RankMe guard), exp7 (Jacobian — fp32 probe, double-backward cost), exp10 (ContrastiveCrop — encoder-heatmap warmup, multi-crop integration).
6. Local smoke only at **model/loss level** (torchvision 0.26 mismatch blocks the full data pipeline locally — see [[kaggle-jupytext-convention]]); full runs on Kaggle. exp6/exp10 (data-side) can only be fully validated on Kaggle — smoke them with a stubbed transform locally.

**Success criterion**: every `exp<x>.py` (a) imports its mechanism from `batch3/_variants.py` or wires it via `_common.py`, (b) passes a 1-epoch / `max_steps=3` smoke, (c) reduces to baseline when its flag/weight is off, (d) runs unchanged under `run-batch3.py` offline, (e) for exp1/exp5/exp9, off-switch parity is verified bit-for-bit; for exp8/exp7, RankMe/collapse guards are in place.

---

## 6. Open decisions for you (resolve before coding)

1. **Build scope first**: all 10, or the 3 cheap high-fit drop-ins (exp3 narrow projector, exp5 robust EP, exp1 i-Mix) + baseline first? (Recommend the 3 + baseline — all S/M, all directly attack the measured overfit, per batch-3 "Next steps #1".)
2. **exp4 controller honest baseline**: lock in **passive best-ckpt selection** (+2.4pp free) as the number the active controller must beat — agreed as the gate, or run controller blind first?
3. **exp2 R-Drop**: include it at all? It only does anything if projector dropout is deliberately enabled (batch flagged ViT-S SSL usually runs dropout=0). Build it but mark hold-for-later?
4. **exp8 / exp9 covariance overlap**: both add covariance-level structure on top of SIGReg's marginal Gaussianity — keep both single-variable for now, or drop one to avoid redundant compute?
5. **exp10 ContrastiveCrop**: full multi-crop heatmap integration now, or phase it (v0 = stronger fixed crop, no new module; v1 = learned heatmap sampler) like batch-1's AutoView?
6. **Compose later?**: i-Mix (exp1) + narrow projector (exp3) are orthogonal anti-overfit levers — keep all exps single-variable for ranking, or pre-plan one "stack the winners" run afterwards?
