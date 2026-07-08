# Paper ablation baselines (arXiv:2511.08544, Table 1 + views/λ)

Reference numbers extracted from the LeJEPA paper full-text to compare *trends* against
our imagenet10 ablations.

## ⚠️ Comparability caveat — read first

Paper Table 1 setup: **ViT-Large/14, ImageNet-1K, 100 pretrain epochs, frozen in-domain
linear probe (top-1 %)**. Our setup: **ViT-Small/16, imagenet10 (~28k train), 50–100 ep**.

→ **Absolute numbers are NOT comparable.** Use these only for the *direction/shape* of each
ablation (does top1 go up or down as the knob moves) and the *magnitude of sensitivity*
(flat vs steep). The eval recipe matches (concat CLS last-2 + LN + AdamW wd1e-6 + warmup/cosine),
so trend comparison is valid; the dataset/scale/arch differ.

Numbers below were pulled from the arXiv HTML via an assistant model. Sub-table (b) extraction
was noisy/incomplete — **verify against the PDF before quoting (b)**.

## (a) Epps-Pulley: integration domain × quadrature points × slices

top1 for (5, 17, 41 points):

| domain [−t_max, t_max] | 512 slices | 2048 slices |
|---|---|---|
| [−1, 1] | 71.82 / 72.13 / 72.04 | 72.88 / 72.30 / 72.69 |
| [−3, 3] | 73.95 / 74.16 / 74.04 | 75.02 / 74.68 / 74.77 |
| [−5, 5] | 73.71 / 74.21 / 74.15 | 74.50 / 74.80 / 74.77 |

**Trend:** domain ≥[−3,3] matters a lot vs [−1,1] (+2pt); #points (5/17/41) ≈ flat (paper: "negligible");
more slices = marginal gain. → our defaults t_max=3, n_points=17, num_slices=1024 sit on the good plateau.

## (b) Number of views *(noisy extraction — verify in PDF)*

| V_g | V (total) | top1 |
|---|---|---|
| 1 | 4 | 53.06 |
| 2 | 6 | 73.07 |
| 4 | 8 | 64.46 |
| 2 | 10 | 68.97 |

**Trend (tentative):** 2 global views clearly beats 1; more local views help up to a point.

## (c) Batch size

| 128 | 256 | 512 | 1024 |
|---|---|---|---|
| 72.20 | 74.15 | 74.72 | 74.07 |

**Trend:** competitive down to 128; ~512 is the sweet spot (our default).

## (d) Embedding dim × projector dim (× slices)

top1 by projector dim (64 / 128 / 256 / 512 / 1024):

| slices / embed | 64 | 128 | 256 | 512 | 1024 |
|---|---|---|---|---|---|
| 1024 / 512 | 75.29 | 74.77 | 74.56 | 73.94 | 73.65 |
| 1024 / 2048 | 75.32 | 75.09 | 74.66 | 74.11 | 73.94 |
| 4096 / 512 | 75.50 | 75.26 | 75.08 | 74.81 | 74.71 |
| 4096 / 2048 | 75.65 | 75.47 | 75.02 | 74.65 | 74.79 |

**Trend:** **smaller projector dim is better** (64 > 1024, ~+1.5pt); more slices helps;
embed 512 vs 2048 ≈ small. → note: our default projector_dim=512 is on the *worse* end of this curve.

## (e) Register tokens

| tokens | 1024 slices | 4096 slices |
|---|---|---|
| 0 | 75.14 | 75.61 |
| 1 | 75.18 | 75.58 |
| 2 | 75.08 | 75.67 |
| 4 | 75.34 | 75.63 |
| 8 | 75.23 | 75.84 |

**Trend:** essentially flat (±0.2pt); register tokens are not a meaningful lever here.

## Mapping to our batches

- Paper-covered (we re-verify low-data): `epps` (a), `views` (b), `projector_dims`/`reg_tokens` (d/e, both currently skipped).
- Novel (paper does NOT ablate): `predictor`, `sigreg_target`, `patch_masking`, `drop_path`,
  `aggregation`, `projector_depth` (paper ablates proj *dim*, not *depth*).
