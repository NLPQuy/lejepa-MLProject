# Research-Idea Skills for Claude Code

Two markdown-only Claude Code skills that work as a pair: one **proposes** research ideas to climb a benchmark **on a specific task** (problem framing), the other **vets** them adversarially before you commit compute. Both skills require an explicit task description alongside the benchmark name — a benchmark alone is not enough, since most benchmarks cover multiple tasks.

```
.claude/skills/
├── benchmark-climb-ideation/   Propose 5–10 ideas for a specific benchmark
│                               (multi-tier search, 12 patterns, 7-step verification)
└── idea-vetting/               Attack each idea through 8 stages
                                (adversarial personas, rebuttal loop, KILL/TOY/FULL verdicts)
```

Both are **standalone**, **portable**, and **markdown end-to-end** — no Python, no extra dependencies, no framework lock-in. Drop this `.claude/skills/` directory into any project that uses Claude Code and the slash commands work immediately.

## Quick start

```bash
# 1. Propose ideas for a benchmark + task (greenfield, default tier mix 45/35/20)
/benchmark-climb-ideation MATH-500 \
  --task "competition-level math word problems with single numeric answer"
# → ./ideation-output/MATH-500/batch-1.md (5-10 ideas, each with primary paper,
#   mechanism, gain estimate, falsification test)

# 1b. Or: enhance an existing pipeline (≥ 50% enhance-existing ideas, in-field biased)
/benchmark-climb-ideation HumanEval \
  --task "function-level Python code completion from docstring + signature" \
  --pipeline ./pipelines/code_pipeline.md \
  --tier-mix 55/30/15

# 2. Vet the batch adversarially (task + pipeline inherited from the batch header)
/vet-ideas ideation-output/MATH-500/batch-1.md
# → ./vetting-output/MATH-500/batch-1/idea-<i>-vetting.md + batch-summary.md
#   verdicts: KILL / REFRAME / TOY / FULL SEND

# 3. Re-propose with vetting feedback
/benchmark-climb-ideation MATH-500 \
  --task "competition-level math word problems with single numeric answer" \
  --given-vetting vetting-output/MATH-500/batch-1/batch-summary.md
# → batch-2.md, avoiding killed patterns, biased toward survived ones
```

You can also use either skill alone — paste a single idea, paper proposal, or YAML task-notes block. In all cases the skill will ask for the **task / problem** if it cannot find one (benchmark name alone is insufficient), and will ask whether you have an **existing pipeline** to enhance vs. starting from scratch.

## What these skills do

### `benchmark-climb-ideation`

For a named benchmark **and a named task** (problem framing), produce a **verified, diverse batch of 5–10 research ideas** with grounded sources. The task description is mandatory — the skill refuses to run with only a benchmark name. If you also supply an **existing pipeline** (`--pipeline`), the batch shifts to `enhance-existing` mode and ≥ 50% of ideas must modify a component of that pipeline rather than redesign it from scratch. Hard-enforces:

- **Three-tier search** — default in-field 45 % / adjacent 35 % / cross-domain 20 %, with bands ±10 pp. Tunable via `--tier-mix <a>/<b>/<c>` (must sum to 100, each ≥ 10).
- **12 idea patterns** (P1–P12: Combine / Transfer / Replace / Scale / Decompose / Verify / Iterate / Specialize / Tool-use / Sampling / ICL / Self-play); max 2 ideas per pattern, ≥ 5 distinct patterns per batch
- **Anti-bias rules** — ≥ 3 distinct venues, ≥ 3 time windows, ≥ 3 technique families, ≤ 2 ideas per institution
- **7-step verification per idea** — Novelty / Provenance / Feasibility / Gain-sanity / Falsification / Risk / Compliance, with controlled-vocabulary verdicts
- **Reverse-search + devil's-advocate** passes to fill gaps and pressure-test the top pick
- **Append-only logs** under `_logs/` for search queries, proposals, rejections

See [`.claude/skills/benchmark-climb-ideation/README.md`](.claude/skills/benchmark-climb-ideation/README.md) for flags and file layout.

### `idea-vetting`

For each idea, run an **8-stage adversarial pipeline** with persona switching. Produces an explicit `KILL` / `REFRAME` / `TOY` / `FULL SEND` verdict with confidence tag.

| Stage | Persona | Goal |
|-------|---------|------|
| 1 — Problem Framing | Senior Advisor | Is the problem real or a benchmark artifact? |
| 2 — Prior Work Attack | Prior-Work Hunter | Has someone already published this? (early-exit on hard duplicate) |
| 3 — Novelty Decomposition | Critical Reviewer | Which of 8 novelty axes does this hit? Is it rebranding? |
| 4 — Theory Grounding | Theorist | What's the mechanism? Does multi-view analysis hold? |
| 5 — Feasibility Analysis | Pragmatic PM | Cost / wallclock / significance — with numbers, not vibes |
| 6 — Killer Baseline | Skeptical Empiricist | Will a simple tuned baseline match this? |
| 7 — Reviewer Simulation | R1/R2/R3 sub-personas | Will this survive peer review? |
| 8 — Decision Gate | PI | Synthesize → KILL / REFRAME / TOY / FULL SEND |

Each attack runs through a **rebuttal loop**: steel-manned rebuttal → persona response → DEFLECTED / WEAKENED / UNREBUTTED. UNREBUTTED attacks **downgrade** the stage verdict. Toy verdicts come with numeric falsification thresholds fixed before the toy runs.

See [`.claude/skills/idea-vetting/README.md`](.claude/skills/idea-vetting/) and [`.claude/skills/idea-vetting/SKILL.md`](.claude/skills/idea-vetting/SKILL.md) for the full pipeline + 4 worked examples in `examples/`.

## How they chain (file contract)

```
ideation-output/<bench>/batch-<N>.md            ← ideation writes
                  │
                  ▼
         vetting reads, parses
                  │
                  ▼
vetting-output/<bench>/batch-<N>/
  ├── idea-<i>-vetting.md  (one per idea)
  └── batch-summary.md     ← can be fed back via --given-vetting
                  │
                  ▼
         ideation reads on next call,
         avoids killed patterns, biases toward survivors
```

Loose coupling: vetting never modifies ideation outputs; ideation never reads vetting internals. Either skill works without the other present.

## Requirements

- **Claude Code** (any version with skill support)
- Tools enabled: `WebSearch`, `WebFetch`, `Read`, `Write`, `Edit`, `Bash`
- Write access to the project root (skills create `ideation-output/`, `vetting-output/`, `_logs/`)

No Python, no API keys beyond what Claude Code already uses, no external services.

## Plugging into a research project

1. Copy `.claude/skills/` into the target project root (or merge if `.claude/` already exists).
2. Open the project in Claude Code.
3. The slash commands `/benchmark-climb-ideation`, `/vet-ideas`, `/red-team-ideas`, `/defend-ideas` are now available.
4. Outputs land under `./ideation-output/` and `./vetting-output/` relative to the project root.

That's it. The skills are markdown specs Claude reads on demand; nothing to install or initialize.

## File structure

```
.
├── README.md                            (this file)
├── CLAUDE.md                            (guidance for Claude when editing the skills)
└── .claude/
    └── skills/
        ├── benchmark-climb-ideation/    11 files — SKILL.md + rules/ + patterns/
        │                                + templates/ + checklists/ + examples/
        └── idea-vetting/                ≈ 35 files — SKILL.md + stages/ + personas/
                                         + question-banks/ + templates/ + rules/
                                         + checklists/ + _logs/ + examples/
```

## License

Released as part of a research-tooling effort. Use freely; if you adapt the skills for a paper, attribution is appreciated but not required.
