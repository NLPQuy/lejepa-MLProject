---
name: stage-2-questions
description: Question bank for Stage 2 — Prior Work Attack (Prior-Work Hunter persona)
load-trigger: Loaded at start of Stage 2 execution
---

# Stage 2 Question Bank — Prior Work Attack

Hostile-until-novel. Every answer must cite a paper (title + author + venue + year + arXiv/DOI) or admit the search came up empty.

## Mandatory (must answer all 5)

1. **M1.** List ≥ 5 papers similar to this idea. Cite each: title, first author, venue, year, arXiv ID.
2. **M2.** Concurrent work in the last 6 months? Cite ≥ 2 candidates from arXiv (filter by date) or note "search returned 0 within window".
3. **M3.** Hidden equivalence with a classical method? Name the classical method and explain the mapping (e.g., "this is greedy beam search with a learned scorer").
4. **M4.** Is this an engineering trick on top of an existing method? If yes, name the existing method and what is added.
5. **M5.** Survey paper coverage? Find ≥ 1 recent survey that touches this area and cite the section/paragraph addressing this idea (or note "no survey covers this yet").

## Aggressive attacks (issue ≥ 3, with citations)

6. **A6.** "Isn't this just `<X>`?" — name `X` with citation.
7. **A7.** "This smells like `<Y>`" — name `Y` with citation; explain the smell.
8. **A8.** "`<Author>` did this in `<year>`, see arXiv:`<id>`" — find the most likely prior author.
9. **A9.** "`<Paper title>` seems identical" — exact-phrase match search; if any title matches > 60% of the idea's keywords, cite it.
10. **A10.** "Code already exists at github.com/`<repo>`" — run a GitHub query for the unique mechanism keywords.

## Differentiation (if M1-A10 reveal close prior work)

11. **D11.** What is the concrete delta from the closest prior work? Name 1-3 axes (mechanism, scale, benchmark, regime).
12. **D12.** Would the delta survive Reviewer 3 (novelty-focused)? Imagine R3's first paragraph of the review — does it accept the delta as substantial, or call it incremental?
13. **D13.** Is the delta defensible as a standalone contribution at an A* venue, or only as a workshop note?
14. **D14.** Is the idea a subset of broader prior work (e.g., the prior paper proposed a framework and this idea is one instantiation)?
15. **D15.** Are there ≥ 3 concurrent papers in the last 12 months on the same topic? (Saturation signal — even if no exact duplicate, the field has converged.)

## Coverage record

`Questions covered: M1..M5, A6, A7, A8, D11, D12 (10/15)`. Stage 2 cannot pass with fewer than M1-M5 + 3 attacks attempted.
