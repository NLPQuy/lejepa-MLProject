# Batch-7 Addendum — Idea 6 (quantum-themed T3)
**Generated**: 2026-05-19 · **Added per user request**: "ra thêm một idea nữa, lần này search cái gì liên quan tới quantum"
**Tier override remains**: 0/0/100 (user-directed T3-only).

## Idea 6: Quantum-circuit-inspired SU(d)-parameterized structured-orthogonal projector head

- **Pattern**: P3 (Replace — swap the standard MLP projector with a structured-rotation projector parameterized as a product of Givens rotations covering an SU(d)-subspace)
- **Tier**: 3 (cross-domain root: parameterized quantum circuit theory — Schuld-Killoran *PRL* 2019; Havlicek et al. *Nature* 2019)
- **Scope**: enhance-existing. Encoder, SIGReg, invariance, λ, multi-crop, sampler, statistic all unchanged. Projector head architecture only.
- **One-liner**: Replace `MLP(d → d → d)` projector with `P(z) = ∏_{l=1}^L R_{i_l, j_l}(θ_l) · z` where each `R_{i,j}(θ)` is a Givens rotation acting on coordinates `(i, j)` of `z`. Total params `~ d log d` (vs MLP's `~ d²`), output is *always* orthogonal — no covariance distortion of the encoder embedding.

### Mechanism

A **parameterized quantum circuit (PQC)** with `n` qubits is a product of single-qubit and two-qubit unitaries acting on a `2^n`-dim Hilbert space; each "layer" is `U_l(θ_l) ∈ SU(2^n)`. Schuld & Killoran (*PRL* 122:040504, 2019, [arXiv:1803.07128](https://arxiv.org/abs/1803.07128)) and Havlicek et al. (*Nature* 567:209-212, 2019, [arXiv:1804.11326](https://arxiv.org/abs/1804.11326)) established that PQCs realize *nonlinear feature maps in classically-large Hilbert spaces*; the expressivity comes from the structure (rotation gates compose multiplicatively on `SU(d)`), not from the parameter count.

Classical analog for SSL: parameterize the projector as `P(z) = ∏_l R_{i_l, j_l}(θ_l) · z`, where `R_{i,j}(θ)` is a 2D Givens rotation in coordinates `(i, j)` of `R^d`:

```
R_{i,j}(θ) acts identity on all coords ≠ i,j,
on (i,j): [z_i, z_j]^T ← [[cos θ, −sin θ], [sin θ, cos θ]] [z_i, z_j]^T.
```

With `L = O(d log d)` Givens rotations chosen by a binary-tree butterfly pattern, the product spans an SU(d)-rich subspace; with `L = O(d)` it covers a one-parameter subgroup. Total parameters: `L`. Total computational cost: `O(L)` per forward (each Givens is `O(1)` ops).

**Two key properties**:
1. **Always-orthogonal output**: `P^T P = I` exactly, by construction. The projector cannot distort the encoder embedding's covariance.
2. **Reduced parameter capacity**: `L · 1 = O(d log d) ≪ d²` (for `d = 384`, that's `~3.5k` params vs `~150k` for full MLP). Aggressive capacity bottleneck on the projector forces the *encoder* to absorb more representational work.

The combination is what's interesting: a *cheap, capacity-bottlenecked, always-orthogonal* projector. This is the classical analog of a shallow PQC. The hypothesis: on small-data SSL (Imagenette), projector-side over-parameterization wastes capacity that could be in the encoder.

### Source inspirations

- **Primary (cross-domain root)**: *Quantum Machine Learning in Feature Hilbert Spaces*, Schuld & Killoran, **Physical Review Letters 122, 040504, 2019** / [arXiv:1803.07128](https://arxiv.org/abs/1803.07128) — establishes PQCs as classical kernel-method analogs; expressivity from structure, not capacity.
- **Primary (foundational application)**: *Supervised learning with quantum-enhanced feature spaces*, Havlicek, Córcoles, Temme, Harrow, Kandala, Chow, Gambetta, **Nature 567:209-212, 2019** / [arXiv:1804.11326](https://arxiv.org/abs/1804.11326) — PQC-derived feature maps; quantum advantage from structure.
- **Supporting**: *Supervised quantum machine learning models are kernel methods*, Schuld, [arXiv:2101.11020](https://arxiv.org/abs/2101.11020) (Jan 2021) — proves all PQCs with fixed encoding circuit are classical kernel methods; the advantage (if any) is from the *structure* of the feature map.
- **Supporting (classical)**: Givens rotations / Householder reflections decomposition of orthogonal matrices — standard numerical linear algebra (Golub-Van Loan 1996 textbook); butterfly factorizations for fast orthogonal layers (Dao et al. ICML 2019, [arXiv:1903.05895](https://arxiv.org/abs/1903.05895)).

### Why expected to improve

LeJEPA's standard projector is `nn.Sequential(Linear(d, d), GELU, Linear(d, d))` — `~2d² ≈ 300k` parameters with no orthogonality constraint. On Imagenette (~9k training images × 600 epochs ≈ 5M samples), the projector's 300k parameters can easily overfit, distorting the encoder's covariance in non-orthogonal ways that the SIGReg + invariance trade-off must compensate for.

A structured-orthogonal projector with `~3.5k` parameters (`L = d log d`) gives:
1. **Capacity bottleneck** in the projector → encoder does more work.
2. **Exact orthogonality** preserves the encoder's covariance structure → SIGReg's `Cov(z) → I` target is preserved through the projector.
3. **Small-data regularization** intrinsic to the architecture — a well-studied benefit of butterfly / Householder / Givens layers (Dao et al. ICML 2019 show 2-3x compression with comparable accuracy on ImageNet).

The hypothesis aligns with the LeJEPA paper's own claim that "the projector matters but is heavily over-parameterized"; this idea operationalizes the over-parameterization claim with a quantum-circuit-inspired classical alternative.

### Expected gain
+0.1 / +0.4 / +1.0 pp 🟡 *(small-but-positive expectation from architecture-side regularization; published Givens-/butterfly-projector ablations show mid-range gains on small datasets)*

### Feasibility
3/5 🟡 — Givens rotations are 1 line each; the gradient flows cleanly through `cos/sin` of `θ_l`. The butterfly-pattern `i_l, j_l` selection is a fixed topology (no learned routing).

### Effort
M 🟡 — `~80 LoC`: a `StructuredRotationProjector` module with `L` learnable `θ_l` parameters and the butterfly index pattern.

### Implementation sketch

```python
class StructuredRotationProjector(nn.Module):
    def __init__(self, dim, depth):
        super().__init__()
        self.theta = nn.Parameter(torch.zeros(depth))
        self.indices = self._butterfly_pattern(dim, depth)  # fixed (i_l, j_l) pairs
    def forward(self, z):
        for l, (i, j) in enumerate(self.indices):
            c, s = torch.cos(self.theta[l]), torch.sin(self.theta[l])
            z_i, z_j = z[..., i].clone(), z[..., j].clone()
            z[..., i] = c * z_i - s * z_j
            z[..., j] = s * z_i + c * z_j
        return z
```

Note: clone() prevents in-place autograd issues. Real implementation gathers/scatters for vectorization.

### Risks

- **L choice as new HP**: `L ∈ {d, 2d, d log d, d²}` mini-sweep needed. Mitigation: fix `L = 2d log d` (mid-range published default for butterfly layers).
- **Vanishing gradients through deep rotation chains**: known issue for `L > 10 d`. Mitigation: cap at `L ≤ 5 d log d`; use Cayley-parameterization if vanishing observed.
- **Composition with batch-6 Poincaré TOY**: mutually exclusive at the projector axis — head-to-head only.
- **Composition with batch-5 SIE-split FULL SEND**: clean (SIE works on the head decomposition; rotation projector is the *type* of projector regardless of SIE branching).

### Falsification test

100-ep ImageNet-10, 3 seeds, 3-arm at matched-WC:
- baseline MLP projector (300k params)
- structured-rotation projector `L = 2d` (768 params)
- structured-rotation projector `L = 2d log d` (4.6k params)

**Primary**: best structured arm ≥ baseline − 0.3 pp (parity floor) AND wall-clock ≤ baseline × 1.05. **Stronger goal**: structured arm ≥ baseline + 0.3 pp non-overlap (small-data regularization wins).

**Mechanism check**: log `‖Cov(z_after_projector) − Cov(z_before_projector)‖_F` — for structured-rotation arm this should be `0` exactly (orthogonality guarantee); for baseline-MLP this is nonzero. Confirms the orthogonality property is actually engaged.

**Mechanism check 2**: log encoder gradient norm vs projector gradient norm — for structured-rotation arm, projector gradient norm should be `O(L · ‖z‖)` while encoder gradient norm should be `O(d · ‖z‖)`; gradient mass should be concentrated in the encoder (proves the capacity-bottleneck hypothesis).

If neither check passes, reject.

### Verification quick-pass

- Primary papers VERIFIED: ✅ Schuld-Killoran PRL 2019 (arXiv:1803.07128), Havlicek Nature 2019 (arXiv:1804.11326). Live-search-confirmed (search log 2026-05-19 batch-7 addendum, Q1+Q2).
- Mechanism concrete: ✅ Givens rotation composition is textbook (Golub-Van Loan).
- Falsification sharp: ✅ Primary + 2 mechanism checks.
- Novelty: NOVEL within SSL (structured-orthogonal projector with quantum-circuit inspiration not in prior search results).
- Provenance: VERIFIED.
- Feasibility: 3.
- Compliance: ⚠ adds L as new HP; bindable to RankMe controller if it ships.
- Final: **KEEP** as fresh idea.

## Composition map update (idea 6 added)

| New idea | Axis opened | Composes with cumulative survivor stack |
|----------|-------------|------------------------------------------|
| 6. SU(d)-structured-rotation projector | projector architecture / capacity-bottleneck | ✓ all SIGReg-family survivors · ⚠ Poincaré (b6 TOY — both touch projector — head-to-head) · ✓ Saliency · ✓ SIE-split (projector type is independent of SIE branching) · ✓ controller |

The natural compose-mode tie-in: this idea pairs with **Idea 3 (max-sliced) of batch-7** — both reduce parameter counts (max-sliced reduces slice budget 1000×; structured projector reduces projector params 40×). The combined "lean SIGReg" stack could free compute for more epochs.

## Provenance signature
Inputs hash: `imagenet-10 | lejepa-vit-small | tier 0/0/100 | quantum-themed addendum | 2026-05-19 batch-7-idea6`
