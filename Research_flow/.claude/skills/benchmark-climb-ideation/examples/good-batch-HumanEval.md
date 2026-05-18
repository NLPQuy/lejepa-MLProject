# Idea Batch 1 — HumanEval (--focus tier-3)
**Generated**: 2026-05-18T10:15:00Z
**Time-to-batch**: 13 min
**Skill version**: 0.1.0
**Skill invocation**: `/benchmark-climb-ideation HumanEval --focus tier-3`

> **Note on distribution**: user passed `--focus tier-3`, which overrides the default 40/30/20 quota with a 4/1/1 cross-domain-heavy split (T1: 1, T2: 1, T3: 4). The `⚠️ tier-distribution skewed` warning below is INTENTIONAL — it is the requested mode, not a defect.

## Inputs
- Benchmark: HumanEval (164 problems, pass@1)
- Baseline: gpt-4o-mini @ 87.2%
- Compute budget: $40
- Time budget: 1 hour
- Constraints: prompting only, no fine-tuning
- Focus: tier-3 (cross-domain inspirations preferred)

## Summary
| Metric | Value |
|--------|-------|
| Batch size | 6 |
| Tier 1 / 2 / 3 | 1 / 1 / 4 (per `--focus tier-3`) |
| Patterns used | P6, P3, P2, P7, P9, P5 (6 distinct) |
| Distinct venues | 5 (NeurIPS, ICLR, ICML, Science, arXiv) |
| Time windows | `<12mo` (2), `12-36mo` (2), `36-72mo` (2) |
| Avg feasibility | 3.5 / 5 |
| Avg confidence | 🟢 33%, 🟡 50%, 🔴 17% |

## Summary table
| # | Title | Pattern | Tier | Gain (mid) | Feas | Effort | Score |
|---|-------|---------|------|------------|------|--------|-------|
| 1 | AlphaCodium-style flow with self-tests | P7 | 1 | +2.0 | 4 | M | 2.4 |
| 2 | CodeT — model-generated test filtering | P6 | 2 | +1.5 | 4 | M | 2.2 |
| 3 | Property-based testing as oracle | P6 | 3 | +1.8 | 3 | M | 2.1 |
| 4 | Genetic-programming candidate evolution | P2 | 3 | +1.5 | 2 | L | 1.5 |
| 5 | Type-directed enumerative search | P5 | 3 | +1.0 | 3 | M | 1.8 |
| 6 | Compile-and-fuzz repair loop | P3 | 3 | +1.2 | 3 | M | 1.9 |

## Top-3 recommendations

### 🏆 Top-1 by composite score
**Idea 1: AlphaCodium-style flow** — Score: 2.4
Multi-stage prompt flow: spec → public-tests → solution → self-test → iterate.

### ⚡ Quick win
**Idea 2: CodeT test filtering** — Effort: M, well-replicated pattern.

### 🛡️ Safe bet
**Idea 1** — Confidence 🟢 (replicated on HumanEval+).

## Ranked ideas

### Idea 1: AlphaCodium-style flow with self-tests
- **Pattern**: P7 (Iterate) — **Tier**: 1
- **One-liner**: Replace single-shot generation with a 5-stage flow (spec → test-gen → solve → exec → repair).

**Mechanism**: (1) Restate the docstring as a formal spec. (2) Generate 3 example I/O cases. (3) Generate a candidate. (4) Run candidate on the examples in a subprocess. (5) On failure, feed the failing trace back and regenerate up to 3 times.

**Source inspirations**:
- Primary: "Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering", Ridnik et al., 2024 [arXiv:2401.08500]
- Supporting: "Self-Refine", Madaan et al., NeurIPS 2023 [arXiv:2303.17651]

**Expected gain**: +1.0 / +2.0 / +3.5 pp 🟢 — **Feas**: 4/5 — **Effort**: M
**Falsification test**: 164-problem run, pass@1 ≥ baseline + 1.0pp; else fails.

### Idea 2: CodeT — model-generated test filtering
- **Pattern**: P6 (Verify) — **Tier**: 2 (Adjacent: MBPP → HumanEval)
- **One-liner**: Generate K candidates + M model-written tests; pick the candidate that passes the most tests.

**Source inspirations**:
- Primary: "CodeT: Code Generation with Generated Tests", Chen et al., ICLR 2023 [arXiv:2207.10397]

**Expected gain**: +0.8 / +1.5 / +2.5 pp 🟢 — **Feas**: 4/5 — **Effort**: M

### Idea 3: Property-based testing as oracle
- **Pattern**: P6 (Verify) — **Tier**: 3 (Cross-domain: formal methods → code-gen)
- **One-liner**: Use a Hypothesis-style property generator to fuzz candidates against invariants extracted from the docstring.

**Mechanism**: From the docstring, extract type signatures and invariants (e.g., "returns list of same length"). Auto-generate 100 random inputs satisfying the type, run candidate, check invariants. Rank K=20 candidates by invariant-pass rate.

**Source inspirations**:
- Primary: "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs", Claessen & Hughes, ICFP 2000 (classic, T3)
- Supporting: "PAL: Program-aided Language Models", Gao et al., ICML 2023 [arXiv:2211.10435]

**Expected gain**: +0.8 / +1.8 / +3.0 pp 🟡 — **Feas**: 3/5 — **Effort**: M
**Adjacent / Cross-domain notes**:
- Original domain: formal verification / property-based testing
- Target domain: code synthesis
- Adaptation: replace human-written invariants with LLM-inferred ones from docstrings; tune false-positive rate.

### Idea 4: Genetic-programming candidate evolution
- **Pattern**: P2 (Transfer from evolutionary computation) — **Tier**: 3
- **One-liner**: Treat candidates as a population; mutate via prompt-driven edits; select by test-pass rate.

**Source inspirations**:
- Primary: "A Field Guide to Genetic Programming", Poli et al., 2008 (foundational, T3 classic)
- Supporting: "AlphaCode", Li et al., Science 2022 [arXiv:2203.07814]

**Expected gain**: +0.5 / +1.5 / +3.0 pp 🔴 (speculative)
**Feas**: 2/5 🟡 — **Effort**: L 🟡
**Risks**: prompt-driven mutation cost; convergence not guaranteed; budget overrun likely.
**Falsification test**: 5-gen run on 50 problems with pop=20. If best-of-population pass@1 ≤ 1-shot baseline → fails.

### Idea 5: Type-directed enumerative search
- **Pattern**: P5 (Decompose) — **Tier**: 3 (Cross-domain: program synthesis)
- **One-liner**: Decompose the target into typed holes; LLM fills holes one at a time, type-checker prunes.

**Source inspirations**:
- Primary: "Type-and-Example-Directed Program Synthesis", Osera & Zdancewic, PLDI 2015 (T3 classic)
- Supporting: "Tree of Thoughts", Yao et al., NeurIPS 2023 [arXiv:2305.10601]

**Expected gain**: +0.5 / +1.0 / +2.0 pp 🟡 — **Feas**: 3/5 — **Effort**: M

### Idea 6: Compile-and-fuzz repair loop
- **Pattern**: P3 (Replace) — **Tier**: 3 (Cross-domain: compiler tooling)
- **One-liner**: Replace the "guess and submit" loop with "guess → compile → fuzz → repair on fuzz-failure".

**Source inspirations**:
- Primary: "Self-Repair Is a Silver Bullet for Code Generation", Olausson et al., ICLR 2024 [arXiv:2306.09896]
- Supporting: "American Fuzzy Lop" fuzzing methodology (T3 classic, tool docs)

**Expected gain**: +0.5 / +1.2 / +2.0 pp 🟡 — **Feas**: 3/5 — **Effort**: M

## Verification report
| # | Title | Novelty | Provenance | Feas | Gain | Falsif | Risk | Comply | Final |
|---|-------|---------|------------|------|------|--------|------|--------|-------|
| 1 | AlphaCodium-flow | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +2.0 🟢 | OK | LOW | PASS | **KEEP** |
| 2 | CodeT filtering | EXTENDS ✅ | VERIFIED ✅ | 4/5 | +1.5 🟢 | OK | LOW | PASS | **KEEP** |
| 3 | Property-based | NOVEL ✅ | VERIFIED ✅ | 3/5 | +1.8 🟡 | OK | MED | PASS | **KEEP** |
| 4 | Genetic prog | NOVEL ✅ | VERIFIED ✅ | 2/5 | +1.5 🔴 | OK | HIGH ⚠️ | WARN (cost) | **KEEP (flag)** |
| 5 | Type-directed | NOVEL ✅ | VERIFIED ✅ | 3/5 | +1.0 🟡 | OK | MED | PASS | **KEEP** |
| 6 | Compile-and-fuzz | NOVEL ✅ | VERIFIED ✅ | 3/5 | +1.2 🟡 | OK | MED | PASS | **KEEP** |

Counts — Verified: 6, Rejected: 0, Downgraded: 0, Re-search cycles: 0.

## Notes & warnings
- ⚠️ **Tier distribution intentionally skewed (1/1/4)** per `--focus tier-3` flag — this is the requested mode.
- Idea 4 (Genetic) flagged HIGH risk: budget overrun likely. Run only after 1-2 cheaper ideas land.
- HumanEval baseline (87.2%) leaves only ~13pp headroom — any single-idea gain estimate > 8pp is flagged 🔴 by `gain-sanity` check.

## Next steps for user
1. Run **Idea 1** (AlphaCodium-style) first — best replication evidence + safe.
2. If headroom remains, run **Idea 3** (property-based) — most novel-but-grounded.
3. Hold **Idea 4** unless cheap pre-flight (50-problem subset) shows the GP loop converges.

## Provenance signature
SHA256: `<hash of inputs + paper IDs + timestamp>`
