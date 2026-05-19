# Idea 6 Vetting — SU(d)-parameterized structured-orthogonal projector (quantum-circuit-inspired)
**Source**: `ideation-output/ImageNet-10/batch-7-idea6-addendum.md` · **Mode**: `--climb-mode` · **Vetted**: 2026-05-19

## Idea snapshot
Replace MLP projector (300k params, non-orthogonal) with a product of `L = O(d log d)` Givens rotations (~3.5k params, exact orthogonal). Quantum-circuit-inspired classical analog (Schuld-Killoran PRL 2019, Havlicek Nature 2019). Cross-domain T3.

Pattern P3 (Replace), Tier 3, Scope enhance-existing.

---

### Stage 1: Problem Framing
**Persona**: Advisor. **Declared**: "Adopting persona: Advisor. Stance: does the framing connect quantum circuits to LeJEPA's linear-probe goal?"

**Attack 1**: "The 'quantum-circuit-inspired' framing is decorative. The actual mechanism is 'parameter-efficient orthogonal projector via Givens rotations' — that's a Dao et al. ICML 2019 butterfly-layer idea. The quantum framing adds zero predictive power for whether it works on Imagenette."

**Steel-manned rebuttal** (Round 1):
> The framing route surfaces a *specific architectural choice* — capacity-bottlenecked AND exactly-orthogonal — that Dao et al. 2019 (butterfly factorizations for compression) treats as a compression target, not as an SSL-projector design principle. The quantum-circuit framing motivates the *structure choice* (rotation-product = SU(d) coverage) which is mechanistically distinct from random butterfly compression. Schuld's 2021 result (arXiv:2101.11020 — PQCs ≡ classical kernel methods) explicitly identifies "feature-map structure, not parameter count" as the source of expressivity — that's the operational hypothesis here: an aggressively-compressed-but-structured projector beats an over-parameterized MLP projector on small data.

**Source**: auto-steelman.

**Persona response** (Round 1): "Framing connects via 'feature-map structure determines expressivity, not param count'. The quantum link is *motivational* rather than load-bearing — but the architectural choice is well-defined. The actual climb-mode contribution is the architecture, not the framing. WEAKENED — framing is admissible but inessential to the empirical question."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡. **Time**: 2 min. **Notes for Stage 8**: idea survives without the quantum framing; the empirical question is "does a small structured-orthogonal projector beat the LeJEPA MLP projector on Imagenette."

---

### Stage 2: Prior Work Attack
**Persona**: Prior-Work Hunter.

**Attack 1**: "Dao et al. ICML 2019 (arXiv:1903.05895) is the direct prior art for butterfly-pattern orthogonal layers in deep networks. Their experimental section covers ImageNet classification with butterfly projection layers, showing 2-3× compression at comparable accuracy. The proposed idea is 'apply Dao's butterfly layer to LeJEPA's projector' — a 1-line substitution."

**Steel-manned rebuttal** (Round 1):
> Dao 2019 evaluated butterfly layers for *fully-supervised* image classification and replaced *the entire fully-connected layers* of a CNN. The present idea uses Givens rotations on the *SSL projector head only*, with explicit *exact orthogonality* constraint (Dao's butterfly is approximately orthogonal under certain initializations but not exactly so). The SSL-projector slot is empty. Furthermore, butterfly factorizations are one *specific* structured-orthogonal family; SU(d) Givens composition is another with different inductive bias (Givens chains favor coordinate-pairwise mixing).

**Source**: auto-steelman.

**Persona response** (Round 1): "Slot is empty (SSL-projector application), mechanism distinction (exact-orthogonal vs approx-orthogonal) is real but narrow. EXTENDS, not DUPLICATE. WEAKENED."

**Status after Round 1**: ⚠️ WEAKENED.

**Additional attack**: "Householder reflections / Orthogonal-RNN literature (Vorontsov et al. ICML 2017, arXiv:1701.09175) covers parameterized orthogonal layers via products of reflections. Same family." — Status: ⚠️ WEAKENED, no rebuttal cycle (same family argument as Dao; mitigation identical).

**Rebuttal-cycle summary**: DEFLECTED 0, WEAKENED 1, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN. **Confidence**: 🟢. **Notes**: Mechanism is well-known in DL; slot-application is the delta.

---

### Stage 3: Novelty Decomposition
**Persona**: Critical Reviewer.

**Attack 1**: "Mechanism = Givens rotation composition (textbook). Application = SSL projector. Synthesis = 1 substitution. Same novelty grade as Idea 4 — narrow, single-paragraph contribution."

**Steel-manned rebuttal** (Round 1):
> Climb-mode does not require novelty grandeur. The cost is `~80 LoC`, the experiment is a clean 3-arm at matched WC, and the result (whether structured-orthogonal beats MLP) is informative whichever way it goes. Closes a corner the LeJEPA paper explicitly flagged (projector over-parameterization).

**Source**: auto-steelman.

**Persona response** (Round 1): "Climb-mode-admissible. The 'closing an LeJEPA-flagged corner' framing strengthens the contribution. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 4: Theory Grounding (lite)
**Persona**: Theorist.

**Attack 1**: "Vanishing gradients through long rotation chains (L > 10·d) are documented in Helfrich et al. 2018 (Orthogonal RNNs). With L = 2d log d ≈ 4500 rotations for d=384, every parameter receives gradient through ~4500 nested `cos/sin` — chain-rule shrinkage will kill training."

**Steel-manned rebuttal** (Round 1):
> Helfrich et al. found vanishing gradient *for recurrent* orthogonal nets where the same orthogonal matrix is applied at every time step (so depth = sequence length × rotation count). In the present setting, the rotation product is applied *once* per forward pass with `L = O(d log d)` total rotations — the *effective depth* is just `O(d log d) ≈ 4500` linear operations. Modern optimizers (AdamW with proper LR scaling) handle this routinely (compare: ViT-L has ~100 transformer blocks × 4 matmuls = 400-depth and trains fine). The vanishing-gradient concern at depth-4500 of *linear* ops is empirically mild; the real concern is at non-linearities, of which there are zero.

**Source**: auto-steelman.

**Persona response** (Round 1): "Linear-only depth-4500 is mild. But the `cos/sin` nonlinearities at each `θ_l` *do* add small curvature; the 'no nonlinearities' claim is imprecise. WEAKENED — survivable but not fully rebutted."

**Status after Round 1**: ⚠️ WEAKENED.

**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 5: Feasibility Analysis
**Persona**: Pragmatic PM.

**Attack 1**: "Naive Givens rotation in PyTorch with per-rotation `cos/sin` and in-place index updates is SLOW. The forward pass needs `L = 4500` sequential operations vs MLP's 2 matmuls. Even if each op is `O(1)`, the kernel launch overhead at L=4500 on GPU is a 50-100× slowdown vs MLP. Not feasible at 4 GPU-h budget."

**Steel-manned rebuttal** (Round 1):
> The butterfly pattern is *parallelizable*: at each "level" of the butterfly, `d/2` Givens rotations act on disjoint coordinate pairs and can be applied simultaneously as a single GPU operation. The total *sequential* depth is `O(log d) ≈ 9` levels, not L=4500. Per-forward time is `O(log d · batch_size · d)` — comparable to a single matmul. The cost is `~5-10%` overhead vs MLP, not 50×.

**Source**: auto-steelman.

**Persona response** (Round 1): "Butterfly-pattern parallelization is the right answer. DEFLECTED on feasibility. **However** — this depends on a *vectorized* butterfly implementation, not the naive sketch in the idea's §Implementation sketch (which uses Python-loop per-rotation). The implementation needs to follow Dao 2019's butterfly kernel."

**Status after Round 1**: ✅ DEFLECTED (with implementation note).

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 6: Killer Baseline
**Persona**: Skeptical Empiricist.

**Attack 1**: "The killer baseline is **'MLP projector with explicit weight-decay regularization'** — if the over-parameterization concern is real, weight decay on the projector should already fix it. A 3-arm experiment must include `MLP-with-wd=0.5` and `MLP-with-wd=0.05` (baseline) as controls. If `MLP-with-strong-wd` matches structured-rotation, the structure is decorative and weight decay was sufficient."

**Steel-manned rebuttal** (Round 1):
> Weight decay shrinks weights *toward zero*, not *toward orthogonality*. The two regularizations have different effects: weight-decay produces a small-norm MLP with no orthogonality guarantee; structured rotation produces an exactly-orthogonal layer of bounded norm. The empirical question is whether the *orthogonality-specifically* (vs general small-norm-MLP) is the load-bearing property. Adding `MLP-strong-wd` as a 4th control is reasonable — but a structured-rotation win over even strong-wd MLP would be the cleanest evidence for the orthogonality hypothesis.

**Source**: auto-steelman.

**Persona response** (Round 1): "Adding `MLP-strong-wd` as a 4th control is mandatory. As proposed (3 arms only), the experiment cannot distinguish 'capacity bottleneck' from 'orthogonality'. WEAKENED — needs experimental redesign."

**Status after Round 1**: ⚠️ WEAKENED.

**Attack 2**: "The LeJEPA paper §5.2 (ablation table) reports that *removing the projector entirely* (using encoder output directly) loses only ~1 pp on Imagenette. If the projector contributes only 1 pp, then a 'better projector' can win at most 0.5 pp — within seed-variance noise (σ ~0.5 pp). The expected gain estimate `+0.1 / +0.4 / +1.0 pp` is in the noise regime."

**Steel-manned rebuttal** (Round 1):
> If the projector contribution is small in absolute terms, then the matched-WC budget for testing this is also small — running 3 seeds at 100 ep ImageNet-10 is ~6 GPU-h, low-stakes. The downside of the test is bounded; the upside (a `+0.5 pp` confirmation that small-projector helps small-data SSL) is informative regardless. Furthermore, the "remove-projector" ablation is an extreme: the structured-rotation projector tests the *middle* hypothesis (orthogonal-but-non-identity is better than both extremes).

**Source**: auto-steelman.

**Persona response** (Round 1): "Noise-regime concern is real — the 0.5 pp σ on Imagenette means the test may produce 'indistinguishable' results regardless of which projector wins. WEAKENED."

**Status after Round 1**: ⚠️ WEAKENED.

**Rebuttal-cycle summary**: DEFLECTED 0, WEAKENED 2, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN (2 WEAKENED — cannot exceed WARN per UNREBUTTED-downgrade rule). **Confidence**: 🟡.

---

### Stage 7: Reviewer Simulation
**Skipped** per `--climb-mode`.

---

### Stage 8: Decision Gate
**Verdict summary**: S1 WARN · S2 WARN · S3 PASS · S4 WARN · S5 PASS · S6 WARN — **0 FAIL + 4 WARN**.

**Rule fired**: Rule #5 (`0 FAIL + 3-4 WARN → TOY`).

**Verdict**: 🧪 **TOY EXPERIMENT FIRST**. **Confidence**: 🟡.

**Justification**: Idea is mechanically sound and inexpensive; the quantum framing is decorative-but-not-load-bearing (Stage 1 WEAKENED); the prior art (Dao butterfly, Householder OrthRNN) makes the synthesis incremental (Stage 2 WEAKENED); the Stage 6 noise-regime concern is real (signal may be in seed-variance). TOY with a 4-arm experimental design (must include `MLP-strong-wd` control) is the right call.

---

## Toy Experiment Design

**Idea being toyed**: SU(d)-structured-orthogonal projector vs MLP projector.
**Triggered by**: Stage 6 noise-regime concern + Stage 6 capacity-vs-orthogonality control concern.

### Setup
- **Dataset**: ImageNet-10 (Imagenette).
- **Model**: ViT-S/16 + LeJEPA; projector head varies across 4 arms.
- **Arms (mandatory 4)**:
  - **A**: baseline MLP projector (wd=0.05, LeJEPA default)
  - **B**: MLP projector with strong weight decay (wd=0.5) — disambiguates capacity-bottleneck from orthogonality
  - **C**: structured-rotation `L = 2d = 768` rotations
  - **D**: structured-rotation `L = 2d log d ≈ 4600` rotations
- **Config**: 100 ep, ASHA-best (lr, wd, λ), 3 seeds each.
- **Implementation requirement**: vectorized butterfly pattern (per Stage 5 note); not naive Python loop.
- **Budget**: 4 arms × 3 seeds × 100 ep × ~1 GPU-h/run = **12 GPU-h**.
- **Wallclock**: 4 hr on 3 GPUs in parallel.

### Success criterion
- **Primary**: best structured arm (C or D) ≥ baseline (A) + 0.4 pp non-overlap AND > MLP-strong-wd (B) by ≥ 0.3 pp — proves the structure-vs-capacity distinction.
- **Parity floor**: structured arm ≥ baseline − 0.3 pp (can replace MLP without regression).
- **Cost floor**: structured-arm wall-clock ≤ baseline × 1.10 (vectorized butterfly).

### Confound check
3-seed baseline ARM (A) IS the noise estimate; σ ~ 0.5 pp known from prior batches.

### Falsification thresholds
| Observation | Action |
|-------------|--------|
| Structured arms ≤ baseline − 0.3 pp | KILL (structured projector hurts) |
| MLP-strong-wd (B) ≈ Structured (C/D) within ±0.3 pp | REFRAME — "use weight decay" is the simpler fix; structure is decorative |
| Structured (C/D) > baseline + 0.4 pp AND > MLP-strong-wd by ≥ 0.3 pp | **FULL SEND** as new LeJEPA projector default |
| All 4 arms within ±0.3 pp | NOISE — re-run at 600 ep (full schedule); if still indistinguishable → KILL |
| Wall-clock overhead > 25 % vs baseline | REFRAME — vectorization is broken; fix kernel |

### Estimated cost
12 GPU-h.

### Estimated time
4 hr wall-clock (3 GPUs parallel).

### Re-vet trigger
`/vet-ideas --given-toy ./structured-projector-results.md idea-6-batch-7`.

### Salvageable / Resurrection-eligible
Yes / Yes.

---

## Notes for the batch summary

This idea adds:
- **Toy queue entry** at 12 GPU-h (priority slot 3-4 of batch-7 toys; cheaper than Idea 3-B max-sliced at 15 GPU-h but pricier than Idea 2-B Hyvärinen at 6 GPU-h).
- **Composition tie-in** with Idea 3 (max-sliced) of batch-7: combined "lean SIGReg + lean projector" stack would free compute for ~30 % more effective epochs at the same budget — interesting compose-mode target.
- **No interaction risk** with surviving stack EXCEPT batch-6 Poincaré TOY (same projector axis — head-to-head only).
