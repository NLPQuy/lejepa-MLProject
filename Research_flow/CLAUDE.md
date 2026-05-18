# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

A pair of markdown-only Claude Code skills for research-idea proposal and adversarial vetting. See [README.md](README.md) for the user-facing description.

There is **no code, no tests, no build step**. The skills are markdown files Claude reads on demand. Editing them = editing the spec.

## Skill locations

- [`.claude/skills/benchmark-climb-ideation/`](.claude/skills/benchmark-climb-ideation/) — propose ideas
- [`.claude/skills/idea-vetting/`](.claude/skills/idea-vetting/) — vet ideas

Each skill has its own `SKILL.md` entry point and a layered file structure (`rules/`, `templates/`, `patterns/` or `stages/`+`personas/`+`question-banks/`, `checklists/`, `examples/`, `_logs/`).

## Skill output locations (created on demand at project root)

```
ideation-output/<benchmark>/batch-<N>.md      proposed-idea batches
ideation-output/<benchmark>/_logs/            search / proposal / rejection logs
vetting-output/<benchmark>/batch-<N>/         per-idea reports + batch summary
vetting-output/<benchmark>/_logs/             vetting / killed / passed / toy-queue
```

These are project-local outputs, not part of the skill. Treat them as data, not code.

## When editing the skills

- **Keep SKILL.md files lean.** They are the upfront context Claude loads when the skill triggers. Detail belongs in `rules/`, `templates/`, or `stages/` files that load on demand.
- **Frontmatter matters.** Every skill file uses YAML frontmatter (`name`, `description`, `load-trigger`). Don't strip it.
- **Internal links are relative.** Use `./rules/foo.md`, `../templates/bar.md` — never absolute paths.
- **Controlled vocabularies are load-bearing.** Verdict words (`PASS`/`WARN`/`FAIL`, `DEFLECTED`/`WEAKENED`/`UNREBUTTED`, `NOVEL`/`EXTENDS`/`DUPLICATE`, `VERIFIED`/`BROKEN_LINK`/`MISREPRESENTED`, `KILL`/`REFRAME`/`TOY`/`FULL SEND`) are referenced across files. Renaming any of them is a multi-file change.
- **Append-only logs are append-only.** Files under `_logs/` (in either the skill itself OR project outputs) must never have prior entries deleted or rewritten. New entries go below `<!-- entries appended below -->`.
- **Append-only for the toy-queue is two-section.** `_toy_queue.md` has `## Active` and `## Completed` sections — new TOYs go under `## Active` in cost-ascending order, completed toys get appended under `## Completed`.

## Adding new content to a skill

Common cases:

- **New idea pattern (P13, P14, …)** — append to `benchmark-climb-ideation/patterns/pattern-catalog.md`. The `≥ 5 distinct patterns per batch` rule still holds; consider whether the new pattern needs to be added to the diversification recommendations.
- **New conference / venue** — append to `benchmark-climb-ideation/rules/conference-tiers.md` under the right field section.
- **New persona** — add `idea-vetting/personas/<name>.md` (≈ 2 KB, voice-pattern-heavy) AND wire it into the stage that uses it.
- **New question in a stage Q-bank** — append with a new stable ID (`M6`, `R11`, etc.). Existing IDs are referenced by stage output `Questions covered` lines — never renumber existing IDs.
- **New mode flag** — document in the relevant `SKILL.md` (Inputs / Workflow section) AND in the skill's `README.md` flag table.

## When NOT to use these skills

- **General coding tasks.** These skills are research-idea-flow specific. For a normal coding request, just code.
- **Brainstorming with no benchmark.** The ideation skill requires a named benchmark.
- **Already-implemented work.** Vetting is for pre-implementation gating; running it on shipped work is sunk-cost wasted compute.
- **Trivial changes (< 2 h implementation).** Skip vetting; just do it.

## Anti-patterns when working with these skills

- **Don't manufacture web-search results.** The vetting skill's Stage 2 and the ideation skill's multi-tier search both require live `WebSearch` queries with logged citations. Simulating them defeats the adversarial purpose.
- **Don't inflate steel-manned rebuttals.** A weak rebuttal is *diagnostic* — it means the idea is vulnerable. Don't pretend it's strong to "make the example look better."
- **Don't skip persona declaration.** Every vetting stage starts with an explicit persona-switch quote. The audit trail depends on it.
- **Don't mix the output trees.** `ideation-output/` is the ideation skill's territory; `vetting-output/` is vetting's. Cross-writes break the loose-coupling contract.

## What to do if a skill file gets too big

The Phase-1 cap was 8 KB per file; some files (especially `SKILL.md` after multiple phases) grew past that. If a file becomes hard to load:

1. Push detail into a referenced sub-file (`rules/`, `templates/`).
2. Replace inline content with `[link](./relative/path.md)` pointers.
3. Keep the controlled vocabulary and the hard rules inline — these must stay close to where they fire.

## Testing changes

There is no test suite. The closest thing to a regression check is:

1. Re-read the modified file's `## Hard rules` section (if any) — make sure your change doesn't violate one.
2. `grep` for the file's `name:` slug across the rest of the skill — any place that references it should still parse.
3. If you change a controlled-vocabulary word, search both skills for the old word and update every callsite.

For new significant features, hand-walk one of the `examples/` reports against the new behavior to confirm the example would still be valid.
