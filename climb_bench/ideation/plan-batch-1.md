# Implementation Plan — Batch 1 (Imagenette / LeJEPA improvements)

**Source ideas**: [batch-1.md](batch-1.md) (10 ideas, all `enhance-existing`)
**Target**: jupytext experiment files `exp<x>.py` under `climb_bench/batch1/`, uploaded to Kaggle, run **offline**.
**Hard rule**: every `exp<x>.py` calls **modules that live in the official source** (`stable_pretraining.*`) — experiment-specific logic goes into `stable_pretraining/methods/lejepa_variants.py` (the existing variant home), never copied ad-hoc into the runner.

---

## 0. How the official repo already does this (the convention we must follow)

```
stable_pretraining/methods/
  lejepa.py            # LeJEPA base (backbone+projector+predictor+SlicedEppsPulley)
  lejepa_variants.py   # SRHTSlicedEppsPulley, HyvarienSIGReg, AdversarialSIGReg,
                       # FMSIGReg, FMInvariance, LeJEPAFMInv(LeJEPA)   ← variant logic
benchmarks/imagenet10/
  lejepa-vit-small.py  # baseline runner (argparse + spt.Manager + callbacks)
  lejepa-srht.py …     # variant runners: import a variant, swap it in, train
climb_bench/
  lejepa-nointernet-setup.py   # Kaggle jupytext orchestrator (!python … per block)
```

Two established swap mechanisms (we reuse exactly these):
- **SIGReg-swap** — `model.sigreg = CustomSIGReg(...)`. The custom module takes projections `[N,K]` → scalar. Used by srht/hyvarinen/adversarial/fm-sigreg.
- **Subclass-swap** — define `class LeJEPAxxx(LeJEPA)` overriding `forward`/`_compute_loss`, instantiate it directly. Used by `LeJEPAFMInv` when the change touches invariance/loss, not just the GoF statistic.
- **Constructor injection (no official-source change)** — `LeJEPA(projector=<custom nn.Module>, predictor=…)`. Usable when the change is fully expressible through existing constructor hooks.

`OnlineProbe` (linear, lr 0.03, wd 1e-6, on `embedding`) + `OnlineKNN` (k=20) + `RankMe` already run inside every runner and are our comparison metrics.

---

## 1. Decision: Option 1 vs Option 2 → **Option 2 (recommended)**

> Each experiment = one **plain `exp<x>.py` runner** (argparse, like the official benchmark scripts) + **one jupytext orchestrator** `run-batch1.py` modeled on `lejepa-nointernet-setup.py`.

**Why Option 2 over Option 1 (each exp = a standalone jupytext notebook):**
1. **Matches the repo** — official runners are plain argparse `.py`; `lejepa-nointernet-setup.py` is already the orchestrator. Lowest surprise, reuses an existing template.
2. **Diff/test friendly** — plain `.py` has no notebook-pairing/JSON-merge issues; reviewable in git; importable in a smoke test.
3. **Kaggle session model still satisfied** — Kaggle runs ~1 notebook/session (≤12 h GPU). In the orchestrator you uncomment **one** `!python exp<x>.py …` block per session; outputs land in `/kaggle/working`. No code lives in the notebook, only invocation.
4. **No duplication blow-up** — shared boilerplate (transforms, datasets, forward, args, callbacks) is factored once into `climb_bench/batch1/_common.py`, so each `exp<x>.py` is ~30–50 lines (import official variant → build/swap → `run(...)`).

**When Option 1 would be better** (note, not chosen): if you want each experiment to be an *independently committable Kaggle notebook* scheduled separately for full isolation. We can convert any `exp<x>.py` to a standalone jupytext notebook later via `jupytext --to notebook` since they are already percent-format friendly — so Option 2 does not lock us out of Option 1.

### Resulting layout
```
climb_bench/batch1/
  _common.py        # shared: transforms, dataset loader, lejepa_forward, build_trainer/run()
  exp1.py … exp10.py# one thin runner per idea (jupytext percent header optional)
  run-batch1.py     # jupytext orchestrator (clone of lejepa-nointernet-setup.py)
  README.md         # what each exp is + how to run on Kaggle offline
```
`_common.py` is the only place that duplicates baseline boilerplate (extracted from `lejepa-vit-small.py`). Optionally promote it to `benchmarks/imagenet10/_lejepa_common.py` in official source later; for now keep it in `batch1/` to avoid touching shared benchmarks.

---

## 2. Per-idea implementation map

Legend — **Mechanism**: `sigreg-swap` | `subclass` | `ctor-inject` | `callback` | `data/transform`.
Each "New official module" goes into `stable_pretraining/methods/lejepa_variants.py` (or noted otherwise) so the exp runner only *imports + wires*.

| exp | Idea (batch-1 #) | Mechanism | New thing in official source | Runner does |
|-----|------------------|-----------|------------------------------|-------------|
| exp1 | #1 Learned/max-sliced slices | sigreg-swap | **reuse `AdversarialSIGReg`** (already max-sliced) ⚠️ | `model.sigreg = AdversarialSIGReg(dim=proj_dim)` |
| exp2 | #2 Cramér-Wold metric | sigreg-swap | `CramerWoldSIGReg(nn.Module)` | `model.sigreg = CramerWoldSIGReg(...)` |
| exp3 | #3 Coding-rate term | subclass | `LeJEPACodingRate(LeJEPA)` (β·logdet in `_compute_loss`) | instantiate subclass |
| exp4 | #4 Uniformity term | subclass | `LeJEPAUniformity(LeJEPA)` (γ·uniformity) | instantiate subclass |
| exp5 | #5 EMA teacher | subclass | `LeJEPAEMATeacher(LeJEPA)` (uses `backbone.TeacherStudentWrapper`) | instantiate subclass |
| exp6 | #6 Dense patch objective | subclass | `LeJEPADensePatch(LeJEPA)` (patch-token SIGReg+inv) | instantiate subclass |
| exp7 | #7 DynTanh projector | ctor-inject | `DynTanhMLP` builder (small) | `LeJEPA(projector=DynTanhMLP(...))` |
| exp8 | #8 NN-positive invariance | subclass | `LeJEPANNCLR(LeJEPA)` (support queue + NN target) | instantiate subclass |
| exp9 | #9 AutoView adversarial views | data/transform + subclass | `AutoViewPolicy(nn.Module)` + view hook | swap transforms; optional joint-opt |
| exp10 | #10 RankMe-gated λ | callback | `RankMeLambdaController(pl.Callback)` mutating `model.lamb` | add callback to trainer |

**Notes / risks baked into the plan:**
- **exp1 is near-duplicate of an existing variant** (`AdversarialSIGReg` = adversarial max-sliced SIGReg). Recommendation: implement exp1 as a *thin reuse* of `AdversarialSIGReg` and treat it as the batch-1 #1 realization (also gives a free comparison to the prior batch's `lejepa-adversarial.py`). If `AdversarialSIGReg` already optimizes worst-case slices, **only** add the "mix random+learned slices" knob (the unbiasedness mitigation from batch-1 #1) — otherwise skip new code.
- **exp9 (AutoView)** is the heaviest. Phase it: v0 = stronger fixed multi-crop (no new module, just `_global/_local_transform` tuning) to get a cheap signal; v1 = learned `AutoViewPolicy`. Mark v1 as L-effort / hold.
- **exp10 (RankMe-λ)** uses the existing `RankMe` callback's rank estimate; the controller reads it from logged metrics and sets `module.model.lamb`. Keep the control law a 1-line proportional rule (avoid new meta-knobs).
- **exp3/exp4** are the cheap wins → build + smoke-test these first.
- All subclasses override the **staticmethod** `LeJEPA._compute_loss` by reimplementing it in the subclass `forward` (same pattern as `LeJEPAFMInv`); keep added terms behind a weight arg defaulting to 0 so the subclass reduces to baseline when off (sanity check).

---

## 3. Shared runner contract (`_common.py`)

Extract verbatim from `lejepa-vit-small.py` (do not re-derive):
- `_backbone_tag`, `_photometric_transforms`, `_global_transform`, `_local_transform`, `_build_datasets`, `lejepa_forward`.
- A single `run(model, args)` that builds `spt.data.DataModule`, `spt.Module`, `pl.Trainer` with the **identical** callback stack (OnlineProbe linear + OnlineKNN + RankMe + ModelCheckpoint + LRMonitor) and `spt.Manager(...)()`.
- A shared `get_args()` superset adding per-exp knobs (`--coding_beta`, `--uniformity_gamma`, `--ema_momentum`, `--nn_queue`, `--dyntanh_alpha`, …), all defaulting to the baseline/off value.

Each `exp<x>.py` then is essentially:
```python
# %% jupytext percent header (optional, lets it open as a notebook too)
from _common import get_args, run
from stable_pretraining.methods.lejepa import LeJEPA
from stable_pretraining.methods.lejepa_variants import LeJEPACodingRate  # exp3 example
def main():
    args = get_args()
    model = LeJEPACodingRate(encoder_name=args.backbone, lamb=args.lamb,
                             n_slices=args.n_slices, n_points=17,
                             projector_dim=args.proj_dim, coding_beta=args.coding_beta)
    run(model, args)
if __name__ == "__main__": main()
```

---

## 4. Evaluation consistency (frozen ViT-S linear probe)

- **Primary comparison metric across all exps = the online callbacks already in the runner** (`linear_probe/top1`, `knn_probe/top1`, `rankme`) — identical config for every exp → apples-to-apples. Do **not** vary probe settings between exps.
- ⚠️ **Spec mismatch to resolve**: batch-1 task specifies the probe = *concat CLS of last 2 layers + LayerNorm, AdamW lr 1e-3 wd 1e-6*, but `OnlineProbe` uses single-`embedding` `nn.Linear`, lr 0.03. Two options (decide once, apply to ALL exps):
  - (A) **Keep OnlineProbe as-is** (consistent, zero new code) and treat it as the ranking metric; run the paper-spec probe only once on the final winner.
  - (B) Add a shared **offline frozen-probe eval** (`eval-frozen.py`) matching the spec, run after each 400-ep checkpoint.
  Default = **(A)**; add (B) only for the final 2–3 candidates.
- Pretrain length: **400 epochs** (research target) vs the scripts' default 100. Confirm Kaggle wall-clock: ViT-S, bs128, ~74 steps/ep × 400 ≈ 30k steps — should fit one ≤12 h GPU session; if not, checkpoint every `max_epochs//2` (already configured) and resume.

---

## 5. Kaggle offline runbook (reuse `lejepa-nointernet-setup.py`)

`run-batch1.py` = copy of the setup cells from `climb_bench/lejepa-nointernet-setup.py`, with the run-command blocks pointing at `climb_bench/batch1/exp<x>.py`:
1. **Cell [1]** — set `SOURCE`, `DATA=$SOURCE/data/imagenet10`, `CKPT=/kaggle/working/checkpoints`, `BATCH=$SOURCE/climb_bench/batch1`; set `PYTHONPATH` to `$SOURCE/stable-pretraining` **and** `$BATCH` (so `from _common import …` resolves); stub `requests_cache`.
2. **Cell [1b]** — `!pip install {WHEELS}/*.whl --no-deps -q` once.
3. **Cell [2]** — GPU check.
4. **Run blocks** — one per exp, e.g.:
   ```
   # !python {BATCH}/exp3.py --backbone vit_small_patch16_224 --max_epochs 400 \
   #     --batch_size 128 --num_workers 4 --coding_beta 0.01 \
   #     --data_local_path {DATA} --checkpoint_dir {CKPT}/exp3-codingrate-vits --no_wandb
   ```
   `--no_wandb` (CSV) for offline; `--wandb_offline` if syncing later. Uncomment ONE block per session.

---

## 6. Build & verification order (goal-driven)

1. **`_common.py`** → smoke test: `python exp_baseline.py --max_epochs 1 --batch_size 8 --num_workers 0` (a baseline exp wrapping plain `LeJEPA`) reproduces `lejepa-vit-small.py` numbers on 1 epoch. *Verify*: runs end-to-end, probe metric logged.
2. **Cheap wins first**: exp3 (coding-rate), exp4 (uniformity), exp7 (DynTanh) — each with its weight set to 0 must equal baseline (sanity), then with weight on. *Verify*: 1-epoch smoke passes; loss terms logged.
3. **exp2 (Cramér-Wold), exp1 (reuse Adversarial)** — sigreg-swap; *verify* SIGReg scalar shape/grad OK.
4. **exp8, exp5, exp10** — subclass/callback; *verify* queue/EMA/controller update once without NaN.
5. **exp6 (dense), exp9 (AutoView)** — heaviest; gate behind `/idea-vetting` before full 400-ep runs.
6. Each new official class added to `lejepa_variants.py` gets a 3-line unit smoke in `tests/` mirroring existing variant tests (if any), `--max_steps 3 --accelerator cpu`.

**Success criterion for this plan's execution**: every `exp<x>.py` (a) imports its mechanism from `stable_pretraining` official source, (b) passes a 1-epoch/`max_steps=3` smoke on CPU, (c) reduces to baseline when its new weight is 0 (where applicable), (d) runs unchanged under the Kaggle offline orchestrator.

---

## 7. Open decisions for you (resolve before coding)

1. **Probe metric**: keep OnlineProbe (A, default) or add paper-spec offline probe (B)?
2. **exp1**: reuse `AdversarialSIGReg` as-is, or only add the random+learned slice-mix knob (or drop exp1 as duplicate of prior batch)?
3. **`_common.py` location**: keep in `climb_bench/batch1/` (surgical, default) or promote to `benchmarks/imagenet10/` official source?
4. **Scope of first build**: all 10, or the 4 cheap wins (exp3/4/7 + baseline) first?
5. **New classes destination**: confirm OK to extend official `lejepa_variants.py` (consistent with convention) vs a new `climb_bench/batch1/_variants.py` (keeps official source untouched but technically not "official module").
