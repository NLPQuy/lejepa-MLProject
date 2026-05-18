# Idea 1 Vetting — RankMe-driven adaptive-λ controller
**Batch**: 6 · **Date**: 2026-05-18 · **Mode**: --climb-mode
**Pattern**: P6 (Verify) · **Tier**: 1 · **Source**: ideation batch-6 Idea 1

## Stage 1 — Problem Framing
> Adopting persona: `Advisor`. Stance: is the controller solving a real ImageNet-10 bottleneck, or a publication-friendly framing?

**Attack 1.1**: "The recurring 'single-λ branding drift' is a *paper-narrative* concern, not a benchmark-climb concern. ImageNet-10 linear probe doesn't care how many HPs LeJEPA has."
- Steel-manned rebuttal: The controller's *primary* value is not the branding — it's that it **eliminates the λ sweep**, reducing total compute to find the best-of-sweep arm by 3-8× (Garrido et al. 2023 Fig. 2 shows RankMe-vs-probe correlation ≥ 0.85 on multiple SSL methods, enabling label-free HP selection). On the 1×A100 budget cap (4 GPU-h per 100-ep run), saving 3-8 runs is ~12-32 GPU-h freed for actual idea-stack iteration. The single-λ branding is the *side benefit*; compute-budget freed is the bottleneck-fix.
- Persona verdict: ✅ DEFLECTED (compute-freed argument is real on the stated budget).

**Attack 1.2**: "PIT-uniformity monitor (batch-3 Idea 3 FULL SEND, 🟢) is already shipped and is also a label-free quality monitor. Why a *second* monitor?"
- Steel-manned rebuttal: PIT is a held-out **monitor** — it scores SIGReg fit but does not feed back into training. RankMe-controller *modifies λ* during training. Different role. Composition map already declared them orthogonal: PIT diagnoses, controller adjusts. The two can co-ship; PIT validates the controller's setpoint convergence.
- Persona verdict: ✅ DEFLECTED.

**Verdict**: PASS. Rebuttal-cycle summary: 2 DEFLECTED / 0 WEAKENED / 0 UNREBUTTED.

## Stage 2 — Prior Work Attack
> Adopting persona: `Prior-Work Hunter`. Stance: someone has done "RankMe-as-controller" already.

**Attack 2.1**: "RankMe was proposed *as an HP-selection criterion* (Garrido 2023). Selecting an HP value via offline rank ≠ feeding rank into an online PI controller. But: the LeCun lab's α-ReQ follow-up and the WACV 2025 HEX paper both use rank-style signals adaptively during training — closer to the proposal."
- Steel-manned rebuttal: HEX uses rank-emergence signals to *adaptively weight loss components*, but does not close the loop with a controller updating a regularization weight. α-ReQ is a better-fitted metric; using it instead of RankMe is a refinement, not a competing prior. No paper I (the persona) can cite proposes a published PI-controller wrapping RankMe → λ. The claim "RankMe-as-controller is novel-as-mechanism within SSL" survives.
- Persona verdict: ⚠️ WEAKENED — RankMe-feedback for HPs has prior art in spirit; the *specific* PI-controller-on-λ is novel mechanism. Recommend Stage 3 downgrade novelty from NOVEL to EXTENDS.

**Verdict**: PASS (no hard duplicate). Rebuttal: 0 DEFLECTED / 1 WEAKENED / 0 UNREBUTTED.

## Stage 3 — Novelty Decomposition
> Adopting persona: `Critical Reviewer`.

Decomposition: (a) RankMe metric [Garrido 2023 — published], (b) PI controller on RegLoss weight [classical control + published in RL/optim], (c) target setpoint `ρ* = 0.6·d` [novel calibration — needs justification beyond "published RankMe-vs-probe curve"], (d) application to LeJEPA's λ [novel application]. Net: **EXTENDS** (Stage 2 confirms — not NOVEL).

**Verdict**: WARN (extends, not novel; gain claim must adjust).

## Stage 4 — Theory Grounding (climb-mode lite)
> Adopting persona: `Theorist`.

**Attack 4.1**: "Setpoint `ρ* = 0.6·d` is asserted from 'Fig. 3 of arXiv:2210.02885' — but RankMe's optimum varies by dataset and method. On Imagenette specifically, the optimum is unmeasured."
- Steel-manned rebuttal: True. Mitigation: **bisection setpoint search** over the first 100 ep on 3-arm A/B/C at `ρ* ∈ {0.4·d, 0.6·d, 0.8·d}`; the falsification test already includes the 0.5d / 0.7d arms. So the setpoint is itself measured, not fixed-by-prior.
- Persona verdict: ⚠️ WEAKENED — the controller doesn't actually remove the sweep, it relocates it from λ-space to setpoint-space. Net compute saved is ≤ 2×, not 3-8×.

**Verdict**: WARN.

## Stage 5 — Feasibility
> Adopting persona: `Pragmatic PM`.

50 LoC; RankMe via `torch.linalg.svdvals` — verified trivial. PI controller well-understood. Risk: controller oscillation if K_p mis-tuned. **PASS**.

## Stage 6 — Killer Baseline
> Adopting persona: `Skeptical Empiricist`.

**Attack 6.1**: "The killer baseline is a 3-arm fixed-λ sweep at the same total compute. Controller arm wins ONLY if it matches best-of-sweep AT or BELOW that compute. On Imagenette, λ sensitivity for LeJEPA is *flat* (LeJEPA paper §C.3) — best-of-sweep is within 0.2 pp across λ ∈ [0.02, 0.2]. There may be **no win to extract**."
- Steel-manned rebuttal: If the λ landscape is flat, the controller still **costs nothing extra** (50 LoC, ~1 % overhead per step). It does no harm. The compose-mode value (binding new HPs from ideas 3/4/5/6 to the controller setpoint) is independent of the flatness of the λ axis itself.
- Persona verdict: ⚠️ WEAKENED — "does no harm" is not "FULL SEND material". Without a real per-idea win on Imagenette, this is **infrastructure**, not a research idea.

**Attack 6.2**: "If the λ landscape is flat, the right *measurement* is to publish the flatness — not deploy a controller. This proposal smuggles infrastructure as research."
- Steel-manned rebuttal: The proposal explicitly states "the *primary* deliverable is compute saved on the λ sweep + a clean adaptive-λ controller for binding new HPs (ideas 3-6) to a single setpoint". That is mechanism + falsification, not infrastructure. The mechanism-check (controller-λ trajectory must converge, not oscillate, within 20 ep) is sharp.
- Persona verdict: ⚠️ WEAKENED — survives Attack 6.2, but the WEAKENED from 6.1 stands.

**Verdict**: WARN. Rebuttal: 0 DEFLECTED / 2 WEAKENED / 0 UNREBUTTED.

## Stage 8 — Decision Gate
> Adopting persona: `Advisor (PI mode)`.

Stage results: Stage 1 PASS / Stage 2 PASS (WEAKENED) / Stage 3 WARN / Stage 4 WARN / Stage 5 PASS / Stage 6 WARN. **3 WARN, 0 FAIL → TOY** per decision-logic.md priority 5.

**Verdict**: 🧪 **TOY** · Confidence 🟢

### Toy Experiment Design
- **Phase A (1 hr CPU, free)**: 10-ep CIFAR-10 sanity prototype. Controller dynamics: K_p, K_i tuning; verify λ trajectory converges, not oscillates. Decision: if oscillation > 30 % of mean within last 5 ep, retune; if no retuning works, KILL.
- **Phase B (~12 GPU-h)**: 100-ep ImageNet-10, 3-arm at total-compute-matched: fixed-λ-best (assumed ASHA-found) / controller @ setpoint 0.6d / controller @ setpoint 0.5d. Decision rule: best controller arm must match fixed-λ-best within ±0.3 pp linear probe **at total compute ≤ fixed-λ-best**. If yes → graduate to FULL SEND with compose-mode use case for ideas 3-6. If matches probe but uses more compute → REFRAME as "compose-mode binder, no compute saving". If loses on probe → KILL.
- **Dependency**: Phase B requires ASHA Step-0 to have completed (provides the fixed-λ-best target).
