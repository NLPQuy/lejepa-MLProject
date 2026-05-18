---
name: rebuttal-format-template
description: Block format for one attack → rebuttal → persona-response cycle
load-trigger: Stages 1-7 emit one block per attack
---

# Rebuttal Block Format

Use this block for **every attack** that gets a full rebuttal cycle (max 3 per stage; see [../rules/rebuttal-loop.md](../rules/rebuttal-loop.md)).

```markdown
**Attack <K>**: "<attack text — must cite a specific paper / metric / baseline / mechanism>"

**Steel-manned rebuttal** (Round 1):
> <The strongest possible counter-argument the idea author would give.
>  Cite papers; use math or logic, not handwaving; address the attack's specific claim,
>  not a paraphrase. If you cannot write a strong steel-man, mark UNREBUTTED.>

**Source**: auto-steelman   <-- or "user" if the user provided this rebuttal

**Persona response** (Round 1):
> <Does the persona accept the rebuttal? Why or why not?
>  What additional evidence would flip WEAKENED → DEFLECTED?
>  Be specific — name the ablation, the missing seed count, the missing citation.>

**Status after Round 1**: ✅ DEFLECTED  /  ⚠️ WEAKENED (still concern)  /  ❌ UNREBUTTED (attack stands)

<!-- Round 2 is OPTIONAL. Include only if Round 1 ended WEAKENED and a refinement is genuinely possible.
     Round 3 is FORBIDDEN. -->

**Refined rebuttal** (Round 2, optional):
> <Address the persona's Round-1 concern directly. Same steel-man rules apply.>

**Persona response** (Round 2):
> <Final evaluation. Persona must commit — no further rounds allowed.>

**Status after Round 2**: ✅ DEFLECTED  /  ⚠️ WEAKENED  /  ❌ UNREBUTTED

**Final status**: ✅ DEFLECTED  /  ⚠️ WEAKENED  /  ❌ UNREBUTTED   <-- this is the value Stage 8 reads
```

## Hard rules

- **Status vocabulary is fixed**: exactly `DEFLECTED`, `WEAKENED`, or `UNREBUTTED`. No free-form verdicts.
- **Round counter is required.** If a block lacks the explicit `Round 1` / `Round 2` labels, the budget rule was not enforced.
- **`Source` field is required.** Either `auto-steelman` (the skill wrote the rebuttal) or `user` (the user provided it via interjection per `rebuttal-loop.md §User-input`).
- **No Round 3.** If a block contains a Round 3 anywhere, re-run the stage.
- **`Final status` must equal `Status after Round 2`** when Round 2 exists, otherwise equal `Status after Round 1`. Stage 8 reads `Final status`.
- **Additional attacks beyond the 3rd get a 1-line entry** in the stage output (not a full rebuttal block). Format:
  > `Additional attack: "<text>" — Status: <one-of-three>, no rebuttal cycle (budget exhausted).`
