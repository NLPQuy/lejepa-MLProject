# BAD Batch Example — Vague + Fake Citations (Annotated)

> **This is a teaching example.** Each idea below has at least one specific defect (vague mechanism, fabricated citation, missing falsification). Diagnostics at the bottom.

# Idea Batch 1 — MATH-500
**Generated**: 2026-05-17T08:00:00Z
**Skill version**: 0.1.0

## Inputs
- Benchmark: MATH-500
- Baseline: gpt-4o-mini @ 70.2%
- Constraints: prompting only

## Summary table
| # | Title | Pattern | Tier | Gain | Feas | Effort |
|---|-------|---------|------|------|------|--------|
| 1 | Use a better reasoning method | P? | 1 | "big" | 5 | S |
| 2 | Smart sampling | P10 | 1 | +5.0 | 5 | S |
| 3 | Leverage embeddings | P11 | 2 | +3.0 | 5 | M |
| 4 | Apply quantum-inspired search | P2 | 3 | +10.0 | 4 | L |
| 5 | Multi-agent debate | P1 | 1 | +4.0 | 4 | M |

## Ranked ideas

### Idea 1: Use a better reasoning method
- **Pattern**: (unspecified)
- **Mechanism**: "Make the model reason better by improving how it thinks about problems."
- **Source inspirations**:
  - Primary: "Reasoning in LLMs", Smith et al., NeurIPS 2025 [arXiv:2511.12345]
- **Expected gain**: "big" 🟢
- **Falsification test**: *(missing)*

### Idea 2: Smart sampling
- **Pattern**: P10 — **Tier**: 1
- **Mechanism**: "Sample smartly to get better answers."
- **Source inspirations**:
  - Primary: "Better Sampling for LLMs", Doe & Roe, ICML 2025 [arXiv:2503.99999]
- **Expected gain**: +5.0 pp 🟢
- **Falsification test**: "It will work if it works."

### Idea 3: Leverage embeddings
- **Pattern**: P11 — **Tier**: 2
- **Mechanism**: "Use embeddings to retrieve relevant context and improve performance."
- **Source inspirations**:
  - Primary: "Self-Consistency", Wang et al., ICLR 2023 [arXiv:2203.11171]
  - *(Note: Wang et al. is real, but the paper is about majority-voting over CoT samples — it does NOT propose embedding-based retrieval. The citation is MISREPRESENTED.)*
- **Expected gain**: +3.0 pp 🟢
- **Falsification test**: "Better than baseline."

### Idea 4: Apply quantum-inspired search
- **Pattern**: P2 (Transfer) — **Tier**: 3
- **Mechanism**: "Use quantum-inspired search algorithms to explore the reasoning space more efficiently."
- **Source inspirations**:
  - Primary: "Quantum Computing for NLP", Lee et al., Nature Quantum 2024 [arXiv:2406.88888]
  - *(No such paper exists; venue name is fabricated.)*
- **Expected gain**: +10.0 pp 🟢
  - *(Baseline 70.2% + claimed 10pp = 80.2%; current published SOTA on MATH-500 with gpt-4o-mini-class models is ~76%. This gain is `> headroom_to_realistic_SOTA × 2` → must downgrade to 🔴.)*
- **Falsification test**: *(missing)*

### Idea 5: Multi-agent debate
- **Pattern**: P1 (Combine) — **Tier**: 1
- **Mechanism**: "Have multiple agents debate the answer to improve correctness."
- **Source inspirations**:
  - Primary: "Multi-agent Debate", Anonymous, Workshop 2024 (no arXiv ID, no venue)
- **Expected gain**: +4.0 pp 🟢
- **Falsification test**: *(missing)*

---

## What's wrong with each idea

| # | Defect | Stage that should catch it | Fix |
|---|--------|----------------------------|-----|
| 1 | Vague mechanism ("reason better"); fabricated arXiv ID (`2511.*` is future-dated); pattern unspecified; no gain number; no falsification | `checklists/per-idea.md` (fails ≥ 4 boxes → drop entirely) | Drop the idea. Re-draft with a concrete technique (CoT, decomposition, verifier, etc.). |
| 2 | Vague mechanism; fabricated authors; tautological falsification ("works if it works") | Per-idea checklist (mechanism), `verification.md` Step 2 (provenance — `BROKEN_LINK`), Step 5 (falsification — `REJECT`) | Drop. If you mean "temperature sweep", say so and cite Holtzman et al. nucleus sampling. |
| 3 | MISREPRESENTED citation: Wang et al. cited but its paper is not about embeddings | `verification.md` Step 2 (`MISREPRESENTED` → REJECT) | Replace with a real ICL/retrieval paper (e.g., Liu et al. 2021 [arXiv:2101.06804]). |
| 4 | Fabricated paper + fabricated venue ("Nature Quantum" does not exist as a venue); implausible gain (+10pp without precedent); no adaptation plan despite Tier-3 tag | `verification.md` Step 2 (`BROKEN_LINK` → REJECT), Step 4 (gain-sanity → DOWNGRADE 🔴), `idea-template.md` requires Adjacent/Cross-domain notes for Tier 3 | Drop. If "quantum-inspired" means "amplitude-amplification-style biased sampling", say so concretely and cite a real adaptation paper. |
| 5 | Anonymous + workshop-only + no arXiv ID = Tier-4 source per `source-trust.md`; vague mechanism (no debate protocol named); no falsification | `verification.md` Step 2 (`BROKEN_LINK`), `source-trust.md` (Tier-4 not acceptable as primary), per-idea checklist | Rewrite with a concrete protocol (e.g., Du et al. "Improving Factuality and Reasoning in Language Models through Multiagent Debate" [arXiv:2305.14325]) and a numeric falsification. |

## Batch-level diagnosis

- 5/5 ideas fail the per-idea checklist (no falsification test on any).
- 4/5 ideas have BROKEN_LINK or MISREPRESENTED provenance.
- 1/5 ideas (Idea 4) fails gain-sanity (implausibly large gain vs. headroom).
- 5/5 ideas tagged 🟢 confidence despite weak evidence → batch-wide over-confidence smell.

**Expected final action by the skill**: REJECT all 5 ideas, return to Step 2 with a focused re-search round. If 2 re-search rounds still cannot produce 5 verified ideas, present an empty batch with a single explanatory message — **never ship vague or fabricated content as a batch**.

## Fix recipe

1. Always fill `Falsification test` with a numeric threshold + observable.
2. Always resolve every citation's arXiv ID before drafting — if you cannot reach the paper, you cannot cite it.
3. Read the cited paper's abstract + a relevant section to confirm it supports the claim — do not assume from the title.
4. For Tier-3 ideas, fill the `Adjacent / Cross-domain notes` block; "quantum-inspired" without an adaptation plan is hand-waving.
5. Anonymous / workshop / blog citations are Tier-4 and can only appear as `Contrasting` or "concept reference", never as `Primary`.

Reference: a correctly-formatted batch is [./good-batch-MATH500.md](./good-batch-MATH500.md).
