---
name: conference-tiers
description: Venue whitelist by field and tier — used to filter search inputs (NOT to rank outputs)
load-trigger: Step 2 (during search) and Step 4 (during Provenance check)
---

# Conference & Venue Tiers

Use this whitelist to **filter input** (does a paper come from a trusted venue?). Do NOT use venue prestige to rank ideas — see `./anti-bias.md` §Venue-blind ideation.

## ML general
- **A***: NeurIPS, ICML, ICLR
- **A**: AAAI, IJCAI, AISTATS, UAI, COLT
- **Journal A***: JMLR, MLJ, TPAMI

## NLP
- **A***: ACL, EMNLP, NAACL
- **A**: EACL, COLING, CoNLL
- **A-**: ACL Findings (long/short), TACL is journal-tier A*
- **Journal**: TACL, Computational Linguistics

## Computer Vision
- **A***: CVPR, ICCV, ECCV
- **A**: BMVC, WACV, ACCV
- **Journal**: IJCV, TPAMI

## Data Mining / IR
- **A***: KDD, SIGIR, WWW, WSDM, CIKM
- **A**: ICDM, ECIR, SDM
- **Journal**: TKDE, TOIS

## Robotics
- **A***: ICRA, IROS, RSS, CoRL
- **A**: AAMAS
- **Journal**: IJRR, T-RO

## Theory
- **A***: STOC, FOCS, SODA

## Security / Crypto
- **A***: CRYPTO, EUROCRYPT, S&P (Oakland), CCS, USENIX Security, NDSS

## HCI
- **A***: CHI, UIST, CSCW
- **Journal**: TOCHI

## Speech / Audio
- **A***: INTERSPEECH, ICASSP

## Reinforcement Learning / Agents
- **A***: see ML general (NeurIPS / ICML / ICLR cover this)
- **A**: AAMAS, AISTATS

## Workshop papers
- Treat as **Tier 2** if workshop is co-located with an A* venue (e.g., NeurIPS Workshops, ICML Workshops, ACL Workshops).
- Treat as **Tier 3** otherwise.

## Industry tech reports
- Default: **Tier 2** (Google / OpenAI / Anthropic / Meta / Microsoft / DeepMind technical reports).
- Promote to **Tier 1** if ≥ 1 of:
  - Peer-reviewed at an A* venue afterwards.
  - Code released AND independently reproduced.
  - > 100 citations.

## Old papers (> 10 years)
- Skip the venue check — community acceptance is implied.
- Valid Tier-3 inspiration for foundational concepts (MCTS, beam search, dropout, batch norm, attention, EM, …).

## Auto-reject signals
Reject the paper as a source if ANY of:
- Citation count < 5 after 18 months since publication.
- No code released **AND** result depends on a closed model the user cannot access.
- Open-review reviewers flagged reproducibility concerns.
- Paper exists only as a blog post / Medium article / lecture slides (Tier 4 — see `./source-trust.md`).
- First-author has no other publication on the topic AND citation count is 0 after 12 months.

## When in doubt
- Check CORE conference ranking (`portal.core.edu.au/conf-ranks/`).
- Distinguish "main track" vs "Findings" / "Short paper" / "Late-breaking" — the lower variant is usually one tier down.
