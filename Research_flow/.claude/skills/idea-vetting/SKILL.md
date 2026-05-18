---
name: idea-vetting
description: Adversarial vetting of research ideas — runs an 8-stage attack pipeline to filter ideas before implementation. Use when the user has 1+ research ideas and wants an explicit KILL / REFRAME / TOY / FULL verdict before committing compute.
triggers:
  slash-commands:
    - /vet-ideas
    - /red-team-ideas
    - /defend-ideas
  keywords:
    - "vet these ideas"
    - "attack this idea"
    - "stress test this proposal"
    - "would this survive review"
tools-required: [WebSearch, WebFetch, Read, Write, Edit, Bash]
input-types:
  - batch file (from ideation skill output)
  - single idea text
  - paper-style proposal
  - yaml task-notes
default-budget-per-idea: 8 min
max-budget-per-batch: 60 min
---

# Idea Vetting Skill

## When to use

Use **AFTER** ideas exist (from `/propose-benchmark-ideas`, paper reading, or user thinking) and **BEFORE** committing significant compute or time to implementation.

Use when:
- You have ≥ 1 idea worth scrutinizing.
- The stakes are high enough that wasting compute on a bad idea hurts.
- You want an explicit `KILL` / `REFRAME` / `TOY` / `FULL` decision, not "looks ok".

Do NOT use when:
- The user is brainstorming (use the ideation skill instead).
- The idea is a trivial change (< 2h implementation).
- Implementation already started (sunk cost; vetting now wastes time).

## Inputs required

1. **Ideas to vet** — file path or pasted text.
2. **Benchmark name** — the evaluation set ideas target.
3. **Task / problem** — the concrete problem framing being solved on that benchmark (e.g., "code completion from docstring", "multi-hop QA"). If the input is an ideation-skill batch file, parse it from the batch header (`Task / problem` line). If pasted single idea or paper proposal: ASK USER if not stated. Vetting on a benchmark without a task is not allowed — Stage 1 (Problem Framing) cannot run otherwise.
4. **Resource constraints** — compute, time, person-hours.
5. **Mode** — `--climb-mode` (skip Stage 7 publish-focused) or `--paper-mode` (full Stage 7).

If inputs missing → ASK USER. Specifically, if the user supplies only a benchmark with no task description, ASK: "Trên benchmark này, các ideas này nhắm giải bài toán cụ thể gì?"

## Adversarial mindset (MANDATORY — load every session)

Read [./rules/adversarial-mindset.md](./rules/adversarial-mindset.md) at the start of every session.

Core rule: **Try to kill each idea. If it survives, it's worth implementing.** Suppress default LLM agreeableness. Steel-man rebuttals; stay hostile to weak ideas.

## Persona switching

Each stage uses a specific persona (see [./personas/](./personas/)). Switching is **explicit**, not implicit. When entering a stage, declare:

> Adopting persona: `<name>`. Stance: `<one-line stance>`.

Personas attack the IDEA, never the user. See `adversarial-mindset.md §Safety`.

## Workflow

### Step 1: Pre-vet
Run [./checklists/pre-vet.md](./checklists/pre-vet.md). It confirms inputs, loads [./rules/adversarial-mindset.md](./rules/adversarial-mindset.md), and reads the 4 log files in `./_logs/` to surface prior context (avoid re-attacking already-killed angles; surface pending toys; identify open re-vet triggers).

### Step 2: Parse ideas

The skill accepts **3 input types**. Detect by inspecting the input:

#### Input type A — Ideation-skill batch file
Path matches `ideation-output/<bench>/batch-<N>.md` (or any path containing `## Ranked ideas`). Expected format (produced by the `benchmark-climb-ideation` sibling skill):

```
# Idea Batch <N> for benchmark <BENCHMARK>
## Summary table
| # | Title | Pattern | Tier | Gain | Feas | Effort | Score |
| 1 | <title> | P2 | 3 | +1.5 | 4 | M | 3.0 |
...
## Ranked ideas
### Idea 1: <title>
- **Pattern**: P<n>
- **Tier**: <n>
...
### Idea 2: ...
```

Parser procedure:
1. Read the file.
2. Extract `<BENCHMARK>` and `<TASK>` from the H1 (new format: `# Idea Batch <N> — <BENCHMARK> / <TASK>`) and the `## Inputs` block's `Task / problem:` line. If the batch file pre-dates this format and `Task / problem` is absent, ASK USER for the task before proceeding.
3. Read the `## Summary table` to get the idea count, titles, and score metadata (used for the `batch-summary.md` recommendations).
4. Split `## Ranked ideas` on `^### Idea ` headers; each split is one idea.
5. For each idea, extract: Pattern, Tier, Target task, Scope (enhance-existing / greenfield, when present), One-liner, Mechanism, Source inspirations (primary + supporting), Expected gain, Feasibility, Effort, Falsification test, Risks. If an idea's `Target task` drifts from the batch-level `<TASK>`, note it — Stage 1 (Problem Framing) will surface this as a framing attack. If the batch header has `Existing pipeline: <description>`, propagate that context: Stage 6 (Killer Baseline) treats the existing pipeline as the de-facto baseline to beat, and `greenfield` ideas in an enhance-mode batch must justify why a redesign beats a component swap (Stage 5 Feasibility attack).
6. ALSO read `ideation-output/<bench>/_logs/_proposal_log.md` (context) and `_rejection_log.md` (avoid re-attacking already-rejected angles).

#### Input type B — Single idea text (pasted)
The user pastes a free-form idea description in the conversation. Wrap as a 1-idea batch with `<BENCHMARK>` AND `<TASK>` asked from the user if not stated. Use whatever structure the user provided; flag missing fields (mechanism / primary paper / falsification) — those become Stage-1 / Stage-2 / Stage-5 attacks.

#### Input type C — Paper-style proposal / YAML task-notes
A markdown or YAML proposal block. Extract title + task framing + mechanism + claimed-baseline-improvement. Same flow as B (1-idea batch). For YAML, parse the `task-notes` block per the user's project conventions.

#### Announce
After parsing: "Vetting `<N>` ideas on `<BENCHMARK>` for task `<TASK>`. Estimated time: `<N × 8>` min (cap 60 min)."

#### Output directory
Create `vetting-output/<bench>/batch-<N>/` if not present. For single-idea inputs without a source batch number, use `vetting-output/<bench>/standalone-<YYYYMMDD-HHMM>/`.

### Step 3: For each idea, run the 8-stage pipeline
Load each stage file and execute its procedure. Within every stage, every attack runs through the **rebuttal loop**:

1. Persona issues an attack (cited, specific).
2. Skill generates a **steel-manned rebuttal** — the strongest possible counter the idea author would give (cite papers, use math, no handwaving). See [./rules/rebuttal-loop.md](./rules/rebuttal-loop.md) §Steel-man rule.
3. Persona evaluates: ✅ **DEFLECTED** / ⚠️ **WEAKENED** / ❌ **UNREBUTTED**.
4. If WEAKENED, persona may issue ONE refined follow-up (Round 2). **Max 2 rebuttal rounds per attack; max 3 attacks per stage get the full rebuttal treatment; max 16 cycles per idea.**
5. Each cycle is emitted using [./templates/rebuttal-format.md](./templates/rebuttal-format.md).
6. The user MAY interject with their own rebuttal at any point (see `rebuttal-loop.md §User-input rebuttal`). The persona re-evaluates honestly.
7. After all attacks, the stage's verdict is **downgraded** per `./rules/decision-logic.md §UNREBUTTED downgrade rule` based on the UNREBUTTED count.

Early-exit shortcuts apply (see flow below):

| # | Stage | Persona | File |
|---|-------|---------|------|
| 1 | Problem Framing | Advisor | [./stages/1-problem-framing.md](./stages/1-problem-framing.md) |
| 2 | Prior Work Attack | Prior-Work Hunter | [./stages/2-prior-work-attack.md](./stages/2-prior-work-attack.md) |
| 3 | Novelty Decomposition | Critical Reviewer | [./stages/3-novelty-decomposition.md](./stages/3-novelty-decomposition.md) |
| 4 | Theory Grounding | Theorist | [./stages/4-theory-grounding.md](./stages/4-theory-grounding.md) |
| 5 | Feasibility Analysis | Pragmatic PM | [./stages/5-feasibility-analysis.md](./stages/5-feasibility-analysis.md) |
| 6 | Killer Baseline | Skeptical Empiricist | [./stages/6-killer-baseline.md](./stages/6-killer-baseline.md) |
| 7 | Reviewer Simulation | Reviewers R1/R2/R3 | [./stages/7-reviewer-simulation.md](./stages/7-reviewer-simulation.md) |
| 8 | Decision Gate | Advisor (PI mode) | [./stages/8-decision-gate.md](./stages/8-decision-gate.md) |

**Stage execution flow:**

```
For each idea:
  Stage 1 → if FAIL → skip to Stage 8 (KILL)
  Stage 2 → if FAIL (hard dup) → skip to Stage 8 (KILL)
  Stage 3 → always
  Stage 4 → if --climb-mode, lite version
  Stage 5 → always
  Stage 6 → if FAIL → skip to Stage 8 (KILL or REFRAME)
  Stage 7 → if --no-publish or --climb-mode, skip
  Stage 8 → always (final synthesis)
```

Each stage output uses [./templates/per-stage-output.md](./templates/per-stage-output.md).

Write the per-idea report to `vetting-output/<bench>/batch-<N>/idea-<i>-vetting.md` using [./templates/per-idea-report.md](./templates/per-idea-report.md).

### Step 4: Batch summary

Aggregate per-idea verdicts into a single `batch-summary.md` using [./templates/batch-summary.md](./templates/batch-summary.md). Apply [./rules/decision-logic.md §Batch aggregation](./rules/decision-logic.md):

1. Count `KILLED` / `REFRAMED` / `TOY` / `FULL_SEND`. Compute `survival_rate = (FULL_SEND + TOY) / N`.
2. Apply the calibration check (< 30 % suggests weak batch; > 80 % suggests insufficient rigor — spot-audit).
3. Pick the **Top-3 across 3 distinct axes** per `decision-logic.md §Diversification`:
   - 🥇 Top FULL SEND (composite × vetting-confidence)
   - ⚡ Fastest to validate (lowest `toy_cost`)
   - 🎯 Highest expected value (`gain_mid × P(survive)`)
4. Write `batch-summary.md` to `vetting-output/<bench>/batch-<N>/batch-summary.md`. Required sections: Verdicts table / Survival rate / Top-3 / Killed table / Reframed table / Toy queue (cost-sorted ascending) / FULL SEND queue (composite-sorted descending) / Recommended user action.

For TOY verdicts, the per-idea report's `Toy Experiment Design` block uses [./templates/toy-experiment-design.md](./templates/toy-experiment-design.md). The Toy queue in `batch-summary.md` references each.

### Step 5: User-facing output
Print:
- Per-idea verdict table
- Top recommendations (FULL ideas ranked; TOY ideas with toy-design pointers)
- Path to full reports
- Suggested next action

### Step 6: Log

Append entries to four **append-only** log files. Use the entry format defined at the top of each file — every field is required for parseability across sessions. Logs are read by Step 1 of future sessions to filter duplicate attacks and surface pending work.

Logs live in TWO locations:
- **Skill-local** (`./_logs/` — templates with format spec): [./_logs/_vetting_log.md](./_logs/_vetting_log.md), [./_logs/_killed_ideas.md](./_logs/_killed_ideas.md), [./_logs/_passed_ideas.md](./_logs/_passed_ideas.md), [./_logs/_toy_queue.md](./_logs/_toy_queue.md). These hold the entry-format specs — DO NOT write session data here.
- **Project-local** (`vetting-output/<bench>/_logs/`): the actual append targets. Create them if missing by copying the headers (frontmatter + H1 + `<!-- entries appended below -->`) from the skill-local templates, then append session entries below that comment.

Append per session:
1. **`_vetting_log.md`** — one entry per batch (or per single-idea re-vet). Format: `## <datetime> — Batch <N> vetting` block with Benchmark / Source / Ideas vetted / Verdicts / Time / Survival / Top pick / Notable / Re-vet trigger.
2. **`_killed_ideas.md`** — one entry per KILLed idea. Format: `## <date>` → `### Batch <N> — <BENCHMARK>` → `#### Idea <i>: <title>` with Killed-at / Killing-attack / Evidence / Salvageable / Confidence / Source / Resurrection-eligible.
3. **`_passed_ideas.md`** — one entry per FULL SEND. Format: `#### Idea <i>: <title>` with Verdict / Confidence / Composite / Gain / Cost / Priority / Risk-mitigation / Source / Status.
4. **`_toy_queue.md`** — one entry per TOY. Append under `## Active`, **maintain cost-ascending order**. On completion (user reports toy results), append a parallel entry under `## Completed` and update the Active entry's Status to `completed`.

**Append-only discipline**: never overwrite, never delete prior entries. To "edit" status, append a new dated entry that supersedes (e.g., a TOY graduating to FULL SEND gets a new `_passed_ideas.md` entry tagged `(post-toy)`; the original TOY entry in `_toy_queue.md` stays for audit, with Status updated to `completed`).

Run pre-deliver audit per [./checklists/pre-deliver.md](./checklists/pre-deliver.md) before printing.

(Optional) Append a 1-line entry to project-root `cross-skill-log.md` if it exists, per `templates/batch-summary.md §Cross-skill log entry`.

## Decision logic

All Stage 8 verdicts follow [./rules/decision-logic.md](./rules/decision-logic.md). Priority order:

1. Stage 2 FAIL → **KILL**
2. Stage 6 FAIL → **KILL** unless reframe addresses
3. ≥ 3 stages FAIL → **KILL**
4. 0 FAIL + ≤ 2 WARN + Stage 5 PASS → **FULL SEND**
5. 0 FAIL + 3-4 WARN → **TOY EXPERIMENT FIRST**
6. 0 FAIL + ≥ 5 WARN → **REFRAME**
7. 1 FAIL + others PASS/WARN → **REFRAME or TOY**
8. 2 FAIL → **REFRAME or KILL** (depends on which stages)

Confidence tags 🟢🟡🔴 per `decision-logic.md §Confidence tags`.

## Stop conditions

- Step 5 completed (success)
- > 60 min wall-clock for batch
- > 12 min for single idea
- User interrupt

## Quality gates (self-check before delivery)

- [ ] All 8 stages run per idea (or explicit skip with reason logged)
- [ ] Each stage 1-7 has ≥ 1 attack issued **with a full rebuttal cycle** (steel-manned rebuttal + persona response, round 1 or 1+2)
- [ ] Steel-manned rebuttals follow `./rules/rebuttal-loop.md §Steel-man rule` (cite papers, use math, no handwaving)
- [ ] No rebuttal block exceeds 2 rounds; no stage exceeds 3 full-rebuttal attacks; total ≤ 16 cycles per idea
- [ ] `Rebuttal-cycle summary` (DEFLECTED / WEAKENED / UNREBUTTED counts) present in every stage
- [ ] UNREBUTTED-downgrade rule applied to each stage verdict before Stage 8 reads it
- [ ] User-input rebuttals (if any) are tagged `Source: user` in the block
- [ ] Persona switch declared at the start of each stage
- [ ] Final verdict justified by stage results
- [ ] Confidence tag on verdict (🟢🟡🔴)
- [ ] Toy design provided if verdict = TOY
- [ ] Reframe suggestion provided if verdict = REFRAME
- [ ] Kill rationale documented if verdict = KILL
- [ ] Per-idea report written to `vetting-output/`
- [ ] Logs updated

## Anti-patterns

- Don't say "this is a great idea, here's how to improve" — that's the ideation skill, not vetting.
- Don't issue vague attacks ("seems incremental") — cite specific paper / metric / baseline.
- Don't skip Stage 6 (killer baseline) — it is the most-painful, highest-value stage.
- Don't lean toward KILL when uncertain — lean toward TOY (reversible).
- Don't attack the user; attack the idea.

## Integration with the ideation skill

The vetting skill is designed to **chain** with `benchmark-climb-ideation` but is **not coupled** to it.

### Standalone use (no ideation skill required)

Vetting accepts three input forms that have nothing to do with the ideation skill:
1. **Pasted single idea** in the chat (free-form text — `/vet-ideas "<idea text>"`).
2. **Paper-style proposal** (markdown or PDF excerpt the user pastes).
3. **YAML task-notes** the user maintains separately.

For any of these, Step 2 wraps the input as a 1-idea batch with output path `vetting-output/<bench>/standalone-<YYYYMMDD-HHMM>/`. The full 8-stage pipeline runs identically.

### Chained use (ideation → vetting)

When the user invokes `/vet-ideas ideation-output/<bench>/batch-<N>.md`, the skill reads the ideation skill's output directly.

**Input file format expected** (must match the ideation skill's §13.1 spec):

```markdown
# Idea Batch <N> — <BENCHMARK_NAME> / <TASK>
**Generated**: <ISO datetime>

## Inputs
- Benchmark: <name>
- Task / problem: <concrete task framing>
- ...

## Summary
| Metric | Value | ... (Tier 1/2/3, Patterns used, etc.)

## Top-3 Recommendations
### 🏆 Top-1 by composite score
**Idea <X>: <Title>** — Score: <S>

## Ranked ideas
### Idea 1: <Title>
- **Pattern**: P<n>
- **Tier**: <n>
- **One-liner**: ...
- **Mechanism**: ...
- **Source inspirations**:
  - Primary: <Paper>, <Authors>, <Venue Year> [arXiv:XXXX.XXXXX]
- **Expected gain**: +X.X / +Y.Y / +Z.Z pp 🟢🟡🔴
- **Feasibility**: <1-5>
- **Effort**: <S/M/L/XL/XXL>
- **Falsification test**: ...

### Idea 2: ...

## Verification report
| # | Title | Novelty | Provenance | Verdict |
| 1 | ... | NOVEL ✅ | VERIFIED ✅ | KEEP |
```

Parser procedure: see Step 2 §Input type A.

**Cross-skill files vetting READS**:

| Path | Purpose |
|------|---------|
| `ideation-output/<bench>/batch-<N>.md` | Primary input — the batch to vet |
| `ideation-output/<bench>/_logs/_proposal_log.md` | Prior-batch context — avoid re-vetting an already-shipped idea |
| `ideation-output/<bench>/_logs/_rejection_log.md` | Already-rejected angles — do not waste a new Stage-2 attack on these |
| `ideation-output/<bench>/_logs/_search_log.md` | Optional — surfaces what ideation already searched (Stage 2 can skip duplicate queries) |
| `vetting-output/<bench>/_logs/_killed_ideas.md` | Own log — filter out attack angles already exhausted on prior vetting batches |
| `vetting-output/<bench>/_logs/_vetting_log.md` | Own log — see what's been vetted, surface open re-vet triggers |
| `vetting-output/<bench>/_logs/_passed_ideas.md` | Own log — track shipped FULL SEND ideas |
| `vetting-output/<bench>/_logs/_toy_queue.md` | Own log — surface pending toys |

**Cross-skill files vetting WRITES**:

| Path | Content |
|------|---------|
| `vetting-output/<bench>/batch-<N>/idea-<i>-vetting.md` | One per idea — full 8-stage report |
| `vetting-output/<bench>/batch-<N>/batch-summary.md` | Aggregate report (per `./templates/batch-summary.md`) |
| `vetting-output/<bench>/_logs/_vetting_log.md` | Append one entry per batch |
| `vetting-output/<bench>/_logs/_killed_ideas.md` | Append one entry per KILL |
| `vetting-output/<bench>/_logs/_passed_ideas.md` | Append one entry per FULL SEND |
| `vetting-output/<bench>/_logs/_toy_queue.md` | Append one entry per TOY (cost-ascending) |
| `cross-skill-log.md` (project root, optional) | Append 1-line entry per batch |

### Feedback to the ideation skill

The ideation skill can consume vetting output on the next ideation call:

- `/propose-benchmark-ideas <bench> --given-vetting vetting-output/<bench>/batch-<N>/batch-summary.md` — biases the next batch toward patterns that survived vetting and away from patterns that died.
- `/propose-benchmark-ideas <bench> --avoid-patterns P4,P10` — explicit list of patterns to skip (often derived from the killed-ideas log).

The vetting skill does NOT modify ideation files; it only writes to `vetting-output/`. The ideation skill's `--given-vetting` flag is the read-side of this contract.

### Re-vetting after results

When the user obtains real experimental results for a FULL SEND or TOY idea:

- `/vet-ideas --given-result "Idea 5 got 72.5%, +2.3pp over baseline" idea-5` — re-runs Stages 4, 5, 6 with the new evidence and emits `vetting-v2.md` per `rules/decision-logic.md §Versioning`.
- `/vet-ideas --given-toy ./toy-results.md idea-5` — same flow, triggered by toy-experiment results.
- `/vet-ideas --resurrect idea-2 --counter-argument "..."` — re-runs vetting on a previously KILLed idea using the user's counter-argument as a user-input rebuttal.

### Loose-coupling guarantee

The vetting skill's contract with the ideation skill is **read-only on ideation outputs + write-only on vetting outputs**. Nothing in `ideation-output/` is ever modified. If the ideation skill is absent from a project, vetting runs against pasted ideas or paper proposals with identical pipeline behavior.

## Reference files (load on-demand)

- [./stages/](./stages/) — 8 stage execution scripts
- [./personas/](./personas/) — 6 persona definitions
- [./templates/per-idea-report.md](./templates/per-idea-report.md) — final report format
- [./templates/per-stage-output.md](./templates/per-stage-output.md) — per-stage block format
- [./rules/adversarial-mindset.md](./rules/adversarial-mindset.md) — mindset override (MANDATORY)
- [./rules/rebuttal-loop.md](./rules/rebuttal-loop.md) — attack → steel-manned rebuttal → persona-response mechanism
- [./rules/decision-logic.md](./rules/decision-logic.md) — Stage 8 synthesis + UNREBUTTED downgrade + batch aggregation + diversification
- [./templates/rebuttal-format.md](./templates/rebuttal-format.md) — per-attack rebuttal block
- [./templates/batch-summary.md](./templates/batch-summary.md) — batch aggregate report
- [./templates/toy-experiment-design.md](./templates/toy-experiment-design.md) — toy block when verdict = TOY
- [./checklists/pre-vet.md](./checklists/pre-vet.md) — pre-vet input + log-load checklist
- [./checklists/pre-deliver.md](./checklists/pre-deliver.md) — final audit before printing
- [./_logs/](./_logs/) — append-only log templates (`_vetting_log.md`, `_killed_ideas.md`, `_passed_ideas.md`, `_toy_queue.md`)
- `./question-banks/stage-N-questions.md` — full Q-banks (Phase V2, not present yet)

## Activation flow

Slash (`/vet-ideas <input>`): execute Steps 1-6.
Natural language ("attack this idea: X"): confirm intent → same flow.
