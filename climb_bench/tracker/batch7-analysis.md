# Batch-7 analysis — Phase 0 (pre-GPU gates)

**Date**: 2026-07-17 · **Plan**: [../ideation/plan-batch-7.md](../ideation/plan-batch-7.md) · **Ideas**: [../ideation/batch-7.md](../ideation/batch-7.md) + idea6/7/8 addenda
**Cost**: ~1 min CPU total, 0 GPU-h. Four verdicts reached before any Kaggle spend.

## TL;DR

| exp | Idea | Phase-0 verdict | Action |
|-----|------|-----------------|--------|
| exp1 | 2 — Hyvärinen score matching | ✅ **SHIPS** as rewritten (`KLScoreSIGReg`) | build |
| exp2 | 3 — Adversarial max-sliced | ⚠️ **PARTIAL** — works but ~50–100× slower | build, **M=1-random control mandatory** |
| exp3 | 7 — FM-SIGReg | ✅ **SHIPS** as `FMSIGRegB(path=ot, t∈[0.3,0.7])`; the **as-written spec fails** | build B-form only |
| exp4 | 1 — FM-invariance | not testable by this harness (invariance term, not SIGReg) | build, verify at smoke |
| exp5 | 5 — Simplex-ETF prototypes | ✅ prior-art gate **CLEARED**; built frozen-ETF (1 knob, not 3) | build |
| exp7 | 4 — RL crop policy | ⚠️ built; **the spec's reward sign contradicts its own rationale** | build, guards mandatory |
| exp6 | 6 — Rotation projector | 🔴 **DEAD** — confirmed numerically | drop |
| exp8 | 8 — CLIP | 🔴 KILL (framing) — unchanged | drop |

Harness: [../batch7/test_statistics.py](../batch7/test_statistics.py). Runner: [../batch7/run-batch7.py](../batch7/run-batch7.py).

## The harness had to be redesigned twice — both times the bug was mine

**(1) Scalar comparison is meaningless.** The plan proposed ranking each candidate's scalar across synthetic distributions. That cannot work: for the KL-surrogate family the encoder-facing term is `0.5·E‖z‖² + E[s(z)·z]`, and by integration by parts `E[∇log p(z)·z] = −d` for **every** smooth density. The surrogate's *value* degenerates to the second moment and carries no Gaussianity signal — only its *gradient* is meaningful.

Redesign: **free-z descent**. Let `z` be a free parameter matrix (the maximally-flexible encoder), descend the candidate objective exactly as production does (one optimizer over `{z} ∪ {module's internal net}`), and measure `z` with an **independent yardstick** the objective never sees — baseline sliced Epps–Pulley, per-coord std, `‖Cov−I‖_F`. If an objective has a collapse attractor, an unconstrained encoder finds it.

**(2) The first run mislabelled 5/7 candidates.** The init had std 2.47, so the verdict rule `std > 2.0 → DIVERGE` auto-labelled anything that *didn't move* as diverging. Fixed by standardising the init (bimodal + anisotropic, but mean per-coord std = 1) and adding a `NO-SIGNAL` verdict. With that, "did nothing" is distinguishable from "blew up".

## Results (n=256, d=16, 1500 steps; ref N(0,I) ep = 1.116)

```
baseline_ep      CONVERGE   ep 49.0 -> 0.15   std 0.991   <- positive control OK
klscore          CONVERGE   ep 51.0 -> 0.48   std 1.015
orig_hyvarinen   NO-SIGNAL  ep 45.7 -> 86.4   std 0.943
adversarial      PARTIAL    ep 49.0 -> 13.7   std 0.948   (@12k steps, still falling)
fm_a_ot          NO-SIGNAL  ep 46.3 -> 61.0   std 0.722
fm_b_ot          CONVERGE   ep 46.4 -> 0.87   std 1.104   (@12k steps, stable)
fm_b_vp          NO-SIGNAL  ep 44.1 -> 26.7   std 0.583
```

### exp1 — the §3.1 rewrite is validated, and the original is confirmed broken

`klscore` converges (ep 51 → 0.48, std 1.015, cov_err 0.809) — matching the baseline EP statistic's own quality. The two-player split (score net descends ISM on detached `z`; encoder descends the KL surrogate with the score frozen), taken from `refs/sliced_score_matching/losses/wae.py::wae_ssm`, works.

`orig_hyvarinen` (the untouched `lejepa_variants.py::HyvarienSIGReg`) drives **ep from 45.7 to 86.4 — it nearly doubles**. The §3.1 claim is confirmed *in direction*: descending the ISM scalar with the encoder pushes it the wrong way, because ISM's optimum value is `−0.5·E‖∇log p_z‖²` and jointly minimizing it *maximizes* the encoder's own Fisher information.

⚠️ **My predicted failure mode was wrong**: I said "collapse to a peaked distribution"; the measured mode is *actively anti-Gaussian* at roughly unit scale (std 0.943, cov_err 13.8). Right direction, wrong death.

### exp3 — the as-written spec fails; the two-player reformulation ships

`fm_a_ot` — the addendum's actual spec, copied verbatim — **fails** (ep 46.3 → 61.0, std drifting to 0.72). Predicted collapse; measured stall-and-worsen within 1500 steps. Either way it does not drive the encoder to N(0,I).

`fm_b_ot` — the new two-player form — **converges** (ep → 0.87, stable at 12k steps).

**The velocity→score algebra is verified.** `refs/flow_matching` contains no velocity↔score conversion anywhere (`grep -r score` over the package returns nothing), so a unit test *is* the verification: train the velocity net on a Gaussian with analytic score, compare.

```
t=0.1  scale_vs_analytic=+0.819  rel_rmse=1.316
t=0.3  scale_vs_analytic=+1.101  rel_rmse=0.255
t=0.5  scale_vs_analytic=+1.001  rel_rmse=0.090
t=0.9  scale_vs_analytic=+0.996  rel_rmse=0.009
```

The identity `s_t = −[(1−t)·v(z_t,t) + z_t]/t` is right (scale 1.001 at t=0.5). But it **divides by t**, amplifying the velocity net's irreducible error by 1/t. My first version used a fixed `t_eval=0.1` — the single worst choice — and diverged.

**The t-band is the whole mechanism**, and the sweep is a textbook bias–variance curve:

| band | verdict | ep | std |
|---|---|---|---|
| ot [0.1, 0.3] | DIVERGE | 112 | 2.86 |
| **ot [0.3, 0.7]** | **CONVERGE** | **0.59** | **1.056** |
| ot [0.5, 0.9] | COLLAPSE | 93 | 0.161 |
| ot [0.05, 0.95] | NO-SIGNAL | 38 | 1.89 |

Small `t` → 1/t noise amplification → diverge. Large `t` → `p_t → N(0,I)` regardless of `P_z`, so the score carries no information about the encoder → **collapse** (std 0.161). Mid-band → converge, at ep 0.59, *below* the reference N(0,I) value of 0.708.

Averaging over a band is exactly the "time-averaged, visits all scales" property idea 7 advertises as its headline advantage over single-scale score matching. **The fix is the mechanism, not a patch.**

⚠️ **`vp` path is unnecessary.** I proposed the variance-preserving interpolant to fix "soft spot 1" (under `ot`, `z₀ ~ N(0,I)` gives `z_t ~ N(0, ((1−t)²+t²)I) ≠ N(0,I)`, so the target is a fixed point only at `t ∈ {0,1}` — I expected variance shrinkage). It did not bite: `ot` reaches std 1.056. And `vp` is *worse* (NO-SIGNAL, std 0.583). Keep `--fm_path` for the record; default `ot`.

### exp2 — sound but slow; idea 3's headline claim is unsupported

`adversarial` at 12k steps: ep 49 → 13.7, **still falling**. Not broken — roughly **50–100× slower** than baseline/klscore. Consistent with the mechanism: M=1 adversarial slice fixes one direction at a time, against d=16.

This directly undercuts idea 3's central claim — *"M=1 adversarial slice replaces M=1024 random — net 100×–1000× cheaper SIGReg per step"* and *"single slice suffices in principle"*. Per-step cost falls; **step count rises**. The saving may be illusory.

Caveat: free-z with d=16 is an artificial, harsh setting and may understate a real encoder. Not a kill. But it makes the **`M=1 random` control arm mandatory** (already in `batch-7.md` §Idea 3's falsification), and the matched-wall-clock comparison load-bearing rather than a formality.

### exp6 — dead both ways, 0 GPU

Fed a **perfect `N(0, I₃₈₄)`** source through an orthogonal projector:

```
ep(z, 384-d)                 = 1.046   <- the floor
ep(orthogonal proj -> 512-d) = 20.424  <- rank of Cov(proj) = 384 / 512
ep(orthogonal proj -> 384-d) = 1.021   (vs source 1.025) -> exactly a no-op
```

- At the **baseline config** (`embed_dim=384 → proj_dim=512`): no isometry `R³⁸⁴ → R⁵¹²` exists, so 128 coordinates have exactly zero variance and SIGReg reads **20.4 vs a floor of 1.05 even when the encoder is already perfect**. The objective is structurally unsatisfiable.
- At **`proj_dim=384`** (the only dims where an isometry exists): the projector is a **no-op for SIGReg** (`ep(proj) == ep(source)`), so SIGReg-on-proj ≡ SIGReg-on-embed — the measured `sigreg_target=embed` regime, **top1 0.2371 = collapse**.

Combined with the measured projector-capacity curve running the opposite way to the idea's hypothesis (`Linear` 0.2343 < `MLP2` 0.5713 < `MLP` 0.5946 < `MLP4` **0.6126**), exp6 is dropped. The butterfly vendoring plan (§3.4) is moot; `refs/learning-circuits` stays cited for the record.

## Scorecard: pre-registered predictions vs measured

| candidate | predicted | measured | |
|---|---|---|---|
| baseline_ep | CONVERGE | CONVERGE | ✅ |
| klscore | CONVERGE | CONVERGE | ✅ |
| orig_hyvarinen | COLLAPSE | NO-SIGNAL (anti-Gaussian) | ⚠️ right direction, wrong mode |
| adversarial | CONVERGE | PARTIAL (slow) | ⚠️ |
| fm_a_ot | COLLAPSE | NO-SIGNAL (stall+worsen) | ⚠️ right verdict, wrong mode |
| fm_b_ot | CONVERGE | CONVERGE (only in-band) | ✅ with a caveat I did not predict |
| fm_b_vp | CONVERGE | NO-SIGNAL | ❌ mitigation unnecessary and harmful |

2/7 clean hits. The pre-registration was worth keeping precisely *because* it was mostly wrong: the plan's §3.2 collapse argument reached the right **verdict** on `fm_a` via a mechanism (conditional-variance → 0 at `δ₀`) that the measurement does not show within 1500 steps. Do not quote the collapse-attractor story as measured fact — quote the verdict.

## Build + model-level smoke (2026-07-17)

`batch7/` = `_common.py` (fork) + `_variants.py` (self-contained) + `exp_baseline/exp1/exp2/exp3/exp4.py` + `test_statistics.py`. All five build, forward and backward on CPU at `proj_dim=64, n_slices=32`:

```
exp          sigreg            loss      inv    sigreg | grps    auxP    auxLR  auxWD     grads
exp_baseline ep              0.1866   0.1344    2.6131 |    1       0  0.0e+00   None   162/162
exp1         klscore        -1.1183   0.1344  -62.6308 |    2   33088  4.0e-04    0.0   166/166
exp2         adversarial     0.4859   0.1344   17.5782 |    2   33088  4.0e-03    0.0   166/166
exp3         fm              0.0449   0.1344   -4.4709 |    2   49472  4.0e-04    0.0   166/166
exp4         ep(FMinv)       0.2043   0.1520    2.6131 |    1       0  0.0e+00   None   166/166
```

Isolation verified by construction, not by assertion:
- `inv = 0.1344` identical across exp_baseline/1/2/3 → the SIGReg swap does not touch the invariance term.
- `sigreg = 2.6131` identical between exp4 and exp_baseline → FM-invariance does not touch SIGReg.
- exp_baseline gets **1** param group with an empty aux set → reduces exactly to batch-2's flat `model.parameters()`.
- exp2's aux lr is `4.0e-3` = 10× base (batch-7.md §Idea 3); every aux group is `wd=0`.
- 166/166 params receive gradients — no dead parameters.

### `_common.py` scope decision

Batch-2's optimizer machinery (Muon / schedule-free / SAM / PCGrad / SWA / stochastic-depth scheduling) and its `_vendor` wheels were **removed**, not carried. Batch-7 is a loss/objective batch — every exp is stock AdamW in automatic optimization. Keeping it would have meant copying four batch-2 callback classes into `batch7/_variants.py` that no batch-7 exp ever constructs.

### exp1's negative loss is expected; the init pathology behind it is real but mild

`sigreg = −62.6` (total loss −1.12) is not a bug: the KL surrogate is `KL` up to an additive constant, so its *value* is not floored at 0. Only its gradient is meaningful — the same reason the scalar-comparison harness design failed.

But it exposed a two-timescale risk worth checking. At init the score net is random, so `s ≈ −z`, hence `E[s·z] ≈ −E‖z‖²` and the surrogate ≈ `−0.5·E‖z‖²` — **the encoder is briefly rewarded for inflating `‖z‖`** until the score net catches up. Measured (encoder lr fixed at 1e-2, score-net lr scaled):

| score-net lr | final ep | peak std during run |
|---|---|---|
| 0.1× | 2.527 | **1.378** |
| **1.0× (default)** | **0.483** | 1.026 |
| 5.0× | 1.651 | 1.089 |
| 20× | 0.435 | 1.035 |

The mechanism is real and visible at 0.1× (peak std 1.378, worse final ep) but **self-correcting and absent at ≥1×**. So `--aux_lr_mult 1.0` is validated as exp1's default and needs no warmup; the actionable rule is simply **never set `aux_lr_mult < 1` for exp1**. The cosine schedule decays both groups proportionally, so the ratio holds for the whole run.

## exp5 (ETF) + exp7 (RL) — build findings

### exp5 gate CLEARED, and the reason matters

Searched *"Cramér–Wold neural collapse simplex ETF"* and *"isotropic Gaussian embedding implies simplex ETF class means"*. No equivalence theorem exists — and none should. **SIGReg constrains the MARGINAL law of all samples; ETF is a statement about CLASS-CONDITIONAL means.** The two are logically independent: `P_z = N(0,I)` holds perfectly with every class mean stacked at the origin, which is chance-level probe accuracy. So the idea's premise — that neither SIGReg nor the invariance term constrains cluster geometry — is sound.

### exp5 built with one term and one knob, not three

Idea 5 proposed *learnable* prototypes + an `L_ETF` penalty pulling their cosines to `−1/(K−1)`, i.e. two weights (`α`, `β`) plus a K sweep. The simplex ETF is closed-form — there is nothing to learn. Following `refs/Neural-Collapse/models/resnet.py:213`, `build_simplex_etf` constructs it exactly and registers it as a **buffer, not a Parameter**, so it never reaches the optimizer. That deletes `L_ETF` and `α`, leaving `L_cluster` and `--etf_w`.

Verified:

```
ETF K=20 d=512: norms=1.0000..1.0000  off-diag cos=-0.052632..-0.052632  (target -0.052632)
ETF K=10 d=512: norms=1.0000..1.0000  off-diag cos=-0.111111..-0.111111  (target -0.111111)
exp5_off vs baseline: EXACT (bit-for-bit)
exp5 usage_entropy = 2.9953   vs   max log(20) = 2.9957
```

The ETF is exact to 6 decimals, the off-switch is bit-for-bit, and the SwAV-derived Sinkhorn produces an almost perfectly balanced assignment at init — the anti-collapse mitigation is engaged, not aspirational. `fit/etf_usage_entropy` is the run-time guard: a drop below ~log(K) means the assignment collapsed onto few prototypes.

### exp7 — two spec problems, one of them a contradiction

**(1) The reward sign contradicts itself in the ideation doc.** `batch-7.md` §Idea 4 implementation step 3 specifies

    r_i = L_invariance_random_baseline − L_invariance(crop_i)

which rewards crops with *lower* invariance loss — **easy** views. But §Why-expected-to-improve says the policy should shift "toward 'hard' views — those with the highest per-image invariance loss", and cites arXiv:2310.03940 (*Beyond Random Augmentations: Pretraining with Hard Views*) as the supporting evidence. **The formula and the rationale have opposite signs.** `--rl_reward {hard,easy}` exposes both; the default is `hard`, following the rationale and the cited literature rather than the formula. Both arms are in `run-batch7.py`. Resolve at vetting.

**(2) The "data/transform" surface is not viable.** The policy is a GPU net conditioned on the image; transforms run in CPU dataloader workers, so a per-sample GPU call from a worker is not possible. The policy therefore crops **on GPU inside `forward`**, using `global_views[0]` (224px) as the source and `F.grid_sample` to produce local-sized crops. The semantics shift honestly: the policy chooses *which sub-region of this global view a local crop should look at*, rather than re-cropping the original image.

View order into `_compute_loss` is `[globals | random locals | policy crops]`, so the random locals are an **in-batch control at every step** — the reward needs no separate control forward, which is cheaper than the spec's "compute baseline once per image".

Smoke: policy = 8763 params (negligible), grads 171/171, init entropy 4.257 (broad), init reward −0.012 ≈ 0 — i.e. policy crops start no harder than random, the closest achievable analogue of "starts neutral". ⚠️ A Gaussian policy **cannot** exactly reproduce `RandomResizedCrop`'s law, so the honest off-switch is the `--rl_crops` flag (absent ⇒ stock LeJEPA), *not* the init. The plan's "random policy within 0.1 pp of the random-crop baseline" check is therefore approximate by construction.

### exp7's A/B set was corrected, not just costed

`batch-7.md` §Next-steps demands a tight A/B against SelfAugment. `refs/selfaugment/slm_utils/faa_search_legit.py` shows SelfAugment is **Ray Tune + HyperOpt TPE offline search over Fast-AutoAugment policies across 5 pre-trained k-fold MoCo checkpoints** — not online RL at all. Two consequences: (a) idea 4's "EXTENDS bordering DUPLICATE" flag should be **downgraded to EXTENDS** — online REINFORCE-during-pretraining is genuinely mechanism-distinct; (b) the demanded A/B is un-runnable at this batch's budget, so the comparison set is random crops + b5 saliency, as `batch-7.md`'s own falsification test already specifies. Strike the "A/B vs SelfAugment" demand.

## What Phase 0 cost vs saved

~1 min CPU. It killed exp6 outright, killed the `fm_a` spec, caught a fatal `t_eval` choice that would have looked like "idea 7 doesn't work" after ~15 GPU-h, and flagged idea 3's compute claim. The plan's §6 framing — "the highest-value step in this plan" — held up.

## Next

`_common.py` fork → runners → smoke. exp5 still gated on the free prior-art search (*"Cramér–Wold neural collapse simplex ETF"*). exp7 (RL) last.
