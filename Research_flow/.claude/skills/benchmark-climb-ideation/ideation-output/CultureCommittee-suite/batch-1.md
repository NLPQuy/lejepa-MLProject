# Idea Batch 1 — CultureCommittee 5-bench suite / single-model multi-agent panel + robust fusion
**Generated**: 2026-05-31T07:08:48Z
**Time-to-batch**: ~10 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation` (5-bench suite; RACECAR project)

## Inputs
- Benchmark: NormAd-ETI (acc) + DICES-350/990 (base-2 JSD) + GlobalOpinionQA (1-JSdist) + VITAL (JS dist) + Scruples (base-2 JSD + acc).
- Task / problem: Training-free, label-free cultural/moral/safety alignment of ONE frozen open LLM (Qwen2.5-7B-Instruct). Read answer-token logits only (never generate); two metric families — ACCURACY (NormAd) and DISTRIBUTION-MATCH (DICES/GOQA/VITAL/Scruples).
- Existing pipeline: `exps/exp003_single_model_panel.py` — `[1]` multi-axis internal panel (persona x paraphrase x option-order views; per-view softmax over answer tokens; canonical remap), `[2]` geometric-median robust barycenter (Weiszfeld, breakdown 0.5), `[3]` decode/metric. Baselines: raw_single, mean_panel, disca_shrink, panel_med (OURS). Current real result: Qwen2.5-7B tracked (Round 1).
- Batch scope: **enhance-existing** (10/10 ideas modify a named pipeline component).
- Tier mix (configured): **45/35/20** (default). Note: skill suggests 55/30/15 when a pipeline is supplied; I kept the balanced default because the most novel fusion-op ideas are genuinely cross-domain (statistics / optimal transport) and a T1-heavy mix would crowd them out. Observed mix 40/30/30 is within all default ±10pp bands.
- Baseline: Qwen2.5-7B-Instruct; NormAd-rot single ~63-71 acc (SOTA 80.4 debate); GOQA vanilla ~0.565 (beat 0.684); DICES prompted ~0.33 (trained DiADEM 0.045); VITAL EthosAgents 0.242; Scruples non-saturated.
- Compute budget: Kaggle T4/RTX Pro 6000, offline, K cheap forwards/item, no fine-tuning.
- Time budget: per-bench cache then fusion sweep (hours).
- Constraints: **single model only** (K calls = the panel; fusing 2+ models FORBIDDEN); post-forward distribution math only; no trainable params; no generation (logits only); no test-set tuning / magic thresholds.

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 10 |
| Tier 1 / 2 / 3 (counts) | 4 / 3 / 3 |
| Tier mix vs configured | 40/30/30 vs 45/35/20 (deviation <=10pp per tier ✓) |
| Scope mix | 10 enhance-existing / 0 greenfield (>=50% ✓) |
| Patterns used | P1, P2, P3, P4, P6, P8, P10 (7 distinct) |
| Distinct venues | ICML, ICLR, NAACL, EMNLP, ACL, Statistical Science, SIAM J Math Anal, arXiv-stat/math (>=8) |
| Time windows | <12mo (4), 12-36mo (3), 36-72mo (1), 72+mo (2) |
| Avg feasibility | 4.1/5 |
| Avg confidence | 🟢 30%, 🟡 60%, 🔴 10% |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|------|------|--------|-------|
| 1 | Reliability-weighted geometric median (coherence weights) | P6 | 1 | +2.0 | 4 | M | 3.94 |
| 2 | Per-view contextual calibration before fusion | P3 | 1 | +2.5 | 5 | S | 3.90 |
| 3 | Context-removal contrast axis (CAD-style anti-sycophancy) | P1 | 2 | +2.5 | 4 | M | 3.66 |
| 4 | Layer-contrast (DoLa) view at zero extra forwards | P1 | 2 | +1.2 | 4 | S | 3.50 |
| 5 | Dispersion-driven temperature calibration of P* | P10 | 1 | +1.8 | 5 | S | 3.46 |
| 6 | Log-opinion-pool robust fusion (median in logit space) | P3 | 3 | +1.2 | 4 | S | 3.30 |
| 7 | Dispersion-gated neutral/abstain routing (NormAd) | P8 | 1 | +2.0 | 4 | S | 3.22 |
| 8 | Depth-trimmed barycenter (tunable robustness/pluralism) | P2 | 3 | +1.2 | 3 | M | 2.86 |
| 9 | Robust Wasserstein barycenter on ordinal labels | P2 | 3 | +1.5 | 3 | L | 2.62 |
| 10 | Stability early-stop of view sampling (smaller K) | P4 | 2 | +0.2 | 5 | S | 2.50 |

## Top-3 recommendations

### 🏆 Top-1 by composite score
**Idea 1: Reliability-weighted geometric median** — Score 3.94
Down-weight low-confidence / incoherent views *inside* the Weiszfeld iteration using a label-free per-view reliability score (negative entropy + panel-agreement), generalizing the unweighted median you ship today. Helps both metric families and is strictly more general than DISCA's single scalar shrinkage. (Promoted to #1 after the devil's-advocate pass dinged Idea 2 — see Notes.)

### ⚡ Quick win (lowest effort)
**Idea 4: Layer-contrast (DoLa) view at zero extra forwards** — Effort S
Read a premature-layer answer-token distribution from the *same* forward pass already running, contrast it against the final layer, and add the result as one more panel view. Near-zero added compute (no new forward), directly enlarges the panel along an internal axis nobody else fuses.

### 🛡️ Safe bet (highest confidence)
**Idea 5: Dispersion-driven temperature calibration of P*** — Confidence 🟢
Temperature-rescale the fused distribution by a factor derived from the panel's own inter-view dispersion. Argmax-invariant ⇒ **cannot hurt NormAd accuracy**, and directly attacks the over-sharp-vs-human-distribution gap on the four distribution-match benches. Only touches the readout; trivial to ablate.

## Ranked ideas

### Idea 1: Reliability-weighted geometric median (coherence weights)

- **Pattern**: P6 (Verify)
- **Tier**: 1
- **Target task**: Training-free fusion of K single-model panel views into P* for both accuracy (NormAd) and distribution-match (DICES/GOQA/VITAL/Scruples).
- **Scope**: enhance-existing — modifies fusion `[2]` (weighted Weiszfeld); panel `[1]` and decode `[3]` unchanged. Adds a per-view weight computed from quantities already available in the forward.
- **One-liner**: Weight each view by a label-free reliability score before the robust median, so confidently-coherent views pull P* harder and noisy framings contribute less than the equal vote they get now.

**Mechanism**:
For each view v compute a reliability weight w_v from two post-forward signals: (a) negative Shannon entropy of P_v over the answer tokens (sharper view = more reliable), and (b) agreement = mean cosine/1-JSD of P_v to the other views (a view that disagrees with everyone is likely a framing artifact). Set w_v = softmax(alpha*(-H(P_v)) + beta*agreement_v) with alpha,beta fixed a priori (or read off panel dispersion, not the eval set). Replace the unweighted Weiszfeld update `P* <- sum_v P_v/||P*-P_v|| / sum_v 1/||P*-P_v||` with the weighted update `... w_v/||P*-P_v|| ...`. Output the weighted geometric median.

**Source inspirations**:
- Primary: "Representation Consistency for Accurate and Coherent LLM Answer Aggregation", Imperial/JPMorgan, 2025 [arXiv:2506.21590]
- Supporting: "Confidence Improves Self-Consistency in LLMs" (CISC), 2025 [arXiv:2502.06233]
- Supporting: "The Geometric Median and Applications to Robust Mean Estimation", SIAM J. Math. Data Sci. 2024 [arXiv:2307.03111]

**Why expected to improve**:
Representation Consistency shows that down-weighting answers whose generating states are *incoherent* lifts aggregation accuracy up to ~4pp over strong test-time-scaling baselines; CISC shows confidence-weighted voting beats plain self-consistency with 40% fewer samples. Porting reliability weights into the robust median keeps the breakdown-0.5 protection while adding a per-view (not per-panel) signal that DISCA's single scalar shrinkage cannot express — incoherent sycophantic views are suppressed both by being outliers (median) and by low weight.

**Expected gain**: +0.8 / +2.0 / +3.5 pp 🟡 (NormAd acc; DICES/GOQA/VITAL/Scruples JSD improvements of similar relative size)
**Feasibility**: 4/5 🟢
**Effort**: M 🟢

**Implementation sketch**:
1. In the cached panel, store per-view entropy and pairwise JSD (both already computable from P_v).
2. Add `weighted_weiszfeld(P_views, w)` next to the existing Weiszfeld; default w=1 reproduces panel_med exactly (no-op guard).
3. Sweep alpha,beta on a tiny dev slice fixed a priori (or set from median panel dispersion); report panel_med vs weighted on all 5 benches.

**Risks**:
- Entropy weighting can over-trust a view that is confidently wrong (shared bias) — partly mitigated by the agreement term and by Idea 2/Idea 3.
- If reliability is uncorrelated with correctness on a bench, weights add variance — falsifiable below.

**Falsification test**: On NormAd-rot (Qwen2.5-7B) with the current panel, if weighted-median acc <= panel_med acc within +/-0.3pp AND mean DICES-350 JSD is not reduced by >=0.005, the reliability signal carries no information here — abandon.

### Idea 2: Per-view contextual calibration before fusion

- **Pattern**: P3 (Replace)
- **Tier**: 1
- **Target task**: Remove shared per-view answer-token bias so fusion reflects content, not the model's A/"yes" prior — accuracy (NormAd) + distribution-match.
- **Scope**: enhance-existing — inserts a calibration step on each P_v inside panel `[1]` *before* canonical remap and before fusion `[2]`. Fusion op unchanged.
- **One-liner**: Subtract each view's content-free answer-token prior (contextual calibration / PriDe) before the geometric median, because the median removes *outlier* views but not a bias *shared by the majority* of views.

**Mechanism**:
For each prompt template, run one extra forward on a content-free input (empty / "N/A" / shuffled-option probe) to estimate the model's answer-token prior p0 under that framing; or estimate the option-ID prior PriDe-style by permuting option contents on a handful of items. Calibrate each view P_v <- normalize(P_v / p0) (affine in logit space) before remapping to canonical order and fusing. This is the diagonal-W special case of Calibrate-Before-Use applied per view.

**Source inspirations**:
- Primary: "Calibrate Before Use: Improving Few-Shot Performance of Language Models", Zhao, Wallace, Feng, Klein, Singh, ICML 2021 [arXiv:2102.09690]
- Supporting: "Large Language Models Are Not Robust Multiple Choice Selectors" (PriDe), Zheng et al., ICLR 2024 [arXiv:2309.03882]
- Supporting: "CalibraEval: Calibrating Prediction Distribution to Mitigate Selection Bias in LLMs-as-Judges", ACL 2025 [arXiv:2410.15393]
- Contrasting: "Look at the Text: Instruction-Tuned LMs are More Robust MCQ Selectors than You Think", 2024 [arXiv:2404.08382]

**Why expected to improve**:
Contextual calibration lifts GPT-family accuracy up to 30pp by zeroing the content-free prior; PriDe removes option-ID/order bias label-free. The robust median cannot cancel a bias the majority of framings share (e.g., a uniform lean to "yes"/first option), which is exactly the NormAd over-confidence pathology (neutral acc 0.42). Per-view calibration removes that shared component pre-fusion.

**Expected gain**: +1.0 / +2.5 / +5.0 pp 🟡 (NormAd; smaller on distribution-match)
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add `estimate_prior(template)` (content-free forward) cached once per template.
2. Apply per-view division before `canonical_remap`; identity when p0 uniform (no-op guard).
3. Compare raw vs calibrated panel under panel_med on all 5 benches; report per-label NormAd macro (de-sycophancy).

**Risks**:
- Instruction-tuned Qwen2.5-7B may already be near-debiased (see Contrasting 2404.08382) ⇒ gain could be small on NormAd.
- Content-free prior can be unrepresentative for long cultural stories — use the shuffled-option probe variant as fallback.

**Falsification test**: On NormAd-rot, if calibrated-panel macro-F1 improves <0.3pp over raw-panel AND the neutral-label recall does not rise by >=2pp, calibration is redundant for this instruction-tuned model — drop.

### Idea 3: Context-removal contrast axis (CAD-style anti-sycophancy)

- **Pattern**: P1 (Combine)
- **Tier**: 2
- **Target task**: Isolate the culturally/contextually conditioned signal and suppress the model's default prior — NormAd accuracy + de-sycophancy; helps culture-conditioned GOQA.
- **Scope**: enhance-existing — adds a new perturbation axis to panel `[1]` (a paired "context-removed" view per view) and a contrastive pre-combination feeding the *existing* fusion `[2]`.
- **One-liner**: For each view, also compute the answer distribution with the cultural context (country/value/RoT) stripped, then fuse the context-amplified contrast (log P_with - lambda*log P_without) so framing-default mass is cancelled.

**Mechanism**:
NormAd already ships 5 conditioning settings (none/country/value/cval/rot). Treat the "none" (context-free) distribution as the model's default prior P_no. For each conditioned view P_ctx, form the context-aware-decoding contrast in logit space: logit* = (1+lambda)*logit(P_ctx) - lambda*logit(P_no), softmax, then feed these contrasted views into the geometric median. lambda fixed a priori. For GOQA/VITAL where there is no native "none" setting, build P_no by masking the country/persona tokens.

**Source inspirations**:
- Primary: "Trusting Your Evidence: Hallucinate Less with Context-aware Decoding", Shi et al., NAACL 2024 [arXiv:2305.14739]
- Supporting: "Contrastive Decoding: Open-ended Text Generation as Optimization", Li et al., ACL 2023 [arXiv:2210.15097]

**Why expected to improve**:
CAD amplifies the context-vs-no-context difference and is shown to override a model's incorrect prior knowledge; here the "prior" is the sycophantic framing-default that NormAd's neutral failure exposes. The contrast removes mass the model would assign regardless of culture, sharpening the genuinely culture-conditioned signal before robust fusion.

**Expected gain**: +1.0 / +2.5 / +4.5 pp 🟡 (NormAd, esp. country/Global-South splits; modest GOQA)
**Feasibility**: 4/5 🟢
**Effort**: M 🟡

**Implementation sketch**:
1. Cache the "none"-setting distribution alongside each conditioned view (already computed for NormAd's 5 settings — near-free there).
2. Add `cad_contrast(P_ctx, P_no, lambda)`; lambda=0 reproduces the current panel (no-op guard).
3. Fuse contrasted views with panel_med; sweep lambda in {0.25,0.5,1.0} on a fixed dev slice.

**Risks**:
- Over-large lambda can push mass onto implausible labels (CAD instability) — bound lambda and clip.
- For non-NormAd benches, the masked "none" view doubles forwards on those items (~2x there).

**Falsification test**: On NormAd-country (the setting CAD should help most), if contrasted panel_med acc <= plain panel_med at every lambda in {0.25,0.5,1.0}, the context-contrast carries no signal — drop the axis.

### Idea 4: Layer-contrast (DoLa) view at zero extra forwards

- **Pattern**: P1 (Combine)
- **Tier**: 2
- **Target task**: Enlarge the panel with an internal-axis view that boosts factual/normative reliability, at ~zero added compute — both metric families.
- **Scope**: enhance-existing — adds one within-forward view to panel `[1]`; fusion `[2]` and decode `[3]` unchanged.
- **One-liner**: Read the answer-token logits from a premature transformer layer in the *same* forward and contrast against the final layer (DoLa) to produce an extra "factuality-amplified" panel view for free.

**Mechanism**:
During each existing forward, additionally project a small set of early/middle layers to the vocab via the tied unembedding (no extra forward). Pick the premature layer maximizing JSD to the final layer (DoLa's dynamic selection), form logit_final - logit_premature over the answer tokens, softmax to P_dola, and add P_dola as one more view per existing view into the geometric median.

**Source inspirations**:
- Primary: "DoLa: Decoding by Contrasting Layers Improves Factuality in Large Language Models", Chuang et al., ICLR 2024 [arXiv:2309.03883]
- Supporting: "Representation Consistency for Accurate and Coherent LLM Answer Aggregation", 2025 [arXiv:2506.21590]

**Why expected to improve**:
DoLa improves truthfulness 12-17pp on TruthfulQA with no extra forward and no fine-tuning by surfacing knowledge localized in later layers. Adding it as a panel axis injects a view whose errors are decorrelated from prompt-perturbation views, which is exactly the diversity a robust barycenter exploits — and it costs only intermediate-logit reads.

**Expected gain**: +0.4 / +1.2 / +2.5 pp 🟡 (broad, small; strongest where factual normative knowledge matters)
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Hook hidden states for a candidate layer bucket; project with the model's unembedding; cache per item.
2. Add P_dola views to the panel; identity-skip if DoLa selection degenerates (no-op guard).
3. Ablate: panel_med with vs without the DoLa axis on all 5 benches.

**Risks**:
- Premature-layer logits can be noisy for a 7B model on long inputs — bounded by dynamic layer selection.
- Extra memory for hidden-state caching (mitigate by computing P_dola on the fly).

**Falsification test**: Add the DoLa axis to the NormAd-rot panel; if panel_med acc changes by <0.3pp AND no distribution-match bench improves JSD by >=0.003, the layer-contrast view adds no decorrelated signal — drop it.

### Idea 5: Dispersion-driven temperature calibration of P*

- **Pattern**: P10 (Sampling/decoding-distribution)
- **Tier**: 1
- **Target task**: Match the *shape* of the fused distribution to human distributions — DISTRIBUTION-MATCH only (DICES/GOQA/VITAL/Scruples). Argmax-invariant ⇒ no NormAd-accuracy effect.
- **Scope**: enhance-existing — adds a post-fusion temperature rescale at decode `[3]`; panel `[1]` and fusion `[2]` unchanged.
- **One-liner**: The robust median produces an over-sharp P*; rescale its temperature by a factor read off the panel's own inter-view dispersion so the output entropy tracks genuine pluralism instead of false confidence.

**Mechanism**:
After computing P*, set T = g(D) where D = mean pairwise JSD across panel views (label-free dispersion) and g is a fixed monotone map (e.g., T = 1 + c*D, c fixed a priori). Output P*_cal = softmax(logit(P*)/T). High panel disagreement -> higher T -> flatter, more human-like distribution; consensus -> T~1. No eval-set tuning; D is intrinsic to the panel.

**Source inspirations**:
- Primary: "On Calibration of Modern Neural Networks", Guo, Pleiss, Sun, Weinberger, ICML 2017 [arXiv:1706.04599]
- Supporting: "A Roadmap to Pluralistic Alignment" (distributional pluralism), Sorensen et al., ICML 2024 [arXiv:2402.05070]

**Why expected to improve**:
Temperature scaling is the canonical post-hoc fix for overconfident distributions and is argmax-preserving. The four distribution-match benches reward P* whose spread matches human disagreement; a robust median deliberately collapses spread, so its P* is systematically too sharp. Driving T from panel dispersion restores legitimate spread without erasing the consensus mode.

**Expected gain**: +0.6 / +1.8 / +3.0 (relative JSD reduction, %) 🟢 on DICES/GOQA/VITAL/Scruples; **0.0 on NormAd acc by construction**
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Compute D (mean pairwise JSD) per item from the cached panel.
2. Apply P*_cal = temperature(P*, T=1+c*D); c from a fixed prior, then a single sensitivity curve (not eval-tuned).
3. Report base-2 JSD before/after on the four distribution benches; confirm NormAd argmax unchanged.

**Risks**:
- Single-metric-family: helps distribution-match only (explicitly noted).
- If panel dispersion is uncorrelated with human dispersion, T mis-scales — falsifiable.

**Falsification test**: On DICES-350, if temperature-calibrated P* does not reduce mean base-2 JSD by >=0.005 at any c on a fixed sweep, the panel-dispersion -> human-spread link is absent — drop.

### Idea 6: Log-opinion-pool robust fusion (median in logit space)

- **Pattern**: P3 (Replace)
- **Tier**: 3
- **Cross-domain transfer**: statistics (opinion pooling / external Bayesianity) -> LLM panel fusion operator.
- **Target task**: A fusion operator with better distribution-combination properties — both metric families.
- **Scope**: enhance-existing — replaces the probability-simplex Weiszfeld in fusion `[2]` with a logit-space robust aggregate; panel `[1]`/decode `[3]` unchanged.
- **One-liner**: Aggregate the views by a robust (coordinate-wise median / geometric median) in *logit* space — the logarithmic opinion pool — instead of the probability-space median, gaining the external-Bayes property that prob-space averaging lacks.

**Mechanism**:
Map each view to logit space l_v = log P_v; compute a robust center (coordinate-wise median, or geometric median of the l_v); softmax back. This is the robustified logarithmic opinion pool. Unlike the arithmetic mean (mean_panel) it is zero-preserving and external-Bayesian (Genest-Zidek); unlike the prob-space geometric median it down-weights a view that is extreme in *evidence* (logit) terms, not just in probability terms.

**Source inspirations**:
- Primary: "Combining Probability Distributions: A Critique and an Annotated Bibliography", Genest & Zidek, Statistical Science 1986, 1(1):114-135 [DOI:10.1214/ss/1177013825]
- Supporting: "The Geometric Median and Applications to Robust Mean Estimation", SIAM J. Math. Data Sci. 2024 [arXiv:2307.03111]

**Why expected to improve**:
Log-pooling is the unique externally-Bayesian aggregator and is standard in expert-fusion; combining it with a high-breakdown robust center keeps DISCA-style outlier protection while operating in the evidence geometry where LLM logits actually live. Should be at least as good as panel_med on accuracy and better on calibrated distribution-match because log-pool concentrates agreement multiplicatively.

**Expected gain**: +0.3 / +1.2 / +2.5 pp 🟡 (both families; safe lower bound = ties panel_med)
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Add `logpool_median(P_views)` = softmax(geom_median(log P_views)).
2. Guard zeros with a small epsilon floor.
3. Compare panel_med vs logpool_median across all 5 benches.

**Risks**:
- Logit-space is sensitive to near-zero probabilities (epsilon choice) — bound and report.
- May coincide numerically with panel_med on low-dispersion items (small benches) — that is the honest no-op case.

**Falsification test**: Across all 5 benches, if logpool_median never beats panel_med by >=0.2pp (acc) or >=0.003 (JSD) on any bench, the logit-geometry change is inert — keep panel_med.

### Idea 7: Dispersion-gated neutral/abstain routing (NormAd)

- **Pattern**: P8 (Specialize)
- **Tier**: 1
- **Target task**: Fix NormAd's documented neutral-label collapse (acc 0.42, overconfidence) — NormAd ACCURACY + macro only.
- **Scope**: enhance-existing — adds a decode-time routing rule at `[3]`; panel `[1]`/fusion `[2]` unchanged.
- **One-liner**: When the panel disagrees a lot and the fused top-2 margin is thin, route the answer to "neutral" — turning the panel's own dispersion into the abstention signal the model currently lacks.

**Mechanism**:
For each item compute panel dispersion D (mean pairwise JSD) and the top-1/top-2 margin m of P*. If D exceeds a band derived from the global panel-dispersion distribution AND m < that band, output "neutral"; else argmax. The band is set from the panel's own dispersion quantiles (label-free, a priori), never from NormAd labels. Targets exactly the items where the model is overconfident between yes/no while humans say neutral.

**Source inspirations**:
- Primary: "NormAd: A Framework for Measuring the Cultural Adaptability of Large Language Models", NAACL 2025 [arXiv:2404.12464]
- Supporting: "Jury Learning: Integrating Dissenting Voices into Machine Learning Models", Gordon et al., CHI 2022 [arXiv:2202.02950]

**Why expected to improve**:
NormAd itself reports the neutral label is where models fail worst (0.42 acc) due to overconfidence, while humans hit 98%. The panel's framing-induced spread is a direct overconfidence proxy: high spread + thin margin = "the model is guessing". Abstaining to neutral on those items recovers the class the argmax never picks.

**Expected gain**: +0.5 / +2.0 / +4.0 pp 🟡 (NormAd micro acc + macro; **NormAd only**)
**Feasibility**: 4/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Compute D and margin m per item from the cached panel.
2. Set the (D,m) band from panel-dispersion quantiles fixed a priori; route to neutral inside the band.
3. Report micro acc + per-label recall (neutral) + macro-F1 vs panel_med.

**Risks**:
- Single-bench, single-metric-family (NormAd accuracy) — noted.
- A poorly placed band can over-route to neutral and hurt yes/no recall — falsifiable; band is quantile-derived not hand-tuned.

**Falsification test**: On NormAd-rot, if dispersion-gated routing does not raise neutral-label recall by >=3pp without dropping overall micro acc, the dispersion->neutral link is too weak — drop.

### Idea 8: Depth-trimmed barycenter (tunable robustness/pluralism)

- **Pattern**: P2 (Transfer)
- **Tier**: 3
- **Cross-domain transfer**: multivariate statistics (Tukey halfspace data depth / depth-trimmed means) -> robust panel fusion with an explicit pluralism dial.
- **Target task**: A fusion family that interpolates between full robustness (median) and pluralism preservation (mean) via a principled trimming fraction — both families, and the DISCA-collapse counter-example.
- **Scope**: enhance-existing — replaces fusion `[2]` with a depth-trimmed L-estimator that contains panel_med and mean_panel as special cases.
- **One-liner**: Rank views by data depth on the simplex, trim the shallowest tau fraction (likely framing artifacts), average the rest — a one-knob family where tau=0 is mean_panel and the depth-weighted limit is the robust median.

**Mechanism**:
Compute a depth score for each view P_v (Tukey halfspace depth approximation, or the cheaper geometric-median-distance rank) within the panel. Discard the lowest-depth tau fraction and take the (depth-weighted) average of the survivors as P*. tau is set from the breakdown the panel needs (e.g., tau = expected corrupted-view fraction from exp002), not from the eval set.

**Source inspirations**:
- Primary: "Depth based trimmed means", 2025 [arXiv:2505.03523]
- Supporting: "Mathematics and the Picturing of Data" (halfspace depth), Tukey, Proc. ICM 1975

**Why expected to improve**:
Depth-trimmed means are consistent, high-breakdown, and—unlike the pure median—retain controllable spread, directly addressing the pluralism-vs-robustness tension this project flags (mean collapses nothing/over-keeps bias; median over-collapses spread on distribution-match). The single tau makes the robustness/pluralism trade explicit and theorem-friendly (breakdown >= tau).

**Expected gain**: +0.3 / +1.2 / +2.5 (acc pp and relative JSD) 🟡 (both families; main value on distribution-match where pure median over-collapses)
**Feasibility**: 3/5 🟡
**Effort**: M 🟡

**Implementation sketch**:
1. Implement a cheap depth proxy (rank by distance to geometric median) + optional Tukey-depth approximation.
2. `depth_trimmed_bary(P_views, tau)`; tau=0 reproduces mean_panel (no-op guard), depth-weighted limit ~ panel_med.
3. Sweep tau in {0, 0.1, 0.25, 0.4} a priori; report all 5 benches incl. the spread (entropy) of P*.

**Risks**:
- Exact Tukey depth is expensive in high dim; the proxy may not match true depth — bounded by using the cheap rank version first.
- For tiny label spaces (binary Scruples) depth degenerates to 1-D — falls back to trimmed mean.

**Falsification test**: If across tau in {0.1,0.25,0.4} the depth-trimmed barycenter never simultaneously (a) matches panel_med on NormAd acc within 0.3pp and (b) beats it on >=2 distribution benches by >=0.004 JSD, the depth machinery buys nothing over the existing two operators — drop.

### Idea 9: Robust Wasserstein barycenter on ordinal labels

- **Pattern**: P2 (Transfer)
- **Tier**: 3
- **Cross-domain transfer**: optimal-transport mathematics (Wasserstein barycenters) -> distribution-match fusion that respects label ordering.
- **Target task**: DISTRIBUTION-MATCH on benches with ordered/structured label spaces — NormAd yes/neutral/no (neutral between), DICES safe/unsure/unsafe, ordinal opinion scales in GOQA/VITAL.
- **Scope**: enhance-existing — swaps fusion `[2]` for a *robust* Wasserstein barycenter on an ordinal ground cost; used as the distribution-match readout (Idea 5/7 cover accuracy).
- **One-liner**: Fuse views with a robust Wasserstein barycenter under a ground cost that encodes label order (neutral lies between yes and no), so the fused distribution matches human distributions that are themselves ordinally structured.

**Mechanism**:
Define a ground cost C on the label space encoding ordinal distance (yes-neutral=1, yes-no=2, etc.; for GOQA/VITAL use the Likert order). Compute the **robust** Wasserstein barycenter of the views under C (robust variant to keep breakdown protection — plain W-barycenter is outlier-sensitive). Output as P* for the distribution-match metrics.

**Source inspirations**:
- Primary: "Robust Wasserstein barycenter", 2026 [arXiv:2603.07563]
- Supporting: "Fast Computation of Wasserstein Barycenters", Cuturi & Doucet, ICML 2014 [arXiv:1310.4375]
- Supporting (foundational): "Barycenters in the Wasserstein Space", Agueh & Carlier, SIAM J. Math. Anal. 2011 [DOI:10.1137/100805741]

**Why expected to improve**:
TV/Euclidean fusion (current median) treats yes/no/neutral as unordered, so it cannot exploit that human safety/opinion distributions concentrate on *adjacent* labels. A Wasserstein barycenter on an ordinal cost moves mass coherently along the order, matching the geometry of the target distributions; the robust variant (2603.07563) avoids the outlier-blur that plain barycenters suffer (the explicit devil's-advocate fix).

**Expected gain**: +0.5 / +1.5 / +3.0 (relative JSD reduction, %) 🔴 (distribution-match only; high variance)
**Feasibility**: 3/5 🟡
**Effort**: L 🟡

**Implementation sketch**:
1. Define ordinal ground cost per bench; implement robust-W-barycenter (Sinkhorn + robust reweighting).
2. Use only for distribution-match readout; keep panel_med for NormAd argmax.
3. Compare base-2 JSD vs panel_med on DICES/GOQA/VITAL/Scruples.

**Risks**:
- Only meaningful where labels have a real order — binary Scruples gains little.
- Sinkhorn entropic blur can re-introduce the over-smoothing it aims to fix — use low epsilon / debiased Sinkhorn.

**Falsification test**: On DICES-350 (ordered safe/unsure/unsafe), if the robust ordinal W-barycenter does not beat panel_med base-2 JSD by >=0.005, the ordinal geometry does not help — drop.

### Idea 10: Stability early-stop of view sampling (smaller K)

- **Pattern**: P4 (Scale, down)
- **Tier**: 2
- **Target task**: Cut compute (forwards/item) while holding the fused metric — efficiency across all 5 benches ("lightweight is a plus").
- **Scope**: enhance-existing — adds an early-stop controller to panel generation `[1]`; fusion `[2]`/decode `[3]` unchanged.
- **One-liner**: Generate panel views sequentially and stop adding views once the running geometric median stops moving (JSD delta < epsilon), shrinking K per item without changing the operator.

**Mechanism**:
Order the perturbation axes; after each new view, recompute the running Weiszfeld median and measure JSD(P*_t, P*_{t-1}); stop when it falls below epsilon for w consecutive views (Adaptive-Consistency style stability rule). epsilon, w fixed a priori. Easy items stop early; ambiguous items use the full panel.

**Source inspirations**:
- Primary: "Reliability-Aware Adaptive Self-Consistency for Efficient Sampling in LLM Reasoning" (ReASC), 2026 [arXiv:2601.02970]
- Supporting: "Let's Sample Step by Step: Adaptive-Consistency for Efficient Reasoning and Coding with LLMs", Aggarwal et al., EMNLP 2023 [arXiv:2305.11860]

**Why expected to improve**:
Adaptive-Consistency cuts sample budget up to 7.9x with <0.1% accuracy drop; the same logic applied to panel views reduces mean K (the project's headline compute metric) while the robust median—which is stable once enough views agree—keeps the same P*. This is a compute win, not a metric win (flagged).

**Expected gain**: +0.0 / +0.2 / +0.5 pp 🟡 (metric ~flat by design; **value is ~40-60% fewer forwards/item**)
**Feasibility**: 5/5 🟢
**Effort**: S 🟢

**Implementation sketch**:
1. Make panel generation lazy/sequential; track running median + JSD delta.
2. Stop rule (epsilon, w) fixed a priori; cap at full K.
3. Report mean K and metric delta vs full panel on all 5 benches.

**Risks**:
- Metric-neutral at best — this is an efficiency idea (noted; flagged `marginal` on metric).
- Axis ordering can bias which views are seen first — randomize order by item index.

**Falsification test**: If at the epsilon that cuts mean K by >=30% any bench loses >0.3pp acc or >0.005 JSD vs full panel, early-stop is not free here — keep full K.

## Verification Report — Batch 1

| # | Title (short) | Novelty | Provenance | Feas | Gain (pp) | Falsif | Risk | Comply | Final |
|---|---------------|---------|------------|------|-----------|--------|------|--------|-------|
| 1 | Reliability-weighted median | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +2.0 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 2 | Per-view contextual calibration | EXTENDS ✅ | VERIFIED ✅ | 5/5 | +2.5 🟡 | OK ✅ | MED | PASS | **KEEP (warn)** |
| 3 | Context-removal contrast axis | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +2.5 🟡 | OK ✅ | MED | PASS | **KEEP** |
| 4 | DoLa layer-contrast view | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +1.2 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 5 | Dispersion-temperature P* | EXTENDS ✅ | VERIFIED ✅ | 5/5 | +1.8 🟢 | OK ✅ | LOW | WARN | **KEEP (warn)** |
| 6 | Log-opinion-pool median | NOVEL ✅ | VERIFIED ✅ | 4/5 | +1.2 🟡 | OK ✅ | LOW | PASS | **KEEP** |
| 7 | Dispersion-gated neutral routing | NOVEL ✅ | VERIFIED ✅ | 4/5 | +2.0 🟡 | OK ✅ | MED | WARN | **KEEP (warn)** |
| 8 | Depth-trimmed barycenter | NOVEL ✅ | VERIFIED ✅ | 3/5 | +1.2 🟡 | OK ✅ | MED | PASS | **KEEP** |
| 9 | Robust ordinal W-barycenter | NOVEL ✅ | VERIFIED ✅ | 3/5 | +1.5 🔴 | OK ✅ | MED | WARN | **KEEP (flag)** |
| 10 | Stability early-stop K | EXTENDS ✅ | VERIFIED ✅ | 5/5 | +0.2 🟡 | OK ✅ | LOW | WARN | **KEEP (warn)** |

## Counts
- Verified: 10
- Rejected: 0 (Novelty 0, Provenance 0, Falsification 0, Compliance 0, Other 0)
- Downgraded: 2 (Idea 2 ranking -1 slot after devil's-advocate; Idea 9 gain confidence -> 🔴 per gain-sanity high-variance)
- Re-search cycles used: 0
- Final batch size: 10

## Warnings (per idea)
- Idea 2: instruction-tuned Qwen2.5-7B may already be debiased (contrasting arXiv:2404.08382) — gain on NormAd uncertain; demoted one slot.
- Idea 5: single metric family (distribution-match only); helps DICES/GOQA/VITAL/Scruples, neutral on NormAd by construction.
- Idea 7: single bench + single metric family (NormAd accuracy/macro only).
- Idea 9: distribution-match only; high variance (🔴); meaningful only on ordered label spaces.
- Idea 10: efficiency idea — metric-neutral by design (`marginal`), value is forwards/item reduction.

## Cross-idea consistency
- Near-duplicates collapsed: none. Ideas 6/8/9 all modify the fusion op but are distinct operators (log-pool geometry vs depth-trimmed L-estimator vs ordinal optimal-transport) targeting different metric mixes — **mutually-alternative; ship/compare, don't stack blindly**.
- Contradictions flagged: Idea 10 reduces K while Idea 3/4 add views — not a contradiction (early-stop applies after the enlarged panel is defined; they compose).
- Score-distribution: healthy (feas 3-5; conf mix 🟢/🟡/🔴; not over-confident).

## Notes & warnings
- **Two-metric-family tension (read first)**: a robust point-estimate (median) is ideal for NormAd accuracy but *collapses* the spread that DICES/GOQA/VITAL/Scruples reward. Ideas 5, 9 (and 8's tau dial) specifically restore spread for distribution-match; Ideas 1, 2, 3, 7 target accuracy/de-sycophancy; Ideas 4, 6 help both. Do **not** expect one operator to win both families — the contribution is the *panel of operators* selected per metric, all on the one model.
- **Compliance ✅ single-model hard constraint**: every idea uses ONE frozen model and K post-forward calls; none introduces a second model or fuses distinct models. Ideas 4 (layer contrast) and 10 (early-stop) are extra-lightweight.
- Tier mix observed 40/30/30 vs configured 45/35/20 — within ±10pp bands. T3 at 30% (top of 10-30 band) is intentional: the genuinely novel fusion ops are cross-domain.
- Time windows: <12mo 4, 12-36mo 3, 36-72mo 1, 72+mo 2 — all per-window minimums met (>=2 / >=2 / >=1).
- Source-trust: 8/10 primaries Tier-1/2 (80% >= 60% ✓); Ideas 6 (Genest-Zidek = top journal, T1) excepted, the two T3-trust primaries are recent preprints 2603.07563 and 2601.02970 (flagged).
- Devil's-advocate executed on the top candidate (calibration, Idea 2): arXiv:2404.08382 shows instruction-tuned models are more robust MCQ selectors than assumed -> Idea 2 demoted below Idea 1 (reliability-weighted median) which does not depend on the model being mis-calibrated.
- "EthosAgents 0.242 VITAL" head-to-head figure could **not** be verified from the source abstract (arXiv:2509.10685) — treat the 0.242 target as project-supplied, re-confirm against the paper's tables before claiming a head-to-head win.

## Next steps for user
1. Run Idea 1 (reliability-weighted median) + Idea 5 (dispersion-temperature) together: one helps accuracy, one helps distribution-match, both are cheap and no-op-guarded — fastest path to a both-families lift on the existing cache.
2. Add Idea 4 (DoLa axis) and Idea 2 (per-view calibration) to the panel; ablate axis-by-axis (which axis carries the win — the project's encouraged ablation).
3. Hold Ideas 6/8/9 as a fusion-operator bake-off (mutually alternative); pick per metric family. Hold Idea 10 for the final compute-report once a metric-winning config is fixed.

## Provenance signature
SHA256(inputs + paper IDs + timestamp) = sha256("CultureCommittee-5bench|2102.09690,2309.03882,2410.15393,2404.08382,2506.21590,2502.06233,2307.03111,2305.14739,2210.15097,2309.03883,1706.04599,2402.05070,1177013825,100805741,1310.4375,2603.07563,2505.03523,2404.12464,2202.02950,2601.02970,2305.11860|2026-05-31T07:08:48Z")
