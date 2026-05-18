---
name: pre-vet-checklist
description: Confirm inputs and load prior context before starting Step 2 (Parse ideas)
load-trigger: Step 1 of SKILL.md (every session)
---

# Pre-Vet Checklist

Confirm every item before launching the pipeline. Missing inputs → ASK USER; do not invent.

## Inputs
- [ ] **Ideas to vet** — file path resolved OR pasted text identified OR paper proposal identified
- [ ] **Benchmark name** confirmed (e.g., `MATH-500`)
- [ ] **Task / problem** confirmed — concrete problem framing being solved on that benchmark (e.g., `function-level Python code completion from docstring`). If parsing an ideation batch, lift this from the batch header. If pasted / paper proposal: ASK USER. Without a task, Stage 1 (Problem Framing) cannot run — STOP and ask.
- [ ] **Baseline** known: model + score on this task (if applicable to the user's goal)
- [ ] **Resource constraints**: compute / time / person-hours / deadline declared
- [ ] **Mode flags** parsed: `--climb-mode`, `--no-publish`, `--strict`, `--lenient`, `--resurrect`, `--given-toy`, `--given-result`

## Mandatory rule load
- [ ] [../rules/adversarial-mindset.md](../rules/adversarial-mindset.md) loaded (suppress LLM default agreeableness)

## Prior context (read but do NOT modify)
- [ ] [../_logs/_vetting_log.md](../_logs/_vetting_log.md) loaded — surface prior batches on this benchmark; note any open re-vet triggers
- [ ] [../_logs/_killed_ideas.md](../_logs/_killed_ideas.md) loaded — filter out attack angles already exhausted on prior batches (avoid re-attacking with the same evidence; user has already seen it)
- [ ] [../_logs/_passed_ideas.md](../_logs/_passed_ideas.md) loaded — identify FULL SEND ideas already shipped (avoid re-vetting an already-implemented idea unless `--re-vet-post-result`)
- [ ] [../_logs/_toy_queue.md](../_logs/_toy_queue.md) loaded — surface pending toys; if user passed `--given-toy <path>`, locate the matching toy entry

## Cross-skill context (if input is from ideation skill)
- [ ] `ideation-output/<bench>/_logs/_proposal_log.md` read — context for prior ideation batches
- [ ] `ideation-output/<bench>/_logs/_rejection_log.md` read — avoid re-attacking already-rejected angles
- [ ] Source batch file path validated and parseable

## Output paths prepared
- [ ] `vetting-output/<bench>/batch-<N>/` directory will be created at Step 2 (or `standalone-<YYYYMMDD-HHMM>/` for solo runs)
- [ ] `vetting-output/<bench>/_logs/` directory will be created at Step 6 if missing

If any required input is missing → ASK USER the minimum-needed clarifying question and wait. Do NOT proceed with placeholders.
