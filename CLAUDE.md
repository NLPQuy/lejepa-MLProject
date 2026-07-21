# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. It incorporates Andrej Karpathy's behavioral guidelines to reduce common LLM coding mistakes.

## Fast Q&A Mode (nguyên tắc trả lời nhanh)

**Khi câu hỏi chỉ là tra cứu / hỏi-đáp về repo này ("X ở đâu?", "cái Y là gì?", "chạy Z thế nào?", "tham số nào?") — trả lời NGAY, ngắn gọn, không suy nghĩ dài dòng.**
- Ưu tiên trả lời thẳng từ chỉ mục dưới đây; chỉ mở file/`grep` khi index không đủ hoặc cần con số/chi tiết chính xác.
- 1–3 câu hoặc một bảng nhỏ là đủ. Không mở đầu rào đón, không liệt kê phương án không dùng đến.
- Kèm đường dẫn file clickable (`path:line`) để người đọc tự nhảy tới.
- Không xác minh lại điều index/CLAUDE.md đã khẳng định trừ khi sắp **sửa** nó hoặc nghi ngờ đã cũ.
- Chế độ nhanh **chỉ** áp dụng cho hỏi-đáp/tra cứu. Khi **viết/sửa code** thì quay lại đầy đủ Karpathy Guidelines bên dưới (think-before-coding, verify).

## Chỉ mục CLAUDE.md (mục lục tra cứu)

| Mục | Nội dung tra nhanh |
|-----|--------------------|
| [Karpathy Guidelines](#karpathy-guidelines-for-claude) | 4 quy tắc hành vi khi code: think-before, simplicity, surgical, goal-driven |
| [Overview](#overview) | LeJEPA = SIGReg (arXiv:2511.08544); 4 thành phần repo: `lejepa/`, `stable-pretraining/`, `train_eval_vit_b.py`, `scripts/` |
| [Installation](#installation) | `pip install -e .`; harness: `cd stable-pretraining && pip install -e .` |
| [Running Tests](#running-tests) | `pytest tests/` (chỉ `lejepa/`); `stable-pretraining/` có pytest.ini riêng |
| [Architecture › Core idea](#core-idea) | Loss = `λ·SIGReg + (1−λ)·Invariance`; λ ≈ 0.01–0.1 |
| [`lejepa/` package](#lejepa-package) | `univariate` (EppsPulley + bạn bè) · `multivariate` (SlicingUnivariateTest, BHEP…) |
| [Dual EppsPulley](#dual-eppspulley-implementations) | 2 bản độc lập: `lejepa.univariate` vs `stable_pretraining.methods.lejepa` |
| [`stable-pretraining/`](#stable-pretraining-package) | Bảng module: Module, Manager, data/, backbone/, callbacks/, methods/lejepa.py |
| [LeJEPA model API](#lejepa-model-api-train-vs-eval) | Train: `global_views=/local_views=` · Eval: `images=` → `.embedding` |
| [Training entry points](#training-entry-points) | Minimal · ablation runner · Kaggle `train_eval_vit_b.py` |
| [Key Hyperparameters](#key-hyperparameters) | λ, lr, weight_decay, num_slices, n_points, V, precision, sigreg_target |
| [Research track: `climb_bench/`](#research-track-climb_bench) | Pipeline 6 bước Imagenette; batch-7 bỏ online probe; leobench |
| [SIGReg ablation study (PAUSED)](#sigreg-ablation-study-hyperparameters--components--status--follow-ups-paused) | Đã chạy/lên slides; pipeline under-fit; follow-up: fix aug trước |

## Tra "X ở đâu?" (file → vai trò)

| Cần gì | Ở đâu |
|--------|-------|
| Class model LeJEPA (backbone+projector+loss) | `stable-pretraining/stable_pretraining/methods/lejepa.py` |
| EppsPulley bản thư viện | `lejepa/univariate/` (`epps_pulley.py`) |
| Slicing wrapper cho embedding cao chiều | `lejepa/multivariate/` (`SlicingUnivariateTest`) |
| Chạy ablation (render/list/summarize) | `scripts/ablations.py` + `scripts/ablations/specs.py::BASE_OVERRIDES` |
| Runner train ablation local | `scripts/train_lejepa_ablation.py` (self-patch sys.path) |
| Baseline trainer climb_bench | `climb_bench/batch1/_common.py`; batch-7: `climb_bench/batch7/_common.py` |
| Variant classes đúng (đã verify Phase-0) | `climb_bench/batch7/_variants.py` (KLScoreSIGReg, FMSIGRegB) |
| ⚠️ Variant file cũ (frozen, 2/5 SAI) | `stable_pretraining/methods/lejepa_variants.py` — **đừng copy từ đây** |
| Phase-0 gate (test objective ~1 phút CPU) | `climb_bench/batch7/test_statistics.py` |
| Eval paper-spec frozen probe | `climb_bench/viz/eval-frozen-paperspec.py`; runner Kaggle: `run-eval-paperspec.py` |
| Viz kết quả (curves/bars) | `climb_bench/viz/viz_metrics.py`, `viz_paperspec.py` |
| Findings mỗi batch | `climb_bench/tracker/batch<N>-analysis.md` |
| Slides chính (build xelatex) | `slides/slides_main.tex`; hình ở `slides/figures/` |
| Kết quả ablation đã gộp | `ablation_results/` (+ `ablation_summary.{csv,md}`) |

## Karpathy Guidelines for Claude
**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.
When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"
For multi-step tasks, state a brief plan:
`1. [Step] → verify: [check]`
Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

## Overview

**LeJEPA** is a self-supervised learning library implementing *Sketched Isotropic Gaussian Regularization* (**SIGReg**), the core objective of the paper [arXiv:2511.08544](https://arxiv.org/abs/2511.08544). The repository contains:
- `lejepa/` — the pip-installable core library of statistical tests
- `stable-pretraining/` — a PyTorch Lightning training harness (separate package)
- `train_eval_vit_b.py` — a Kaggle/Colab-oriented training script for ViT-B/16 on ImageNet-1K
- `scripts/` — Hydra-based sweep launchers

## Installation

```bash
# Core library only
pip install lejepa

# Or from source
pip install -e .

# Training harness (needed for scripts/train_lejepa_ablation.py and train_eval_vit_b.py)
cd stable-pretraining && pip install -e .

# Minimal example dependencies
pip install torch torchvision timm wandb hydra-core datasets huggingface-hub
```

## Running Tests

```bash
# All tests (root-level, for the lejepa package)
pytest tests/

# Single test file
pytest tests/test_epps_pulley.py

# Single test class / function
pytest tests/test_epps_pulley.py::TestEppsPulley::test_standard_normal_samples_low_statistic

# stable-pretraining tests (separate test suite with pytest.ini)
cd stable-pretraining && pytest
```

The root `tests/` suite covers only the `lejepa/` package. The `stable-pretraining/` suite is independent with its own `pytest.ini`.

## Architecture

### Core idea

The LeJEPA training loss is:

```
LeJEPA_loss = λ · SIGReg(proj) + (1 − λ) · Invariance(proj)
```

where:
- **Invariance loss** — forces multi-view projections to agree: `(proj.mean(0) - proj).square().mean()`
- **SIGReg** — regularizes projections toward N(0, I) using a univariate ECF (empirical characteristic function) test applied across random 1-D slices of the embedding space

`λ` is the single tunable hyperparameter (typically `0.01–0.1`).

### `lejepa/` package

Two submodules, both exposing `torch.nn.Module`-compatible loss functions:

**`lejepa.univariate`** — goodness-of-fit tests comparing a 1-D sample to N(0,1):
- `EppsPulley` ← **primary test used by SIGReg** — computes the L² distance between the empirical characteristic function and the standard normal CF, integrated over `[0, t_max]` with precomputed trapezoid weights. Exploits symmetry of the CF to halve the integration domain.
- Others (`AndersonDarling`, `CramerVonMises`, `ShapiroWilk`, `Watson`, `Moments`, `NLL`, `ExtendedJarqueBera`, `VCReg`) share the `UnivariateTest` base class.
- All tests take input shape `(N, K)` and return shape `(K,)` — they test each of the K columns independently.
- `DeprecatedEppsPulley` in `epps_pulley.py` is a dead class kept for reference; ignore it.

**`lejepa.multivariate`** — extends univariate tests to high-dimensional embeddings:
- `SlicingUnivariateTest` ← **primary wrapper** — projects embeddings onto `num_slices` random unit vectors and applies any `UnivariateTest` to each slice. Seed is synchronized across DDP ranks via `all_reduce` to guarantee identical projections everywhere.
- `BHEP`, `BHEP_M`, `COMB`, `HZ`, `HV` — direct multivariate normality tests (alternatives to slicing).

`UnivariateTest.base` handles distributed averaging via `torch.distributed.nn.all_reduce`.

### Dual EppsPulley implementations

There are **two separate, independent implementations** of the Epps-Pulley test:
1. `lejepa.univariate.EppsPulley` — general-purpose, composable with `SlicingUnivariateTest`; lives in the `lejepa/` package
2. `stable_pretraining.methods.lejepa.EppsPulley` + `SlicedEppsPulley` — self-contained copy baked into the `LeJEPA` model class; does not import from the `lejepa/` package

The second implementation exists so `stable_pretraining.methods.lejepa` can be used without installing the `lejepa` package. Both are equivalent in math.

### `stable-pretraining/` package

A full PyTorch Lightning training framework used by the experiment scripts. Key modules:

| Module | Role |
|--------|------|
| `module.py` / `Module` | Lightning module wrapping encoder + projector + loss |
| `manager.py` / `Manager` | Orchestrates training runs, Hydra config, logging |
| `data/` | `HFDataset`, `FromTorchDataset` — dict-structured datasets |
| `backbone/` | timm model wrappers; `TeacherStudentWrapper` for EMA |
| `losses/` | Loss registry |
| `callbacks/` | `OnlineProbe`, `OnlineKNN`, `RankMe`, `LiDAR`, `ImageRetrieval`, `EarlyStopping` |
| `optim/` | Optimizer + scheduler builders |
| `static.py` | `TIMM_PARAMETERS` dict mapping backbone names → parameter counts |
| `cli.py` / `run.py` | Entry points for Hydra CLI |
| `methods/lejepa.py` | **`LeJEPA` model class** — self-contained backbone + projector + loss |

Data flows as **dicts** (`{"image": ..., "label": ...}`) through all components so any intermediate value is accessible in callbacks.

### `LeJEPA` model API (train vs eval)

`stable_pretraining.methods.lejepa.LeJEPA` has different forward signatures per mode:

```python
# Training: pass global and local view lists separately
output = model(global_views=[img1, img2], local_views=[img3, img4, img5, img6])
output.loss.backward()
# output fields: loss, embedding, inv_loss, sigreg_loss

# Eval: pass a single images tensor
output = model(images=torch.randn(4, 3, 224, 224))
features = output.embedding  # [N, D]
```

The center for the invariance loss is computed from **global views only** (`all_projected[:n_global].mean(0)`). Global views are 224×224; local views are 98×98. `sigreg_target` controls which tensor gets the SIGReg loss: `"proj"` (default), `"embed"`, or `"both"`.

### Training entry points

**Minimal (self-contained, no stable-pretraining)**  
Described in `docs/MINIMAL.md` — a ~130-line script using `timm`, `datasets`, `wandb`, and `hydra`. (The `mnist.py` invocation below is illustrative from that doc; there is no `mnist.py` in this checkout.)

```bash
python mnist.py +lamb=0.02 +V=4 +proj_dim=16 +lr=2e-3 +bs=256 +epochs=800
```

**Ablation runner (current executable path)**  
`scripts/ablations.py` renders sweep commands and `scripts/train_lejepa_ablation.py` runs local LeJEPA ablation smoke/training jobs. Run both from the **project root**; `train_lejepa_ablation.py` self-patches `sys.path` to find `stable-pretraining/`.

```bash
python scripts/ablations.py list
python scripts/ablations.py show epps
python scripts/ablations.py render epps
python scripts/ablations.py render epps --smoke
python scripts/ablations.py write-scripts --ready-only
python scripts/ablations.py summarize logs/ --metric val/knn_top1

python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 accelerator=cpu devices=1 precision=32
```

The canonical ablation baseline overrides live in `scripts/ablations/specs.py::BASE_OVERRIDES`. A spec's `status` field controls whether `write-scripts --ready-only` includes it.

The old markdown launch files under `scripts/launch_*_ablation.md` are
legacy/manual notes. Do not use `scripts/je.py`; older docs reference it, but
that file does not exist in this checkout.

**Legacy Hydra sweep note**  
`scripts/launch_inet10.py` generates a shell command for a multi-backbone sweep
on ImageNet-10, but the generated target references missing `scripts/je.py`.

**Kaggle / large-scale (train_eval_vit_b.py)**  
Jupytext `.py` notebook targeting Kaggle with ImageNet-1K loaded as a local `ImageFolder`. Sets `HF_DATASETS_CACHE=/dev/shm` for RAM-based caching and uses `GITHUB_TOKEN` / `HF_TOKEN` secrets for repo + hub access.

## Key Hyperparameters

| Param | Recommended | Notes |
|-------|-------------|-------|
| `λ` (lambda) | `0.02` | Balance SIGReg vs invariance; lower = more invariance |
| `lr` | `5e-4` | AdamW; use linear warmup + cosine annealing |
| `weight_decay` | `5e-2` (ViT), `5e-4` (ResNet) | |
| `num_slices` | `1024` | More slices = stronger test, higher cost |
| `n_points` (EppsPulley) | `17` | Integration quadrature points (must be odd) |
| `V` (num views) | `8` (2 global + 6 local) | Multi-crop DINO-style augmentation |
| precision | `bfloat16` | Stable without gradient clipping |
| `sigreg_target` | `"proj"` | Where to apply SIGReg: `"proj"`, `"embed"`, or `"both"` |

Linear probe evaluation uses **concatenated CLS tokens from the last two layers** + `LayerNorm`, with AdamW at `lr=1e-3` and `weight_decay=1e-6`.

## Research track: `climb_bench/`

Active research goal: improve LeJEPA on **Imagenette** ("ImageNet-10" here == fast.ai's 10-class subset, ~9.5k train), pretrain in-domain 400 epochs, eval with a **frozen** `vit_small_patch16_224` linear probe. Low-data regime → data-efficiency / anti-overfit dominate. (batch-1..3 ranked with an in-training probe + kNN; batch-7 onward evaluates only with the paper-spec probe — see step 4.)

Iteration pipeline (branch `clim-bench`):
1. **Ideate** with the `/benchmark-climb-ideation` skill → `climb_bench/ideation/batch-<N>.md` (output path overridden from the skill default).
2. **Plan** → `climb_bench/ideation/plan-batch-<N>.md`.
3. **Implement** → `climb_bench/batch<N>/`: thin `exp<x>.py` runners + `_common.py` (shared trainer, extracted from `stable-pretraining/benchmarks/imagenet10/lejepa-vit-small.py`) + `_variants.py` (batch-local variant classes) + `run-batch<N>.py` (jupytext Kaggle-offline orchestrator).
4. **Analyze/eval** → `climb_bench/viz/`, all batch-parameterized (`--batch batch_<N>` / `BATCH=`): `viz_metrics.py` online-metric curves + ranking (reads `metric_results/<batch>/`); `eval-frozen-paperspec.py` the paper-spec frozen probe = concat CLS last-2 + LN + AdamW wd 1e-6 (supports `--qk_norm`/`--conv_stem` to rebuild exp2/exp6 archs); `run-eval-paperspec.py` unified Kaggle GPU runner (per-batch `PLANS` registry, self-locating via glob, loads full Lightning `.ckpt` directly so NO extract step needed); `viz_paperspec.py` paper-spec bar chart (reads `eval_results/<batch>/`). `extract_backbones.py` is now legacy/optional (direct ckpt load supersedes it). Findings in `climb_bench/tracker/` (one `batch<N>-analysis.md` per batch; reusable `analysis_template.md`).
   - **NB (batch-1..3): the online `OnlineProbe` used to rank ideas is NOT the paper eval recipe** (single CLS, no LN, lr 0.03) — re-run `eval-frozen-paperspec.py` on idea checkpoints for paper-comparable numbers.
   - **batch-7 onward drops the online probe/kNN entirely** (`batch7/_common.py`) — batch-2 showed its ranking does not survive the paper recipe, so it cost training time for a number we then refused to trust. Only `RankMe` is kept, as a cheap in-training collapse guard. **Consequence: best-ckpt selection moves to eval time** — training saves a weights-only ckpt every `--ckpt_every_n_epochs` (default 20) and `PLANS["batch_7"]` sweeps several epochs per exp, scoring each exp at its *best* epoch. `last.ckpt` keeps full optimizer state for Kaggle session resume. If you copy this pattern into a new batch, keep the cadence: without it, the only surviving checkpoint is the last one — precisely the overfit point (the baseline decays ~2.4pp past its peak).
5. **Leo-bench (paper comparison)** — NB: "leobench" is the *action* of climbing the paper benchmark, **not a directory** (`climb_bench/leobench/` was never created). NB: local `data/imagenet10` = the 10 Imagenette classes but **~28k train (≈2.2× the paper's inet10=13k)** — valid for ablation Δ, not for absolute comparison to paper Table 5.
6. **Report to slides** → the benchmark-climb story (batch-1/2 results) lives in `slides/slides_main.tex` under `\section{Nghiên cứu mở rộng: Benchmark Climb trên Imagenette}` (~L2255–2516). **5 visible frames**: research question/headroom · Hướng 1 objective+representation head · insight hướng 1 (SIGReg + MLP projector = the balance point) · Hướng 2 optimizer+training geometry · conv-stem as a separate arch track. A 6th "Tổng hợp" frame is the *only* part still wrapped in `\iffalse … \fi` (~L2469–2514) — the section itself is **visible**. Frames pull numbers from `tracker/batch{1,2}-analysis.md` + `viz/eval_results/`.
   - **Only `fig_climb_objective_bars.pdf` is actually `\includegraphics`'d** (~L2306). `fig_climb_{overfit,scatter}` are orphaned — no deck includes them; `fig_climb_{optbars,convstem}` are used only by `slides/archive/slides_main_climb_bench.tex`. Standalone-compiling figures to PDF is still the convention (inline pgfplots `axis` breaks beamer's frame-body collection) — mirror the deck's A/B/C figures.
   - **Layout**: assets live in `slides/figures/` (both the `.pdf` and the standalone `.tex` that produces it), planning docs in `slides/planning/`, the old fork in `slides/archive/`. `slides_main.tex` sets `\graphicspath{{figures/}}`, so `\includegraphics` keeps taking bare filenames.
   - **Build with `xelatex → bibtex → xelatex → xelatex`.** The deck loads `fontspec`, so **pdflatex will not work** (the archived `slides_main_climb_bench.tex` fork uses `inputenc/fontenc` and *is* pdflatex — do not confuse them). BibTeX is required: bare `xelatex ×2` leaves the "Tài Liệu Tham Khảo" frame empty when no `slides_main.bbl` exists. NB "Latin Modern Sans" must be installed or pagination shifts (34 → 33 pages).

Conventions when implementing variants:
- Reuse the three swap mechanisms: `model.sigreg = ...`, subclass `LeJEPA` overriding `_compute_loss`, or `LeJEPA(projector=...)`. Variant logic goes in a `_variants.py` module; runners only import + wire. Give additive terms a weight-0 off-switch that reduces *exactly* to baseline.
- jupytext orchestrators: **double-`#`** (`# # !python ...`) for inert command cells — single-`#` magics get auto-activated on read (`comment_magics`). No `[...]` in `# %%` cell titles.
- Existing variants in `stable_pretraining/methods/lejepa_variants.py` (SRHT, Hyvärinen, Adversarial max-sliced, FM-SIGReg, FM-Invariance) + batch-1 ideas are already taken — new batches must not duplicate them. ⚠️ **That file is a frozen record, not a library: nothing imports it, none of it was ever executed, and two of its five classes are wrong.** `HyvarienSIGReg` has the encoder descend the ISM scalar, whose optimum value is *minus* the Fisher information — measured to drive the embedding *away* from N(0,I). `FMSIGReg` (form "a") lets encoder and velocity net descend the same CFM loss, which collapse minimises. Corrected, Phase-0-verified versions live in `climb_bench/batch7/_variants.py` (`KLScoreSIGReg`, `FMSIGRegB`) — copy from there, not from the official file. Evidence: `climb_bench/tracker/batch7-analysis.md`.
- **batch-7 is self-contained**: `batch7/_variants.py` *copies* every mechanism (even the sound ones) rather than importing from `lejepa_variants.py`, mirroring the dual-EppsPulley precedent above. Each copied class carries a provenance header naming its origin commit and what changed. Prefer this for new batches — a batch is a Kaggle-uploadable unit, and a cross-package import can silently change underneath it.
- Before spending GPU on a new SIGReg-family objective, run the Phase-0 gate `climb_bench/batch7/test_statistics.py` (~1 min CPU): it descends the objective on a free `z` and checks with an independent yardstick that the result goes to N(0,I) rather than collapsing. It has already killed one idea outright and caught a fatal hyperparameter choice that would have cost ~15 GPU-h to discover.
- Reference clones of third-party repos live in `refs/` (**gitignored**, ~36 MB) — read-only citations, never imported at runtime. See `climb_bench/ideation/plan-batch-7.md` §2 for what each settles.
- Local conda env `lejepa` has torchvision 0.20.1 but the repo needs 0.26.0; full data pipeline only runs on Kaggle (pinned wheels) — smoke-test at model level locally.

## SIGReg ablation study (hyperparameters + components) — status & follow-ups (PAUSED)

Benchmark of LeJEPA across hyperparameter/component settings. **Ran, analyzed, and put
on slides; NOT rerunning for now.** Pick this up from here if asked to extend/rerun.

**Where things are:**
- Raw Kaggle output (notebook `mlinh776/lejepa-ablation-full`, 22 versions) → `ablation_raw/*.zip` → merged into `ablation_results/` (62 jobs, 8 ablations).
- Aggregate: `scripts/ablations/collect_summaries.py` (reads `summary.json`→`paper_eval`, **not** `metrics.csv` which has only loss) → `ablation_results/ablation_summary.{csv,md}`.
- Figures: `scripts/ablations/viz_ablation.py` (heatmaps A/B, bars C/E/F, tornado D) + `viz_paper_tables.py` (paper-style tables a–e) → `ablation_results/figures/`.
- Analysis: `climb_bench/tracker/ablation-measured-analysis.md`. Slides A/B/C in `slides/slides_main.tex` (frames after the commented paper-stability frame).

**Known limitations (read before rerunning / quoting numbers):**
1. **Pipeline is UNDER-FIT.** `train_lejepa_ablation.py:152` `_train_transform` has **only `RandomResizedCrop`** — missing ALL photometric aug that the project baseline `climb_bench/batch1/_common.py:39` (`_photometric_transforms`: flip/color-jitter/grayscale/blur/solarize) uses. → anchor top1 **59.5%** vs project baseline **89.5%** (`eval_results/batch_2/baseline_100.json`). Absolute NOT comparable; only internal Δ. Structural conclusions (collapse at `sigreg=embed`/`projector=Linear`, `num_slices↑`, predictor-not-needed) hold; regularization conclusions (`drop_path`/`patch_mask`/views "don't help") are confounded by the under-fit regime.
2. **Single seed (42), no error bars** → small Δ (1–2pt) indistinguishable from noise.
3. Harness diffs vs baseline (all in Comparability table of the analysis note): batch 512 vs 128, λ 0.05 vs 0.02, fp16 vs bf16.

**Follow-ups, priority order (Kaggle GPU only — local can't run full pipeline):**
1. **Fix aug** — add `_photometric_transforms` to `_train_transform` (mirror `_common.py`). ~5 lines, biggest impact.
2. **Multi-seed** (2–3) for small-Δ ablations → error bars.
3. **batch_size ablation** — code ready (`TrainConfig.batch_size`), just add a spec grid; directly quantifies the batch confound. Best-value of the untried ablations.
4. `projector_dim` works (1-D); **`embedding_dim` NOT settable** (LeJEPA derives it from backbone, `lejepa.py:410`). `reg_tokens` code exists but timm `vit_small` support is env-dependent (may fail). **`cls2` aggregator NOT implemented** (`lejepa.py:383` accepts only `cls`/`mean`/`cls_mean`).
