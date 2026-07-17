# LeJEPA — study fork

A coursework/research fork of **LeJEPA** used to (a) reproduce the method, (b) run a
component/hyperparameter ablation of **SIGReg**, and (c) try to climb a small
benchmark (Imagenette) with new objectives.

> **This is not the official repository.** LeJEPA is the work of Randall Balestriero
> and Yann LeCun. All credit for the method belongs to them.
>
> | | |
> |---|---|
> | 📄 Paper | [LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics](https://arxiv.org/abs/2511.08544) (arXiv:2511.08544) |
> | 🏠 Official repo | **[rbalestr-lab/lejepa](https://github.com/rbalestr-lab/lejepa)** ← go here for the method itself |
> | 🧰 Training harness | [galilai-group/stable-pretraining](https://github.com/galilai-group/stable-pretraining) (vendored under `stable-pretraining/`) |
> | ⚖️ License | CC BY-NC 4.0, inherited from upstream |
>
> `lejepa/`, `stable-pretraining/`, `docs/MINIMAL.md` and the demo assets in `eval/`
> come from upstream. **Upstream's ImageNet-1K benchmark tables are deliberately not
> reproduced here** — none of those numbers were produced by this fork, and repeating
> them in this README would only invite them to be read as ours. See the
> [official repo](https://github.com/rbalestr-lab/lejepa) and the paper for those.

---

## What LeJEPA is, in one block

```
LeJEPA_loss = λ · SIGReg(proj) + (1 − λ) · Invariance(proj)
```

- **Invariance** — multi-view projections must agree: `(proj.mean(0) - proj).square().mean()`
- **SIGReg** — *Sketched Isotropic Gaussian Regularization*: pushes embeddings toward
  `N(0, I)` by applying a univariate Epps–Pulley normality test across random 1-D
  slices of the embedding space (Cramér–Wold).

`λ` is the single trade-off hyperparameter (~`0.01–0.1`). No stop-gradient, no
teacher–student, no schedulers.

```python
import lejepa

univariate_test = lejepa.univariate.EppsPulley(num_points=17)
loss_fn = lejepa.multivariate.SlicingUnivariateTest(
    univariate_test=univariate_test, num_slices=1024
)
loss = loss_fn(embeddings)   # embeddings: [num_samples, num_dims]
loss.backward()
```

See [`docs/MINIMAL.md`](docs/MINIMAL.md) for a ~130-line end-to-end example.

---

## What this fork adds

Everything below is **ours**. The numbers are measured in this repo on **Imagenette**
(the 10-class ImageNet subset), with a frozen `vit_small_patch16_224` and the paper's
linear-probe recipe (concat CLS of the last two layers + LayerNorm, AdamW lr `1e-3`,
wd `1e-6`).

### 1. Benchmark-climb track — `climb_bench/`

Batches of ideas, each: ideate → plan → implement as single-variable variants →
evaluate with the paper-spec probe → write up. Measured at 100-epoch pretrain:

| arm | top-1 | Δ vs baseline |
|---|---:|---:|
| **conv-stem** (architecture co-design) | **0.9208** | **+2.6 pp** |
| SAM | 0.8972 | +0.2 |
| stochastic-depth schedule | 0.8950 | +0.0 |
| **baseline LeJEPA ViT-S** | **0.8949** | — |
| PCGrad | 0.8944 | −0.1 |
| SWA | 0.8911 | −0.4 |
| QK-Norm | 0.8909 | −0.4 |
| deep supervision | 0.8894 | −0.6 |
| schedule-free AdamW | 0.8872 | −0.8 |
| LLRD | 0.8616 | −3.3 |
| Muon | 0.8574 | −3.8 |

The honest summary: **the optimizer axis is a dead end** — every optimizer variant
lands within noise of, or well below, plain AdamW. The one real win came from changing
the *architecture*, not the objective. Write-ups per batch in `climb_bench/tracker/`.

Two methodology findings worth more than the table:

- **Online ranking ≠ paper recipe.** The in-training probe used to rank ideas (single
  CLS, no LN, lr 0.03) does **not** preserve ordering under the paper's recipe. Ideas
  that looked good online died on re-evaluation. From batch-7 on, training drops the
  online probe entirely and evaluates only with `viz/eval-frozen-paperspec.py`.
- **Cheap CPU gates beat expensive GPU runs.** `climb_bench/batch7/test_statistics.py`
  descends a candidate objective on a free `z` and checks — with an independent
  yardstick the objective never sees — whether it converges to `N(0,I)` or collapses.
  ~1 minute of CPU killed one idea outright and caught a fatal hyperparameter choice
  that would otherwise have cost ~15 GPU-hours to discover.
  See `climb_bench/tracker/batch7-analysis.md`.

### 2. SIGReg ablation study — `ablation_results/`

62 jobs across 8 ablations (aggregation, drop-path, Epps–Pulley quadrature, predictor,
projector depth, SIGReg target, patch masking, views). Structural findings:

| knob | result |
|---|---|
| `projector_arch` | `Linear` **0.2343** (collapse) < `MLP2` 0.5713 < `MLP` 0.5946 < `MLP4` **0.6126** — more projector capacity helps monotonically |
| `sigreg_target` | `proj` 0.5946 vs `embed` **0.2371** (collapse) — SIGReg must act on the projection |
| `predictor` | not needed |
| `num_slices` | more slices → better |

> ⚠️ **These ablation numbers are internally comparable only.** That pipeline is
> under-fit: its training transform has `RandomResizedCrop` but none of the
> photometric augmentation the project baseline uses, so its anchor is **0.5946**
> against the project baseline's **0.8949**. Deltas and structural conclusions hold;
> absolute values are **not** comparable to the table above, or to the paper.
> `CLAUDE.md` records the limitation and the fix.

> ⚠️ **Not comparable to paper Table 5 either.** Local `data/imagenet10` has ~28k
> train images, ≈2.2× the paper's inet10 (13k).

### 3. Slides — `slides/`

Vietnamese presentation deck covering the paper and both tracks. Build with
`xelatex → bibtex → xelatex → xelatex` — it loads `fontspec`, so `pdflatex` will not
work. Assets in `slides/figures/`, planning docs in `slides/planning/`.

---

## Layout

```
lejepa/                 core SIGReg library (UPSTREAM) — univariate + multivariate tests
stable-pretraining/     PyTorch Lightning harness (UPSTREAM, vendored)
docs/                   upstream docs (MINIMAL.md) + this fork's plans
eval/                   upstream demo assets

climb_bench/            <- ours: the benchmark-climb research track
  ideation/               idea batches + implementation plans
  batch1/ batch2/ batch7/ runners: exp<x>.py + _common.py + _variants.py
  viz/                    eval + plots (eval-frozen-paperspec.py = the paper recipe)
  tracker/                findings, one analysis note per batch
ablation_results/       <- ours: 62-job SIGReg ablation + figures
ablation_raw/           <- ours: raw Kaggle output
scripts/ablations/      <- ours: sweep specs, collection, plots
slides/                 <- ours: the deck
refs/                   third-party repos cloned for reference (gitignored)
```

## Install

```bash
pip install lejepa                            # core library only (upstream, on PyPI)

pip install -e .                              # or from this source
cd stable-pretraining && pip install -e .     # training harness, needed by the scripts
pip install -r requirements.txt               # full experiment environment
```

## Run

```bash
pytest tests/                                 # core library tests

python climb_bench/batch7/test_statistics.py  # CPU objective gate, ~1 min

python scripts/ablations.py list              # ablation sweeps
python scripts/ablations.py render epps --smoke
```

Full pretraining runs on **Kaggle** (pinned wheels); the jupytext orchestrators are
`climb_bench/batch<N>/run-batch<N>.py`. The local conda env ships torchvision 0.20.1
while the data pipeline needs 0.26 — smoke-test at the model/loss level locally, train
on Kaggle.

Read [`CLAUDE.md`](CLAUDE.md) before contributing. It is the working map of this fork:
conventions, known-stale traps, and what has already been tried and killed.

## Citation

Cite the original authors, not this fork:

```bibtex
@misc{balestriero2025lejepaprovablescalableselfsupervised,
      title={LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics},
      author={Randall Balestriero and Yann LeCun},
      year={2025},
      eprint={2511.08544},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2511.08544},
}
```

Questions about **LeJEPA itself** → the [official repo](https://github.com/rbalestr-lab/lejepa)
or rbalestr@brown.edu. Questions about **this fork's experiments** → open an issue here.
