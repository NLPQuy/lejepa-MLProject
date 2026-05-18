# Idea 5 Vetting — Poincaré-ball hyperbolic projector head
**Batch**: 6 · **Date**: 2026-05-18 · **Mode**: --climb-mode
**Pattern**: P2 (Transfer) · **Tier**: 3 · **Source**: ideation batch-6 Idea 5

## Stage 1 — Problem Framing
> Adopting persona: `Advisor`.

**Attack 1.1**: "Imagenette has 10 classes in 2 super-clusters (animal / manmade-vehicle / instrument). Hierarchy depth = 2. Hyperbolic embeddings shine at depth ≥ 4–6 (Nickel-Kiela's WordNet had depth ~16). On a depth-2 hierarchy, Euclidean and hyperbolic have indistinguishable representation capacity."
- Steel-manned rebuttal: True — gain is bounded. Mid +0.7 pp may be optimistic. But the *real* test is whether the implicit class-substructure (within "manmade", there's "cassette" / "garbage truck" / "gas pump" — different shape geometries; within "animal", "tench" / "English springer" / "French horn") has unmeasured depth that Euclidean buries. **The right move is to pre-flight the hierarchy depth before committing.**
- Persona verdict: ⚠️ WEAKENED — Stage 5 needs an in-line cheap pre-flight measurement.

**Verdict**: PASS-with-pre-flight.

## Stage 2 — Prior Work Attack
> Adopting persona: `Prior-Work Hunter`.

**Attack 2.1**: "Surís et al. *Learning the Predictability of the Future* CVPR 2021, Ge et al. *Hyperbolic Contrastive Learning* CVPR 2023, Atigh et al. *Hyperbolic Image Segmentation* CVPR 2022 — hyperbolic vision SSL is **not novel**. All show small or context-dependent gains."
- Steel-manned rebuttal: Hyperbolic *SSL* has been tried. The proposal's novelty is the *interaction with SIGReg* — keeping SIGReg on the tangent space while applying hyperbolic distance for invariance is a specific combination not in prior art. But that combination is also a *small* mechanism change.
- Persona verdict: ⚠️ WEAKENED — narrow novelty. Combined with shallow hierarchy concern, expected gain shrinks toward the low end (+0.2 pp).

**Verdict**: PASS (no hard duplicate; narrow novelty).

## Stage 3 — Novelty Decomposition
EXTENDS (Nickel-Kiela embedding + Ganea hyperbolic ops + tangent-space SIGReg combo). The combo is the only novel piece.

## Stage 4 — Theory Grounding (lite)
**Attack 4.1**: "exp_0(v) is a diffeomorphism on R^d, so SIGReg on v is *equivalent* to SIGReg on the push-forward wrapped-normal on the ball. But the linear probe sees `p` (the ball point), not `v` — so the linear-probe-relevant geometry is hyperbolic. Linear probes are *linear in Euclidean space*; on hyperbolic data they are systematically biased. The proposal says 'log_0 back to tangent for probe input' — but log_0(exp_0(v)) = v, so the probe sees the *same v* as a Euclidean projector would. **The hyperbolic structure is decorative — the probe doesn't see it.**"
- Steel-manned rebuttal: If `L_inv` uses `d_H(p^v1, p^v2)` (hyperbolic distance), the gradient w.r.t. encoder parameters is different from the gradient from Euclidean L². So even though the linear probe sees `v`, `v` is shaped differently by training. The encoder learns to put hierarchy-related axes near the Poincaré boundary (where hyperbolic distance amplifies them) — this *does* affect downstream.
- Persona verdict: ⚠️ WEAKENED — the gradient-shape argument is real but the magnitude is unclear; published hyperbolic-SSL gains are typically 0.5 pp at best on shallow-hierarchy data.

**Verdict**: WARN.

## Stage 5 — Feasibility
`geoopt` is mature. Numerical stability near boundary is a real but manageable risk. **PASS** with M-effort.

## Stage 6 — Killer Baseline
**Attack 6.1**: "Killer baseline = Euclidean projector at matched capacity. 2-arm: Euclidean / Poincaré at c=1.0. Pre-flight: measure super-cluster-vs-within ratio on the baseline Euclidean embedding. If ≤ 1.3, hyperbolic adds nothing — KILL pre-emptively without spending the 25 GPU-h."
- Steel-manned rebuttal: This pre-flight is fast (~1 hr CPU on a saved baseline checkpoint) and decisive. Adopt as Phase A.
- Persona verdict: ✅ DEFLECTED via Phase A pre-flight.

**Verdict**: PASS-with-Phase-A.

## Stage 8 — Decision Gate
Stages: 1 PASS-w/-preflight / 2 PASS / 3 WARN / 4 WARN / 5 PASS / 6 PASS-w/-PhaseA. **2 WARN, 0 FAIL → FULL SEND** technically, but **two prior-art / narrow-novelty WEAKENED + shallow-hierarchy concern + small expected gain** → downgrade to **TOY** (which the Phase A pre-flight basically already is).

**Verdict**: 🧪 **TOY** · Confidence 🟡

### Toy Experiment Design
- **Phase A (free, 1 hr CPU)**: on any saved baseline LeJEPA checkpoint (e.g., from ASHA), compute the super-cluster-vs-within class-mean distance ratio in **Euclidean** projector output. Decision: if ratio ≥ 1.5 → fire Phase B (real hyperbolic-vs-Euclidean A/B); if 1.3 ≤ ratio < 1.5 → defer to lowest-priority TOY; if ratio < 1.3 → KILL idea (Imagenette hierarchy too shallow).
- **Phase B (~25 GPU-h, gated)**: 100-ep ImageNet-10, 2-arm: Euclidean baseline / Poincaré (c=1.0). 3 seeds. Decision: hyperbolic arm ≥ 0.4 pp non-overlap AND super-cluster ratio in hyperbolic representation ≥ 1.5× Euclidean → FULL SEND; else KILL.
- **Dependency**: ASHA Step-0 (provides a baseline checkpoint for the ratio measurement). Order **last** in the batch-6 queue.
