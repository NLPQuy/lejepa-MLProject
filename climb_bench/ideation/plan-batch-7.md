# Implementation Plan — Batch 7 (Imagenette / LeJEPA — T3 cross-domain: flow-matching, score-matching, game theory, RL, neural collapse)

**Source ideas**: [batch-7.md](batch-7.md) (ideas 1–5) + [batch-7-idea6-addendum.md](batch-7-idea6-addendum.md) (quantum/Givens projector) + [batch-7-idea7-addendum.md](batch-7-idea7-addendum.md) (FM-SIGReg) + [batch-7-idea8-addendum.md](batch-7-idea8-addendum.md) (CLIP guidance)
**Target**: jupytext experiment files `exp<x>.py` under `climb_bench/batch7/`, uploaded to Kaggle, run **offline** (torchvision 0.26 pinned wheels).
**Reference code**: cloned under [refs/](../../refs/) — see §2. Read before touching any mechanism.

> **Status (2026-07-17): approved; Phase 0 RUN and complete.** Results and the full
> pre-registration scorecard: [../tracker/batch7-analysis.md](../tracker/batch7-analysis.md).
> Verdicts now settled — **exp1 ships as rewritten**; **exp3 ships as `FMSIGRegB(path=ot, t∈[0.3,0.7])`
> while the as-written spec fails**; **exp2 ships but is ~50–100× slower than claimed**;
> **exp6 dropped (confirmed dead, 0 GPU)**. §3.2's `vp` mitigation proved unnecessary and worse.
> Where this document and the tracker disagree, the tracker is the measured record.

---

## 0. The two facts that reshape this batch

### 0.1 Four of the eight ideas already have prior art in-repo — but batch7 is self-contained

[stable_pretraining/methods/lejepa_variants.py](../../stable-pretraining/stable_pretraining/methods/lejepa_variants.py) (commits `b3670b0`, `7ec8f45`) already contains code for batch-7 ideas 1, 2, 3 and 7:

| batch-7 idea | Existing class | Verdict on that code |
|---|---|---|
| 2 — Hyvärinen score matching | `HyvarienSIGReg` | ⚠️ **structurally wrong** — see §3.1 |
| 3 — Adversarial max-sliced | `AdversarialSIGReg` | ✅ sound; deviates from spec on lr-ratio |
| 7 — FM-SIGReg | `FMSIGReg` | ⚠️ **collapse attractor** — see §3.2 |
| 1 — FM-invariance | `FMInvariance` + `LeJEPAFMInv` | ✅ sound |
| (b3 idea 2) SRHT | `SRHTSlicedEppsPulley` | ✅ sound |

**Nothing imports them.** No runner, no benchmark, no test — they have never been executed. So batch-7 is *not* mostly a writing job; it is a **fix + falsify** job. This inverts the effort estimates in `batch-7.md`, which costed all four as fresh M-effort builds.

**Decision (user, resolves the `CLAUDE.md` hard-rule conflict): `climb_bench/batch7/` is fully self-contained. No `exp<x>.py` imports from `lejepa_variants.py`.** Every mechanism — including the two classes judged sound — is **copied into `batch7/_variants.py`** and owned there. The official file is neither edited nor imported; it stays a frozen record of what was tried.

This follows the repo's own precedent rather than fighting it: `CLAUDE.md` §"Dual EppsPulley implementations" documents that `stable_pretraining.methods.lejepa` deliberately keeps its own copy of `EppsPulley`/`SlicedEppsPulley` so it can run without the `lejepa` package. Same reasoning here — a batch is a self-contained, Kaggle-uploadable unit, and copying ~200 lines is cheaper than a cross-package dependency that silently changes under a batch's feet. Cost of the duplication is honest and accepted: a fix in `batch7/_variants.py` does **not** propagate to the official file, and vice versa.

### 0.2 The repo's own ablation already predicts idea 6 fails

`ablation_results/ablation_summary.csv`, `projector_depth` + `sigreg_target` ablations (single seed, under-fit pipeline — but `CLAUDE.md` states these **structural** conclusions hold):

| Setting | top1 |
|---|---|
| `projector_arch=Linear` | **0.2343** ← collapse |
| `projector_arch=MLP2` | 0.5713 |
| `projector_arch=MLP` (baseline) | 0.5946 |
| `projector_arch=MLP4` (deeper) | **0.6126** ← more capacity wins |
| `sigreg_target=embed` | **0.2371** ← collapse |
| `sigreg_target=proj` (baseline) | 0.5946 |

Idea 6 (structured-orthogonal Givens/butterfly projector) rests on "the projector is over-parameterized, bottleneck it so the encoder does more work." The measured capacity curve runs **monotonically the other way**: `Linear < MLP2 < MLP < MLP4`. Three independent strikes:

1. **Capacity direction is backwards.** Deeper projector is the best measured arm; the idea proposes 3.5k params against MLP's ~300k.
2. **An orthogonal projector is a constrained Linear projector.** `Linear` measures 0.2343 — collapse. Orthogonality is a *further* restriction on top of that.
3. **Orthogonal ⇒ SIGReg-on-proj degenerates to SIGReg-on-embed.** If `P` is an isometry, `Cov(Pz) = P Cov(z) Pᵀ` — same spectrum, so the test on projections is the test on embeddings up to rotation. `sigreg_target=embed` measures 0.2371 — collapse.

Plus a dimension bug the addendum never addresses: `vit_small` `embed_dim=384`, baseline `proj_dim=512`. **No isometry exists from R³⁸⁴ onto R⁵¹²** — its image is a 384-dim subspace, so 128 of the 512 coordinates have exactly zero variance and sliced-EP sees a maximal violation on every slice touching them. Idea 6 therefore *forces* `proj_dim=384`, which is no longer the baseline configuration — so its arm needs a `proj_dim=384` **MLP control** or the comparison is confounded by projector width, not projector structure.

**Recommendation**: demote idea 6 to a **1-hour pre-registered cheap kill** (§6 Phase 0), not an M-effort build. If it is built anyway, it must ship the `proj_dim=384` MLP control arm.

### 0.3 Idea 8 (CLIP) is not implemented

Its own addendum lists three 🚨 blockers: task-framing violation (in-domain SSL implies no external foundation model), full duplicate of NOVA (arXiv:2602.00653), and a killer baseline (frozen CLIP-ViT-L direct probe ≈97–98% vs LeJEPA-ViT-S ≈85–90%) that asymptotically dominates. Imagenette's 10 classes are in CLIP's training set, so the unsupervised framing is broken outright. **No exp file. Recorded as KILL.** Reopen only if the user rescopes the benchmark to allow foundation-model distillation, which is a different benchmark.

---

## 1. Per-idea implementation map

Legend — **Surface**: `sigreg-swap` (`model.sigreg = …`) | `subclass` (override `_compute_loss`) | `ctor-inject` (`LeJEPA(projector=…)`) | `callback` | `data/transform`.
All mechanism code is **defined in `climb_bench/batch7/_variants.py`** (copied, never imported from `stable_pretraining/` — §0.1). `_common.py` wires. Runners stay ~30 lines.

| exp | Idea | Surface | Status | What batch7/_variants.py owns | Runner |
|-----|------|---------|--------|-------------------------------|--------|
| exp1 | #2 Hyvärinen score matching | sigreg-swap | ⚠️ **rewrite** | `KLScoreSIGReg` — two-player KL surrogate (§3.1) | `model.sigreg = KLScoreSIGReg(dim=512)` |
| exp2 | #3 Adversarial max-sliced | sigreg-swap | ✅ **copy + control arms** | `AdversarialSIGReg` (copy, verbatim) | `model.sigreg = AdversarialSIGReg(...)` |
| exp3 | #7 FM-SIGReg | sigreg-swap | ⚠️ **copy + reformulate** | `FMSIGRegA` (as-written) + `FMSIGRegB` (two-player, §3.2) + collapse guard | `--fm_form {a,b}` |
| exp4 | #1 FM-invariance | subclass | ✅ **copy** | `FMInvariance` + `LeJEPAFMInv` (copy, verbatim) | instantiate subclass |
| exp5 | #5 Neural-collapse ETF prototypes | subclass | 🆕 **build** | `LeJEPAETF(LeJEPA)` — fixed simplex-ETF bank + Sinkhorn assignment (§3.3) | `--etf_w 0.0` (off ⇒ baseline) |
| exp6 | #6 Structured-rotation projector | ctor-inject | 🔴 **pre-killed** — Phase 0 only | `ButterflyProjector` (vendored, §3.4) **if** it survives Phase 0 | `LeJEPA(projector=…)`, `--proj_dim 384` |
| exp7 | #4 RL augmentation policy | data/transform + callback | 🆕 **build** (last) | `CropPolicy` + `REINFORCECallback` (§3.5) | `--rl_crops` (off ⇒ baseline) |
| — | #8 CLIP guidance | — | 🔴 **KILL** (§0.3) | — | — |

Off-switch == exact baseline for every exp (`etf_w=0`, `rl_crops` absent, stock `model.sigreg`), verified by identical 1-epoch loss — the batch-1/2/3 convention.

**Copy provenance rule**: each class copied into `_variants.py` carries a one-line header comment naming its origin (`# copied from stable_pretraining/methods/lejepa_variants.py @ 7ec8f45 — batch-local, do not re-import`) plus, for exp1/exp3, what was changed vs that origin. Without this the duplication becomes unreadable in three batches' time.

---

## 2. Reference repos (`refs/`) — what each one settles

Cloned `--depth 1` at plan time. These are **read-only references**, not dependencies; nothing in `refs/` is imported at runtime. Add `refs/` to `.gitignore` (§7 Q4).

| Repo | Used for | The finding |
|---|---|---|
| [refs/sliced_score_matching](../../refs/sliced_score_matching) (Song & Ermon, NeurIPS 2019) | idea 2 | `losses/wae.py::wae_ssm` is **literally this idea**: regularize an encoder's latent toward N(0,I) with a score net. It uses a **separate optimizer** for the score net and a **different loss** for the encoder. Our `HyvarienSIGReg` uses one loss for both → §3.1. |
| [refs/flow_matching](../../refs/flow_matching) (Meta, Lipman et al.) | ideas 1, 7 | `path/affine.py::AffineProbPath` confirms our interpolant/target convention is right, and confirms nothing in the CFM theorem constrains the *source* distribution — exactly why joint minimization over the encoder is unsound → §3.2. **Negative finding**: the library has *no* velocity↔score conversion (`grep -r score` over the whole package returns nothing), so §3.2's B-form algebra has no reference backing and must be checked numerically in Phase 0. |
| [refs/swav](../../refs/swav) (FAIR) | idea 5 | `main_swav.py`: prototypes L2-normalized every step; `--freeze_prototypes_niters 313` (freeze at start, else collapse); `distributed_sinkhorn` for balanced assignment. All three are the mitigations idea 5 lists as "TODO". |
| [refs/Neural-Collapse](../../refs/Neural-Collapse) (Ding et al.) | idea 5 | `models/resnet.py:213` builds an **exact** simplex ETF `√(K/(K−1))·(I − (1/K)11ᵀ)` and sets `requires_grad_(False)`. `validate_NC.py:123::compute_ETF` is the ready-made mechanism-check metric. → §3.3 |
| [refs/learning-circuits](../../refs/learning-circuits) (Dao et al., ICML 2019) | idea 6 | `torch_butterfly/multiply.py:28::butterfly_multiply_torch` — a ~20-line **pure-PyTorch** butterfly (no CUDA build, Kaggle-offline-safe). Makes idea 6's naive `for l in range(L)` loop obsolete → §3.4. |
| [refs/selfaugment](../../refs/selfaugment) (Reed et al., CVPR 2021) | idea 4 | **SelfAugment is not online RL.** `slm_utils/faa_search_legit.py` is Ray Tune + HyperOpt TPE over Fast-AutoAugment policies, requiring **5 pre-trained k-fold MoCo checkpoints** + a separate search phase. → §3.5 |

`ishansd/max-sliced-wasserstein` (idea 3's CVPR-2019 reference impl) **no longer exists on GitHub** — 404. Idea 3 is already implemented from the paper, so this is not blocking; noted so nobody hunts for it.

---

## 3. Mechanism notes (the parts that are not mechanical)

### 3.1 exp1 — Hyvärinen: the existing implementation optimizes the wrong sign

`HyvarienSIGReg.forward` returns `0.5‖s+z‖² + v·∇s·v` and **both** the score net and the encoder descend it under one optimizer (`_adamw_params` → `model.parameters()`).

The ISM objective is a **minimum over the score function only**. For a fixed distribution `p_z`:

```
min_s  E[ 0.5‖s(z)‖² + tr(∇s(z)) ]  =  −0.5 · E[ ‖∇log p_z(z)‖² ]      (at s* = ∇log p_z)
```

The optimum **value** is *minus* the Fisher information of `p_z`. So letting the encoder descend the same scalar pushes it to **maximize its own Fisher information** — toward a sharply peaked distribution. That is a collapse direction, not a route to N(0,I). The residual parameterization `s = head(z) − z` fixes the convex-decoy that the ideation doc worried about, but it does not touch this: the decoy was never the real problem.

`refs/sliced_score_matching/losses/wae.py::wae_ssm` shows the correct two-player split, and it is the same problem (encoder latent → N(0,I)):

```python
ssm_loss, *_ = sliced_score_estimation_vr(score, z)   # score net only, score_opt.step()
...
nlogpz = z ** 2 / 2. + np.log(2. * np.pi) / 2.        # cross-entropy to N(0,I)
scores = score(z)
entropy_surrogate = (scores.detach() * z).sum(dim=-1) # ∇_φ of −H(P_z)
loss = recon + lam * (nlogpz + entropy_surrogate)     # encoder only
```

Because `KL(P_z ‖ N(0,I)) = −H(P_z) + E[−log N(z;0,I)]`, the encoder's term is exactly `KL(P_z ‖ N(0,I))` up to a constant — a **better-motivated SIGReg replacement than the ideation doc claimed**, since it is a bona-fide divergence to N(0,I) rather than a goodness-of-fit statistic.

`KLScoreSIGReg` implements this with `AdversarialSIGReg`'s single-optimizer detach trick (no second optimizer, no manual optimization):

```python
def forward(self, z):
    # score-net path: descends ISM on detached z  → learns ∇log p_z
    z_d = z.detach().requires_grad_(True)
    s_d = self.score_net(z_d) - z_d
    v = torch.randn_like(z_d)
    jvp = torch.autograd.grad((s_d * v).sum(), z_d, create_graph=True)[0]
    ism = 0.5 * (s_d + z_d).pow(2).sum(-1).mean() + (v * jvp).sum(-1).mean()

    # encoder path: descends KL(P_z ‖ N(0,I)) with the score net frozen
    s = (self.score_net(z) - z).detach()
    kl = 0.5 * z.pow(2).sum(-1).mean() + (s * z).sum(-1).mean()

    return ism + kl          # gradients are disjoint by construction
```

Two `autograd.grad(create_graph=True)` calls per step; ~10% step cost at `d=512`.

### 3.2 exp3 — FM-SIGReg: the as-written form has a collapse attractor; build two forms and let Phase 0 pick

**The problem.** `FMSIGReg` lets the encoder and the velocity net descend the same `‖v_ψ(z_t,t) − target‖²`. At the velocity optimum the loss is the **conditional variance** `E[Var(z₁−z₀ | z_t)]`. Now let the encoder collapse `P_z → δ₀`. Then `z_t = t·z₁ + σε`, so `z₁ ≈ z_t/t` is *fully determined by `z_t`* — conditional variance → 0. **Collapse is the global minimum of L_FM.**

The addendum asserts the loss "increases monotonically with `W₂(P_z, N(0,I))`" and predicts a positive plateau `~d`. Both claims fail at the collapsed point, and the addendum's own mechanism check ("if it hits 0, the velocity collapsed → reject") is describing this attractor without naming it. The v2 docstring credits a "(B) KL bound" upgrade, but **no KL bound appears in the code** — only the ExFM target and Hungarian coupling. `refs/flow_matching` confirms nothing in the CFM theorem pins the source distribution: CFM assumes `P₀` is *given*, not optimized.

**Idea 7 is kept (user decision), so it needs a sound form, not a guard.** Build both and let Phase 0 choose:

- **`FMSIGRegA`** — the as-written joint-minimization form, copied verbatim. This is the addendum's actual spec and the thing under test. It is also the arm the collapse argument predicts will fail.
- **`FMSIGRegB`** — two-player split, same shape as exp1 (§3.1): the velocity net descends the CFM loss with the encoder **detached** (it just learns the marginal velocity of the *current* `P_z`); the encoder descends a KL surrogate built from a velocity-derived score, detached. This preserves the addendum's stated headline motivation — "time-averaged smoothing … implicitly visiting all scales" — while removing the joint-minimization pathology.

**⚠️ The B-form rests on a derivation I have not verified against any reference.** For the interpolant `z_t = (1−t)z₀ + t·z₁` with `z₁ ~ N(0,I)`, conditioning gives `E[z₁|z_t] = (1−t)·v_ψ(z_t,t) + z_t`, hence a smoothed score `s_t(z) = −[(1−t)·v_ψ(z,t) + z] / t`. That drops into exp1's encoder KL surrogate with `s_t` in place of the single-scale score net. **`refs/flow_matching` contains no velocity↔score conversion at all** — `grep -r score` over the whole library returns nothing — so unlike §3.1 (which `wae.py` corroborates line-for-line) this has **no reference implementation backing it**. It is my algebra. Two known soft spots, both to be settled numerically in Phase 0, not by argument:
  1. `s_t` is the score of the *smoothed* `p_t`, not of `P_z`. Its fixed point may not be exactly `P_z = N(0,I)`: if `z₀ ~ N(0,I)` then `p_t = N(0, ((1−t)²+t²)·I)` ≠ `N(0,I)` for `t ∈ (0,1)`. So the target is a fixed point only at `t ∈ {0,1}`, which likely **biases the encoder toward a shrunken variance**.
  2. Mitigation to test if (1) bites: a **variance-preserving** interpolant `z_t = cos(πt/2)·z₀ + sin(πt/2)·z₁`, under which `z₀ ~ N(0,I) ⇒ z_t ~ N(0,I)` for *every* `t` — restoring the target as a fixed point at all scales. Ship as `--fm_path {ot,vp}`.

**Phase 0 decides**, and it is cheap (CPU, ~1h): whichever of `{A, B×ot, B×vp}` satisfies `loss(collapsed) > loss(N(0,I))` and `loss(anisotropic) > loss(N(0,I))` goes to GPU; the rest are recorded as killed in `tracker/batch7-analysis.md`. If **none** passes, that is the honest finding and exp3 reports it — do not ship an arm that rewards collapse just to have an arm.

Both forms log `L_FM` every step and carry the RankMe collapse guard regardless of which wins.

**Consequence for the exp1↔exp3 A/B**: if `FMSIGRegB` is the survivor, exp3 is "exp1's KL surrogate with an annealed multi-scale score" — genuinely mechanism-distinct from exp1's single-scale score net, which makes the head-to-head the addendum demands *meaningful* rather than a formality. That is the best case for idea 7 and the reason keeping it is defensible.

### 3.3 exp5 — ETF: fix the prototypes, don't penalize toward them

Idea 5 proposes learnable prototypes `μ_k` plus `L_ETF = Σ(cos(μ_k,μ_k') + 1/(K−1))²` to pull them toward the ETF, adding two weights (`α`, `β`) and a K sweep.

`refs/Neural-Collapse/models/resnet.py:213` does it in one line — construct the ETF in closed form and **freeze** it:

```python
weight = torch.sqrt(torch.tensor(K/(K-1))) * (torch.eye(K) - (1/K)*torch.ones((K,K)))
weight /= torch.sqrt((1/K * torch.norm(weight, 'fro')**2))
m.weight = nn.Parameter(torch.mm(weight, torch.eye(K, d)))
m.weight.requires_grad_(False)
```

The simplex ETF is a *closed-form* geometry — there is nothing to learn. Fixing it deletes `L_ETF`, deletes `α`, and leaves **one** term (`L_cluster`) and **one** weight (`etf_w`). Per `CLAUDE.md` §2 (Simplicity First) this is the formulation to build. It also strengthens the falsification: with the target geometry fixed and exact, "did the embedding adopt it" is measured directly by `validate_NC.py::compute_ETF` on validation class-means, with no confound from prototypes that drifted.

Anti-collapse mitigations, taken from `refs/swav/main_swav.py` rather than reinvented: L2-normalize prototypes each step (moot when fixed), `distributed_sinkhorn` for balanced assignment (SwAV's `--epsilon 0.05`, 3 iters), and a warmup period mirroring `--freeze_prototypes_niters 313`. `K=20` per the idea; `K ∈ {10,20,40}` only if the primary arm shows signal.

⚠️ Open prerequisite from the ideation doc, still unresolved and still free: search *"Cramér–Wold neural collapse simplex ETF"*. If SIGReg's N(0,I) target already implies ETF emergence, exp5 is redundant. **Do this before writing exp5.**

### 3.4 exp6 — if built at all: vendor the butterfly, do not loop

The addendum's sketch loops `L = 2d·log d ≈ 4600` Givens rotations in Python with a `.clone()` per step — ~4600 sequential kernel launches per forward, which is not runnable at 400 epochs regardless of merit.

`refs/learning-circuits/torch_butterfly/multiply.py:28::butterfly_multiply_torch` does the identical algebra in `log₂(n)=9` **vectorized** steps (all `n/2` rotations at a given stride applied at once), in ~20 lines of pure PyTorch with no CUDA extension — Kaggle-offline-safe to vendor into `batch7/_vendor/` (batch-2 already has a `_vendor/` precedent). Parameterize each 2×2 twiddle as `[[cos θ, −sin θ],[sin θ, cos θ]]` → exactly orthogonal by construction, `nblocks·log₂n·n/2` params.

This only matters if exp6 survives §0.2. It is documented so the Phase-0 kill is on the *idea*, not on a strawman implementation.

### 3.5 exp7 — RL: the good news and the bad news

**Good news (novelty ↑)**: `batch-7.md` flags idea 4 "EXTENDS bordering DUPLICATE" of SelfAugment and its §Next-steps demands a tight A/B against it. Reading `refs/selfaugment` shows SelfAugment is **offline Bayesian (TPE) policy search over Fast-AutoAugment policies across 5 k-fold MoCo checkpoints** — not online RL at all. Online REINFORCE-during-pretraining is genuinely mechanism-distinct. The DUPLICATE flag should be **downgraded to EXTENDS**.

**Bad news (cost ↑)**: the demanded A/B is therefore un-runnable — a faithful SelfAugment baseline is 5 pretrains + a Ray search, an order of magnitude over batch-7's entire budget. The A/B must be against **random crops** (baseline) and **b5 saliency crops** (the static-prior alternative on the same axis), exactly as the falsification test in `batch-7.md` already specifies. The §Next-steps "A/B vs SelfAugment" demand should be struck.

**Kept (user decision), built last.** It remains the heaviest item — policy net, reward plumbing, warmup phase, entropy bonus — and the reward signal is the fragile part, so it goes at the end of the build order where it can slip without blocking anything else. Two guards from the ideation doc are non-negotiable because they are what distinguish "the policy learned something" from "the policy drifted":

- **Entropy monotonicity**: `H(π_φ)` must decrease from the uniform-prior value. Flat entropy ⇒ not learning ⇒ reject.
- **Reward monotonicity**: mean `r` must stay positive and rise. `r ≈ 0` ⇒ reward too noisy, idea reduces to baseline ⇒ reject.

Plus the init sanity: a randomly-initialized policy must match the random-crop baseline within 0.1 pp invariance, proving the policy starts neutral (i.e. `--rl_crops` off ⇒ exact baseline).

Reward choice: per-image invariance-loss drop vs a control random crop, EMA-smoothed. ⚠️ If exp3/exp4 (flow-matching) end up in the same stack, the reward becomes `ΔL_FM` rather than `ΔL_MSE` — the ideation doc flags this and it is unverified that the FM loss is informative per-crop. **Keep exp7 on the stock MSE invariance for its own falsification run**; composing it with a flow arm is a later question.

---

## 4. Shared runner contract (`batch7/_common.py`)

Fork `climb_bench/batch2/_common.py` (transforms, `_build_datasets`, `lejepa_forward`, OnlineProbe+OnlineKNN+RankMe, `run()`). Additions:

- `--sigreg {ep,hyvarinen,adversarial,fmsigreg,srht}` dispatch feeding `model.sigreg = …` (exp1/2/3), default `ep` ⇒ baseline.
- `--adv_lr_mult` (exp2) — **spec deviation to fix**: `batch-7.md` §Idea 3 says `η_φ = 10 · η_θ`, but `_adamw_params` returns a flat `model.parameters()`, so the adversary currently trains at the encoder's lr *and* inherits the cosine decay to ~0. Add a param-group split so the adversary/score/velocity nets get their own lr multiplier.
- **`weight_decay` exclusion group** — `wd=0.05` currently lands on the score net, velocity field, adversary head and prototype bank. Wrong for all four (SwAV normalizes prototypes rather than decaying them). Add them to a `wd=0` group in the same split.
- `--etf_w`, `--etf_k`, `--etf_warmup_ep`, `--sinkhorn_eps` (exp5); `--rl_crops`, `--rl_warmup_ep`, `--rl_entropy_beta` (exp7); `--proj_dim 384` + `--projector {mlp,butterfly}` (exp6, only if it survives).
- Callback registry: `FMCollapseGuard` (exp3, §3.2), `REINFORCECallback` (exp7).
- All new flags default to the **baseline/off value**.

Everything stays in **automatic optimization**. `KLScoreSIGReg`, `AdversarialSIGReg` and `FMSIGReg` all use the single-optimizer detach trick, so no manual-opt branch and no `SAMModule`-style custom step is needed this batch.

Each `exp<x>.py` stays ~30 lines, batch-2 style:

```python
# exp1.py (Hyvärinen → KL score SIGReg) — sigreg-swap, stock LeJEPA
from _common import base_parser, run
from _variants import build_lejepa, KLScoreSIGReg

def main():
    args = base_parser("LeJEPA batch-7 exp1 (KL score SIGReg)").parse_args()
    model = build_lejepa(encoder_name=args.backbone, lamb=args.lamb,
                         n_slices=args.n_slices, projector_dim=args.proj_dim)
    model.sigreg = KLScoreSIGReg(dim=args.proj_dim)
    run(model, args, tag="exp1-klscore")

if __name__ == "__main__":
    main()
```

---

## 5. Evaluation consistency (frozen ViT-S linear probe)

Unchanged from batch-3, restated because it bit batch-2:

- **Ranking metric = the online callbacks in `run()`** (`linear_probe/top1`, `knn_probe/top1`, `rankme`), identical config for every exp. Do not vary probe settings between exps.
- ⚠️ **The online `OnlineProbe` is NOT the paper recipe** (single CLS, no LN, lr 0.03). Use it only to KILL losers; re-run `viz/eval-frozen-paperspec.py` on survivors (concat CLS last-2 + LN + AdamW lr 1e-3 wd 1e-6). Batch-2 proved online ranking does not survive the paper recipe — require ≥ ~0.02 margin before trusting a pre-eval result.
- **Report best-ckpt, not last** — the baseline overfits (−2.4pp post-peak).
- ⚠️ **`rankme` is load-bearing this batch, not decorative.** exp1/exp3/exp5 all have collapse attractors (§3.1, §3.2, §3.3). A high-looking probe number with a collapsing RankMe is a failed run, not a win.
- 400-epoch pretrain; resume across Kaggle ≤12h sessions.

---

## 6. Build & verification order (goal-driven)

**Phase 0 — statistic sanity harness (CPU, local, ~1h, no data, no GPU).** The highest-value step in this plan and the one that runs despite the local torchvision 0.20 vs 0.26 mismatch (model/loss level only).

Write `batch7/test_statistics.py`: feed each candidate `sigreg` module synthetic `z` drawn from
(a) `N(0,I)` — the target, (b) a non-Gaussian (Laplace / bimodal mixture), (c) an **anisotropic** Gaussian, (d) a **collapsed** `δ₀ + ε`. Then assert, for a *fixed* module with its internal net trained to convergence on each input:

```
loss(N(0,I))  <  loss(non-Gaussian)      # the test detects non-Gaussianity
loss(N(0,I))  <  loss(anisotropic)       # the test detects anisotropy
loss(N(0,I))  <  loss(collapsed)         # THE test — collapse must not be rewarded
```

Baseline `SlicedEppsPulley` passes by construction and serves as the positive control. **Gates**: exp1 (validates the §3.1 rewrite), exp2, exp3 (**selects among `{A, B×ot, B×vp}` per §3.2** — including the unverified velocity→score algebra, which this harness checks numerically). Also run the exp6 pre-kill here: a `proj_dim=384` orthogonal-projector 1-epoch smoke against the §0.2 prediction.

1. **Fork `_common.py`** (`--sigreg` dispatch, adversary/score lr + wd param-group split, callback flags) → smoke: `exp_baseline.py` (stock LeJEPA, all knobs off) reproduces the batch-1/2 baseline for 1 epoch. *Verify*: probe metric logged, loss matches.
2. **Copy in the two sound ones (S-effort, no new mechanism)**: exp4 (`FMInvariance` + `LeJEPAFMInv`), exp2 (`AdversarialSIGReg` + `--adv_lr_mult 10`). Verbatim copies + provenance header (§1). *Verify*: `max_steps=3` smoke; exp2's init sanity from `batch-7.md` §Idea 3 step 5 — with a random `g_φ`, `T(Z·g_φ)` matches the random-slice baseline within 5%.
3. **exp1 rewrite** (`KLScoreSIGReg`) — only after Phase 0 signs off. *Verify*: Phase-0 assertions pass; `max_steps=3` smoke; score-net and encoder gradients are disjoint (assert `score_net` grads are `None` on the KL term and encoder grads are `None` on the ISM term).
4. **exp3** (`FMSIGRegA` / `FMSIGRegB` × `--fm_path {ot,vp}`) — ship whichever form Phase 0 cleared; if none cleared, report that as the result and skip the GPU run. *Verify*: `max_steps=3` smoke; collapse guard fires on a synthetic collapsing run; `L_FM` logged every step.
5. **exp5 ETF** — do the free prior-art search (§3.3) *first*; then fixed-ETF bank + Sinkhorn assignment. *Verify*: `etf_w=0` ⇒ bit-for-bit baseline loss; `compute_ETF` on the fixed bank returns ~0 (it is an exact ETF); no assignment collapse over 3 smoke epochs.
6. **exp6** — build only if Phase 0 contradicts §0.2. If built: vendor `butterfly_multiply_torch`, ship the `proj_dim=384` MLP control.
7. **exp7 RL** — last (heaviest, fragile reward). *Verify*: init-neutrality (random policy within 0.1 pp of random-crop baseline), then the entropy- and reward-monotonicity guards from §3.5 over a short run before any 400-ep commitment.

**Success criterion**: every `exp<x>.py` (a) imports its mechanism from `batch7/_variants.py` or wires it via `_common.py`, (b) passes a `max_steps=3` smoke, (c) reduces to baseline when its flag/weight is off, (d) runs unchanged under `run-batch7.py` offline, (e) for exp1/exp3/exp5, passes the Phase-0 assertions and keeps RankMe above the collapse floor.

---

## 7. Kaggle offline runbook (`run-batch7.py`)

Clone `climb_bench/batch2/run-batch2.py`. Per the kaggle-jupytext convention:
- **Double-`#`** every `!python …`/`!pip …` block (`# # !python …`) so "Run All" stays inert; user deletes one `# ` per session.
- No `[...]` in `# %%` cell titles.
- `PYTHONPATH` → both `stable-pretraining` and `climb_bench/batch7`; `SPT_LIGHT_IMPORT=0`; stub `requests_cache`.
- **No extra wheels** — every mechanism is pure-torch. `scipy` (Hungarian coupling in exp3) is already on Kaggle; the copied `_hungarian_couple` falls back to identity on ImportError, so exp3 degrades silently rather than crashing. ⚠️ **Log which path was taken** — a silent fallback means upgrade (C) is off and the arm is not testing what it claims. Consider promoting the fallback to a hard failure under `--fm_form b`.
- One run-block per exp, `--no_wandb` (CSV) offline.

---

## 8. Open decisions for you (resolve before coding)

**Resolved by user** (recorded here so the rationale survives):
- **Self-containment (§0.1)** — `batch7/` copies every mechanism into `_variants.py`; no imports from `lejepa_variants.py`, which stays frozen. Follows the repo's existing dual-EppsPulley precedent.
- **Idea 7 kept (§3.2)** — build `FMSIGRegA` + `FMSIGRegB`, Phase 0 selects. Not dropped.
- **Idea 4 kept (§3.5)** — built last, with entropy- and reward-monotonicity guards; A/B against random crops + b5 saliency, not SelfAugment.

**Still open:**

1. **exp6 (§0.2)**: accept the pre-registered cheap kill (Phase 0, ~1h) and drop it, or build it in full despite the repo's own projector-capacity curve pointing the other way? **Recommend: cheap kill.** Its `proj_dim=384` requirement also makes it the only arm not comparable to baseline at matched width. (Idea 8 stays killed per §0.3 unless you say otherwise.)
2. **exp3 fallback (§3.2)**: if Phase 0 clears *none* of `{A, B×ot, B×vp}`, do we report the negative result and stop, or spend more design time on a fourth form? **Recommend: report and stop** — a clean "transport-based SIGReg rewards collapse in all three forms we could construct" is a real finding and cheap to write up.
3. **`refs/` in git**: `.gitignore` it (6 repos, ~36 MB, one 19 MB, currently untracked) or commit a `refs/README.md` with clone commands + pinned SHAs so the plan's citations stay reproducible? **Recommend: gitignore + README with pinned SHAs.**
4. **Build scope first**: all seven exps, or baseline + the 3 cheap ones (exp2/exp4 copy-and-run, exp1 rewrite) first? **Recommend: baseline + the 3** — exp2/exp4 are copy-and-run, exp1 is the batch's best-motivated mechanism once corrected (a real KL divergence to N(0,I), not a goodness-of-fit statistic). exp3/exp5/exp7 follow as their gates clear.
5. **exp5 prerequisite**: run the free "Cramér–Wold ↔ ETF" prior-art search now and let it gate exp5, or build exp5 regardless? **Recommend: gate on it** — it is 0-cost and can delete an M-effort build.
