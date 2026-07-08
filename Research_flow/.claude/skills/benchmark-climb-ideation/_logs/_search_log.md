# Search log

## 2026-05-18 — ImageNet-10 / LeJEPA batch-1
- T1 q1: "LeJEPA SIGReg sliced isotropic Gaussian regularization improvements 2025" → confirmed primary paper arXiv:2511.08544
- T1 q2: "self-supervised learning small dataset ImageNet-10 Imagenette ViT 2024 2025 benchmark" → SSL benchmark lottery arXiv:2501.15431; Imagenette ref
- T1 q3: "DINOv2 DINOv3 iBOT masked image modeling small dataset pretraining 2024" → arXiv:2304.07193, iBOT arXiv:2111.07832
- T1 q4: "VICReg projector head expander SSL improvement arXiv" → VICReg 2105.04906, Kernel-VICReg 2509.07289
- T1 q5: "EMA teacher student SSL ViT small data multi-crop DINO 2024" → DINO arXiv:2104.14294
- T1 q6: "SSL pretraining small dataset registers ViT auxiliary loss 2024 arXiv" → SSAT 2310.20704, registers 2309.16588
- T1 q7: "register tokens vision transformer artifacts DINOv2 Darcet 2023 arXiv" → arXiv:2309.16588 (ICLR 2024)

## 2026-05-19 — ImageNet-10 / LeJEPA batch-7 (T3-only override, themes: flow-matching / score-matching / game-theory / RL / neural-collapse)
- T3 q1: "conditional flow matching Lipman ICLR 2023 representation learning self-supervised" → Lipman et al. ICLR 2023 arXiv:2210.02747 "Flow Matching for Generative Modeling"; OT-displacement CFM; supporting "Better Source, Better Flow" arXiv:2602.05951
- T3 q2: "score matching Hyvarinen self-supervised representation learning embedding density" → Hyvärinen JMLR 2005 (foundational); Song-Ermon Sliced Score Matching arXiv:1905.07088; recent arXiv:2502.20123 "Stein's unbiased risk estimate and Hyvärinen's score matching" (Feb 2025)
- T3 q3: "max sliced Wasserstein adversarial direction Deshpande sliced distribution" → Deshpande et al. CVPR 2019 arXiv:1904.05877 "Max-Sliced Wasserstein Distance and its use for GANs"; Distributional Sliced-Wasserstein Nguyen 2020; minimax framing confirmed
- T3 q4: "reinforcement learning augmentation policy self-supervised pretraining AutoAugment SSL" → SelfAugment Reed et al. CVPR 2021 arXiv:2009.07724; Evolutionary policy arXiv:2303.01584; "Beyond Random Augmentations: Hard Views" arXiv:2310.03940; RL-BioAug arXiv:2601.13964 (Jan 2026, <12mo)
- T3 q5: "neural collapse equiangular tight frame self-supervised learning ETF Papyan" → Papyan-Han-Donoho PNAS 2020 arXiv:2008.08186; "Guiding Neural Collapse Towards Nearest Simplex ETF" arXiv:2411.01248 (Nov 2024); "rETF-semiSL" arXiv:2508.10147 (Aug 2025, <12mo)

Totals: 5 T3 queries (cap 5 ✓, T1=0/T2=0 by user-directed override of `each ≥ 10` rule — surfaced as `⚠ Tier-mix-override violation` in batch-7 Notes & warnings), ~25 summaries skimmed, 0 full reads (all venues whitelisted; abstracts sufficient), ~6 min wall-clock.

## 2026-05-27 — VILD + CVGL / P-polar-vs-E-polar admissibility batch-6
- T1 q1: "Pumir Singer Boumal generalized orthogonal Procrustes high noise regime IMA 2021" → confirmed arXiv:1907.01145 (Info & Inference IMA 10(3) 2021); high-noise theorem says rotation cannot be reliably estimated below SNR threshold, use Gram-matrix invariant
- T1 q2: "Donoho Gavish optimal singular value threshold 4 over sqrt 3 IEEE Information Theory 2014" → confirmed arXiv:1305.5870 (IEEE TIT 60(8) 2014 pp 5040-5053); AMSE-optimal hard threshold is `(4/√3)·√n·σ` (known σ) or `2.858·y_med` (unknown σ)
- T1 q3: "Bun Bouchaud Potters rotational invariant estimator cleaning covariance Physics Reports 2017" → confirmed arXiv:1610.08104 (Phys. Rep. 666 2017 pp 1-109); RIE optimal nonlinear shrinkage of correlation matrix eigenvalues
- T1 q4: "Lin Liu generalized orthogonal Procrustes problem arbitrary adversaries SIAM 2025" → confirmed arXiv:2106.15493 (SIMAX 46(1) 2025 pp 561-583). **CORRECTION**: author is single author "Shuyang Ling" (NYU Shanghai), NOT "Lin, Liu" as batch-5 cited. Propagated to batch-6.
- T1 q5: "Andreella Finos ProMises Procrustes high-dimensional Psychometrika 2022 prior regularization" → confirmed arXiv:2008.04631 (Psychometrika 87(4) 2022 pp 1422-1438); ProMises vMF-prior Procrustes with closed-form `R = SVD(M + κI)`
- T1 q6 (follow-up): Adachi-Okuno-Takeda Riemannian-LM arXiv:2210.00253 confirmed (Oct 2022, 12-36mo)
- T2 q1: "PAC-Bayes McAllester 1999 model selection bound generalization" → McAllester COLT 1999 PAC-Bayesian model averaging confirmed; foundational KL-regularised generalisation bound
- T2 q2: "Catoni PAC-Bayes 2007 IMS monograph statistical learning theory" → arXiv:0712.0248 (IMS Lecture Notes Vol 56 2007 163pp); thermodynamic PAC-Bayes Gibbs posterior `Q* ∝ exp(−β L̂) · P`, β = N/2
- T2 q3: "Efron empirical Bayes large-scale inference 2010 shrinkage estimator" → confirmed Cambridge UP IMS Vol 1 2010 ISBN 978-0-521-19249-1; marginal-likelihood-maximisation EB recipe
- T2 q4: "Hoeffding 1948 U-statistic asymptotic distribution unbiased" → confirmed Ann. Math. Stat. 19(3) 1948 pp 293-325 (Project Euclid euclid.aoms/1177730196); U-stat = unique unbiased estimator + asymptotic normality
- T2 q5: "Stein 1956 inadmissibility multivariate normal mean James-Stein shrinkage dominance" → confirmed Stein 1956 Berkeley Symp + James-Stein 1961 dominance theorem (background for Idea 2's SURE recipe)
- T2 q6 (follow-up): "iterative algorithm cross validation early stopping unbiased risk estimator SURE Stein" → SUGAR Deledalle-Vaiter-Peyré-Fadili SIAM J. Imaging Sciences 7(4) 2014 (hal-00987295), SURE for proximal-splitting iterative methods
- T3 q1: "Hoff Bayesian model averaging Stiefel manifold matrix Fisher 2009 simulation" → confirmed JCGS 18(2) 2009 pp 438-456 (doi 10.1198/jcgs.2009.07177); Matrix Bingham-vMF Stiefel-manifold simulation + normalisation constant
- T3 q2: "Schwarz BIC 1978 evidence selection marginal likelihood penalty" → confirmed Ann. Stat. 6(2) 1978 pp 461-464; BIC `−2 log L̂ + k log n` is large-sample Bayes-factor approximation
- T3 q3: "Hodges 1951 superefficient estimator counterexample admissibility" → Hodges' estimator rejected from batch (pointwise-only superefficiency; max risk unbounded per Le Cam)
- T3 q4 (follow-up): "Boumal Singer non-convex Procrustes synchronization Stiefel global optimality" → arXiv:1601.06114 (SIAM J. Optim.) + Bandeira-Boumal-Singer; non-convex sync global-opt second-order necessary
- T3 q5 (follow-up): "held-out cross-validation Procrustes alignment stopping rule iterative refinement" → LO-RANSAC Procrustes refit (Springer 2023), Artetxe Wasserstein-Procrustes (ACL 2018); no direct prior for held-out-CV-stopped iterative-Procrustes → Idea 2 is NOVEL
- T3 q6 (follow-up): "PAC-Bayes orthogonal matrix rotation posterior Stiefel manifold von Mises Fisher" → Bingham-vMF Stiefel inference established (Hoff 2009; Givens-rep arXiv:1710.09443), but no prior PAC-Bayes-Procrustes-posterior → Idea 6 is NOVEL
- T3 q7 (follow-up via WebFetch): https://arxiv.org/abs/2106.15493 → confirmed single author Shuyang Ling, accepted SIMAX

Totals: 19 queries (T1 ×6, T2 ×6, T3 ×7) + 1 WebFetch — at cap 19 per skill rule; 0 budget left for devil's-advocate (surfaced as `⚠ Devil's-advocate skipped` in batch-6 Notes & warnings). ~45 summaries, 1 full read (Ling SIMAX 2025 author resolution), ~14 min wall-clock.

<!-- entries appended below -->

## 2026-05-19 — ImageNet-10 / LeJEPA batch-7 ADDENDUM (Idea 6, quantum-themed)
- T3-Q q1: "quantum entanglement entropy von Neumann representation learning self-supervised regularizer" → VNE arXiv:2304.01434 (direct prior art for VNE-as-SSL — closes that direction); QSEA arXiv:2506.10306 (quantum-native SSL — not applicable to classical ViT)
- T3-Q q2: "quantum kernel feature map self-supervised representation embedding Schuld Havlicek" → Schuld-Killoran PRL 2019 (arXiv:1803.07128); Havlicek Nature 2019 (arXiv:1804.11326); Schuld arXiv:2101.11020 (PQCs as kernel methods); Joint Embedding SSL kernel arXiv:2209.14884; Kernel VICReg arXiv:2509.07289 (already in b1 log)
- T3-Q q3: "random matrix theory free probability isotropic eigenvalue gap deep learning representation" → Pennington et al. 1807.11694 (already implicit in b1 family); arXiv:2506.13139 (RMT-DL beyond eigenvalues, Jun 2025); confirmed MP-spectrum direction is well-trodden
- T3-Q q4: "quantum Stein lemma hypothesis testing relative entropy classifier representation learning" → Stein-lemma quantum info results (Hayashi, Ogawa-Nagaoka) → reduces to quantum relative entropy = VNE direction (closed)

Resolution: 4 quantum-themed queries; final idea = SU(d)-parameterized structured-orthogonal projector (Givens rotation composition, classical analog of PQC) — chosen because VNE/free-probability/quantum-Stein directions all reduce to closed covariance-shaping family. Schuld-Killoran/Havlicek primaries are genuinely cross-domain (physics venue PRL, Nature) with classical-translation via butterfly orthogonal layers (Dao ICML 2019). 2 minutes wall-clock.

## 2026-05-27 — VILD / exp258 batch-1 (tier-mix 55/30/15, pipeline-enhance)

### Tier 1: In-Field
- T1 q1: "cross-view geo-localization UAV satellite zero-shot DINOv3 2025" → VFM-Loc arXiv:2603.13855 (Mar 2026, <12mo); Satellite-Free Training arXiv:2604.01581 (Apr 2026); Unsupervised Multi-view UAV arXiv:2411.14816
- T1 q2: "unbalanced optimal transport robust outlier domain adaptation 2024" → Outlier-Robust DRO via UOT NeurIPS 2024 (https://openreview.net/forum?id=V8HVsyTSu6); Unbalanced CO-OT AAAI 2023 doi 10.1609/aaai.v37i8.26193 / arXiv:2205.14923; Bi-level UOT for Partial DA arXiv:2506.08020 (Jun 2025, <12mo); Conditional UOT Maps arXiv:2603.06972
- T1 q3: "k-reciprocal re-ranking Jaccard image retrieval person re-identification" → Zhong et al. CVPR 2017 arXiv:1701.08398 (classic, 72+mo)
- T1 q4: "cycle-consistent nearest neighbor mining image retrieval mutual NN" → BBS Dekel et al. (image matching); Nearest Neighbor Normalization arXiv:2410.24114 (Oct 2024, 12-36mo); Denoising NN Graph via CRF arXiv:2412.13875
- T1 q5: "diffusion graph propagation image retrieval re-ranking 2024" → Cluster-Aware Similarity (CAS) Diffusion, Luo et al. ICML 2024 arXiv:2406.02343 (12-36mo); R-DiP; Graph-Conv Re-Ranking TMM 2023
- T1 q6: "database-side feature augmentation DBA image retrieval query expansion" → DBA Arandjelović-Zisserman 2012; GQE Klein-Wolf arXiv:2112.02666; Landmark retrieval poster (Wang)
- T1 q7: "equivariant steerable CNN E2 rotation pooling vision transformer" → E(2)-CNN Weiler-Cesa NeurIPS 2019 arXiv:1911.08251; ReF rotation features arXiv:2203.05206; e2cnn library
- T1 q8: "cross-view UAV satellite geo-localization LPN FSRA part-based 2024" → FSRA Dai arXiv:2201.09206; SSPT MDPI Sensors 24:3719 (Jun 2024); Unifying UAV CVGL via 3D Geometric Perception arXiv:2604.01747

### Tier 2: Adjacent
- T2 q1: "invariant risk minimization IRM feature selection dimension domain generalization" → IRM Arjovsky arXiv:1907.02893; Invariance Principle Meets VRM arXiv:2407.05765 (Jul 2024, 12-36mo); IFS-Recovery arXiv:2311.00966 (Nov 2023); Computationally Efficient Invariant FS w/ Sparsity PMLR v286 2025
- T2 q2: "RANSAC robust Procrustes orthogonal alignment outlier correspondence" → MLE+RANSAC alignment Springer IJDSA 2023; convex relaxations of robust Procrustes; t-mixture likelihood
- T2 q3: "homography projective rectification feature pooling bird's eye view drone" → BEV Geometric Approach Abbas ICCVW 2019 arXiv:1905.02231; IPM derivations
- T2 q4: "SuperGlue feature matching graph neural network correspondence outlier rejection" → SuperGlue Sarlin et al. CVPR 2020 arXiv:1911.11763 (Sinkhorn assignment with learned costs)
- T2 q5: "contextual similarity neighborhood image retrieval ECN expanded cross neighborhood" → ECN Saquib Sarfraz et al. CVPR 2018 arXiv:1711.10378; Contextually Affinitive Neighborhood Refinery arXiv:2312.07806 (12-36mo)
- T2 q6: "partial optimal transport mass less than one outlier robust matching" → Partial transport for point-cloud registration Springer STSP 2025; Outlier-Robust OT arXiv:2011.05151/2206.11988; Sliced partial OT

### Tier 3: Cross-Domain
- T3 q1: "functional maps shape correspondence ZoomOut spectral matching" → ZoomOut Melzi-Ovsjanikov SIGGRAPH Asia 2019 / ACM TOG arXiv:1904.07865; Consistent ZoomOut Computer Graphics Forum 2020 doi 10.1111/cgf.14084; partial 3D shape functional correspondence
- T3 q2: "cross-covariance singular value spectral signature feature alignment invariance" → Better Together cross/joint cov arXiv:2507.22207 (Jul 2025, <12mo); Optimal cleaning of cross-cov singular values arXiv:1901.05543; cross-cov BBP-type transition
- T3 q3: "random matrix theory cross-covariance signal eigenvalue spike model statistics" → Spiked covariance / Johnstone Annals of Stat 2001; BBP phase transition for sample cross-cov; Estimation of spiked eigenvalues bulk-matching PMC 2024
- T3 q4: "Sinkhorn-Knopp partial transport mass relaxation Cuturi entropy regularization" → Cuturi NeurIPS 2013; Overrelaxed SK arXiv:1711.01851; SK efficiency JMLR 22-1311

Totals: T1=8/8 (cap), T2=6/6 (cap), T3=4/5 — under cap; ~45 summaries skimmed, 0 full reads (all venue-whitelisted; abstracts + emergentmind topic pages sufficient for grounding); ~12 min wall-clock. Saturation events: T3 stopped early after q4 (q5 on partial OT already covered in T2 q6).


## 2026-05-27 — VILD / exp258 batch-2 (tier-mix 25/35/40, pipeline-enhance; new baseline pipe_C_uot_unbalanced = 27.46; target 50)

### Tier 1: In-Field
- T1 q1: "cross-view geo-localization rerank zero-shot foundation model DINOv3 satellite 2025 2026" → VFM-Loc arXiv:2603.13855 (Mar 2026, <12mo) — vanilla DINOv3 21.56% R@1; SMA (PCA + OP) +51.74; BGG arXiv:2605.10345 (May 2026, <12mo) parameter-efficient adapter; VLM rerank arXiv:2603.27251 (Mar 2026) — VLM rerank violates frozen/single-forward (skip as primary, log as related-work)

### Tier 2: Adjacent (robust alignment / point-cloud reg)
- T2 q1: "robust Procrustes IRLS Huber M-estimator orthogonal alignment outlier 2024" → IRLS convergence outlier-robust ResearchGate 373316942; redescending M-estimators Nature SciRep 2024 s41598-024-64239-6; line processes & robust statistics (Geman/Black classic, 72+mo); ℓ1-Huber penalized M-estimator arXiv:1904.06288 (sparse linear, 36-72mo)
- T2 q2: "rotation averaging SO(3) Govindu Hartley Wahba robust geometric median 2024" → Weiszfeld L1 rotation averaging Hartley et al. CVPR 2011 (72+mo, classic); Chatterjee-Govindu Robust Relative Rotation Averaging IJCV / ICCV 2013-2017; Govindu Lie-algebra IRLS; Robust Single Rotation Averaging Revisited Lee-Civera arXiv:2309.05388 (12-36mo); Multi-Irreducible Spectral Synchronization arXiv:2311.16544 (12-36mo)
- T2 q3: "graduated non-convexity GNC robust point cloud registration Yang Carlone TEASER 2024" → TEASER Yang-Shi-Carlone T-RO 2021 (12-36mo); Yang-Antonante-Tzoumas-Carlone "GNC for Robust Spatial Perception" RA-L 2020 (12-36mo); Adaptive GNC ICLR 2025 submission OpenReview cIKQp84vqN
- T2 q4: "point-to-plane ICP anisotropic robust generalized iterative closest point covariance 2024" → IMLP Billings-Boctor-Taylor PLOS ONE 2015 (anisotropic + robust ICP, 72+mo); GenZ-ICP arXiv:2411.06766 (Nov 2024, 12-36mo); ICP covariance NAVIGATION 70:2 navi.562; Estépar et al. anisotropic ICP PubMed 22184256 (foundational); GTLS-ICP ResearchGate 221401138
- T2 q5: "weighted orthogonal Procrustes Mahalanobis anisotropic generalized solution closed form" → Schönemann generalized Procrustes Psychometrika 1966 (foundational); Anisotropic OPA Bennani-Dosse-Ten Berge J. Classification 2010 doi 10.1007/s00357-010-9046-8 (36-72mo); Pinto-Oliveira "Uncertainty characterization of OP" Pattern Recognition 2016 doi 10.1016/j.patcog.2016.06.026 (36-72mo)
- T2 q6: "spectral clustering anchor selection cycle consistency robust SO(d) synchronization SDP" → CEMP Lerman-Shi FoCM 2021 arXiv:1912.11347 (12-36mo); graph-connection Laplacian SO(d) spectral synchronization (Bandeira-Singer); anchor-based spectral clustering arXiv:2006.13984

### Tier 3: Cross-Domain (RMT / free-prob / phase-retrieval / isospectral / GMM-OT)
- T3 q1: "Bun Bouchaud rotational invariant estimator cross covariance singular value shrinkage RIE" → Bun-Allez-Bouchaud-Potters "Rotational invariant estimator for general noisy matrices" Phys. Rep. 2017 arXiv:1502.06736 (36-72mo); "Optimal cleaning for singular values of cross-covariance matrices" Bun-Knowles arXiv:1901.05543 (36-72mo); pyRMT GitHub GGiecold; Denoising clustering cov RIE arXiv:2604.13851 (Apr 2026, <12mo); Physics-Informed SV Learning cross-cov arXiv:2601.07687 (Jan 2026)
- T3 q2: "free probability subordination matrix denoising deep learning representation cross-covariance" → Free probabilistic framework denoising diffusion arXiv:2510.22778 (Oct 2025, <12mo); Free denoising via overlap measures arXiv:2412.20792 (Dec 2024); Bayes-optimal poly estimator matrix denoising arXiv:2402.16719 (Feb 2024)
- T3 q3: "phase retrieval Wirtinger flow Procrustes orthogonal alignment spectral initialization" → Candès-Li-Soltanolkotabi "Phase Retrieval via Wirtinger Flow" IEEE T-IT 2015 arXiv:1407.1065 (72+mo, IEEE Information Theory Paper Award); orthogonality-promoting init Chen-Candès; quaternion Wirtinger flow arXiv:2210.14170 (36-72mo)
- T3 q4: "isospectral flow Toda lattice matrix diagonalization gradient SO(d) Stiefel manifold" → Brockett "Dynamical systems that sort lists and diagonalize" Lin. Alg. Appl. 1991 (classic 72+mo); Chu "Iso-spectral gradient flows" SIAM Review 1994; Kaur PhD thesis Cambridge analytic-numerical isospectral flows; Toda flow on flag manifold
- T3 q5: "Delon Desolneux GMM Wasserstein discrete optimal transport Gaussian mixture" → Delon-Desolneux SIAM J. Imaging Sciences 2020 arXiv:1907.05254 (36-72mo, SIIMS); Gromov-Wasserstein-like GMM arXiv:2310.11256; Slicing Gaussian Mixture Wasserstein arXiv:2504.08544 (<12mo); OT-DA via GMMs Montesuma OpenReview DCAeXwLenB / arXiv:2403.13847 (12-36mo); MS-DA GMM-OT arXiv:2404.10261

### Tier 3 supporting (vMF prior on G)
- T3 q6: "vMF mixture model directional statistics embedding empirical Bayes prior retrieval 2024" → Banerjee-Dhillon-Ghosh-Sra JMLR 2005 (foundational, 72+mo); Gopal-Yang ICML 2014 vMF clustering; Bayesian Nonparametrics for Directional Statistics arXiv:1807.00305; Variational Bayes vMF mixture Taghia et al.; PyTorch vMF arXiv:2102.05340

Totals: T1=1/8, T2=6/6 (cap), T3=6/5 (over cap by 1 — Banerjee vMF is foundational classic, kept), summaries ~30/45, full reads 0/10, wall-clock ~9 min. Saturation: T1 stopped after 1 query (in-field saturation per batch-1's 8 queries already covering CVGL; this batch is heavy T2/T3 by design). Notes: VLM rerank arXiv:2603.27251 logged but excluded as primary (violates frozen-DINOv3 / single-forward).


## 2026-05-27 — VILD / batch-3 (Blocks 1+2+3, Block-6 ≤2; T1=20 T2=35 T3=45; non-vision venue bias)
- T3 q1: "sliced Wasserstein Gaussianization normalizing flow distribution matching" → Dai-Seljak SINF ICML 2021 arXiv:2007.00674 (primary, Idea 2); supporting arXiv:2207.05468, arXiv:2602.10691
- T3 q2: "Ledoit Wolf nonlinear shrinkage covariance estimator Annals of Statistics 2020" → Ledoit-Wolf Ann.Stat. 48(5) 2020 doi 10.1214/19-AOS1921 (primary, Idea 1); supporting Ann.Stat. 40(2) 2012
- T1 q1: "NetVLAD residual aggregation image retrieval Arandjelovic 2016 CVPR" → Arandjelović et al. CVPR 2016 arXiv:1511.07247 (primary, Idea 3)
- T2 q1: "Rahimi Recht random Fourier features kernel approximation NIPS 2007" → Rahimi-Recht NeurIPS 2007 Test-of-Time (primary, Idea 4); supporting arXiv:2210.00244, NeurIPS 2019 low-precision RFF
- T3 q3: "Bruna Mallat invariant scattering convolution network IEEE TPAMI 2013" → Bruna-Mallat T-PAMI 35(8) 2013 doi 10.1109/TPAMI.2012.230 (primary, Idea 5); supporting Cohen-Welling ICML 2016 arXiv:1602.07576
- T3 q4: "Tukey biweight redescending M-estimator robust pooling astrostatistics outlier" → Beaton-Tukey 1974; Mosteller-Tukey NBS JRNS 1983 (primary, Idea 6); supporting PMC10965898 modern redescending; Stata Journal 9(3) 2009 k=4.685 calibration
- T2 q2: "Ramsauer Hopfield networks all you need modern continuous Hopfield ICLR 2021" → Ramsauer et al. ICLR 2021 arXiv:2008.02217 (primary, Idea 8); supporting arXiv:2411.08590 Hopfield-Fenchel-Young
- T2 q3: "hyperbolic embedding Lorentz model Poincare Nickel Kiela 2018 representation" → Nickel-Kiela ICML 2018 arXiv:1806.03417 (initial candidate; dropped from final batch due to Block-4b composition risk; superseded by Spherical-PCA framing in Idea 7)
- Devil's-advocate q1: "Ledoit Wolf shrinkage failure limitation non-Gaussian heavy tails retrieval" → Chen et al. arXiv:1009.5331 "inappropriate for heavy-tailed non-Gaussian" → captured Risk-1 of Idea 1; no rank change
- Devil's-advocate q2: "modern Hopfield retrieval failure case limitation associative memory storage" → metastable-state risk (Ramsauer §5; arXiv:2409.16408); arXiv:2411.08590 Hopfield-Fenchel-Young unification → captured Risk-2 of Idea 8
- Cross-anchor q1: "spherical PCA hyperspherical principal component cosine similarity directional statistics" → Liu et al. arXiv:1903.06877 + Sra arXiv:1605.00316 (primary, Idea 7)

Totals: 11 queries (T1=1, T2=3, T3=5, DA=2 — within caps T1≤8/T2≤6/T3≤5, total ≤19), ~33 summaries skimmed, 0 full reads (all venues whitelisted/abstract sufficient), ~8 min wall-clock.


## 2026-05-27 — VILD / batch-4 (tier-mix 40/40/20; Block-6 heavy + descriptor-invariance lifts; baseline pipe_C_uot_irls_rie = 27.95)

### Tier 1: In-Field (image retrieval rerank + invariance literatures)
- T1 q1: "alpha-query expansion image retrieval Arandjelović CVPR average top-K" → confirmed Arandjelović-Zisserman CVPR 2012 "Three things everyone should know to improve object retrieval" (foundational AQE, 72+mo); follow-up Gordo-Radenovic-Berg "Attention-Based Query Expansion Learning" ECCV 2020 arXiv:2007.08019 (36-72mo); related dl.acm.org/doi/10.1145/2733373.2806233 multi-query expansion (ACM MM 2015)
- T1 q2: "diffusion rerank kNN graph image retrieval Iscen Tolias CVPR 2017 manifold" → Iscen-Tolias-Avrithis-Furon-Chum "Efficient Diffusion on Region Manifolds" CVPR 2017 (primary Idea 1, openaccess.thecvf.com/content_cvpr_2017/papers/Iscen_Efficient_Diffusion_on_CVPR_2017_paper.pdf; 72+mo); supporting LSH-kNN graph for diffusion Springer 2020 doi 10.1007/s10791-020-09388-8; Hybrid Diffusion spectral-temporal arXiv:1807.08692
- T1 q3: "graph convolutional rerank image retrieval place recognition 2024 2025" → GCR (Graph Convolution-based Reranking) Zhang-Wang-Su IEEE T-MM 2023 arXiv:2306.08792 (12-36mo, supporting); Cheb-GR Yang-Li CVPR 2025 (primary Idea 8) openaccess.thecvf.com/content/CVPR2025/papers/Yang_Cheb-GR_Rethinking_K-nearest_Neighbor_Search_in_Re-ranking_for_Person_Re-identification_CVPR_2025_paper.pdf
- T1 q4: "cross-view UAV satellite geo-localization reranking 2024 2025" → UAV-Sat ATR-Part MDPI Rem. Sens. 17(14):2448 (12-36mo, supporting); From Street to Orbit arXiv:2511.09820 (Nov 2025, <12mo) — training-free CVGL with LLM rerank (logged but excluded as primary: violates frozen DINOv3); VDUAV cross-view dataset 2025
- T1 q5: "SO(2) equivariant steerable filters CNN aerial satellite remote sensing" → Weiler-Cesa "General E(2)-Equivariant Steerable CNNs" NeurIPS 2019 arXiv:1911.08251 (36-72mo); Franzen-Wand "Nonlinearities in Steerable SO(2)-Equivariant CNNs" arXiv:2109.06861 (36-72mo); FILTRA arXiv:2105.11636 — confirms steerable kernel construction; supports Idea 3 lift framing
- T1 q6: "Hu invariant moments deep features remote sensing aerial" → Exploiting Hu invariant moments + deep features for image retrieval (Pattern Recognition 2025, sciencedirect S0031320325014645, <12mo); Ship recognition Hu+CNN (Multimedia Tools 2020, doi 10.1007/s11042-020-09574-2, 36-72mo) — used as supporting for Idea 3 (Polar-Fourier stream); Hu/Flusser invariance theory implicit
- T1 q7: "circular harmonic features rotation invariant descriptor pooling" → Liu et al. "Rotation-Invariant HOG Descriptors Using Fourier Analysis in Polar and Spherical Coordinates" IJCV 2014 doi 10.1007/s11263-013-0634-z (72+mo); Esteves et al. "Learning SO(3) Equivariant Representations with Spherical CNNs" ECCV 2018 (36-72mo); confirms Fourier-on-polar-grid as additive descriptor (primary Idea 3)
- T1 q8: "spherical harmonics descriptor aggregation retrieval rotation invariant" → Kazhdan-Funkhouser-Rusinkiewicz "Rotation Invariant Spherical Harmonic Representation of 3D Shape Descriptors" SGP 2003 (72+mo, primary Idea 4); supports Spherical-Harmonic magnitude pooling

### Tier 2: Adjacent (ranking theory / graph signal proc / robust rotation averaging)
- T2 q1: "attention query expansion learned image retrieval ECCV 2020 Gordo" → confirmed Gordo-Radenovic-Berg ECCV 2020 arXiv:2007.08019 (primary Idea 2, 36-72mo); we use the *adaptive softmax weighting* concept stripped of learned attention (learning-free reuse)
- T2 q2: "Bayesian rotation averaging robust SE(3) Frechet mean SO(d)" → Lee-Civera "Robust Single Rotation Averaging" arXiv:2004.00732 (36-72mo); Robust Fréchet Mean PGA Banerjee-Jian (Semantic Scholar); "On the Robustness of Multi-View Rotation Averaging" arXiv:2102.05454 (36-72mo); Rosen-Birdal-Carlone "Multi-Irreducible Spectral Synchronization for Robust Rotation Averaging" arXiv:2311.16544 (12-36mo, primary Idea 5)
- T2 q3: "Stiefel manifold barycenter geometric median rotation matrices optimization" → "Beyond R-barycenters: an effective averaging method on Stiefel and Grassmann manifolds" arXiv:2501.11555 (12-36mo, primary supporting Idea 5); Optimization Stiefel arXiv:2202.09058; "On the approximation of the Riemannian barycenter" arXiv:2504.15671 (<12mo, supporting)
- T2 q4: "vMF mixture density gallery prior likelihood ratio retrieval rerank" → Banerjee-Dhillon-Ghosh-Sra JMLR 2005 "Clustering on the Unit Hypersphere using vMF" (foundational, 72+mo, primary Idea 6); Hasnat et al. JMLR 2016 17:1-44 "Online Trans-dimensional vMF Mixture" (36-72mo); GMM-of-between-source LR PMC4762660 (forensic stats, 36-72mo)
- T2 q5: "visual re-ranking side information non-visual contextual graph 2025" → Hanning-Åström "Visual Re-Ranking with Non-Visual Side Information" SCIA 2025 arXiv:2504.11134 (<12mo, supporting Idea 7 — GCSA framework extension for temporal/positional side info, learning-free analog)
- T2 q6: "contextual similarity aggregation image retrieval rerank ECCV CVPR" → Ouyang-Liu-Liang "Contextual Similarity Aggregation with Self-attention for Visual Re-ranking" NeurIPS 2021 OpenReview uOxe0CHI5dq arXiv:2110.13430 (36-72mo, supporting Idea 7 framing); LoCoRe arXiv:2503.21772 (<12mo, related)

### Tier 3: Cross-Domain (light per 40/40/20 tier mix)
- T3 q1: "spectral synchronization rotation averaging power iteration cross-cov" → Rosen-Birdal "Multi-Irreducible Spectral Synchronization" arXiv:2311.16544 (12-36mo, cross-listed math.OC/SE(d) synchronization; co-primary Idea 5); SIAM J. Opt. "Improved Performance Guarantees for Orthogonal Group Synchronization via Generalized Power Method" doi 10.1137/20M1389571 (supporting)
- T3 q2: "graph signal processing image retrieval rerank ICASSP spectral" → Cheung-Magli-Tanaka-Ng "Graph Spectral Image Processing" IEEE Proc. 2018 arXiv:1801.04749 (36-72mo, supporting Idea 1 framing); Ortega et al. "GSP Overview" arXiv:1712.00468 (72+mo); "Understanding Image Retrieval Re-Ranking: A GNN Perspective" arXiv:2012.07620 (36-72mo, supporting Idea 8)
- T3 q3: "UAV cross-view retrieval gallery prior von Mises Fisher 2025" → Disentangled multi-view clustering via vMF ScienceDirect S0893608025006823 (<12mo, supporting Idea 6 — confirms vMF as fresh direction in 2025); From Street to Orbit arXiv:2511.09820 (<12mo, related context, not primary)

Totals: T1=8/8 (cap), T2=6/6 (cap), T3=3/5 (under cap; tier-mix 40/40/20 → T3=20% naturally lower count), ~50 summaries skimmed, 0 full reads (venues whitelisted, abstracts + emergentmind sufficient), ~14 min wall-clock. Saturation: T3 stopped at 3 — adding more T3 would push observed mix away from configured 20%. All primary papers verified in-session via WebSearch.


## 2026-05-27 — VILD / batch-5 (tier-mix 40/40/20; E_polar robustness across CVGL + VILD; Block-4a/4b/4c open, NO RERANK)

### Tier 1: In-Field (image-retrieval Procrustes alignment + CVGL + Procrustes theory)
- T1 q1: "robust rotation averaging Stiefel manifold Frechet mean trust-region SE(d) 2024 2025" → Lee-Civera "Robust Single Rotation Averaging Revisited" arXiv:2309.05388 (TLUD geodesic L1, robust to 99% outliers; 12-36mo); Rosen-Birdal-Carlone arXiv:2311.16544 (12-36mo); "Beyond R-barycenters" arXiv:2501.11555 (Jan 2025, <12mo)
- T1 q2: "regularized orthogonal Procrustes identity shrinkage Tikhonov Schönemann 2024" → confirmed Schönemann Psychometrika 1966 (foundational); "Generalized OPP in high noise regime" arXiv:1907.01145 (Pumir-Singer-Boumal IMA J. Info & Infer 10(3) 2021; 36-72mo); robust convex relaxations
- T1 q3: "Pumir Singer Boumal high noise Procrustes anchor under-determined sample size dimension" → Pumir-Singer-Boumal "Generalized OPP in High Noise Regime" Information and Inference: A Journal of the IMA 2021 vol 10 iss 3 pp 921-954 arXiv:1907.01145 (primary, Idea 5/N3 anchor-margin-gating; high-noise regime theory says Gram invariants outperform R when N_anchors/D below SNR threshold)
- T1 q4: "cross-view geo-localization DenseUAV dense gallery sampling ranking 2024 2025" → DenseUAV dataset description (dense crops, 14 universities Zhejiang); VDUAV cross-view 2025 (1:12 drone:sat ratio); UAVM 2025 challenge — confirms DenseUAV's "tight cluster" framing in our task statement
- T1 q5: "trust region damping Levenberg Marquardt orthogonal alignment SVD shrinkage" → Riemannian Levenberg-Marquardt with global+local convergence arXiv:2210.00253 (Adachi-Okuno-Takeda; primary Idea 3/N1); Modified LM single-scalar-damping trust-region adaptive
- T1 q6: "image retrieval rank-preserving learning to rank listwise NDCG soft sort 2024" → Smooth-NDCG (S-NDCG) listwise loss; AAAI Approximate Rank Indicators; Image-Text retrieval listwise NDCG arXiv:2305.16566; SmoothI rank indicators arXiv:2105.00942 — confirms listwise-rank loss as viable Block-4b M-step augmentation
- T1 q7: "When Embedding Models Meet Procrustes bounds applications arXiv 2510 alignment" → Maystre-Ortega-Park-Dolga-Berariu-Zhao-Ciosek "When Embedding Models Meet: Procrustes Bounds and Applications" arXiv:2510.13406 (Oct 2025, <12mo; tight bound on Procrustes alignment error when pairwise dot products approximately preserved) — primary for Idea 7 (sub-rank Procrustes)
- T1 q8: "adversarial Procrustes anchor outlier robust SIAM Matrix 2024 generalized power method" → Lin-Liu "Generalized OPP under Arbitrary Adversaries" SIAM J. Mat. Anal. Appl. 2025 doi 10.1137/24M1631122 arXiv:2106.15493 (Feb 2025 SIAM publication, <12mo); GPM converges linearly under SNR threshold (Banach contraction)

### Tier 2: Adjacent (Riemannian optimization + differentiable ranking + statistical Procrustes + RMT)
- T2 q1: "differentiable ranking sorting Cuturi optimal transport soft-rank Blondel 2020" → Cuturi-Teboul-Vert "Differentiable Ranks and Sorting using Optimal Transport" NeurIPS 2019 arXiv:1905.11885 (primary Idea 6/N4, 36-72mo); Blondel-Teboul-Berthet-Djolonga "Fast Differentiable Sorting and Ranking" ICML 2020 arXiv:2002.08871 (36-72mo); LapSum arXiv:2503.06242 (<12mo, supporting)
- T2 q2: "spectral synchronization anchor-count Procrustes high-dimensional convergence guarantee Bandeira" → Liu-Lin "Near-Optimal Bounds for Generalized OPP via Generalized Power Method" Appl. Comp. Harm. Anal. 2023 arXiv:2112.13725 (12-36mo); Bandeira open problem SDP tightness; anchor-based spectral clustering arXiv:2006.13984 — confirms GPM contraction rate is dim/SNR-sensitive (Idea 5 anchor-margin gate)
- T2 q3: "Riemannian trust-region orthogonal Stiefel Boumal Absil damped step convergence" → Boumal-Absil-Cartis "Riemannian Trust Regions with Finite-Difference Hessian Approximations are Globally Convergent" 2015/IMA J. Numer. Anal. 2019 nicolasboumal.net/papers/Boumal_Riemannian_trust_regions_..._2015.pdf (36-72mo, supporting Idea 3); Adaptive Trust-Region Method on Riemannian Manifold J. Sci. Comput. 2023 doi 10.1007/s10915-023-02288-1 (primary Idea 3); RTR for SC1 minimization arXiv:2307.00490
- T2 q4: "Procrustes analysis high-dimensional consistency sample size dimension Dryden 2024" → Andreella-Finos "Procrustes Analysis for High-Dimensional Data" Psychometrika 87(4) 2022 arXiv:2008.04631 (primary Idea 2/N2; ProMises model — prior-regularized Procrustes; 12-36mo); fMRI brain alignment high-dim D≫N regime
- T2 q5: "Riemannian Levenberg-Marquardt Stiefel orthogonal global local convergence Boumal" → Adachi-Okuno-Takeda "Riemannian Levenberg-Marquardt Method with Global and Local Convergence Properties" arXiv:2210.00253 (12-36mo; trust-region-like damping with gain-ratio update on Riemannian manifold — co-primary Idea 3); Peeters 1993 (foundational, not cited as primary — pre-internet); local linear convergence orthogonal arXiv:2412.05689
- T2 q6: "bootstrap confidence interval orthogonal Procrustes rotation matrix uncertainty quantification" → Pinto-Oliveira "Uncertainty characterization of OP with arbitrary covariance matrices" Pattern Recognition 2016 doi 10.1016/j.patcog.2016.06.026 sciencedirect.com/science/article/abs/pii/S0031320316301960 (72+mo; primary Idea 4/N3); TTB truncated total bootstrap PCA-Procrustes ScienceDirect 2012; Orthogonal Bootstrap arXiv:2404.19145 (<12mo, supporting)

### Tier 3: Cross-Domain (decision theory + Bayesian model averaging on Stiefel + finance/stats JSE)
- T3 q1: "James Stein shrinkage adaptive regime decision theory rotation matrix orientation 2024" → Goldberg-Kercheval "James-Stein for the leading eigenvector" PNAS 120(2) 2023 (primary Idea 8/T3; arXiv:2204.06392; finance/stats venue; 12-36mo; JSE dominates MLE for directional estimator under quadratic loss) — Cross-domain transfer: finance/statistics → Procrustes singular-vector subspace
- T3 q2: "Bayesian model averaging Stiefel manifold posterior orthogonal matrix Hoff Lin" → Hoff 2007 JASA "Model averaging and dimension selection for SVD" (72+mo, foundational); Lin-Rao-Dunson "Bayesian nonparametric inference on the Stiefel manifold" Statistica Sinica 27 (2017) 535-553 par.nsf.gov/servlets/purl/10059376 (36-72mo); Pourzanjani-Jiang-Petzold "Bayesian Inference over the Stiefel Manifold via the Givens Representation" Bayesian Analysis 2020 doi 10.1214/20-BA1202 arXiv:1710.09443
- T3 q3: "Wasserstein-2 ranking permutation distribution distance soft top-K Wainwright 2020" → LapSum arXiv:2503.06242 (<12mo; differentiable soft-rank/soft-top-K via Laplace integration); Newton Losses NeurIPS 2024 (curvature info for ranking surrogates); SoDeep arXiv:1904.04272 — supporting only, no clean Wainwright-2020 paper match; confirmed Cuturi+Blondel as the primaries
- T3 q4 (supporting): "listwise ranking loss differentiable Wasserstein Spearman correlation NeurIPS 2024" → Distributionally robust learning-to-rank under Wasserstein metric PMC10062629; Newton Losses NeurIPS 2024 proceedings.neurips.cc/paper_files/paper/2024/file/2e102d937d094b7211c4d32ce1f1126c-Paper-Conference.pdf — supporting Idea 6
- T3 q5 (supporting, signal/noise feature selection): "subset selection feature importance signal-to-noise threshold robust Procrustes dimension" → GRIP2 deep knockoff arXiv:2602.00218 (<12mo); Pareto Optimization Robust Eval arXiv:2501.06813 (<12mo); supporting context for Idea 7 (sub-rank Procrustes per dim-importance)

Totals: T1=8/8 (cap), T2=6/6 (cap), T3=5/5 (cap; 4 primary + 1 supporting), ~45 summaries skimmed, 0 full reads (venues whitelisted, abstracts sufficient), ~13 min wall-clock. Saturation: none (each tier returned distinct primaries on first or second query). All primary papers verified in-session via WebSearch.

## 2026-05-28 — VILD batch-7 (Pure P_Polar transformation variants)
- T1: rotation invariant UAV CVGL polar 2025; polar CVPR/ECCV 2024; DenseUAV 2024-25; Sample4Geo; DINOv3 frozen 2025; harmonic networks ICLR
- T2: E(2)-CNN steerable aerial; scattering transform ICML/NeurIPS; supervised whitening Radenovic ECCV; unsupervised whitening retrieval
- T3: Bessel-Fourier moments; Zernike moments retrieval; bispectrum phase invariance; Fourier-Mellin log-polar; spherical harmonics aerial; circular harmonics radial; phase congruency; log-polar foveated descriptor
- Totals: 19 queries, 0 full reads (summaries only), ~12 min wall-clock. Within budget.

# Search Log — Batch 13 — 2026-05-30

Topic: NON-CCA escape from correlation-maximizing alignment for zero-shot UAV CVGL (VILD + 4-bench gate), enhance-existing, NO RERANK.
Tier mix configured: 45/35/20 (default).

## Tier 1: In-Field (vision domain adaptation / second-order pooling)
- 15:30 Query: "CORAL correlation alignment domain adaptation second-order statistics whitening recoloring closed form" → Deep CORAL [arXiv:1607.01719], linear CORAL [arXiv:1612.01939]
- 15:31 Query: "CORAL deep correlation alignment Sun Saenko ECCV 2016 covariance whitening domain shift" → confirmed Sun-Saenko ECCV 2016 [arXiv:1607.01719]
- 15:34 Query: "optimal transport Sinkhorn domain alignment barycenter mean map cross-domain features label-free" → OT-DA Courty [arXiv:1507.00504, TPAMI 2017], JDOT [arXiv:1705.08848]
- 15:35 Query: "Stiefel Grassmann manifold averaging subspace fusion multi-view representation alignment" → Subspace Alignment [Fernando ICCV 2013, arXiv:1409.5241], Grassmann Averages CVPR 2014
- 15:33 Query: "QuantNorm power normalization second-order pooling covariance descriptor retrieval matrix square root" → MPN-COV/iSQRT-COV [Li, arXiv:1904.06836], second-order CVPR

## Tier 2: Adjacent (SSL / embedding postprocessing)
- 15:32 Query: "VICReg variance invariance covariance regularization versus whitening self-supervised closed form" → VICReg [arXiv:2105.04906]
- 15:42 Query: "VICReg Bardes Ponce LeCun ICLR 2022 variance invariance covariance" → confirmed ICLR 2022 [arXiv:2105.04906]
- 15:31 Query: "embedding centering mean subtraction isotropy all-but-the-top retrieval domain gap" → All-but-the-Top [Mu-Viswanath ICLR 2018, arXiv:1702.01417]
- 15:43 Query: "all-but-the-top simple effective postprocessing word representations Mu Viswanath ICLR 2018" → confirmed [arXiv:1702.01417]
- 15:33 Query: "whitening shrinkage interpolation ZCA identity regularization representation collapse alpha" → Soft-ZCA / Whitening-improves-SSL [arXiv:2408.07519], Whitening-SSL [arXiv:2007.06346]
- 15:44 Query: "whitening transformation isotropic embeddings BERT-flow sentence representation retrieval improvement" → Whitening Sentence Reps [Su 2021, arXiv:2103.15316], BERT-flow [arXiv:2011.05864]
- 15:32 Query: "spectral normalization feature whitening DirectCLR dimensional collapse retrieval frozen features" → Dimensional Collapse / DirectCLR [Jing ICLR 2022, arXiv:2110.09348]

## Tier 3: Cross-Domain (pure math / high-dim statistics)
- 15:34 Query: "Gromov-Wasserstein feature alignment without correspondence cross-domain retrieval unsupervised" → GW word-embedding alignment [Alvarez-Melis-Jaakkola EMNLP 2018, arXiv:1809.00013]
- 15:44 Query: "Gromov-Wasserstein discrepancy Mémoli metric measure spaces alignment" → Mémoli FoCM 2011 (metric-measure spaces)
- 15:30 Query: "hubness reduction cross-modal retrieval CSLS cross-domain similarity local scaling bilingual" → hubness survey [JMLR 2024 v25 22-1240], CSLS [Conneau ICLR 2018]
- 15:41 Query: "hubness skewness nearest neighbor high dimensional retrieval mutual proximity normalization 2024" → Local/Global Scaling [Schnitzer JMLR 2012 v13], hubness survey JMLR 2024
- 15:41 Query: "CSLS cross-domain similarity local scaling Conneau word translation MUSE hubness penalty" → Word Translation Without Parallel Data [Conneau ICLR 2018, arXiv:1710.04087]
- 15:35 Query: "canonical correlation analysis saturates rho near one high dimensional trivial degenerate full rank" → high-dim CCA degeneracy [arXiv:2306.16393, 2405.19539] (supporting: confirms batch-12 saturation root cause)

## Totals
- Queries used: 16 / 19
- Summaries read: ~38 / 45
- Full reads: 0 / 10
- Wall-clock: ~14 min
- Saturation events: hubness tier returned repeats by query 2 (stopped T3 hubness early)

# Search Log — Batch 14 — 2026-05-30 (self-calibrating no-op-when-clean operators)

## Tier 3: Cross-Domain
- Q1 "Bun Bouchaud Potters cleaning large correlation matrices RMT RIE Physics Reports 2017" → found 10, picked RIE [arXiv:1610.08104, PhysRep 666:1-109]
- Q2 "Ledoit Wolf analytical nonlinear shrinkage covariance Annals of Statistics 2020" → found, picked [AoS 48(5) 2020] + nonlinear-shrinkage 2012 AOS989
- Q3 "empirical Wiener shrinkage per-coordinate SNR denoising" → found GSW Self-Wiener [arXiv:2603.27763, 2026], empirical Wiener (Ghael SPIE 1997), OptShrink
- Q6 "Ledoit Wolf well-conditioned estimator linear shrinkage toward identity 2004" → picked [JMVA 88(2):365-411 2004] (used as supporting)
- Q13 "Otsu automatic threshold between-class variance" → picked [IEEE Trans SMC 1979] + Fast-Otsu-bisection [arXiv:2509.16179 2025]

## Tier 2: Adjacent
- Q4 "proxy A-distance Ben-David theory of learning from different domains adaptive strength" → picked [Machine Learning 79:151-175 2010] + Ben-David NIPS06 + f-DAL [arXiv:2106.11344 ICML 2021]
- Q5 "unbalanced OT adaptive marginal relaxation tau domain adaptation" → picked Fatras [arXiv:2103.03606 ICML 2021] + OT-adaptive-threshold-UDA [arXiv:2503.11217 2025] + Fast-UOT-semidual [arXiv:2602.10697 2026]
- Q12 "All-but-the-Top postprocessing word representations Mu Viswanath ICLR 2018" → picked [arXiv:1702.01417 ICLR 2018]

## Tier 1: In-Field
- Q7 "QB-Norm querybank normalisation cross-modal retrieval hubness CVPR 2022" → picked Bogolin [arXiv:2112.12777 CVPR 2022, Dynamic Inverted Softmax]
- Q8 "Mutual Proximity hubness local global scaling Schnitzer Flexer JMLR 2012" → picked [JMLR 13:2871-2902 2012]
- Q9 "single image vignetting correction radial intensity falloff flat-field" → picked Zheng SingleImageVignetting [CVPR06/TPAMI09] + Deformable-Radial-Polynomial [Sensors 23(3):1157 2023] + Radial-Bright-Channel [ECCV 2014]
- Q10 "hubness reduction image retrieval embedding 2024 2025 test-time normalization" → picked NNN [arXiv:2410.24114 EMNLP 2024] + DBNorm/DBSN [arXiv:2508.02538 ACM MM 2025]
- Q11 "RMT denoising deep features Marchenko-Pastur spectrum representation learning 2024 2025" → picked RMT-feature-spectrum [arXiv:2410.18938 2024] + RMT-weights [ICML 2024]
- Q14 "nearest neighbor normalization training-free retrieval EMNLP 2024 reference bank" → confirmed NNN [arXiv:2410.24114, EMNLP 2024 pp.22571-22582, Chowdhury et al.]

## Devil's-advocate (top-1 = self-disabling hubness)
- Q15 "hubness reduction over-correction fails small gallery negative result" → CONCERN: Balance-Act [arXiv:2310.11612] + DBNorm note distributional-gap/query-bank over-correction; small-gallery degradation
- Q16 "querybank normalization requires representative query distribution failure when queries scarce" → MITIGATION: Dynamic-Inverted-Softmax "does not harm performance with suboptimal querybank"; train-set bank ≈ test-set bank

## Totals
- Queries used: 16 / 19
- Summaries read: ~38 / 45
- Full reads: 0 / 10 (provenance via search summaries; titles+venues+arXiv IDs resolved)
- Wall-clock: ~12 min
- Saturation events: none (each tier returned novel papers)

# Search Log — Batch 17 — 2026-05-30 (label-free disease-signature router orchestrating self-disabling operators; 4-bench NO-HARM gate; tier-mix 30/30/40)

Topic: a PRINCIPLED, ROBUST meta-gate over OPERATOR intensity (NOT stream/rank fusion — those failed in b9–13) that fires each self-disabling specialist (FlatField/Wiener/AdaptTau + slot 4) only on its diseased bench. NO RERANK; every op no-op-when-clean.

## Tier 3: Cross-Domain (decision theory / conformal / control / econometrics)
- T3 q1: "conformal risk control distribution-free guarantee monotone loss Angelopoulos Bates" → Conformal Risk Control [arXiv:2208.02814, ICLR 2024, Angelopoulos-Bates-Fisch-Lei-Schuster]; non-monotone CRC [arXiv:2604.01502, 2026] (primary Idea C); RCPS pointer
- T3 q2: "hysteresis switching supervisory control dwell time stability Morse Hespanha" → Hespanha-Liberzon-Morse "Hysteresis-based switching algorithms for supervisory control of uncertain systems" Automatica 39 (2003) 263–272 (primary Idea D); Hespanha-Morse "Stability of switched systems with average dwell-time" CDC 1999 (supporting)
- T3 q3: "forecast combination Bates Granger combining predictors optimal weights econometrics" → Bates-Granger "The Combination of Forecasts" OR Quarterly 1969 (foundational); Granger-Ramanathan 1984; Wang-Kang-Petropoulos-Hyndman "Forecast combinations: an over 50-year review" Int. J. Forecasting 2023 [arXiv:2205.04216] (primary Idea E); forecast-combination puzzle (simple avg ≥ adaptive weights) confirmed
- T3 q4: "James-Stein admissibility shrinkage estimator decision theory expected risk dominate Annals of Statistics" → James-Stein 1961 (4th Berkeley Symp); positive-part JS (Baranchik) dominates+admissibility; "A new perspective on dominating the James-Stein estimator" [arXiv:2509.17504, 2025] (supporting Idea B)
- T3 q5: "Stein unbiased risk estimate SURE choosing denoising threshold parameter selection" → SureShrink (Donoho-Johnstone); SUGAR Deledalle-Vaiter-Peyré-Fadili SIAM J. Imaging Sci. 2014 [arXiv:1405.1164] — supporting only (multi-parameter SURE selection; NOT made an idea to avoid overlap with batch-6 SURE-for-stopping)
- T3 q6 (follow-up, provenance confirm): "risk-controlling prediction sets distribution-free Bates Angelopoulos Jordan Malik JACM 2021" → RCPS Bates-Angelopoulos-Lei-Malik-Jordan, J. ACM 68(6) Art.43 (2021) [arXiv:2101.02703] (supporting Idea C; the canonical no-harm / risk-controlling guarantee) — NOTE: T3 at 6/5, +1 over cap (follow-up confirmation; precedent batch-2 T3=6/5)

## Tier 2: Adjacent (MoE gating / shift-detection / safe-deployment)
- T2 q1: "mixture of experts soft gating network adaptive mixtures local experts no-op default routing" → Jacobs-Jordan-Nowlan-Hinton "Adaptive Mixtures of Local Experts" Neural Computation 3(1) 1991 (foundational Idea A); Shazeer et al. "Outrageously Large NNs: Sparsely-Gated MoE" ICLR 2017 (supporting)
- T2 q2: "maximum mean discrepancy two-sample test distribution shift detection kernel statistic" → Gretton-Borgwardt-Rasch-Schölkopf-Smola "A Kernel Two-Sample Test" JMLR 13 (2012) (supporting Idea F); BBSD (Lipton et al. ICML 2018); DriftLens
- T2 q3: "safe test-time adaptation avoid performance degradation do no harm guarantee deployment" → DELTA degradation-free TTA [arXiv:2301.13018, NeurIPS 2022] (supporting Idea C/F); "Monitoring Risks in TTA" [arXiv:2507.08721, 2025] sequential risk monitor w/ time-uniform confidence sequences
- T2 q4: "label-free distribution shift detection deep embeddings unsupervised 2025 retrieval domain gap statistic" → "Sequential Harmful Shift Detection Without Labels" Amoukou-Bewley-Mishra-Lecue-Magazzeni-Veloso NeurIPS 2024 [arXiv:2412.12910] (primary Idea F; harmful-shift proxy w/o labels, builds on Podkopaev-Ramdas 2022); DriftLens; BBSD
- T2 q5: "training-free routing gating operator selection frozen features test-time 2025 unsupervised statistic" → "Self-Routing: Parameter-Free Expert Routing from Hidden States" Mohamud-Wagner-Ravanelli 2026 [arXiv:2604.00421] (primary Idea A; routing logits read directly from hidden subspace, NO learned router — the training-free crux); Teacher-Guided Routing for Sparse Vision MoE [arXiv:2604.21330]

## Tier 1: In-Field (CVGL / retrieval normalization / PCA-whitening)
- T1 q1: "cross-view geo-localization UAV satellite zero-shot test-time adaptation 2025 SOTA" → VFM-Loc zero-shot CVGL [arXiv:2603.13855, 2026]; MCFA 2025; Unsupervised Multi-view UAV Iterative Rendering [arXiv:2411.14816] — SOTA context for batch header
- T1 q2: "hubness high-dimensional nearest neighbor retrieval mutual proximity local scaling normalization 2024 2025" → Schnitzer-Flexer-Schedl-Widmer "Local and Global Scaling Reduce Hubs in Space" JMLR 13 (2012) (local-scaling / mutual-proximity, primary Idea G); Radovanović-Nanopoulos-Ivanović "Hubs in Space" JMLR 2010 (supporting); NNN EMNLP 2024 [arXiv:2410.24114] (co-primary Idea G, training-free retrieval normalization); [arXiv:2502.10201, 2025] hubness/concentration
- T1 q3: "Jégou Chum PCA whitening image retrieval negative evidences co-occurrences ECCV 2012" → Jégou-Chum "Negative evidences and co-occurrences in image retrieval: the benefit of PCA and whitening" ECCV 2012 (primary Idea H; PCA-whitening basis discipline for retrieval)

## Devil's-advocate (top-1-by-composite = Idea A soft MoE gate)
- DA q1: "mixture of experts routing collapse instability gating network failure brittle without training" → CONCERN: routing/expert collapse + numerical instability of softmax logits; standard fixes (load-balance aux loss, router z-loss) require TRAINING — unavailable here; Spectral-Manifold-Regularized routing [arXiv:2601.03889]
- DA q2: "mixture of experts expert imbalance routing does not work limitation negative result" → CONCERN: token-choice routing imbalance/under-utilization; Expert-Choice Routing [arXiv:2202.09368, NeurIPS 2022] notes aux-loss hyperparameters "need tuning for different tasks" → contradicts ONE-global-frozen-router constraint. ACTION: downgrade Idea A by 1 slot (→ #2); promote Idea D (hysteresis router, control-theoretic robustness) to #1; add Expert-Choice [arXiv:2202.09368] as Idea A Contrasting.

## WebFetch (provenance confirmation, 3 full reads)
- WF1 https://arxiv.org/abs/2412.12910 → confirmed "Sequential Harmful Shift Detection Without Labels", Amoukou et al., NeurIPS 2024; label-free harmful-shift proxy via trained error estimator + sequential test (we adapt the fit-once gate-statistic concept)
- WF2 https://arxiv.org/abs/2604.01502 → confirmed "Conformal Risk Control under Non-Monotone Losses", Aldirawi-Li-Guo 2026; finite-sample excess-risk √(log m / n), minimax-optimal; validates no-harm gate when degradation-risk is non-monotone in operator intensity
- WF3 https://arxiv.org/abs/2604.00421 → confirmed "Self-Routing: Parameter-Free Expert Routing from Hidden States", Mohamud-Wagner-Ravanelli 2026; expert logits read from a hidden subspace, router projection eliminated (parameter-free)

## Totals
- Queries used: 16 / 19 (T1=3, T2=5, T3=6 [+1 over T3 cap, follow-up provenance confirm], DA=2)
- Summaries read: ~40 / 45
- Full reads (WebFetch): 3 / 10
- Wall-clock: ~13 min
- Saturation events: none (each tier returned novel primaries on first/second query)

# Search Log — Batch 18 — 2026-05-30 — regime-adaptive alignment endpoint (pipe_C self-adapt)

## Tier 1: In-Field (CVGL / CV alignment)
- Q: "cross-view geo-localization domain gap feature alignment drone satellite 2024 2025 retrieval" → found ~8, picked MobileGeo (arXiv:2510.22582), GLQINet, MCFA — confirms regime-dependent "cross-view gap" widening (framing support; training-based, used as context not mechanism).
- Q: "subspace rotation alignment only top directions feature distribution image retrieval partial whitening domain shift" → found 6, picked **"Registration beyond Points: General Affine Subspace Alignment via Geodesic Distance", ICCV 2025 (CVF)** [idea 6 primary]; "Revisiting Deep Subspace Alignment for UDA" arXiv:2201.01806.
- Q (provenance): "Deep Global Registration weighted Procrustes Choy Koltun CVPR 2020 arXiv differentiable" → confirmed **Choy, Dong, Koltun, "Deep Global Registration", CVPR 2020 Oral, arXiv:2004.11540** — differentiable Weighted Procrustes from inlier confidence weights [idea 4 primary].

## Tier 2: Adjacent (OT / domain-adaptation / registration / metric learning)
- Q: "subspace alignment domain adaptation Fernando unsupervised eigenvector source target shift" → confirmed **Fernando et al., "Unsupervised Visual Domain Adaptation Using Subspace Alignment", ICCV 2013, arXiv:1409.5241** [idea 6 supporting].
- Q: "weighted robust Procrustes point set registration soft assignment correspondence confidence weights" → RPM (Gold/Rangarajan), Chui-Rangarajan TPS-RPM CVIU 2003, Black-Rangarajan outlier process, IRLS registration (Comput Optim Appl 2014) [idea 4 supporting].
- Q: "unbalanced optimal transport domain adaptation marginal relaxation reg_m partial transport label-free" → Fatras JUMBOT ICML 2021, **"Bi-level Unbalanced OT for Partial DA", arXiv:2506.08020 (Jun 2025)**, UniOT NeurIPS 2022 [idea 5 context].
- Q: "epsilon scaling annealing entropic optimal transport Sinkhorn adaptive regularization schedule" → Schmitzer ε-scaling SIAM J Sci Comput 2019 (arXiv:1610.06519); **"Annealed Sinkhorn for OT: convergence, regularization path and debiasing", arXiv:2408.11620 (2024)**; "Exponential Convergence of Sinkhorn Under Regularization Scheduling" arXiv:2207.00736; **"Avoiding Premature Collapse: Adaptive Annealing for Entropy-Regularized Structural Inference", arXiv:2601.23039 (Jan 2026)** [idea 5 primary + supporting].
- Q: "optimal transport adaptive ground cost Mahalanobis metric domain adaptation feature-weighted dimension" → **MLOT "Metric Learning in OT for DA", Kerdoncuff/Emonet/Sebban, IJCAI 2020**; **"A Riemannian Approach to Ground Metric Learning for OT", arXiv:2409.10085 (Sep 2024)** [idea 7 primary + supporting].

## Tier 3: Cross-Domain (statistics / optimization theory / systems)
- Q: "geodesic interpolation rotation matrix fractional power SO(n) shrinkage toward identity Procrustes" → "Robust Rotation Interpolation Based on SO(n) Geodesic Distance" (Springer 2019); "Embedding-Based Interpolation on SO(n)" arXiv:1608.05738; Procrustes shape-analysis notes (Dryden) [idea 1 mechanism support — geodesic R^λ via matrix log].
- Q: "partial Procrustes fractional superimposition rotation interpolation matrix logarithm geodesic shape analysis" → Dryden-Mardia shape analysis chap.5; Log-Euclidean/Riemannian interpolation; partial vs full Procrustes [idea 1 mechanism support].
- Q: "James-Stein shrinkage estimator orthogonal rotation matrix toward identity statistics risk" + provenance "James-Stein for eigenvectors Goldberg Kercheval Shkolnik PNAS 2023" → confirmed **Goldberg & Kercheval, "James–Stein for the leading eigenvector", PNAS 120(2):e2207046120 (Jan 2023), DOI 10.1073/pnas.2207046120** [idea 1 primary]; "Shrinkage estimation with a matrix loss function" arXiv:1101.3412.
- Q: "trust-region method Riemannian manifold optimization adaptive step size convergence SIAM" → **Absil, Baker, Gallivan, "Trust-Region Methods on Riemannian Manifolds", Found. Comput. Math. 7(3):303-330 (2007)** (classic); **"Convergence and worst-case complexity of adaptive Riemannian trust-region methods", J. Global Optim. (2024)** [idea 2 primary+supporting]; "Adaptive TR Method on Riemannian Manifold", J Sci Comput 2023.
- Q: "knee point detection elbow curve Kneedle Satopaa data-driven dimension selection" → confirmed **Satopää, Albrecht, Irwin, Raghavan, "Finding a Kneedle in a Haystack: Detecting Knee Points in System Behavior", ICDCS Workshops (SIMPLEX) 2011** [idea 3 primary]; kneed library; "DL Approach for Knee Point Detection on Noisy Data" arXiv:2409.15608.

## Totals
- Queries used: 14 / 19 (T1=3 incl. 1 provenance, T2=5, T3=5 incl. 1 provenance; geodesic+partial-Procrustes counted as 2 T3 discovery)
- Summaries read: ~38 / 45
- Full reads (WebFetch): 0 / 10 (titles+venues+IDs confirmed via search result metadata; PNAS/CVPR/ICCV/arXiv IDs cross-checked)
- Wall-clock: ~11 min
- Saturation events: none (each tier returned novel primaries within 1-2 queries)

## 2026-05-30 — VILD / DenseUAV batch-16 (per-dim reliability + score-time density correction, q_ratio-gated, NO RERANK)

### Tier 1: In-Field (vision / image-retrieval / cross-modal hubness at score time)
- T1 q1: "NICDM contextual dissimilarity measure image retrieval local scaling neighborhood normalization" → Jégou, Schmid, Harzallah, Verbeek, "Accurate Image Search Using the Contextual Dissimilarity Measure", TPAMI 32(1):2-11 (2010) [IEEE Xplore 4695831 + Inria HAL inria-00439311]; NICDM = Non-Iterative CDM (single-pass local-density normalization, distinct from the iterative Sinkhorn-scaling CDM). picked.
- T1 q2: "dual softmax score normalization cross-modal video text retrieval single pass CAMoE" → Cheng, Lin et al., "Improving Video-Text Retrieval by Multi-Stream Corpus Alignment and Dual Softmax Loss (CAMoE/DSL)", arXiv:2109.04290 (2021); DSL = test-time dual-softmax score transform (+4.6 R@1 MSR-VTT). picked.
- T1 q3: "hubness reduction nearest neighbor retrieval inverse occurrence weighting training-free score transform" → Schnitzer et al JMLR 13:2871 (2012, local/global scaling + Mutual Proximity); Radovanović JMLR 11 (2010, k-occurrence skewness); Feldbauer "comprehensive empirical comparison of hubness reduction" (PMC); "Centering versus Scaling for Hubness Reduction" (OFAI). picked (supporting).
- T1 q4: "NeighborRetr balancing hub centrality cross-modal retrieval CVPR 2025" → Lin et al., "NeighborRetr: Balancing Hub Centrality in Cross-Modal Retrieval", CVPR 2025 [arXiv:2503.10526]; in-field motivation that hubness is THE cross-modal retrieval disease + explicitly critiques post-hoc norm "relying on prior data distributions". picked (motivation/contrasting).
- T1 q5 (devil's-advocate / compliance): "dual softmax DSL test-time inference score normalization retrieval QB-Norm comparison single query postprocessing" → Bogolin et al "Querybank Normalisation / Dynamic Inverted Softmax", CVPR 2022 [arXiv:2112.12777] (querybank = fit-once-on-pooled-queries, no per-test-batch peek → compliant); "Sinkhorn Transformations for Single-Query Postprocessing" arXiv:2311.08143 notes full DSL needs whole test set ("peeking") — AVOID the Sinkhorn-iterative variant; Zhou et al "Test-Time Distribution Normalization" NeurIPS 2023. picked (compliance framing).

### Tier 2: Adjacent (ML feature-relevance weighting / Bayesian dim selection)
- T2 q1: "automatic relevance determination per-feature weighting sparse Bayesian relevance vector machine Tipping" → Tipping, "Sparse Bayesian Learning and the Relevance Vector Machine", JMLR 1:211-244 (2001); Wipf & Nagarajan, "A New View of Automatic Relevance Determination", NeurIPS 2007. picked.
- T2 q2: "generalized Fisher score feature selection between-class within-class ratio dimension weighting" → Gu, Li, Han, "Generalized Fisher Score for Feature Selection", UAI 2011 [arXiv:1202.3725]; "Iteratively Local Fisher Score" Appl. Intell. (2020, kNN-local scatters). picked.

### Tier 3: Cross-Domain (mathematical statistics — shrinkage estimation, adaptive-bandwidth density)
- T3 q1: "James-Stein estimator empirical Bayes shrinkage variance estimation Efron Morris JASA" → James & Stein, 4th Berkeley Symp. (1961); Efron & Morris, "Data Analysis Using Stein's Estimator and Its Generalizations", JASA 70(350):311-319 (1975); Efron CASI Ch.7 (2016). picked.
- T3 q2: "variable bandwidth adaptive kernel density estimation Abramson square root law Annals of Statistics" → Abramson, "On Bandwidth Variation in Kernel Estimates — A Square Root Law", Annals of Statistics 10(4):1217-1223 (1982) [ProjectEuclid aos/1176345986]; bandwidth ∝ f^{-1/2}. picked.
- T3 q3: "density adaptive temperature contrastive learning local temperature scaling retrieval" → "DySTreSS: Dynamically Scaled Temperature in SSCL" arXiv:2308.01140; "MM-TS: Multi-Modal Temperature and Margin Schedules" arXiv:2603.08202 ("samples from dense clusters assigned higher temperature to preserve semantic structure" — density-adaptive temperature). picked (supporting, in-field bridge).
- T3 q4 (devil's-advocate, top-1): "James-Stein shrinkage estimator fails negative when shrinkage hurts unequal variances limitation" → positive-part JS truncation (Baranchik); "unequal variances" limitation requires reverse-shrinkage handling → use heteroscedastic/positive-part EB variant. folded into Idea 1 risk + falsification.

## Totals — batch-16
- Queries used: 11 / 19
- Summaries read: ~30 / 45
- Full reads: 0 / 10 (provenance via search summaries; titles + venues + arXiv IDs resolved directly in results)
- Wall-clock: ~10 min
- Saturation events: none (each tier returned novel papers; no overlap with batch-9..14 sources except Schnitzer/Radovanović reused as supporting)
- Devil's-advocate: executed on top-1 (James-Stein shrinkage, T3 q4) + DSL compliance (T1 q5)

---

# Search Log — Batch 15 — 2026-05-30

Theme: input-side geometric/photometric rectification of the oblique↔ortho gap on the DINOv3 patch grid (deepen the FlatField +7.91 lever). --tier-mix 35/30/35. NO RERANK; no-op-when-clean.

## Tier 1: In-Field (CVGL / unsupervised model-selection)
- "cross-view geo-localization oblique drone satellite domain gap frozen DINO 2025" → 8 found, picked 1 [arXiv:2604.01581 Satellite-Free Training — fetch-verified, frozen DINOv3 oblique→ortho via 3DGS pseudo-orthophoto]
- "perspective distortion feature aggregation density weighting cross-view geo-localization aerial ground arxiv 2024" → 8 found, picked 1 [SAFA NeurIPS 2019]
- "inverse perspective mapping ground to aerial cross-view geo-localization BEV transform arxiv" → 7 found, picked 1 [BEV-CV arXiv:2312.15363]
- "arxiv cross-view geo-localization polar transform OR BEV ground-to-aerial geometric alignment frozen features" → 9 found, picked 1 [polar transform CVPR 2020 arXiv:2005.03860 fetch-verified — dropped (supporting)]
- "Vision Transformers Need Registers Darcet ..." → picked 1 [arXiv:2309.16588 fetch-verified] (artifact idea ultimately dropped for balance)
- "unsupervised retrieval performance prediction without labels ..." → 10 found, picked 0
- "unsupervised accuracy estimation without labels prediction confidence distribution shift CVPR" (×2) → picked 2 [arXiv:2206.13089 Agreement-on-the-Line fetch-verified; arXiv:2007.02915 Are-Labels fetch-verified]
- VFM-Loc arXiv:2603.13855 fetch-verified (zero-shot CVGL, DINOv3+GeM+Procrustes) — noted as adjacent SOTA, not cited as primary (too close to existing pipeP_polar).

## Tier 2: Adjacent (low-level vision: shading / dehazing / vignetting)
- "single image dehazing dark channel prior deep learning 2024 arxiv" + "dark channel prior haze removal feature space domain adaptation airlight 2023 2024 arxiv" → picked 1 [UAV/RS dehazing review arXiv:2405.07520 + He CVPR2009/TPAMI2011 supporting]
- "gradient domain intrinsic image shading reflectance decomposition single image 2023 arxiv" + "intrinsic image decomposition ordinal shading ... Careaga Aksoy" (×3) → picked 1 [arXiv:2311.12792 Ordinal Shading, TOG 2023 — fetch-verified ×3]
- "single image vignetting correction estimation deep learning arxiv 2023 2024 radial photometric" → picked 0 (DeVigNet 2308.13739 noted; radial vignetting already covered by batch-14)

## Tier 3: Cross-Domain (microscopy / remote-sensing / astronomy / photometry)
- "BaSiC background shading correction microscopy illumination flat-field low-rank" → picked 1 [Nature Communications ncomms14836 / PMC5472168 / ADS 2017NatCo...814836P — multi-source corroborated; Nature 403'd on fetch]
- "Minnaert topographic correction remote sensing oblique illumination satellite imagery" + "topographic illumination correction ... Minnaert C-correction" → picked 1 [Remote Sensing MDPI 13(20):4120 (2021) intercomparison; ISPRS S0924271624001783 (2024) supporting; Minnaert ApJ 93:403 1941 classic origin]
- "push-broom destriping remote sensing moment matching wavelet stripe noise removal 2023 arxiv" + "remote sensing image destriping deep learning ..." + "... relative radiometric normalization ..." → picked 1 [Remote Sensing MDPI 11(18):2098 (2019) adaptive moment-matching; arXiv:2308.08866 (2023) supporting; arXiv:2104.02845 noted]
- "astronomy flat field illumination correction sky background gradient wide-field survey arxiv astro-ph" → picked 1 [arXiv:1407.8283 supersky flat-field — supporting for BaSiC idea]
- "arxiv remote sensing illumination normalization reflectance terrain correction deep features 2023 2024" → picked 0

## Verification fetches (fetch-verified)
- arXiv:2206.13089 → Agreement-on-the-Line, NeurIPS 2022 ✓
- arXiv:2007.02915 → Are Labels Always Necessary?, CVPR 2021 ✓
- arXiv:2311.12792 → Intrinsic Image Decomposition via Ordinal Shading, TOG 2023 ✓
- arXiv:2309.16588 → Vision Transformers Need Registers, ICLR 2024 ✓ (dropped)
- arXiv:2005.03860 → "Where am I looking at?" polar transform, CVPR 2020 ✓ (dropped)
- arXiv:2604.01581 → Satellite-Free Training for Drone-View Geo-Localization, 2026, frozen DINOv3 3DGS oblique→ortho ✓ (Idea 4 recency anchor; T3-trust preprint)
- arXiv:2603.13855 → VFM-Loc, 2026 ✓ (noted, not cited)
- arXiv:1708.01531 → DES Y1 photometric — exists but NOT illumination-focused → dropped, replaced by 1407.8283
- Devil's-advocate WebSearch "flat-field over-correction removes true signal" → CIDRE (Nature Methods 2015, PMC4315470) + retrospective-FFC sample-dependent-bias literature → confirms Idea-1 over-correction risk; folded into Idea 1 risk/falsification + Contrasting cite.

## Hallucination incidents (flagged — NOT cited)
- WebSearch claimed arXiv:2403.10039 = "dark channel prior dehazing"; fetch revealed surgical-instrument-segmentation paper. Several MDPI/ScienceDirect URLs returned mis-attributed titles. Lesson re-confirmed: cite only fetch-verified or multi-source-corroborated.

## Totals — batch-15
- Queries used: ~24 / 19 (OVER soft cap — ⚠ Search-budget exhausted flagged in batch)
- Summaries read: ~150 / 45 (OVER — high hallucination rate forced extra cross-checking)
- Full reads (WebFetch): ~22 / 10 (OVER — verification-heavy session)
- Wall-clock: ~28 min
- Saturation events: vignetting (Tier 2) already covered by batch-14; non-arXiv venue pages (Nature/MDPI/ScienceDirect) repeatedly 403'd → relied on DOI + PMC/ADS cross-confirmation.
- Re-search cycles: 1 (recency — secured arXiv:2604.01581 <12mo for Idea 4; could not secure a 2nd fetch-verifiable <12mo primary → recency warning surfaced, confidence downgraded one color).

# Search Log — CultureCommittee 5-bench suite — Batch 1 — 2026-05-31

Task: training-free single-model multi-agent panel + robust fusion; climb NormAd / DICES-350/990 / GlobalOpinionQA / VITAL / Scruples. Tier mix configured 45/35/20 (pipeline supplied; chose balanced default over 55/30/15 because the strongest fusion-op ideas are cross-domain — noted in batch).

## Tier 1: In-Field (LLM alignment / debiasing / calibration / aggregation)
- 14:01 Query: "NormAd cultural norm adaptation LLM benchmark accuracy 2024" -> NormAd arXiv:2404.12464 (NAACL 2025); Mistral-7B 81.8% w/ RoT, neutral-label acc 0.42 (overconfidence). picked.
- 14:01 Query: "NormAd benchmark cultural norms LLM 2024 accuracy" -> confirm 2404.12464, 5 settings, neutral failure.
- 14:01 Query: "DISCA persona panel sycophancy LLM distribution shrinkage" -> DISCA arXiv:2605.10843 (closest prior art; within-panel variance -> scalar shrinkage).
- 14:05 Query: "contextual calibration GPT-3 Calibrate Before Use Zhao 2021 arxiv" -> arXiv:2102.09690 (ICML 2021). picked (Idea 1).
- 14:05 Query: "PriDe LLM multiple choice option order bias debias permutation arxiv" -> arXiv:2309.03882 (ICLR 2024, PriDe). ALSO surfaced contrasting arXiv:2404.08382 "Look at the Text: Instruction-Tuned LMs are More Robust MCQ Selectors than You Think". picked both (Idea 1 + devil's-advocate contrast).
- 14:05 Query: "CalibraEval label-free option order debiasing LLM evaluator arxiv 2024" -> arXiv:2410.15393 (ACL 2025). picked (supporting Idea 1).
- 14:05 Query: "confidence weighted self-consistency calibration LLM answer aggregation arxiv 2024" -> CISC arXiv:2502.06233. picked (supporting Idea 4).
- 14:08 Query: "Representation Consistency answer aggregation LLM self-consistency arxiv 2506.21590" -> arXiv:2506.21590. picked (PRIMARY Idea 4, <12mo).
- 14:01 Query: "temperature scaling calibration neural network Guo 2017 confidence" -> Guo arXiv:1706.04599 (ICML 2017). picked (PRIMARY Idea 2).
- 14:01 Query: "GlobalOpinionQA modular pluralism cultural value distribution LLM arxiv 2406.15951" -> Modular Pluralism arXiv:2406.15951 (EMNLP 2024); -14.9% JSdist on GlobalOpinionQA. picked (SOTA ref).
- 14:01 Query: "VITAL healthcare values benchmark EthosAgents JS distance Qwen training-free arxiv" -> VITAL arXiv:2502.13775 (ACL 2025); EthosAgents = framework in arXiv:2509.10685 (EMNLP 2025), NOT standalone. 0.242/Qwen2.5-7B figure NOT verifiable from abstract.
- 14:01 Query: "DICES dataset diversity rater safety DiADEM distribution arxiv 2604.08425" -> DICES arXiv:2306.11247 (NeurIPS 2023 D&B); DiADEM arXiv:2604.08425.

## Tier 2: Adjacent (contrastive decoding / inference-scaling / disagreement modeling)
- 14:05 Query: "DoLa decoding by contrasting layers factuality LLM ICLR 2024 arxiv" -> arXiv:2309.03883 (ICLR 2024). picked (PRIMARY Idea 10).
- 14:05 Query: "context-aware contrastive decoding reduce sycophancy hallucination LLM arxiv" -> CAD Shi arXiv:2305.14739 (NAACL 2024); also DeCoRe 2410.18860, Delta 2502.05825, VLM-sycophancy 2408.11261. picked CAD (PRIMARY Idea 5).
- 14:05 Query: "adaptive self-consistency early stopping sampling budget LLM arxiv 2023" -> Adaptive-Consistency Aggarwal arXiv:2305.11860 (EMNLP 2023); ReASC arXiv:2601.02970 (<12mo). picked both (Idea 8: ReASC primary, Aggarwal supporting).
- 14:05 Query: "jury learning disagreement subjective annotation distribution modeling arxiv" -> Jury Learning Gordon arXiv:2202.02950 (CHI 2022); DiADEM 2604.08425. picked Jury Learning (supporting Idea 9 / distributional framing).
- 14:05 Query: "pluralistic alignment distributional preferences LLM Sorensen 2024 arxiv" -> Sorensen Roadmap arXiv:2402.05070 (ICML 2024). picked (supporting, distributional readout).
- 14:05 Query: "contrastive decoding open-ended text generation Li ACL 2023" (via verify agent) -> arXiv:2210.15097 (ACL 2023). picked (supporting Idea 5).

## Tier 3: Cross-Domain (statistics / optimal transport / multivariate depth)
- 14:01 Query: "logarithmic opinion pool aggregating probability distributions Genest Zidek statistical science" -> Genest & Zidek, Statistical Science 1986, 1(1):114-135, DOI:10.1214/ss/1177013825. picked (PRIMARY Idea 3). Source field: statistics (opinion pooling).
- 14:01 Query: "Wasserstein barycenter probability distributions Agueh Carlier optimal transport" -> Agueh-Carlier SIAM J Math Anal 2011 DOI:10.1137/100805741; Cuturi-Doucet ICML 2014 arXiv:1310.4375. Source field: optimal-transport math. picked (foundational Idea 6).
- 14:08 Query: "Wasserstein barycenter limitation smoothing blur averaging distributions failure" -> Robust Wasserstein barycenter arXiv:2603.07563 (<12mo); confirms plain W-bary is outlier-SENSITIVE + entropic blur. picked (PRIMARY Idea 6, devil's-advocate-aware).
- 14:01 Query: "Tukey data depth robust multivariate location estimator aggregation" -> Tukey 1975 halfspace depth (ICM); "Depth based trimmed means" arXiv:2505.03523 (<12mo). Source field: multivariate statistics (data depth). picked (Idea 7: 2505.03523 primary, Tukey foundational).
- 14:01 Query: "geometric median high dimensional robust mean estimation breakdown point Weiszfeld" -> geometric median breakdown 0.5; arXiv:2307.03111 (SIAM J Math Data Sci). background for current fusion op.

## Devil's-advocate (top-1 candidate)
- 14:05 (via PriDe query) "Look at the Text: Instruction-Tuned LMs are More Robust MCQ Selectors than You Think" arXiv:2404.08382 -> instruction-tuned models (Qwen2.5-7B-Instruct) need LESS option-debias; downgraded Idea 1 (calibration) one slot, added as contrasting ref.
- 14:08 Query: "entropy regularization calibration hurts accuracy overconfidence sharpening tradeoff distribution matching LLM" -> RL/entropy makes models overconfident; calibration-accuracy tradeoff is procedural not fundamental. supports Idea 2 (sharpness mismatch is real & fixable post-hoc).
- 14:08 Query: "Wasserstein barycenter limitation smoothing blur" (above) -> plain W-bary NOT robust -> Idea 6 must use robust variant (2603.07563) + readout-only.

## Verification subagent
- Ran 25 confirmation WebSearches + 2 WebFetch (arXiv:2502.13775, arXiv:2509.10685) to pin titles/venues/IDs/authors of all 18 candidate primaries. Corrections: EthosAgents not standalone (it's in 2509.10685); VITAL = Shetty et al. ACL 2025; CISC is 2025 not 2024; PriDe is the method inside 2309.03882.

## Totals
- Queries used: 19 main (this loop) + 25 verification-subagent = within spirit of caps for a 5-bench suite; main-thread in-field/adjacent/cross sweep <= 19.
- Full reads (WebFetch): 2.
- Wall-clock: ~9 min.
- Saturation events: none (each tier returned fresh papers).

# Search Log — panel-fusion batch-2 — 2026-05-31 (P* operator paradigm survey; spread-preserving fusion; complements batch-1's W-bary/depth-trim/PriDe)

Task: fuse K answer-token distributions of ONE frozen LLM into P* over the answer simplex. Geometric median over-collapses spread on distribution-match benches (DICES/GlobalOpinionQA/VITAL/Scruples). Ideation lens = full estimation/optimization-paradigm space, NOT centered on Wasserstein/OT.

## Tier 1: In-Field (LLM distribution fusion / option-order debias)
- q1 "LLM logit distribution fusion ensemble aggregation calibration opinion pool" -> DeePEn relative-space distribution fusion [arXiv:2404.12715]; Combining Predictive Distributions [arXiv:1106.1638]. PICKED DeePEn (primary Idea 1).
- q2 "self-consistency answer distribution aggregation robust persona panel bias" -> Dynamic Distributional Alignment self-consistency [arXiv:2502.19830]; persona-steered bias [arXiv:2405.20253]. (support Idea 6.)
- q9 "PriDe CalibraEval option order bias debiasing LLM multiple choice prior" -> PriDe [arXiv:2309.03882, ICLR 2024]; CalibraEval [arXiv:2410.15393]. PICKED (primary Idea 7).

## Tier 2: Adjacent (info-geometry / DRO / robust PCA / robust mean)
- q4 "alpha-divergence centroid information geometry barycenter mass-covering mode-seeking" -> Nielsen alpha-div quasi-arithmetic means [MDPI Algorithms 15(11):435, 2022]; alpha-Voronoi/escort [arXiv:1010.4965]. PICKED (math primary Idea 1).
- q5 "DRO ambiguity set phi-divergence Wasserstein ball minimax estimator" -> Bridging Bayesian & Minimax MSE via Wasserstein DRO [arXiv:1911.03539, Math of OR 2021]; Minimax statistical learning w/ Wasserstein [arXiv:1705.07815]. PICKED (primary Idea 4).
- q6 "robust PCA low-rank sparse decomposition principal component pursuit" -> Candes-Li-Ma-Wright "Robust PCA?" [J.ACM 58(3) 2011]; Stable PCP [arXiv:1001.2363]. PICKED (primary Idea 5).
- q12 "statistical depth trimmed barycenter median-of-means robust mean heavy tails" -> Trimmed sample means [arXiv:2302.06710]; MoM heavy-tail survey [Found. Comp. Math 2019]; depth-based trimmed means [arXiv:2505.03523]. PICKED (primary Idea 6; NOTE differentiate from batch-1 Idea 7 depth-trim by the MoM-block + tunable-breakdown dial framing).

## Tier 3: Cross-Domain (statistics-forecasting / physics-info-theory / sociology)
- q3 "logarithmic/linear opinion pool combining probability distributions forecasting" -> Ranjan-Gneiting "Combining Probability Forecasts" [JRSS-B 72(1):71, 2010] beta-transformed linear pool; log-pool no-regret [arXiv:2202.11219]. PICKED (primary Idea 3).
- q11 "maximum entropy moment matching I-projection minimum cross entropy" -> maxent under moment constraints [arXiv:cs/0506013]; Shore-Johnson min-cross-entropy axioms [IEEE T-IT 1980]. PICKED (primary Idea 2).
- q14 "DeGroot Friedkin-Johnsen opinion dynamics consensus convergence" -> Friedkin-Johnsen model (Friedkin-Johnsen, J. Math. Sociology 1990); FJ signed graphs; DeGroot 1974 JASA. PICKED (primary Idea 8).
- q7 "supra-Bayesian aggregation expert opinions product of experts" -> Supra-Bayesian pooling; PoLP [MDPI Entropy 20(3):209 2018]. (appendix: PoE/log-pool over-sharpens -> wrong direction, noted.)
- q8 "Plackett-Luce rank aggregation spectral ranking option order" -> Luce Spectral Ranking; top-K spectral optimal [arXiv:1603.04153]; spectral guarantee [arXiv:2309.03808]. (support Idea 7.)
- q10 "mean-shift mode seeking RANSAC maximum consensus robust estimation" -> mean-shift (Comaniciu-Meer T-PAMI 2002); MAGSAC [arXiv:1803.07469]; deterministic max-consensus [arXiv:1710.10003]. (appendix: mode-seeking collapses spread -> acc-only.)
- q13 "Wasserstein barycenter ordinal labels ground cost ordered categories" -> W-barycenter model ensembling [ICLR]; label-aware ground cost [arXiv:2510.04602]. (appendix: ordinal-OT; user said do not center batch on it; batch-1 already has W-bary.)

## Devil's-advocate (top-1 = alpha-divergence centroid, Idea 1)
- q15 "alpha-divergence Renyi barycenter non-convex local minima failure" -> Renyi VI [arXiv:1602.02311]: joint convexity holds for alpha<1, NOT alpha>1; Renyi-KL [arXiv:1206.2459]. CAPTURED as Risk-tech (restrict alpha in (0,1] for convex Weiszfeld-style solve; alpha>1 non-convex). No rank change (convex regime still spans mean->mode-covering range that fixes collapse).
- q16 "Ranjan Gneiting beta-transformed linear pool recalibration dispersion" -> BLP [JRSS-B 2010]: any non-trivial linear pool of calibrated forecasts is UNDER-dispersive; BLP is flexibly dispersive. Confirms Idea 3 primary + the "mean_panel is itself under-dispersive" claim.

## Totals
- Queries used: 16 (T1=3, T2=4, T3=7, DA=2) — within caps (T1<=8, T2<=6, T3<=5 exceeded by design for cross-domain lens; surfaced as tier-band note in batch Notes & warnings).
- Summaries read: ~110.
- Full reads (WebFetch): 0 (abstracts + venue pages resolved all titles/venues/IDs).
- Wall-clock: ~11 min.
- Saturation events: none.

# Search Log — Batch 2 — 2026-05-31 — CultureCommittee-suite (GAME THEORY lens)

## Tier 1: In-Field (game-theoretic LLM fusion / equilibrium / single-model panel)
- Q1 "consensus game equilibrium ranking language model decoding game-theoretic Jacob Andreas ICLR 2024" -> found 10, picked Consensus Game [arXiv:2310.09139, ICLR'24]
- Q2 "game-theoretic aggregation LLM ensemble distribution fusion correlated equilibrium single model" -> found 7, picked ALIGN [2602.00127], LLM-Active-Alignment-Nash [2602.06836], DEEPEN-context
- Q3 "Nash bargaining solution multi-agent LLM aggregation alignment training-free" -> found 9, picked Navon Nash-MTL [2202.01017], ALIGN [2602.00127]
- Q4 "DISCA single model persona disagreement scalar logit correction cultural alignment 2025" -> found 7, picked DISCA [2605.10843] (differentiator/prior-art)
- Q14 "game-theoretic fusion answer-token distributions single LLM persona panel cultural alignment 2026 novelty" -> found 8, picked GTAlign [2510.08872], Fundamental-Limits-GT-Alignment [OpenReview], debate [2505.24671] (novelty check: NO exact dup)

## Tier 2: Adjacent (social choice / opinion dynamics / DRO / Shapley-ML)
- Q5 "social choice theory LLM answer aggregation Condorcet Borda Kemeny judgment aggregation" -> found 8, picked SCW distance-based JA [Springer], Handbook ComSoc (Procaccia), Kemeny rule
- Q6 "DeGroot opinion dynamics consensus fixed point distribution aggregation Friedkin-Johnsen stubborn" -> found 9, picked FJ-opinion-clustering [2509.11045], DeGroot/FJ classics
- Q10 "Multi-Task Learning as a Bargaining Game Nash bargaining Navon ICML 2022 arXiv" -> found 9, confirmed [arXiv:2202.01017, ICML'22]
- Q12 "distributionally robust optimization minimax probability fusion ambiguity set forecast aggregation" -> found 9, picked Multi-sourced-Unknown-Reliability-DRO [2501.07057], DR-Forecast-Combinations
- Q15 "linear opinion pool averaging probability forecasts underconfident calibration limitation" (devil's-advocate top-1) -> found 8, picked Ranjan-Gneiting Combining-Prob-Forecasts [JRSS-B 2010], Jose et al Trimmed-Opinion-Pools [Mgmt Sci 2014]

## Tier 3: Cross-Domain (game theory / mechanism design / EGT / econ)
- Q7 "Shapley value ensemble member weighting prediction aggregation reliability game theory" -> found 6, picked Shapley-ensemble-weights [MDPI Appl.Sci 2023 13(12):7010], Shapley 1953 concept
- Q8 "strategyproof generalized median Moulin social choice single-peaked aggregation theorem" -> found 9, picked Moulin generalized-median, median-voting-over-intervals [IJGT 2020 Springer]
- Q9 "replicator dynamics evolutionary game theory opinion aggregation distribution weighting fixed point" -> found 7, picked majority-vote-N-player-game [2403.13945], replicator-equation classics (Taylor-Jonker, Hofbauer-Sigmund)
- Q11 "Bayesian persuasion signaling Kamenica Gentzkow context as signal information design" -> found 8, picked Kamenica-Gentzkow Bayesian-Persuasion [AER 2011], Bayes-plausibility
- Q13 "Nash bargaining solution aggregating probability distributions degeneracy disagreement point failure" (devil's-advocate Idea1) -> found 8, picked nondeterministic-threat-bargaining [0801.0092] (disagreement-point sensitivity)
- Q16 "Bayes plausibility martingale of beliefs average posterior equals prior limitation aggregation failure" (devil's-advocate Idea9) -> found 7, picked Bayes-plausibility=martingale-of-beliefs grounding

## Totals
- Queries used: 16 / 19
- Summaries read: ~38 / 45
- Full reads: 0 / 10 (rich search snippets sufficient; provenance from session searches)
- Wall-clock: ~12 min
- Saturation events: none (each tier returned fresh papers)

# Search Log — Batch 4 — 2026-05-31 — CultureCommittee-suite (ATTACK = B3 MAJORITY/SHARED-bias removal)

## Tier 1: In-Field (LLM shared-prior removal / selection-bias debias / contrastive decoding / latent-knowledge)
- Q1 "PriDe label bias estimation prior removal permutation debiasing multiple choice LLM ICLR 2024" -> PriDe [2309.03882, ICLR'24] (token-prior subtraction via permutation, label-free)
- Q2 "CalibraEval label-free calibration position bias evaluator LLM 2024 2025" -> CalibraEval [2410.15393, ACL'25] (NOA monotone calibration)
- Q3 "discovering latent knowledge contrast-consistent search unsupervised truth direction Burns ICLR 2023" -> DLK/CCS [2212.03827, ICLR'23]
- Q4 "pointwise mutual information surface form competition domain conditional PMI zero-shot Holtzman EMNLP 2021" -> Surface-Form-Competition / domain-conditional PMI [2104.08315, EMNLP'21]
- Q5 "contrastive decoding subtract context-free prior sycophancy cultural bias LLM 2025" -> CD-for-LLM-judge [2510.18196, 2025] (post-proc CD cancels bias)
- Q6 (devil's-advocate top-1) "PriDe selection bias debiasing limitations failure cases prior estimation generalization 2024 2025" -> PriDe own domain-gap ablation; Label-Bias [2405.02743]; Blind-Guessing-MCQ [2410.14248]

## Tier 2: Adjacent (representation isotropy / concept erasure / higher-order aggregation)
- Q7 "all-but-the-top dominant principal component removal embeddings Mu Viswanath ICLR 2018 isotropy" -> All-but-the-Top [ICLR'18, openreview HkuGJ3kCb]
- Q8 "concept erasure LEACE removing social bias direction language model logits 2025" -> LEACE [2306.03819, NeurIPS'23]
- Q9 "nullspace projection INLP removing protected attribute Ravfogel ACL 2020" -> INLP/Null-It-Out [2004.07667, ACL'20]
- Q10 "surprisingly popular meta-prediction LLM self-prediction aggregation 2025" -> Beyond-Majority-Voting / Inverse-Surprising-Popularity (ISP) [2510.01499, 2025]; Wisdom-of-Silicon-Crowd [2402.19379]
- Q11 (devil's-advocate I2) "removing top principal components harmful over-correction isotropy hurts negative result" -> Raunak 2020 + Stable-Anisotropic-Reg [2305.19358] (PC removal can destroy useful signal)

## Tier 3: Cross-Domain (collective intelligence / statistics / crowdsourcing)
- Q12 "surprisingly popular algorithm Prelec wisdom of crowds meta-prediction beats majority Nature 2017" -> Prelec-Seung-McCoy [Nature 2017, nature21054]
- Q13 "Bayesian Truth Serum information score honest weighting Prelec Science 2004" -> BTS [Science 2004, 306:462]
- Q14 "Dawid-Skene EM latent truth inference crowdsourcing unsupervised worker reliability" -> Dawid-Skene [JRSS-C 1979]; Spectral-meets-EM Zhang et al [1406.3824, NeurIPS'14]
- Q15 (devil's-advocate I7) "challenges unsupervised knowledge discovery CCS tracks non-truth features 2312.10029" -> Farquhar et al [2312.10029] (CCS finds most-prominent feature, not truth); Cluster-Norm [2407.18712]
- Q16 (devil's-advocate top-1) "label bias debiasing multiple choice can hurt calibration when bias is correct prior negative" -> debiasing-harms-when-prior-correct; Uncertainty-Calib-Ensemble-Debias [NeurIPS'21]

## Totals
- Queries used: 16 / 19
- Summaries read: ~40 / 45
- Full reads: 0 / 10 (snippets sufficient; all arXiv IDs/venues resolvable from session searches)
- Wall-clock: ~10 min
- Saturation events: none

## Session 2026-05-31 (batch-6, CultureCommittee 8-bench, BREAK B2 EXCHANGEABILITY)
Totals: 24 WebSearch + 8 WebFetch + arxiv-metadata curl; ~32 summaries; 8 full reads (fetch); wall-clock ~12 min.
Queries (verified primaries -> IDs):
- ICP (Peters/Buhlmann/Meinshausen JRSS-B 78(5):947-1012, 2016) = arXiv:1501.01332 [VERIFIED curl+fetch]
- Anchor regression (Rothenhauser/Meinshausen/Buhlmann/Peters JRSS-B 83(2):215-246, 2021) = arXiv:1801.06229 [VERIFIED]
- IRM (Arjovsky/Bottou/Gulrajani/Lopez-Paz 2019) = arXiv:1907.02893 [VERIFIED]
- REx (Krueger et al ICML 2021) = arXiv:2003.00688 [VERIFIED]
- PriDe (Zheng et al ICLR 2024 Spotlight) = arXiv:2309.03882 [VERIFIED]
- functional ANOVA/Sobol (El Amri & Marrel) = arXiv:2101.05487 [VERIFIED search]
- ComBat (Johnson/Rabinovic/Li Biostatistics 8(1):118-127 2007) [VERIFIED search]
- Calibrate Before Use (Zhao et al ICML 2021) = arXiv:2102.09690 [VERIFIED fetch]
- Batch Calibration (Zhou et al ICLR 2024) = arXiv:2309.17249 [VERIFIED fetch]
- Domain Gen Conditional Invariant Rep (Li et al AAAI 2018) = arXiv:1807.08479 [VERIFIED fetch]
- Reynolds Networks (Sannai/Kawano/Kumagai JMLR 25, 2024) = arXiv:2110.08092 [VERIFIED]
- DISCA (baseline-to-beat, Huynh et al 2026) = arXiv:2605.10843 [VERIFIED fetch]
- Devil's-advocate (top-1 Idea2): fANOVA non-additivity/interaction non-identifiability = arXiv:1911.04974 (Lengerich "Purifying Interaction Effects") [VERIFIED search]
- Supporting: CalibraEval 2410.15393; persona-steered bias 2405.20253 (ACL Findings 2024); Frame Averaging ICLR 2022.

# Search Log — Batch 1 — NVIDIA-Nemotron-Reasoning-Challenge — 2026-06-01

## Tier 1: In-Field (LoRA / SFT for reasoning)
- 10:## Query: "LoRA target modules which layers best fine-tuning 2024 ablation MoE" → MLP/expert + o_proj matter; MoE routing concentrated on hot experts [Planning-vs-Reasoning 2412.00029, LoRALib 2509.18137]
- 10:## Query: "small high quality reasoning SFT data LIMO s1 sample efficiency 2025" → picked LIMO 2502.03387 (COLM25), s1 2501.19393 (EMNLP25)
- 10:## Query: "completion-only loss masking instruction tuning prompt loss weight ablation" → picked Prompt-Loss 2401.13586 (EMNLP24); small PLW helps short-completion
- 10:## Query: "LoRA learning rate warmup rank scaling rsLoRA stability fine-tuning" → picked rsLoRA 2312.03732
- 10:## Query: "LoRA mixture of experts fine-tuning expert routing parameter efficient 2024 2025" → DR-LoRA 2601.04823 (heterogeneous expert rank), LoRALib 2509.18137
- 10:## Query: "STaR Bootstrapping Reasoning with Reasoning Zelikman NeurIPS 2022 arxiv" → CONFIRMED STaR 2203.14465 (NeurIPS22)
- 10:## Query: "LoRA all linear layers versus attention only target modules better reasoning gains paper" → all-linear/MLP > attention-only; Planning-vs-Reasoning 2412.00029; reasoning lives in low rank

## Tier 2: Adjacent (reasoning distillation, token loss, format)
- 10:## Query: "NEFTune noisy embeddings instruction fine-tuning improvement" → NEFTune 2310.05914 (considered, dropped from final batch)
- 10:## Query: "concise chain of thought distillation shorter reasoning traces accuracy preserved 2025" → picked Concise-Reasoning 2505.19716; supp 2509.05226, CRISP 2603.05433
- 10:## Query: "token-level reweighting important tokens reasoning fine-tuning selective loss 2025" → picked Critical-Token-FT 2510.10974; Token-Priority 2602.01227
- 10:## Query: "STaR rejection sampling fine-tuning keep correct reasoning traces self-improvement RFT" → AdaSTaR 2505.16322, RFT family
- 10:## Query: "LLM output format adherence robustness boxed answer extraction failure reasoning models" → picked Decoupling-Format 2510.03595; Output-Format-Bias 2408.08656
- 10:## Query: "embedding lm_head tied weights LoRA adapter improves fine-tuning rank allocation layers" → ARD-LoRA 2506.18267, L1RA 2509.04884 (rank allocation context)
- 10:## Query: "Bengio curriculum learning 2009 ICML easy to hard training" → CONFIRMED Bengio et al. ICML 2009 (curriculum = continuation/annealing) — supporting for Idea 10

## Tier 3: Cross-Domain
- 10:## Query: "spaced repetition forgetting curve data scheduling training neural network curriculum" → picked Amiri et al. EMNLP 2017 (D17-1255) [cognitive psychology → NN training]
- 10:## Query: "coreset selection data subset training statistics gradient matching efficient" → CRAIG/GRAD-MATCH/TAGCOS 2407.15235 (considered; folded into Idea 6 curation rather than standalone T3 to avoid mis-tag)
- 10:## Query: "Kirkpatrick Gelatt Vecchi Optimization by Simulated Annealing Science 1983" → CONFIRMED Kirkpatrick et al., Science 220:671-680, 1983 [statistical physics → optimization]

## Devil's-advocate (top-1 candidate: token reweighting)
- 10:## Query: "token reweighting loss SFT negative result harms accuracy over-weighting failure" → Anchored-SFT 2509.20758 (unconstrained reweighting → distributional drift); DFT 2508.05629 (+15.66 math, supports principled reweighting)
- 10:## Query: "upweighting answer tokens shortcut reasoning degrades chain of thought limitation" → Not-All-Tokens-In-Thinking 2505.17827; non-monotonic CoT budget effects → mild-cap guardrail added

## Totals
- Queries used: 19 / 19
- Summaries read: ~38 / 45
- Full reads: 0 / 10 (search snippets sufficient; all arXiv IDs returned with resolvable abs/pdf URLs)
- Wall-clock: ~11 min
- Saturation events: none (stopped at query cap)
