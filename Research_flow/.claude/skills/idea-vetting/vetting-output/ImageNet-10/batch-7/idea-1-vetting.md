# Idea 1 Vetting — Flow-matching invariance (continuous-time velocity field)
**Source**: `ideation-output/ImageNet-10/batch-7.md` · **Mode**: `--climb-mode` · **Vetted**: 2026-05-19

## Idea snapshot
Replace per-pair MSE invariance with conditional flow matching (Lipman ICLR 2023): train velocity field `v_ψ(z, t)` to regress OT-displacement target `z_1 − z_0`. Aligns view distributions distribution-wise rather than per-sample.

Pattern P3 (Replace), Tier 3, Scope enhance-existing. Composite 1.91.

---

### Stage 1: Problem Framing
**Persona**: Advisor. **Persona declared**: "Adopting persona: Advisor. Stance: framing must match Imagenette linear-probe goal."
**Attacks issued**: 1; **with full rebuttal cycle**: 1.

**Attack 1**: "Flow matching is a generative-modeling technique (Lipman ICLR 2023 trains a generator). The idea author claims it as an *invariance* replacement, but generation ≠ alignment. Why would learning `v_ψ` that transports `P_{view-1} → P_{view-2}` produce useful frozen-encoder probe features?"

**Steel-manned rebuttal** (Round 1):
> The CFM theorem (Lipman §3) proves that regressing the conditional velocity `u_t(z|z_0, z_1) = z_1 − z_0` is equivalent to learning the marginal velocity that transports `P_0` to `P_1`. In SSL, "the encoder produces a stable embedding under augmentations" ≡ "the distribution of view-1 embeddings equals the distribution of view-2 embeddings". Flow matching gives a soft, distributional version of this requirement; per-pair MSE is the degenerate `t→0, σ→0` limit of CFM. Direct evidence: arXiv:2512.19729 (Dec 2025, FlowFM) reports linear-probe gains on standard recognition benchmarks when SSL representation is trained jointly with a CFM head.

**Source**: auto-steelman.

**Persona response** (Round 1):
> FlowFM reports gains on probe → the framing is at least empirically defensible. But FlowFM *jointly trains a generator* — the gain may come from the auxiliary generative loss adding gradient signal, not from the "distributional alignment is softer than MSE" claim. The framing-attack DEFLECTS on existence-of-published-SSL-FM but WEAKENS on causality-of-the-claimed-mechanism. Acceptable for in-domain probe target.

**Status after Round 1**: ⚠️ WEAKENED

**Rebuttal-cycle summary**: DEFLECTED 0, WEAKENED 1, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN (1 WEAKENED → demote PASS→WARN).
**Confidence**: 🟡. **Time**: 2 min. **Notes for Stage 8**: Framing is at the same axis as Sinkhorn TOY; head-to-head mandatory.

---

### Stage 2: Prior Work Attack
**Persona**: Prior-Work Hunter. **Persona declared**: "Adopting persona: Prior-Work Hunter. Stance: dig until I find the prior art that buries this."
**Attacks issued**: 2; **with full rebuttal cycle**: 1.

**Attack 1**: "arXiv:2512.19729 (FlowFM, Dec 2025) is exactly this idea: joint CFM + SSL on the embedding. The delta is so small it's a duplicate."

**Steel-manned rebuttal** (Round 1):
> FlowFM jointly trains a representation encoder AND a generative head, optimizing a *combined* recognition + generation objective. The present idea uses CFM **purely as an invariance-loss replacement** — no generative output target, no generator head, no sampling at inference. The mathematical object is the same (CFM regression) but the application slot (alignment vs joint-generation) is different. FlowFM's gains are reported on recognition; we cannot disentangle from their setup how much comes from CFM-as-alignment vs CFM-as-generative-auxiliary. The present idea isolates the alignment-axis effect.

**Source**: auto-steelman.

**Persona response** (Round 1):
> The distinction is real but weak: FlowFM still establishes that CFM-trained SSL representation gives probe gains. The delta is a clean isolation study, valuable but incremental. EXTENDS, not DUPLICATE. WEAKENED.

**Status after Round 1**: ⚠️ WEAKENED.

**Additional attack**: "Sinkhorn invariance (batch-6 Idea 4, currently TOY) occupies the same alignment-axis slot. If Sinkhorn passes Phase A this idea is redundant." — Status: ⚠️ WEAKENED, no rebuttal cycle (budget exhausted; covered by Stage 6).

**Rebuttal-cycle summary**: DEFLECTED 0, WEAKENED 1, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN.
**Confidence**: 🟡. **Notes**: FlowFM = primary related work, isolation-study angle is the delta.

---

### Stage 3: Novelty Decomposition
**Persona**: Critical Reviewer.
**Attacks issued**: 1; **full rebuttal**: 1.

**Attack 1**: "Mechanism axis: 'CFM regression' — Lipman 2023. Application axis: 'SSL invariance' — FlowFM. Synthesis axis: 'CFM as standalone invariance' — narrow. Defensibility = workshop, not A*."

**Steel-manned rebuttal** (Round 1):
> Climb-mode does not require A*-defensibility; it requires *benchmark gain*. The mechanism is well-established (Lipman 2023), the application is empirically validated (FlowFM Dec 2025), and the isolation slot gives a clean ablation. A 1.5 pp lift on ImageNet-10 linear probe is the climb-mode goal, not a NeurIPS submission.

**Source**: auto-steelman.

**Persona response** (Round 1): "Climb-mode framing accepted. Novelty is narrow but the empirical question is honest. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Rebuttal-cycle summary**: DEFLECTED 1, WEAKENED 0, UNREBUTTED 0.
**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 4: Theory Grounding (lite — `--climb-mode`)
**Persona**: Theorist.
**Attacks issued**: 1; **full rebuttal**: 1.

**Attack 1**: "CFM theorem (Lipman §3) gives convergence to the marginal velocity field — but only under iid samples from `P_0` and `P_1`. In multi-crop SSL, `z_0` and `z_1` are *coupled* (same image), so `P_0` and `P_1` are not free marginals but a joint. The CFM marginal-equivalence theorem does not apply."

**Steel-manned rebuttal** (Round 1):
> CFM applies to *any* coupling `π(z_0, z_1)` between source and target; the conditional path `p_t(z|z_0, z_1)` is conditioned on the pair, not on the marginals. With the iid-pair coupling = the SSL-augmentation pair, the conditional velocity `u_t = z_1 − z_0` is *exactly* the right target by construction. The marginal-equivalence is a *bonus* property, not a requirement. The loss is `0` iff `v_ψ` correctly captures the per-pair conditional velocity — which is the actual training signal.

**Source**: auto-steelman.

**Persona response** (Round 1): "The conditional-coupling argument is correct; per-pair regression is identifiable. But the *interpretation* as 'distributional invariance softer than MSE' becomes weak — with the per-pair coupling, CFM ≈ MSE regression in a time-aware embedding, not a genuine distribution-vs-distribution loss. WEAKENED — the mechanism story degrades."

**Status after Round 1**: ⚠️ WEAKENED.

**Rebuttal-cycle summary**: DEFLECTED 0, WEAKENED 1, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN (lite-stage demotion to WARN). **Confidence**: 🟡.

---

### Stage 5: Feasibility Analysis
**Persona**: Pragmatic PM.
**Attacks issued**: 1; **full rebuttal**: 1.

**Attack 1**: "Per-step +20% wall-clock from velocity field forward+backward. At 600 epochs that's +120 ep equivalent. Matched-WC budget eats most of the claimed gain."

**Steel-manned rebuttal** (Round 1):
> The matched-WC falsification protocol explicitly accounts for this. If FM-arm is +20% slower per step, the matched-WC arm runs ~500 effective epochs vs baseline's 600 — and the experiment design (Idea 1 §Falsification) requires the FM-arm to *still* beat baseline. If the mechanism doesn't survive the WC penalty, the falsification rejects. The cost is built into the test.

**Source**: auto-steelman.

**Persona response** (Round 1): "Falsification design is sound. Feasibility passes. DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Stage verdict**: ✅ PASS. **Confidence**: 🟢.

---

### Stage 6: Killer Baseline
**Persona**: Skeptical Empiricist.
**Attacks issued**: 2; **full rebuttal**: 2.

**Attack 1**: "Sinkhorn invariance (batch-6 Idea 4, currently TOY → FULL SEND-eligible on Phase A pass) is the killer baseline. It occupies the exact same alignment-axis slot, with published SSL evidence (SinSim Feb 2025). If Sinkhorn passes its Phase A, this idea has no slot."

**Steel-manned rebuttal** (Round 1):
> The 3-arm bake-off `baseline-MSE / Sinkhorn / Flow-matching` is the test. Stacking is mutually exclusive — A/B is the right protocol, not killing one in favor of the other a priori. Mechanism distinctions: Sinkhorn solves a single static OT problem per batch (single transport plan); FM learns a continuous vector field with time-conditioned regression. Sinkhorn's failure mode is permutation-degeneracy; FM's failure mode is velocity-field underfit. Different gradients, different inductive biases. *Which* wins is an empirical question, not a Stage-6 kill.

**Source**: auto-steelman.

**Persona response** (Round 1): "The 3-arm bake-off framing is fair. But Sinkhorn ships first (b6 TOY → Phase A scheduled), and any FM-vs-Sinkhorn delta has to be measured *after* Sinkhorn's verdict is known. FM is at best a 'second arm' in the alignment-axis bake-off — not a killer-baseline FAIL, but a sequencing dependency. WEAKENED."

**Status after Round 1**: ⚠️ WEAKENED.

**Attack 2**: "Baseline MSE per-pair invariance is the simplest possible alignment. If FM beats MSE by < 0.4 pp the idea is statistically indistinguishable from variance noise (σ ~0.5 pp on small-data SSL); the 'softer alignment' story does not survive."

**Steel-manned rebuttal** (Round 1):
> The falsification threshold of ≥ 0.4 pp non-overlap is exactly this guard. If FM-only achieves < 0.4 pp lift the test rejects. The mechanism check (flow divergence near 0 for incompressible flow) catches the case where the velocity learns a trivial transport.

**Source**: auto-steelman.

**Persona response** (Round 1): "Sharp falsification — DEFLECTED."

**Status after Round 1**: ✅ DEFLECTED.

**Rebuttal-cycle summary**: DEFLECTED 1, WEAKENED 1, UNREBUTTED 0.
**Stage verdict**: ⚠️ WARN. **Confidence**: 🟡.

---

### Stage 7: Reviewer Simulation
**Skipped** per `--climb-mode`.

---

### Stage 8: Decision Gate
**Persona**: Advisor (PI mode). **Persona declared**: "Adopting persona: PI. Stance: synthesize Stages 1–6 against the climb-mode goal."

**Stage verdict summary**: S1 WARN · S2 WARN · S3 PASS · S4 WARN · S5 PASS · S6 WARN — **0 FAIL + 4 WARN**.

**Rule fired**: Rule #5 (`0 FAIL + 3-4 WARN → TOY`). The repeated WARNs cluster on the *same uncertainty*: Sinkhorn (b6 TOY) is at the same alignment-axis slot with closer published SSL evidence; FM's delta is a within-axis isolation question. The mechanism story is genuine but degraded after Stage 4's coupling-argument WEAKEN.

**Verdict**: 🧪 **TOY EXPERIMENT FIRST**. **Confidence**: 🟡.

**Justification**: Run as the 3rd arm in the alignment-axis bake-off after Sinkhorn (b6 Idea 4) Phase A settles. Do NOT spend new compute until Sinkhorn's verdict is known — sequencing constraint.

---

## Toy Experiment Design

**Idea being toyed**: Flow-matching invariance, run as the 3rd arm of the alignment-axis bake-off.
**Triggered by**: Stage 6 alignment-axis slot dependency + Stage 4 mechanism-story degradation.

### Goal
Validate that FM-as-invariance beats both baseline-MSE AND Sinkhorn at matched-wall-clock on ImageNet-10.

### Setup
- **Dataset**: ImageNet-10 (full Imagenette train split + val for probe).
- **Model**: ViT-S/16 + LeJEPA + SIGReg unchanged; invariance term swapped.
- **Config**: 100 ep, ASHA-best (lr, wd, λ), 3 seeds, 3 arms: baseline-MSE / Sinkhorn / Flow-matching. Use Sinkhorn's b6 Phase A config to ensure fair comparison.
- **Budget**: ~12 GPU-h (3 arms × 3 seeds × 100 ep at +20% step time = 12 GPU-h). Sinkhorn-Phase-B is ~15 GPU-h; the increment over Sinkhorn-alone is +5 GPU-h.
- **Wallclock**: 12 GPU-h, parallelizable on 3 GPUs → 4 hr wall-clock.

### Success criterion
- FM-arm ≥ baseline-MSE + 0.4 pp non-overlap AND within ±0.3 pp of Sinkhorn-arm → graduate as 2nd alignment-axis option for compose-mode.
- FM-arm beats baseline-MSE but loses to Sinkhorn by > 0.3 pp → REFRAME (Sinkhorn dominates the axis; archive FM).
- FM-arm fails baseline-MSE bar → KILL FM (Sinkhorn already proved alignment-axis viability; FM is then a strict loss).

### Confound check
3-seed baseline-MSE arm IS the confound check; it doubles as the control. Noise estimate σ ~ 0.5 pp on small-data SSL — required gain ≥ 1 pp (2σ) for non-overlap.

### Falsification thresholds
| Observation | Action |
|-------------|--------|
| FM-arm ≤ baseline-MSE | KILL (FM is a strict regression on this axis) |
| FM-arm beats MSE, loses to Sinkhorn by > 0.3 pp | REFRAME — archive in favor of Sinkhorn |
| FM-arm beats MSE AND within ±0.3 pp of Sinkhorn | FULL SEND as alignment-axis 2nd-option |
| Flow divergence `∇·v_ψ` > 0.5 on val (volume collapse) | KILL — degenerate flow |

### Estimated cost
~12 GPU-h (incremental over Sinkhorn b6 TOY).

### Estimated time
4 hr wall-clock (3 GPUs in parallel).

### Re-vet trigger
After FM-arm results: `/vet-ideas --given-toy ./fm-results.md idea-1-batch-7`.

### Salvageable
Yes — clean 3-arm protocol with sharp falsification.

### Resurrection-eligible
Yes — re-vet on toy results.
