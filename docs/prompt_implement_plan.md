# Prompt For Implementing The CLIMB Slide Redesign

You are implementing a slide-section redesign in the repository:

`/media/mlinh/Kingston/projects/ML/lab-3_LeJEPA/lejepa-MLProject`

Read `docs/plan_climb.md` first. It is the source of truth for the research story, evidence, exclusions, and slide order.

## Non-Negotiable Requirements

- Edit the CLIMB section in `slides/slides_main.tex`; preserve unrelated slides.
- Do not present the story as `Batch 1`, `Batch 2`, or a chronological timeline.
- Do not mention online probe in the redesigned CLIMB slide section.
- Do not include the process diagram `idea -> plan -> train -> eval`.
- Do not use phrases like `13 ideas`, `10 experiments`, or `0/13`.
- Do not use `slides/fig_climb_scatter.pdf` in the redesigned CLIMB section.
- Do not use `slides/fig_climb_overfit.pdf` in the redesigned CLIMB section unless new frozen-eval evidence is added for best pretrain checkpoints; current plan assumes it is removed.
- Do not use `climb_bench/viz/eval_results/batch_2/paperspec_100ep.png` directly because it mixes conv-stem with optimizer/training results.
- Do not claim conv-stem is a LeJEPA objective improvement.
- Do not mix absolute numbers from `ablation_results` with CLIMB baseline around `89.5%`.

## Evidence Contract

All slide claims must be traceable to repository files.

Primary quantitative evidence:

- `climb_bench/viz/eval_results/batch_1/baseline_100.json`: baseline `0.8954`.
- `climb_bench/viz/eval_results/batch_1/idea3_100.json`: coding-rate `0.2673`.
- `climb_bench/viz/eval_results/batch_1/idea4_100.json`: uniformity `0.8888`.
- `climb_bench/viz/eval_results/batch_1/idea7_100.json`: DynTanh `0.5924`.
- `climb_bench/viz/eval_results/batch_2/baseline_100.json`: baseline `0.8949`.
- `climb_bench/viz/eval_results/batch_2/sam_100.json`: SAM `0.8972`.
- `climb_bench/viz/eval_results/batch_2/sdschedule_100.json`: progressive stochastic-depth `0.8950`.
- `climb_bench/viz/eval_results/batch_2/pcgrad_100.json`: PCGrad `0.8944`.
- `climb_bench/viz/eval_results/batch_2/swa_100.json`: SWA `0.8911`.
- `climb_bench/viz/eval_results/batch_2/qknorm_100.json`: QK-Norm `0.8909`.
- `climb_bench/viz/eval_results/batch_2/deepsup_100.json`: deep supervision `0.8894`.
- `climb_bench/viz/eval_results/batch_2/schedulefree_100.json`: Schedule-Free `0.8872`.
- `climb_bench/viz/eval_results/batch_2/llrd_100.json`: LLRD `0.8616`.
- `climb_bench/viz/eval_results/batch_2/muon_100.json`: Muon `0.8574`.
- `climb_bench/viz/eval_results/batch_2/convstem_100.json`: conv-stem `0.9208`.

Mechanism / interpretation evidence:

- `climb_bench/batch1/_variants.py`
- `climb_bench/batch2/_variants.py`
- `climb_bench/ideation/batch-1.md`
- `climb_bench/ideation/batch-2.md`
- `climb_bench/tracker/batch1-analysis.md`
- `climb_bench/tracker/batch2-analysis.md`
- `climb_bench/viz/eval-frozen-paperspec.py`

## Batch 1 - Prepare Figures And Data Tables

Goal:

- Create slide-ready visual evidence for the redesigned CLIMB story.

Files to edit or create:

- Create `slides/fig_climb_objective_bars.tex`.
- Compile it to `slides/fig_climb_objective_bars.pdf`.
- Create or update `slides/fig_climb_optbars.tex` so it is optimizer/training-only and excludes conv-stem.
- Compile it to `slides/fig_climb_optbars.pdf`.
- Create `slides/fig_climb_convstem.tex`.
- Compile it to `slides/fig_climb_convstem.pdf`.

Steps:

1. Build an objective/head chart:
   - baseline `89.54%`;
   - uniformity `88.88%`;
   - DynTanh `59.24%`;
   - coding-rate `26.73%`.
2. Build an optimizer/training chart excluding conv-stem:
   - SAM `+0.23pp`;
   - progressive stochastic-depth `+0.01pp`;
   - PCGrad `-0.05pp`;
   - SWA `-0.38pp`;
   - QK-Norm `-0.40pp`;
   - deep supervision `-0.55pp`;
   - Schedule-Free `-0.77pp`;
   - LLRD `-3.33pp`;
   - Muon `-3.75pp`.
3. Build a conv-stem chart:
   - baseline `89.49%`;
   - conv-stem `92.08%`;
   - delta `+2.59pp`.
4. Keep visual style consistent with the deck colors already defined in `slides/slides_main.tex`.

Completion criteria:

- The three PDFs exist in `slides/`.
- The optimizer chart does not include conv-stem.
- No chart depends on online-probe values.

Expected output:

- `slides/fig_climb_objective_bars.pdf`
- `slides/fig_climb_optbars.pdf`
- `slides/fig_climb_convstem.pdf`

Important notes:

- Use one or two decimal places in plotted percentages.
- If compiling standalone TeX figures creates `.aux` / `.log` files, leave them unless the repository conventions say otherwise.

Do not change:

- Do not edit the paper/theory sections.
- Do not delete existing generated artifacts unless explicitly instructed.

## Batch 2 - Rewrite The CLIMB Section In `slides/slides_main.tex`

Goal:

- Replace the current CLIMB section with a six-slide research-story section.

File to edit:

- `slides/slides_main.tex`

Steps:

1. Locate the section beginning around:
   - `\section{Nghiên cứu mở rộng: Benchmark Climb trên Imagenette}`
   - and ending before the conclusion frame.
2. Replace the current CLIMB frames with exactly these six conceptual slides:
   - Slide 1: `Cau hoi nghien cuu: headroom con nam o dau?`
   - Slide 2: `Huong 1: Objective va representation head`
   - Slide 3: `Insight huong 1: SIGReg + MLP projector la diem can bang`
   - Slide 4: `Huong 2: Optimizer va training geometry`
   - Slide 5: `Conv-stem: architecture co-design rieng`
   - Slide 6: `Tong hop: LeJEPA objective da rat kho cai tien tren fixed ViT-S`
3. Slide 1 must introduce the two research hypotheses:
   - objective / representation head;
   - training geometry / optimizer / backbone inductive bias.
4. Slide 2 must include the objective/head chart or table and interpret:
   - uniformity near but below baseline;
   - DynTanh failure;
   - coding-rate collapse.
5. Slide 3 must explain the insight:
   - SIGReg + MLP projector is a strong and fragile balance;
   - stronger auxiliary geometry can conflict with the baseline;
   - projector normalization is not a disposable detail.
6. Slide 4 must include the optimizer/training chart and interpret mechanism groups:
   - flat minima / regularization schedule: SAM, SWA, progressive stochastic-depth;
   - optimizer replacement: Muon, Schedule-Free, LLRD;
   - gradient geometry: PCGrad;
   - attention / intermediate conditioning: QK-Norm, deep supervision.
7. Slide 5 must present conv-stem as its own track:
   - cite Xiao et al. 2021 or mention the paper title on the slide;
   - explain the 4-conv stem replacing stride-16 patchify;
   - report `89.49% -> 92.08%`, `+2.59pp`;
   - explicitly state this targets backbone inductive bias, not the LeJEPA objective.
8. Slide 6 must synthesize:
   - fixed ViT-S objective/head and optimizer paths have no clear winner;
   - architecture co-design has headroom;
   - missing evidence: multi-seed, params/FLOPs, same-stem non-LeJEPA baselines, frozen eval for best pretrain checkpoint if overfit is discussed.

Completion criteria:

- No CLIMB slide title contains `Batch`.
- No CLIMB slide contains `online probe`.
- No CLIMB slide contains `13 ideas`, `10 experiments`, or `0/13`.
- The process diagram is removed.
- `fig_climb_scatter.pdf` is no longer included in the CLIMB section.
- `fig_climb_overfit.pdf` is no longer included in the CLIMB section.
- Conv-stem is not included in the optimizer-only chart.

Expected output:

- Updated `slides/slides_main.tex`.

Important notes:

- Keep the surrounding deck structure intact.
- Keep slide text concise and analysis-driven.
- Put charts next to the analysis they support.
- Prefer Vietnamese slide text matching the current deck style.

Do not change:

- Do not alter root package code.
- Do not alter CLIMB experiment code.
- Do not reframe results as a universal conclusion beyond the observed setup.

## Batch 3 - References

Goal:

- Ensure the conv-stem source is available and cited correctly.

Files to inspect/edit:

- `slides/references.bib`
- `slides/slides_main.tex`

Steps:

1. Check whether Xiao et al., `Early Convolutions Help Transformers See Better`, NeurIPS 2021, is already in `slides/references.bib`.
2. If missing, add a BibTeX entry.
3. Add a citation on the conv-stem slide only, or a short textual source mention if the deck style avoids citations in that section.

Completion criteria:

- The conv-stem idea has a traceable source in the slide or bibliography.
- No unrelated bibliography churn.

Expected output:

- Possibly updated `slides/references.bib`.
- Conv-stem slide source mention or citation.

Do not change:

- Do not add broad or unrelated references.

## Batch 4 - Verification

Goal:

- Build and verify the redesigned slide section.

Commands:

Run from `slides/`:

```bash
pdflatex slides_main.tex
bibtex slides_main
pdflatex slides_main.tex
pdflatex slides_main.tex
```

Checks:

1. Search the CLIMB section of `slides/slides_main.tex` for banned terms:
   - `Batch 1`
   - `Batch 2`
   - `online probe`
   - `13 ideas`
   - `10 experiments`
   - `0/13`
2. Confirm `fig_climb_scatter.pdf` is no longer included.
3. Confirm `fig_climb_overfit.pdf` is no longer included in the CLIMB section.
4. Confirm all numbers on slides match JSON evidence:
   - objective/head values from `batch_1`;
   - optimizer/training values from `batch_2`;
   - conv-stem values from `batch_2`.
5. Inspect the generated PDF around the CLIMB section:
   - no overlapping text;
   - charts legible;
   - conv-stem caveat visible;
   - story reads as research insight rather than timeline.

Completion criteria:

- `slides/slides_main.pdf` builds successfully.
- CLIMB section has six coherent slides.
- All quantitative claims are traceable.
- No banned process/timeline/online-probe framing remains.

Expected output:

- Updated `slides/slides_main.pdf`.
- Any generated figure PDFs required by the section.

Important notes:

- The repository already has generated slide artifacts; do not delete them unless instructed.
- If LaTeX emits non-fatal warnings, record only material warnings that affect rendering or bibliography.

Do not change:

- Do not run destructive git commands.
- Do not revert user changes.

## Final Acceptance Checklist

- `docs/plan_climb.md` exists and documents the full blueprint.
- `docs/prompt_implement_plan.md` exists and can be handed to another coding agent.
- The eventual slide implementation uses two research directions plus separate conv-stem track.
- Every claim is evidence-backed.
- The story prioritizes insight over process.
