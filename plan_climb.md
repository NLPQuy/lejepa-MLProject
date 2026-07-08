# Blueprint Redesign: CLIMB Research Extension Slides

## Executive Summary

This plan redesigns the CLIMB section in `slides/slides_main.tex` as a research story, not an execution timeline. The section should be rebuilt around two research directions and one separate architecture co-design track.

Core evidence:

- Fixed-backbone LeJEPA baseline is already strong under the frozen linear evaluation used by the paper-style evaluation script:
  - `climb_bench/viz/eval_results/batch_1/baseline_100.json`: top1 `0.8954` (`89.54%`).
  - `climb_bench/viz/eval_results/batch_2/baseline_100.json`: top1 `0.8949` (`89.49%`).
- Objective / representation-head changes did not beat baseline:
  - uniformity: `0.8888`, `-0.66pp` vs batch-1 baseline.
  - DynTanh projector: `0.5924`, `-30.30pp`.
  - coding-rate: `0.2673`, collapse.
- Optimizer / training-geometry changes produced no robust headroom:
  - SAM: `0.8972`, only `+0.23pp`.
  - progressive stochastic-depth: `0.8950`, only `+0.01pp`.
  - PCGrad, SWA, QK-Norm, deep supervision, Schedule-Free, LLRD, and Muon were below baseline.
- Conv-stem is the only clear positive result:
  - `climb_bench/viz/eval_results/batch_2/convstem_100.json`: top1 `0.9208`, `+2.59pp`.
  - It replaces the ViT patch embedding with a convolutional stem, so it must be presented as a separate architecture co-design result, not as a LeJEPA objective improvement.

The redesigned slide section should remove:

- batch/timeline framing (`Batch 1`, `Batch 2`, `13 ideas`, `10 experiments`);
- online-probe discussion;
- the idea -> plan -> train -> eval process diagram;
- standalone measurement lesson slide about online probe inconsistency;
- charts whose main claim depends on online-probe deltas.

## New Research Story

### Slide 1: Research Question - Where Is The Remaining Headroom?

Purpose:

- Open the CLIMB section with the research question rather than a process summary.
- Establish that the project tested whether LeJEPA can be improved in a low-data Imagenette / local ImageNet-10 setup while keeping the frozen ViT-S evaluation protocol fixed.

Content:

- Title: `Cau hoi nghien cuu: headroom con nam o dau?`
- State two hypotheses:
  - **Direction 1: Objective / representation head.** Maybe SIGReg needs an additional geometry signal or a better projector/head.
  - **Direction 2: Training geometry / optimizer / backbone inductive bias.** Maybe the objective is fine, but training dynamics or the ViT input stem limits performance.
- Include a compact evaluation contract:
  - frozen backbone;
  - concat CLS from the last two layers + LayerNorm;
  - linear classifier with AdamW;
  - report top1 / delta against the local baseline.
- Mention baseline once:
  - batch-1 baseline `89.54%`;
  - batch-2 baseline `89.49%`.

Why:

- This reframes the section as a hypothesis-driven investigation.
- It prevents the audience from reading the section as a chronological log.
- It avoids over-explaining the paper-style eval recipe while still making the metric clear.

Evidence:

- `climb_bench/viz/eval-frozen-paperspec.py` documents the frozen eval protocol.
- `climb_bench/viz/eval_results/batch_1/baseline_100.json`
- `climb_bench/viz/eval_results/batch_2/baseline_100.json`

### Slide 2: Direction 1 - Objective And Representation Head

Purpose:

- Show that the first research direction tried to add or alter the representation geometry directly.
- Place quantitative results next to the analysis.

Content:

- Title: `Huong 1: Objective va representation head`
- Use a small bar chart or table with frozen linear top1:

| Experiment | Goal | Hypothesis | Result | Conclusion |
|---|---|---|---:|---|
| baseline_100 | Anchor fixed ViT-S LeJEPA | Existing SIGReg + invariance is the reference | `89.54%` | Strong baseline |
| idea4_100 uniformity | Add pairwise spread on projections | Explicit hypersphere uniformity may complement SIGReg | `88.88%` (`-0.66pp`) | Near baseline but not a win |
| idea7_100 DynTanh | Replace projector BatchNorm with DynTanh | Energy-preserving normalization may improve JEPA-style features | `59.24%` (`-30.30pp`) | Large failure; projector normalization is sensitive |
| idea3_100 coding-rate | Add log-det / full-rank volume signal | Full covariance volume may fight dimensional collapse faster than sliced marginal tests | `26.73%` | Collapse; term likely too strong or conflicts with SIGReg |

Suggested figure:

- New `slides/fig_climb_objective_bars.tex` / `.pdf`, generated from:
  - `climb_bench/viz/eval_results/batch_1/baseline_100.json`
  - `idea3_100.json`
  - `idea4_100.json`
  - `idea7_100.json`
- Bars should be sorted by performance or arranged baseline first, then tested ideas.
- Annotate coding-rate as `collapse`, not merely a lower bar.

Why:

- The slide answers: what was tried, why it was tried, what happened, and what insight follows.
- It avoids listing idea counts.
- It keeps figure and analysis side by side.

Evidence:

- `climb_bench/batch1/_variants.py` documents the mechanisms.
- `climb_bench/ideation/batch-1.md` documents the original hypotheses and citations.
- `climb_bench/tracker/batch1-analysis.md` explains the observed behavior.
- Frozen eval JSON files under `climb_bench/viz/eval_results/batch_1/`.

### Slide 3: Insight From Direction 1

Purpose:

- Convert the negative results into a research insight.

Content:

- Title: `Insight huong 1: SIGReg + MLP projector la diem can bang`
- Main message:
  - The baseline already balances invariance and distribution matching well.
  - Adding a mild global-spread term (uniformity) does not beat the baseline.
  - Adding a strong volume term (coding-rate) can destabilize training / collapse the representation.
  - Replacing projector normalization with DynTanh fails badly, implying the projector is not a disposable detail.
- Avoid:
  - online probe claims;
  - overfit / best-checkpoint claims;
  - `0/3 ideas` phrasing.

Why:

- The section should communicate research learning, not only scores.
- This is the best place to explain successful falsification: the initial hypothesis was plausible, but evidence says SIGReg's existing projector interface is fragile and already effective.

Evidence:

- Same batch-1 sources as Slide 2.
- `climb_bench/viz/figures/batch_1/ranking.csv` and `summary.csv` can be used only as supporting diagnostics, not as headline slide metrics.

### Slide 4: Direction 2 - Optimizer And Training Geometry

Purpose:

- Show that the second research direction tested whether training dynamics, optimizer choice, gradient geometry, or attention/depth supervision can unlock more performance while preserving the ViT-S body.

Content:

- Title: `Huong 2: Optimizer va training geometry`
- Use an optimizer-only bar chart from frozen eval deltas vs baseline. Exclude conv-stem from this chart.

| Experiment | Goal | Hypothesis | Frozen top1 | Delta | Insight |
|---|---|---|---:|---:|---|
| baseline_100 | Anchor | Stock AdamW + cosine + ViT-S | `89.49%` | -- | Strong local anchor |
| SAM | flatter minima | Low-data ViT may benefit from sharpness-aware updates | `89.72%` | `+0.23pp` | Near baseline, not a robust win |
| progressive stochastic-depth | regularization schedule | Ramp regularization as overfit risk rises | `89.50%` | `+0.01pp` | Equivalent to baseline |
| PCGrad | reduce invariance/SIGReg gradient conflict | Project conflicting gradients | `89.44%` | `-0.05pp` | Conflict handling does not improve final features |
| SWA | average tail weights | Flatter averaged weights improve frozen features | `89.11%` | `-0.38pp` | Averaging tail does not help here |
| QK-Norm | stabilize attention logits | Attention normalization improves ViT training | `89.09%` | `-0.40pp` | Attention stabilization gives no headroom |
| deep supervision | shorten gradients to intermediate layers | Auxiliary intermediate losses improve feature hierarchy | `88.94%` | `-0.55pp` | Slightly harmful |
| Schedule-Free | remove cosine schedule dependency | Averaged optimizer improves anytime solution | `88.72%` | `-0.77pp` | Worse than cosine baseline |
| LLRD | tune per-layer adaptation | Slow early layers, adapt late layers | `86.16%` | `-3.33pp` | Clearly harmful |
| Muon | orthogonalized matrix updates | More isotropic updates may improve representation rank | `85.74%` | `-3.75pp` | Clearly harmful |

Suggested figure:

- Reuse or redraw `slides/fig_climb_optbars.pdf` as optimizer-only.
- If redrawing, source data from `climb_bench/viz/eval_results/batch_2/*.json`.
- Do not include conv-stem on this optimizer chart.

Why:

- The slide groups ideas by research mechanism:
  - flat minima / regularization schedule: SAM, SWA, progressive stochastic-depth;
  - optimizer replacement: Muon, Schedule-Free, LLRD;
  - objective gradient geometry: PCGrad;
  - attention / intermediate conditioning: QK-Norm, deep supervision.
- It answers what each group was meant to fix and what the evidence says.

Evidence:

- `climb_bench/batch2/_variants.py`
- `climb_bench/ideation/batch-2.md`
- `climb_bench/tracker/batch2-analysis.md`
- `climb_bench/viz/eval_results/batch_2/*.json`

### Slide 5: Conv-Stem As Separate Architecture Co-Design

Purpose:

- Give conv-stem the separate treatment requested because it is the only clear positive result.
- Explain why it is both valuable and not directly attributable to a better LeJEPA objective.

Content:

- Title: `Conv-stem: architecture co-design rieng`
- Source idea:
  - Xiao et al., `Early Convolutions Help Transformers See Better`, NeurIPS 2021.
  - The idea is that early convolutions inject locality / translation bias that bare ViT patchify lacks.
- Intervention:
  - Replace the single stride-16 patchify layer with a four-convolution stem.
  - Keep the ViT body, token geometry, and CLS readout compatible with the evaluation script.
- Result:
  - baseline `89.49%`;
  - conv-stem `92.08%`;
  - delta `+2.59pp`.
- Interpretation:
  - This is a real empirical improvement.
  - It targets backbone inductive bias, not LeJEPA's SIGReg/invariance objective.
  - It is an architecture co-design insight: low-data SSL benefits from local visual bias before transformer blocks.
- Caveat:
  - No params/FLOPs report found in the current evidence.
  - No re-baseline of other SSL methods with the same conv-stem found.
  - Therefore it cannot be claimed as a LeJEPA-specific objective improvement.

Suggested figure:

- New `slides/fig_climb_convstem.tex` / `.pdf`, side-by-side:
  - baseline `89.49%`;
  - conv-stem `92.08%`.
- Include a small visual schematic: `patchify conv` -> `4-conv stem` -> `same ViT body`.
- Keep the chart close to the explanation.

Why:

- The user explicitly requested conv-stem as its own track.
- It is the only result higher than baseline by a large enough margin to be visually emphasized.
- It also needs a credibility/caveat block so the audience does not over-attribute the gain.

Evidence:

- `climb_bench/ideation/batch-2.md`, section `Idea 6: Early convolutional stem for ViT-S`.
- `climb_bench/batch2/_variants.py`, `ConvStem` and `apply_conv_stem`.
- `climb_bench/viz/eval-frozen-paperspec.py`, evaluation-side `ConvStem` rebuild.
- `climb_bench/viz/eval_results/batch_2/convstem_100.json`.
- `climb_bench/tracker/batch2-analysis.md`, conv-stem caveat.

### Slide 6: Synthesis - What Did We Learn?

Purpose:

- Close the section with research insight and remaining evidence gaps.

Content:

- Title: `Tong hop: LeJEPA objective da rat kho cai tien tren fixed ViT-S`
- Main synthesis:
  - Under fixed ViT-S, neither objective/head add-ons nor optimizer/training-geometry changes produced a reliable winner over the strong baseline.
  - The objective/head failures are informative: projector design is sensitive, and strong auxiliary geometry terms can fight the baseline.
  - The optimizer/training failures are informative: training dynamics were not the main bottleneck under this setup.
  - The positive headroom appears in architecture co-design: conv-stem improves low-data ViT representations, but needs a separate evaluation track.
- Evidence-needed callout:
  - multi-seed runs;
  - conv-stem params/FLOPs;
  - conv-stem with non-LeJEPA baselines or supervised/SSL controls;
  - frozen eval of best pretrain checkpoint if discussing overfit or early stopping.

Why:

- The slide turns negative results into a scientific conclusion.
- It avoids a fake "winner" narrative.
- It identifies actionable next work without claiming unsupported results.

## Mapping All CLIMB Experiments

### Direction 1: Objective / Representation Head

| File / tag | Intervention | Goal | Hypothesis | Metric | Result | Conclusion | Slide insight |
|---|---|---|---|---|---:|---|---|
| `batch_1/baseline_100` | Stock LeJEPA fixed ViT-S | Establish local anchor | SIGReg + invariance is baseline | frozen linear top1 | `0.8954` | Strong baseline | Reference point |
| `batch_1/idea3_100` | coding-rate log-det term | Increase full-rank volume | Full covariance volume may complement sliced tests | frozen linear top1 | `0.2673` | Collapse | Strong auxiliary geometry term can destroy features |
| `batch_1/idea4_100` | uniformity loss | Add pairwise spread | Hypersphere uniformity may improve feature spread | frozen linear top1 | `0.8888` | Slightly below baseline | Mild spread does not beat SIGReg baseline |
| `batch_1/idea7_100` | DynTanh projector | Preserve feature energy / remove BN dependency | DynTanh may improve JEPA projector behavior | frozen linear top1 | `0.5924` | Large failure | Projector normalization is sensitive |

### Direction 2: Training Geometry / Optimizer / Conditioning

| File / tag | Intervention | Goal | Hypothesis | Metric | Result | Conclusion | Slide insight |
|---|---|---|---|---|---:|---|---|
| `batch_2/baseline_100` | Stock LeJEPA fixed ViT-S | Establish local anchor | Stock training recipe is baseline | frozen linear top1 | `0.8949` | Strong baseline | Reference point |
| `batch_2/sam_100` | SAM | Seek flatter minima | Sharpness-aware updates improve small-data ViT generalization | frozen linear top1 | `0.8972` | Near baseline | Small positive, not robust enough as winner |
| `batch_2/sdschedule_100` | progressive stochastic-depth | Schedule regularization | Ramp drop-path with training progress | frozen linear top1 | `0.8950` | Equivalent baseline | No meaningful headroom |
| `batch_2/pcgrad_100` | PCGrad | Resolve loss-term gradient conflicts | Invariance and SIGReg gradients may fight | frozen linear top1 | `0.8944` | No improvement | Gradient surgery unnecessary here |
| `batch_2/swa_100` | SWA | Average tail weights | Averaging gives flatter frozen features | frozen linear top1 | `0.8911` | Below baseline | Tail averaging not useful in this run |
| `batch_2/qknorm_100` | QK-Norm | Stabilize ViT attention | Attention-logit normalization improves ViT pretraining | frozen linear top1 | `0.8909` | Below baseline | Attention stability not the bottleneck |
| `batch_2/deepsup_100` | deep supervision | Improve intermediate features | Auxiliary losses help lower layers | frozen linear top1 | `0.8894` | Below baseline | Intermediate auxiliary objective slightly hurts |
| `batch_2/schedulefree_100` | Schedule-Free AdamW | Remove schedule brittleness | Schedule-free averaging beats cosine | frozen linear top1 | `0.8872` | Below baseline | Cosine AdamW remains better here |
| `batch_2/llrd_100` | layer-wise LR decay | Better per-layer adaptation | Late layers should adapt faster than early layers | frozen linear top1 | `0.8616` | Clear failure | LLRD is harmful for this pretrain setup |
| `batch_2/muon_100` | Muon optimizer | More isotropic matrix updates | Orthogonalized updates improve rank / separability | frozen linear top1 | `0.8574` | Clear failure | Optimizer transfer does not work here |

### Separate Track: Architecture Co-Design

| File / tag | Intervention | Goal | Hypothesis | Metric | Result | Conclusion | Slide insight |
|---|---|---|---|---|---:|---|---|
| `batch_2/convstem_100` | 4-layer convolutional stem | Add local visual inductive bias before ViT body | Early convolutions improve data-efficient ViT training | frozen linear top1 | `0.9208` | Clear positive | Real architecture gain, not a LeJEPA-objective win |

## Parts To Remove From The Current Slide Section

Remove or replace the following from `slides/slides_main.tex`:

- The process diagram `Ideation -> Plan -> Train -> Eval`.
- Any `Batch 1` / `Batch 2` framing in slide titles or main text.
- Any summary based on idea counts, such as `13 ideas`, `10 ideas`, `0/13`.
- The slide titled `Bai Hoc Do Luong: Probe Online Khong Nhat Quan Voi Recipe Paper`.
- Online-probe interpretation and `fig_climb_scatter.pdf`.
- `fig_climb_overfit.pdf` from the main CLIMB story, because the requested story should not discuss online probe or claim `+2.4pp` best-checkpoint without frozen-eval evidence for the best pretrain checkpoint.
- Any claim that optimizer results are a universal failure beyond this setup.
- Any claim that conv-stem proves LeJEPA objective superiority.

## Figures And Tables To Use

Use:

- New objective/head bar chart from `climb_bench/viz/eval_results/batch_1/*.json`.
- New optimizer-only delta chart from `climb_bench/viz/eval_results/batch_2/*.json`, excluding `convstem_100`.
- New conv-stem comparison chart from:
  - `climb_bench/viz/eval_results/batch_2/baseline_100.json`
  - `climb_bench/viz/eval_results/batch_2/convstem_100.json`
- Existing `slides/fig_climb_optbars.pdf` only if it is regenerated or verified to exclude conv-stem and match frozen eval deltas.

Do not use directly:

- `climb_bench/viz/eval_results/batch_2/paperspec_100ep.png`, because it mixes conv-stem with optimizer/training results.
- `slides/fig_climb_scatter.pdf`, because it is about online-vs-frozen eval mismatch.
- `slides/fig_climb_overfit.pdf`, because it supports an online/checkpoint-selection story that should not be part of the redesigned CLIMB section.

## Evidence Gaps And Contradictions

- Online metrics contradict frozen evaluation for some runs:
  - QK-Norm, PCGrad, SWA, and uniformity can look neutral or lightly positive online but do not survive frozen linear evaluation.
  - Per user instruction, do not present online-probe analysis in the slide section.
- No multi-seed evidence was found for CLIMB batch results.
- No frozen evaluation of best pretrain checkpoint was found; avoid claiming `best-checkpoint +2.4pp` as a slide result.
- Conv-stem has no params/FLOPs table in the discovered evidence.
- Conv-stem has no non-LeJEPA or same-stem method re-baseline in the discovered evidence.
- `ablation_results` uses a different harness and has an anchor around `59.46%`; do not mix its absolute scores with CLIMB baseline around `89.5%`.
- `ablation_results` structural conclusions can be mentioned only if explicitly marked as a separate harness, but the redesigned CLIMB section should prioritize `climb_bench` evidence.

## Files Used For Evidence

- `slides/slides_main.tex`
- `slides/fig_climb_optbars.tex`
- `slides/fig_climb_overfit.tex`
- `slides/fig_climb_scatter.tex`
- `climb_bench/tracker/batch1-analysis.md`
- `climb_bench/tracker/batch2-analysis.md`
- `climb_bench/tracker/analysis_template.md`
- `climb_bench/tracker/ablation-measured-analysis.md`
- `climb_bench/ideation/batch-1.md`
- `climb_bench/ideation/batch-2.md`
- `climb_bench/ideation/plan-batch-2.md`
- `climb_bench/ideation/batch-3.md`
- `climb_bench/viz/eval_results/batch_1/baseline_100.json`
- `climb_bench/viz/eval_results/batch_1/idea3_100.json`
- `climb_bench/viz/eval_results/batch_1/idea4_100.json`
- `climb_bench/viz/eval_results/batch_1/idea7_100.json`
- `climb_bench/viz/eval_results/batch_2/baseline_100.json`
- `climb_bench/viz/eval_results/batch_2/convstem_100.json`
- `climb_bench/viz/eval_results/batch_2/deepsup_100.json`
- `climb_bench/viz/eval_results/batch_2/llrd_100.json`
- `climb_bench/viz/eval_results/batch_2/muon_100.json`
- `climb_bench/viz/eval_results/batch_2/pcgrad_100.json`
- `climb_bench/viz/eval_results/batch_2/qknorm_100.json`
- `climb_bench/viz/eval_results/batch_2/sam_100.json`
- `climb_bench/viz/eval_results/batch_2/schedulefree_100.json`
- `climb_bench/viz/eval_results/batch_2/sdschedule_100.json`
- `climb_bench/viz/eval_results/batch_2/swa_100.json`
- `climb_bench/viz/figures/batch_1/summary.csv`
- `climb_bench/viz/figures/batch_1/ranking.csv`
- `climb_bench/viz/figures/batch_1/matched_400.csv`
- `climb_bench/viz/figures/batch_2/summary.csv`
- `climb_bench/viz/figures/batch_2/ranking.csv`
- `climb_bench/viz/metric_results/batch_1/*/metrics.csv`
- `climb_bench/viz/metric_results/batch_2/*/metrics.csv`
- `climb_bench/batch1/_variants.py`
- `climb_bench/batch2/_variants.py`
- `climb_bench/viz/eval-frozen-paperspec.py`
- `climb_bench/viz/run-eval-paperspec.py`
- `climb_bench/viz/viz_metrics.py`
- `climb_bench/viz/viz_paperspec.py`
- `ablation_results/ablation_summary.md`
- `ablation_results/ablation_summary.csv`

## Implementation Defaults

- Create a six-slide CLIMB section.
- Use Vietnamese slide titles and concise Vietnamese body text.
- Keep numbers as percentages with one or two decimals, e.g. `89.5%`, `92.1%`, `+2.6pp`.
- Use `frozen linear eval` or equivalent wording in slide text; avoid repeatedly saying `paper-spec recipe`.
- Keep all claims traceable to the files listed above.
- Do not silently rewrite paper claims outside the CLIMB section.
