# Batch-7 Addendum — Idea 7 (FM-SIGReg)
**Generated**: 2026-05-19 · **Added per user request**: "improve SIGReg using flow matching"
**Tier override remains**: 0/0/100 (user-directed T3-only).

## Idea 7: Flow-Matching SIGReg (transport-based marginal-shape regularizer)

- **Pattern**: P3 (Replace — swap the per-slice Epps–Pulley statistic with a continuous-time velocity-field transport loss to N(0, I))
- **Tier**: 3 (cross-domain root: stochastic-interpolant theory — Albergo & Vanden-Eijnden 2023, *ICLR* — and continuous-time probability transport / Föllmer 1988 Schrödinger problem)
- **Scope**: enhance-existing. Replaces the SIGReg term only. Encoder, projector, invariance, λ, multi-crop unchanged.
- **One-liner**: Train a small velocity field `v_ψ(z, t)` to regress the OT-displacement target between encoder embeddings `z_0 ∼ P_z` and freshly sampled `z_1 ∼ N(0, I)`. The flow-matching loss is **0 (modulo conditional-variance constant) iff `P_z = N(0, I)`** — making it a transport-based SIGReg alternative.

### Mechanism

LeJEPA's SIGReg uses a **test-based** approach: project `z` onto `M=1024` random directions and apply the Epps–Pulley ECF goodness-of-fit test against N(0,1) per slice. Cramér-Wold guarantees consistency in the population limit.

**FM-SIGReg** replaces this with a **transport-based** approach:

```
Per step:
  z_0  ←  encoder(batch)        # shape (B, d)
  z_1  ←  sample from N(0, I)   # shape (B, d), independent
  t    ←  Uniform([0, 1])       # shape (B,)
  z_t  ←  (1-t) · z_0 + t · z_1 + σ · ε   # σ=0.01, ε ~ N(0,I)
  L_FM ←  ‖ v_ψ(z_t, t) − (z_1 − z_0) ‖²
```

Architectural constraint: `v_ψ(z_t, t)` is conditioned ONLY on `(z_t, t)`, NOT on the pair `(z_0, z_1)`. By Lipman et al. (ICLR 2023, [arXiv:2210.02747](https://arxiv.org/abs/2210.02747)), the optimal `v_ψ*(z, t) = E[z_1 − z_0 | z_t = z]` is the **marginal velocity field** that transports `P_z` to N(0, I) along the OT-displacement path.

**Key identity** (CFM theorem, Lipman 2023 §3): the minimum of `L_FM` over `v_ψ` is achieved by the marginal velocity and corresponds to the variance of the conditional velocity around the marginal. This minimum **increases monotonically with `W_2(P_z, N(0,I))`** — the 2-Wasserstein distance between the encoder distribution and the target.

So: minimizing `L_FM` *jointly* over `(v_ψ, encoder)` pushes the encoder toward `P_z = N(0, I)`, exactly SIGReg's goal — but via a learned transport instead of a per-slice test.

### Mechanism-distinct from every existing SIGReg attack

| Existing SIGReg-replacement | Math object | Mechanism family |
|---|---|---|
| EP / Hermite / KSD / Riesz-MMD (closed) | 1-D goodness-of-fit statistic on slices | Test-based |
| b7-I2 Hyvärinen multivariate | L² Fisher-divergence against `s(z) = −z` (closed-form) | Score-based |
| b7-I3 Max-sliced (adversarial) | `max_u T(Z·u)` minimax | Test-based, worst-case |
| **Idea 7 FM-SIGReg** | **Conditional velocity regression toward N(0,I)** | **Transport-based** |

### Distinct from batch-7 Idea 1 (FM-invariance)

| | b7-I1 FM-invariance | b7-I7 FM-SIGReg (this idea) |
|---|---|---|
| Source `z_0` | `encoder(view_1(image_i))` | `encoder(view(image_i))` |
| Target `z_1` | `encoder(view_2(image_i))` | `sample ∼ N(0, I)` |
| Coupling | per-image augmentation pair | unpaired data-vs-prior |
| Axis | Invariance / view alignment | SIGReg / marginal shape |
| What it regularizes | `P_{view_1} = P_{view_2}` | `P_z = N(0, I)` |

The two are **orthogonal** and could compose — "all-flow LeJEPA" = FM-invariance + FM-SIGReg + no MSE + no ECF test.

### Source inspirations

- **Primary (cross-domain root)**: *Stochastic Interpolants: A Unifying Framework for Flows and Diffusions*, Albergo, Boffi, Vanden-Eijnden, **ICLR 2023** / [arXiv:2303.08797](https://arxiv.org/abs/2303.08797) — defines the broader interpolant framework that subsumes FM, score matching, and Schrödinger bridges; the most-general framing for embedding-distribution transport.
- **Primary (computational)**: *Flow Matching for Generative Modeling*, Lipman, Chen, Ben-Hamu, Nickel, Le, **ICLR 2023 Oral** / [arXiv:2210.02747](https://arxiv.org/abs/2210.02747) — closed-form CFM training.
- **Supporting (closest prior art on flow-as-regularizer)**: *Implicit geometric regularization in flow matching via density weighted Stein operators*, [arXiv:2512.23956](https://arxiv.org/abs/2512.23956) (Dec 2025) — uses Stein operators to regularize the *flow itself* during generative training; we use the flow to regularize an *upstream encoder*. Different goal slot but mechanism overlaps.
- **Supporting (theory of FM ↔ score)**: Score-FM equivalence in the small-σ limit — Song-Ermon 2020 NeurIPS / Albergo 2023 §4. Explains why FM-SIGReg can be viewed as a *time-averaged smoothed* Hyvärinen score matching (Idea 2 of batch-7).

### Why expected to improve over Hyvärinen (Idea 2) and per-slice tests

Three motivations:

1. **Time-averaged smoothing**: Hyvärinen score matching (Idea 2) regresses `s_θ(z) = −z` at a single fixed scale. FM-SIGReg regresses across `t ∈ [0,1]`, implicitly visiting *all* scales between `P_z` and N(0, I) — this matches the empirical finding from score-based generative modeling (DDPM, EDM) that annealed-noise training has a smoother loss landscape than single-noise score matching.

2. **No convex-decoy trap**: Hyvärinen has the `s_θ(z) = −z` decoy. FM-SIGReg's analog decoy is `v_ψ(z, t) = a(t) z + b(t)` for some functions of `t` — the architectural constraint `v_ψ(z, t)` (NOT conditioned on the pair) eliminates pair-aware shortcuts; the time-conditioning forces the model to *interpolate* between `P_z` and N(0,I), not just regress.

3. **Full-d, sample-based**: Unlike per-slice tests (sampler family closed), FM-SIGReg evaluates the *full d=384-dim* embedding against N(0, I) without projecting. Unlike multivariate Hyvärinen (which needs Hutchinson trace estimation), FM-SIGReg uses *paired-sample* MC — directly comparable to data-distribution sample complexity.

### Expected gain
+0.2 / +0.6 / +1.5 pp 🟡 *(transport-based regularization for SSL embedding shaping is an unoccupied slot; the Albergo-Vanden-Eijnden ICLR 2023 framework strongly suggests transport-based regularizers should at-least-match score-based ones; direct evidence for FM-as-encoder-regularizer absent)*

### Feasibility
3/5 🟡 — Velocity-field MLP + time-conditioning + paired sampling from N(0, I). `~60 LoC` reusing the standard CFM training pattern. Each step adds one MLP forward+backward (the velocity field) plus a fresh `randn` draw — `~15 %` step-cost overhead.

### Effort
M 🟡

### Implementation sketch

```python
class FMSIGReg(nn.Module):
    def __init__(self, dim, t_emb_dim=64, hidden=4*dim):
        super().__init__()
        self.t_embed = SinusoidalEmbedding(t_emb_dim)
        self.net = nn.Sequential(
            nn.Linear(dim + t_emb_dim, hidden),
            nn.SiLU(),
            nn.Linear(hidden, dim),
        )
    def forward(self, z):
        B, d = z.shape
        z_0 = z
        z_1 = torch.randn_like(z_0)             # fresh N(0, I)
        t = torch.rand(B, 1, device=z.device)
        eps = torch.randn_like(z_0) * 0.01      # small noise
        z_t = (1 - t) * z_0 + t * z_1 + eps
        t_e = self.t_embed(t.squeeze(-1))
        v = self.net(torch.cat([z_t, t_e], dim=-1))
        u = z_1 - z_0                            # OT-displacement target
        return ((v - u) ** 2).sum(-1).mean()
```

Replace `λ · SIGReg(z)` with `λ · FMSIGReg(z)` in the LeJEPA loss. Same `λ` initial value; expect mild re-tuning.

### Risks

- **FM-SIGReg-loss-non-zero-at-target**: at `P_z = N(0,I)`, `L_FM = E[‖z_1 - z_0‖²]/3` (variance of conditional velocity, NOT 0). The encoder gradient is sensitive only to *changes* in this conditional-variance, not its absolute level. Mitigation: monitor `L_FM` trajectory — it should decrease monotonically to a positive plateau (~`d·σ_target² = 384`); divergence or oscillation indicates problems.
- **Score-FM equivalence trap**: if FM-SIGReg in expectation equals smoothed Hyvärinen score matching (Idea 2), the gain is purely from the *smoothing* and not from a fundamentally different mechanism. **Strong head-to-head with Idea 2 is mandatory.**
- **Velocity-field overfitting**: at small batch size B=512, the velocity field could memorize per-batch transport rather than learning a stable marginal velocity. Mitigation: tied weights across global views (one `v_ψ` for the whole batch); EMA of `v_ψ` parameters during training.
- **Composition with b7-I1 FM-invariance**: clean (different `z_1` targets); could stack as "all-flow LeJEPA". With b7-I2 Hyvärinen: **mutually exclusive** at the SIGReg-term slot. With b7-I3 max-sliced: orthogonal in principle (max-sliced replaces *sampler* on a per-slice test; FM-SIGReg replaces the whole test) — but max-sliced is moot if FM-SIGReg wins (no slicing).

### Falsification test

100-ep ImageNet-10 at ASHA-best (lr, wd, λ), 3 seeds, **5-arm at matched-wall-clock** (matched-WC because the velocity-field adds ~15% step cost):

- **A**: SIGReg-only baseline (Epps–Pulley × M=1024 random slices)
- **B**: Hyvärinen-only (b7-I2 — score-based control)
- **C**: FM-SIGReg-only at `σ_target = 0.01` (OT-displacement path)
- **D**: FM-SIGReg-only at `σ_target = 0.1` (diffusion-style path — tests sensitivity to interpolant noise)
- **E**: 50/50 mix `0.5 · SIGReg + 0.5 · FM-SIGReg` (hedge arm)

**Primary**: best FM-arm (C or D) ≥ baseline-EP + 0.3 pp non-overlap **AND** ≥ Hyvärinen (B) by ≥ 0.2 pp — proves the transport-based mechanism adds value over score-based.

**Parity floor**: any FM-arm ≥ baseline − 0.3 pp (cannot replace SIGReg with a regression).

**Mechanism check 1**: `L_FM` trajectory over training — should monotonically decrease to a plateau around `~d · 1` (the conditional-variance baseline); if it diverges or hits 0 (the velocity collapsed), reject.

**Mechanism check 2**: at end of training, compute the *empirical* `W_2(P_z, N(0,I))` via standard Sinkhorn estimator on a 4096-sample validation batch — should be lower for FM-arm than for baseline-EP arm. If not, FM-SIGReg did not actually push `P_z` to N(0,I) — reject.

### Composition map

| New idea | Composes with cumulative survivor stack |
|----------|----------------------------------------|
| 7. FM-SIGReg | ⚠ Hyvärinen (b7-I2 — same slot, mutually exclusive — A/B mandatory) · ⚠ Max-sliced (b7-I3 — moot under FM-SIGReg since no slicing) · ✓ Sinkhorn (b6 — different axis) · ✓ b7-I1 FM-invariance (orthogonal, compose into "all-flow LeJEPA") · ✓ b5 Saliency · ✓ b5 SIE-split · ✓ b4 SAM · ✓ b3 PIT · ✓ b3 SRHT (moot under FM but not conflicting) · ✓ ASHA · ✓ controller (b6) |

Strongest compose-mode bundle in batch-7: **FM-SIGReg + FM-invariance = "all-flow LeJEPA"** — completely removes both the ECF test and the MSE alignment, replacing both with continuous-time velocity field regression.

### Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 0/0/100 | FM-SIGReg addendum | 2026-05-19 batch-7-idea7`
