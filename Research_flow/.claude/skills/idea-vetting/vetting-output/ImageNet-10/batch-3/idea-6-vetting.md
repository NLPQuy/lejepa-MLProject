# Vetting — Batch 3 Idea 6: Embedding-rank curriculum (k_t schedule)
**Pattern**: P5 · **Tier**: 1 · **Mode**: --climb-mode

## Stage 1 — Problem Framing (Advisor)
- **Attack 1**: framing claim is "filter out noise from low-variance directions early" — but at initialisation all 384 directions have similar variance (Gaussian init), so the "filter noise" story does not start. **Rebuttal**: after even 1–2 epochs the encoder begins to differentiate direction variance (RankMe shows this clearly); k_t = 32 then captures the signal-bearing subspace. ⚠️ **WEAKENED** — story holds after warmup but not at step 0.
- **Verdict**: PASS w/ flag

## Stage 2 — Prior Work Attack
- **Attack 1**: ERW (arXiv:2504.10188) does representation warmup but for *generative model training*, not SSL pretraining. Are they really analogous? **Rebuttal**: the principle (low-complexity objective first, full objective later) transfers; the specifics differ. EXTENDS. **DEFLECTED**.
- **Attack 2**: Dimensional collapse literature (Meta blog 2022) argues low-rank embeddings are the *failure mode* SSL must avoid — and this idea *induces* low-rank for half of training. Contradiction? **Rebuttal**: the curriculum *restricts SIGReg's domain* to top-k_t directions, not the encoder's output. The encoder is free to populate all d dimensions; SIGReg just doesn't penalise them in early phase. The final phase restores full-d SIGReg. ⚠️ **WEAKENED** — distinction is correct but subtle; risk that the encoder *adapts* to the low-k_t regime and never repopulates the other dimensions.
- **Verdict**: WARN

## Stage 3 — Novelty Decomposition
- Novel piece: k_t schedule on the SIGReg projection rank specifically.
- Already published: ERW (generative warmup), curriculum learning survey, dimensional-collapse analyses.
- Net novelty: NOVEL composition (SSL + SIGReg + rank curriculum).
- **Verdict**: PASS

## Stage 4 — Theory Grounding
- Final phase = baseline → Cramér–Wold preserved at convergence ✅
- **Attack**: during middle phase, SIGReg pulls only top-k_t toward N(0,I); the remaining d − k_t dimensions can drift to any distribution, including degenerate. If the encoder finds a low-loss equilibrium with k_t isotropic + (d − k_t) collapsed, the curriculum may not recover even after k_t = d. **Rebuttal**: the proposal includes a RankMe monitor that aborts if `rankme(Z) < 4` for > 5 epochs — partial guard, not a guarantee. ❌ **UNREBUTTED** — equilibrium risk is real and the monitor only detects catastrophic collapse, not slow drift.
- **Verdict**: WARN (1 UNREBUTTED on theory)

## Stage 5 — Feasibility
- Running cov + per-step truncated eigendecomp (~6×10⁷ ops at d=384, negligible vs forward pass).
- k_t schedule is a fixed schedule (32 → 384 over 50 % epochs) — no continuous HP.
- **Attack**: schedule milestone (50 %) is a new HP-in-disguise. **Rebuttal**: fixed default + 5-point sensitivity ablation in proposal. Acknowledged. **DEFLECTED**.
- **Verdict**: PASS

## Stage 6 — Killer Baseline (Skeptical Empiricist)
- Killer baseline: **always-full-d SIGReg** at matched epochs.
- **Attack**: ERW-style warmup typically gains at *short* total budgets (50–100 ep) and loses at *long* budgets (300+) where the warmup phase becomes wasted compute. Current Imagenette recipe is 600 ep — well into the regime where warmup may not pay. **Rebuttal**: scale k_t to total-budget proportion (50 % of whatever total). At 600 ep, 300 ep of warmup is a lot — risk is real. ⚠️ **WEAKENED** — the bet is sensitive to total-budget choice.
- **Attack 2**: alternative falsification (reach baseline in ≤ 60 % of epochs) is fair but optimistic — needs a learning-curve crossover study, not single endpoint. **Rebuttal**: proposal's falsification covers this with the "(a) convergence pp OR (b) fewer epochs" disjunction. **DEFLECTED**.
- **Verdict**: WARN

## Stage 8 — Decision Gate
- FAIL: 0 · WARN: 4 (framing flag, prior-art domain transfer, theory UNREBUTTED, killer-baseline scale-sensitive) · UNREBUTTED: 1
- Per `decision-logic.md`: 0 FAIL + 4 WARN → **TOY EXPERIMENT FIRST**
- Confidence: 🟡 (clean composition but multiple risk vectors; equilibrium-during-middle-phase is the unrebutted concern)

## Final verdict: 🧪 **TOY** 🟡
- Toy: 18 GPU-h (3 arms × 3 seeds × ViT-S/100 ep). Arms: baseline (always d=384), curriculum-50% (32→384 over 50 ep), curriculum-30% (32→384 over 30 ep). Log RankMe per epoch.
- Decision rule: best curriculum arm wins by ≥ 0.5 pp linear probe at endpoint **OR** reaches baseline-endpoint pp in ≤ 60 % epochs. Both fail → KILL. Sanity check: RankMe at end of curriculum phase must be ≥ baseline RankMe at same epoch (no slow-drift collapse).
- Falsification trigger: equilibrium risk (top-k_t isotropic + (d−k_t) drifted) is detectable via RankMe gap > 30 % below baseline at end-of-curriculum.
- Dependency: should run **after** batch-2 Idea 5 (ASHA) provides measured baseline.
