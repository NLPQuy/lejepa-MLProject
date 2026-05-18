# Changelog

All notable changes to the `benchmark-climb-ideation` skill.

## [0.1.0] — 2026-05-17

Initial release. Standalone Claude Code skill, markdown-only, no external dependencies beyond the standard Claude Code tool set.

### Capabilities

- **Multi-tier search** — three-tier strategy with hard quotas (T1 in-field 40–50 %, T2 adjacent 30–40 %, T3 cross-domain 20–30 %). Per-tier budget caps (≤ 19 queries, ≤ 45 summaries, ≤ 10 full reads, ≤ 15 min wall-clock). Saturation detection stops a tier early when 3 consecutive queries return only already-seen papers.
- **12-pattern idea generation** — P1 Combine, P2 Transfer, P3 Replace, P4 Scale, P5 Decompose, P6 Verify, P7 Iterate, P8 Specialize, P9 Tool-use, P10 Sampling, P11 ICL, P12 Self-play. Enforces ≥ 5 distinct patterns per batch, max 2 per pattern.
- **7-step per-idea verification** — Novelty → Provenance → Feasibility → Gain-sanity → Falsification → Risk → Compliance. Controlled-vocabulary verdicts (`NOVEL` / `EXTENDS` / `DUPLICATE`, `VERIFIED` / `BROKEN_LINK` / `MISREPRESENTED`, feasibility 1–5, etc.). Stop-early on first REJECT.
- **Anti-bias enforcement** — countable force-lists (≥ 3 distinct venues, ≥ 3 time windows, ≥ 3 technique families, ≤ 2 ideas per first-author institution). Reverse-search pass to fill obvious technique-family gaps. Devil's-advocate pass on the top-1 ranked idea. Venue-blind ranking (venue is filter/tie-break only).
- **Source-trust hierarchy** — 4-tier trust model (A* venues / A venues / preprints / blogs). Batch must have ≥ 60 % primary papers from Tier 1+2 sources.
- **Recency/classics balance** — per-window minimums (≥ 2 papers `<12mo`, ≥ 2 papers `12-36mo`, ≥ 1 paper `36-72mo`). Pure-recency or pure-classics batches surface a calibration warning.
- **Structured batch output** — every batch written to `./ideation-output/<benchmark>/batch-<N>.md` with a fixed schema (inputs, summary, ranked ideas, verification report, notes & warnings, top-3 picks: Quick win / Big bet / Safe bet).
- **Append-only logging** — every query to `_logs/_search_log.md`, every batch to `_logs/_proposal_log.md`, every rejected idea to `_logs/_rejection_log.md` with stage + tag + evidence.
- **Cross-idea consistency** — near-duplicate detection within batch, contradiction flagging, score-distribution sanity check (rejects all-🟢 over-confident batches).
- **Re-search loop** — up to 2 focused re-search cycles when verified-count < 5; partial batches ship with explicit `⚠️ Under-quota` warning rather than fabricating content.

### Flags

`--batch-size`, `--focus`, `--quick`, `--deep`, `--reset`, `--budget-compute`, `--constraints` — see [./README.md](./README.md).

### Out of scope (v0.1.0)

- No integration with any specific research-pipeline framework. The skill is standalone — outputs are markdown files, consumed by the user (or by other tools the user chooses).
- No auto-export to YAML / config snippets for downstream tools.
- No `--reflect` mode for cross-batch self-audit.
- No `--given-result` feedback loop for batch-N+1 informed by batch-N's measured outcome.

These are candidates for future versions.
