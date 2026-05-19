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

<!-- entries appended below -->

## 2026-05-19 — ImageNet-10 / LeJEPA batch-7 ADDENDUM (Idea 6, quantum-themed)
- T3-Q q1: "quantum entanglement entropy von Neumann representation learning self-supervised regularizer" → VNE arXiv:2304.01434 (direct prior art for VNE-as-SSL — closes that direction); QSEA arXiv:2506.10306 (quantum-native SSL — not applicable to classical ViT)
- T3-Q q2: "quantum kernel feature map self-supervised representation embedding Schuld Havlicek" → Schuld-Killoran PRL 2019 (arXiv:1803.07128); Havlicek Nature 2019 (arXiv:1804.11326); Schuld arXiv:2101.11020 (PQCs as kernel methods); Joint Embedding SSL kernel arXiv:2209.14884; Kernel VICReg arXiv:2509.07289 (already in b1 log)
- T3-Q q3: "random matrix theory free probability isotropic eigenvalue gap deep learning representation" → Pennington et al. 1807.11694 (already implicit in b1 family); arXiv:2506.13139 (RMT-DL beyond eigenvalues, Jun 2025); confirmed MP-spectrum direction is well-trodden
- T3-Q q4: "quantum Stein lemma hypothesis testing relative entropy classifier representation learning" → Stein-lemma quantum info results (Hayashi, Ogawa-Nagaoka) → reduces to quantum relative entropy = VNE direction (closed)

Resolution: 4 quantum-themed queries; final idea = SU(d)-parameterized structured-orthogonal projector (Givens rotation composition, classical analog of PQC) — chosen because VNE/free-probability/quantum-Stein directions all reduce to closed covariance-shaping family. Schuld-Killoran/Havlicek primaries are genuinely cross-domain (physics venue PRL, Nature) with classical-translation via butterfly orthogonal layers (Dao ICML 2019). 2 minutes wall-clock.
