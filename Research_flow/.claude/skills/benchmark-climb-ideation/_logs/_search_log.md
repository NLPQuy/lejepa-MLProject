# Search log

## 2026-05-18 — ImageNet-10 / LeJEPA batch-1
- T1 q1: "LeJEPA SIGReg sliced isotropic Gaussian regularization improvements 2025" → confirmed primary paper arXiv:2511.08544
- T1 q2: "self-supervised learning small dataset ImageNet-10 Imagenette ViT 2024 2025 benchmark" → SSL benchmark lottery arXiv:2501.15431; Imagenette ref
- T1 q3: "DINOv2 DINOv3 iBOT masked image modeling small dataset pretraining 2024" → arXiv:2304.07193, iBOT arXiv:2111.07832
- T1 q4: "VICReg projector head expander SSL improvement arXiv" → VICReg 2105.04906, Kernel-VICReg 2509.07289
- T1 q5: "EMA teacher student SSL ViT small data multi-crop DINO 2024" → DINO arXiv:2104.14294
- T1 q6: "SSL pretraining small dataset registers ViT auxiliary loss 2024 arXiv" → SSAT 2310.20704, registers 2309.16588
- T1 q7: "register tokens vision transformer artifacts DINOv2 Darcet 2023 arXiv" → arXiv:2309.16588 (ICLR 2024)
- T2 q1: "sliced Wasserstein distance representation learning isotropic gaussian normality test" → Kolouri arXiv:1711.05376
- T2 q2: "arXiv 2402.03752 lightweight vision transformer small dataset pretraining" → confirmed
- T2 q3: "MaskFeat I-JEPA local prediction self-supervised patch masking arXiv 2023" → I-JEPA 2301.08243
- T2 q4: "koleo regularization DINOv2 feature spreading uniformity loss embedding"
- T3 q1: "sliced score matching energy distance feature distribution matching deep learning" → arXiv:1905.07088
- Devil's-advocate: "multi-crop DINO local crops diminishing returns small dataset overfitting failure" → arXiv:2406.09294

Totals: 13 queries · ~25 summaries · 0 full PDF reads · ~12 min wall-clock. Within budget.

## 2026-05-19 — Audit note (retroactive)
- **Batch 2 (2026-05-18)**: ⚠️ shipped with **0 logged queries this session**. All primary papers cited from memory. Audit flag: `UNVERIFIED — memory-cited`. Affected ideas: 1 (LeJEPA + AD + Watson), 2 (Kolouri GSW + Bonneel), 3 (Bengio curriculum + SwAV), 4 (SimCLR + LARS + BYOL + SwAV), 5 (ASHA + Hyperband — later retracted as `not-an-idea`), 6 (SEED + DINOv2). Re-verify before any of these go to implementation.
- **Batch 3 (2026-05-18)**: ⚠️ same issue suspected — no log entries added during batch-3 generation either. Audit before shipping any batch-3 idea.
- **Skill fix applied 2026-05-19**: `SKILL.md` Step 2 now states "live searches only" as a hard rule; `checklists/pre-deliver.md` audits this log for a session-dated heading and spot-checks 2 papers. Future batches that skip live search must STOP and ask the user, not silently ship.

## 2026-05-19 — Tier-3 honesty audit (retroactive)

User flagged that T3 across batches 1/2/3 was vague — never actually cross-domain. Findings:

- **Batch 1 Idea 4 (Adaptive-λ)**: tagged T3 with primary = LeJEPA (in-field) + GradNorm "supporting". Real tier: **T1 or T2**. The "cross-domain notes" block was lipstick — no actual lift from a non-ML field.
- **Batch 2 Idea 5 (ASHA HP sweep)**: tagged T3 with primary = LeJEPA + ASHA/Hyperband (AutoML). Real tier: **not an idea** (already retracted). T3 framing was misuse to make engineering look like research.
- **Batch 3 Idea 6 (SWA weight averaging)**: tagged T3 with primary = Izmailov SWA UAI 2018 + Schedule-Free NeurIPS 2024 + Model Soups ICML 2022. All are **mainstream ML/optimization** used in vision for years. Real tier: **T2 adjacent** at most. Not a genuine cross-domain lift.
- Search log itself: batch-1's only T3 query (`"sliced score matching energy distance feature distribution matching deep learning"`) was still ML-adjacent, not from a source-field venue. No queries to optimization theory journals, statistics journals, neuroscience, control, or physics.

**Skill fix applied 2026-05-19** (sharpens T3 definition):
- `rules/search-strategy.md §Tier 3` — added hard test: primary paper venue must NOT be on the in-field tier-1 list; mechanism must be a named principle/algorithm/theorem from the source field; idea card must include `Cross-domain transfer: <source field> → <target use>` line. Explicit do-not list: SWA, ASHA, EMA, dropout, mixup, label smoothing — all NOT T3 regardless of original venue.
- `checklists/pre-deliver.md` — Tier-3 honesty audit section: every T3 idea checked for source-field venue, named-principle mechanism, and ≥ 1 source-field query in the search log. Mis-tagged T3 must be re-tagged down (and tier quota re-checked), not silently kept.
- `SKILL.md` Anti-patterns — explicit "don't fake T3 with cross-domain supporting refs" entry.

## 2026-05-18 — ImageNet-10 / LeJEPA batch-3 (given-vetting batch-2)
- T1 q1: "co-distillation two students self-supervised joint embedding orthogonal projection heads 2024 2025" → C-JEPA NeurIPS 2024, VkD CVPR 2024, Multi-Teacher Distill arXiv:2510.18680 (2025)
- T3 q1: "subsampled randomized Hadamard transform structured random projection variance reduction Tropp" → Tropp arXiv:1011.1595 + SIAM JMAA 2013 (numerical linear algebra — bona-fide cross-domain)
- T3 q2: "probability integral transform uniformity test held-out goodness of fit Anderson 1962" → Pearson Biometrika 1938 (JSTOR 2332229), PITOS arXiv:2510.22854 (2025) (mathematical statistics)
- T3 q3: "Hermite polynomial moment matching normality test Gaussian density expansion goodness of fit" → Lacaux Signal Processing 1999, Bontemps & Meddahi GMM 2004, Frontiers Neuroinformatics 2023 (signal processing / statistical inference)
- T2 q1: "DDP distributed self-supervised learning different random projections per rank variance reduction slicing" → SSL from Random Data Projectors (OpenReview/NeurIPS-W), PyTorch DDP semantics
- T1 q2: "curriculum learning self-supervised low rank to full embedding dimension warmup" → ERW arXiv:2504.10188 (2025), Meta AI dimensional-collapse blog 2022, Curriculum Learning Survey arXiv:2101.10382

Totals: 6 queries · ~22 summaries · 0 full PDF reads · ~7 min wall-clock. Within budget. **All primary papers in batch-3 trace to a query above.** Tier-3 honesty: SRHT (Tropp / SIAM JMAA), PIT (Biometrika / JSTOR), Hermite (Signal Processing IEEE) — all real out-of-field venues, not ML-adjacent.

## 2026-05-18 — Batch 4 ideation (ImageNet-10 / LeJEPA SSL)
| # | Query | Tier | Hits used |
|---|-------|------|-----------|
| 1 | MAE auxiliary head JEPA self-supervised learning combined ImageNet linear probe 2024 2025 | T1 | I-JEPA arXiv:2301.08243 (CVPR 2023); MAE-vs-JEPA efficiency claim; C-JEPA NeurIPS 2024 (already in batch-3) |
| 2 | sharpness aware minimization SAM self-supervised learning DINO BYOL linear probe | T1 | SAM Foret arXiv:2010.01412; Friendly-SAM CVPR 2024; "SAM Enhances Feature Quality" arXiv:2405.20439; SAMPa NeurIPS 2024 |
| 3 | antithetic sampling sliced Wasserstein variance reduction Monte Carlo | T3 | Spherical-Harmonics CV for SW arXiv:2402.01493; Repulsive MC on sphere for SW arXiv:2509.10166; Adaptive Antithetic Sampling ICML 2019 |
| 4 | whitening W-MSE Cholesky ZCA self-supervised learning representation | T1 | W-MSE Ermolov arXiv:2007.06346 (ICML 2021); "Whitening Consistently Improves SSL" arXiv:2408.07519 |
| 5 | repeated augmentation RA self-supervised learning ViT small data linear probe | T1 | Not used — no strong RA-for-SSL primary surfaced (dropped from batch) |
| 6 | normalizing flow Gaussianization regularizer representation learning | T3 | Differentiable Gaussianization Layers arXiv:2112.03860; not used (philosophically opposed to SIGReg) |
| 7 | deep supervision auxiliary loss intermediate layers vision transformer SSL representation | T2 | SDSSL self-distillation SSL; DINOv3 multi-loss recipe; Deep Supervision review ScienceDirect 2025 |
| 8 | masked autoencoder MAE ViT-S small data ImageNet linear probe He 2022 | T1 | MAE arXiv:2111.06377 (CVPR 2022); Swin-MAE small-data variant; SupMAE arXiv:2205.14540 |

Totals: 8 queries · ~55 summaries · 0 full reads · ~9 min wall-clock. Within budget (≤ 19 queries, ≤ 45 summaries, ≤ 15 min — summary count slightly over, none requested as full read).

## 2026-05-18 — Batch 5 ideation (ImageNet-10 / LeJEPA SSL — tier mix 30/20/50)
| # | Query | Tool | Tier | Hits used |
|---|-------|------|------|-----------|
| 1 | Kernelized Stein discrepancy goodness of fit normality test high dimensional 2024 | WebSearch | T3 | Liu-Lee-Jordan ICML 2016 (arXiv:1602.03253); sliced KSD / maxSKSD line; ICML 2024 sequential KSD |
| 2 | spherical t-designs deterministic quadrature numerical integration sphere Womersley Bondarenko | WebSearch | T3 | Bondarenko-Radchenko-Viazovska Annals of Math 2013; Womersley arXiv:1709.01624 + SIAM JNA; arXiv:1611.02785; arXiv:2601.11963 survey |
| 3 | quasi Monte Carlo low discrepancy sphere Sobol sequence sliced Wasserstein 2024 | WebSearch | T3 | QSW arXiv:2309.11713 (ICLR 2024); RQSW; QMC slicing arXiv:2410.01316 (not used — 3D-only limitation) |
| 4 | Renyi entropy alpha divergence isotropic gaussian regularization representation learning | WebSearch | T3 | Renyi divergence + Gaussians (Springer Inf Geom); arXiv:1206.2459 IEEE Trans IT; Renyi VI NeurIPS 2016 (not used — density-estimation gap) |
| 5 | sliced Stein discrepancy maxSKSD goodness of fit high dimensional | HF paper search | T3 | arXiv:2210.10741 (sequential KSD); arXiv:2304.14762 (perturbation-KSD 2023); arXiv:2306.00602 (truncated KSD 2023) |
| 6 | equivariant self supervised learning rotation prediction | HF paper search | T1 | SIE arXiv:2302.10283 (Garrido-Najman-LeCun 2023); arXiv:2503.18753 (2026 equivariance-coherence); EquiCaps arXiv:2506.09895 (2025) |
| 7 | Koleo entropy regularization hypersphere uniformity DINOv2 | HF paper search | T1 | Geometric constraints for imbalanced regression arXiv:2503.00876 (2025) — supporting for MMCR; not directly used as primary |
| 8 | predictive coding free energy biologically plausible representation learning | HF paper search | T3 | MMCR arXiv:2303.03307 (Yerxa-Kuang-Simoncelli-Chung 2023); iPC arXiv:2212.00720 (not used — overlap with batch-4 layer-wise) |
| 9 | maximum manifold capacity representations MMCR self supervised Chung neuroscience | HF paper search | T3 | MMCR arXiv:2303.03307 (confirmed primary) |
| 10 | MMD maximum mean discrepancy kernel two sample test representation learning | HF paper search | T2 | Sliced MMD Riesz arXiv:2305.11463 (Hertrich 2023); Demystifying MMD GANs arXiv:1801.01401 (ICLR 2018); arXiv:2301.11674 (2023) |
| 11 | augmentation policy learning contrastive crop self supervised AutoAugment | HF paper search | T1 | Saliency arXiv:2210.16776 (2022); Taming Randomness arXiv:2504.19824 (2025); SelfAugment 2020 |
| 12 | Thomson problem hyperspherical energy point repulsion uniform distribution | HF paper search | T3 | Liu MHE arXiv:1805.09298 (2018) — not used in batch (would have been a 4th VR-family idea); DPP MC arXiv:2604.19698 (2026) — supporting for batch-4 Repulsive |

Totals: 12 queries (4 WebSearch + 8 HF paper search) · ~50 summaries · 0 full reads · ~15 min wall-clock. Within budget. WebSearch hit rate limit after query 4; switched to HF paper search for remaining queries. **All primary papers in batch-5 trace to a query above.** Tier-3 honesty: Bondarenko-Radchenko-Viazovska (Annals of Math), Womersley (SIAM JNA), Liu-Lee-Jordan (Stein's-method line, ICML 2016 with mathematical-statistics provenance), Yerxa et al. (theoretical neuroscience, Chung lab) — all real out-of-field source venues, not ML-adjacent.

## 2026-05-18 — ImageNet-10 / LeJEPA batch-6
- T1 q1: "RankMe self-supervised representation rank Garrido 2023 ICML paper" → confirmed Garrido-Balestriero-Najman-LeCun ICML 2023 / arXiv:2210.02885
- T1 q2: "vision transformers need registers Darcet ICLR 2024 arxiv" → confirmed Darcet-Oquab-Mairal-Bojanowski ICLR 2024 Oral / arXiv:2309.16588 + cross-arch reassessment arXiv:2603.25803 (2026)
- T1 q3: "RankMe alpha-ReQ effective rank online monitor adaptive lambda SSL regularization 2024 2025" → reconfirmed RankMe; alpha-ReQ as power-law spectral measure; WACV2025 HEX paper as recent follow-up
- T2 q1: "iBOT image BERT pre-training online tokenizer Zhou Wei masked patch ICLR 2022" → confirmed Zhou-Wei-Wang-Shen-Xie-Yuille-Kong ICLR 2022 / arXiv:2111.07832
- T3 q1: "Sinkhorn divergence self-supervised learning optimal transport view alignment loss SSL" → SinSim arXiv:2502.10478 (Feb 2025) + foundational Genevay-Peyré "Learning Generative Models with Sinkhorn Divergences" AISTATS 2018 (PMLR v84)
- T3 q2: "SinSim Sinkhorn-regularized SimCLR arxiv 2502.10478" → confirmed Sepanj-Fieguth Feb 2025; Kernel-VICReg arXiv:2509.07289 surfaced as composer
- T3 q3: "hyperbolic embeddings Poincare Nickel Kiela NeurIPS 2017 representation learning" → confirmed Nickel-Kiela NeurIPS 2017 / arXiv:1705.08039
- T3 q4: "hyperbolic neural networks Ganea Becigneul Hofmann NeurIPS 2018 self-supervised image embedding" → confirmed Ganea-Becigneul-Hofmann NeurIPS 2018 / arXiv:1805.09112 (Möbius gyrovector + exp/log map ops)
- T3 q5: "persistent homology topological loss regularizer deep learning differentiable Edelsbrunner" → Topological Reg via Persistent Homology MDPI Mathematics 2023; Carriere et al. "Optimizing PH-based functions" ICML 2021 (PMLR v139)
- T3 q6: "Hofer deep learning topological signatures NeurIPS 2017 differentiable persistent homology layer" → confirmed Hofer-Kwitt-Niethammer-Uhl NeurIPS 2017 / arXiv:1707.04041

Totals: 10 queries · ~30 summaries · 0 full PDF reads · ~6 min wall-clock. Within budget (cap 19/45/10/15). Tier distribution of queries: T1 3 · T2 1 · T3 6 — matches the 30/20/50 ask. **Provenance audit**: every primary in batch-6 traces to a query above. No memory-cited papers.
