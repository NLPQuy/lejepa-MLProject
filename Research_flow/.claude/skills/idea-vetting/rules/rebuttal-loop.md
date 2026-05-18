---
name: rebuttal-loop
description: How attack → steel-manned rebuttal → persona evaluation works in every stage
load-trigger: Stages 1-7 load this when processing attacks
---

# Rebuttal Loop

Real research has dialogue: advisor attacks → student rebuts → advisor refines or accepts. Single-shot attack loses nuance. Every attack in every stage runs through this loop.

## Mechanism (per attack)

```
1. Persona issues an attack (cited, specific — see ../rules/adversarial-mindset.md).
2. Skill generates a steel-manned rebuttal (the strongest possible counter the idea-author would give).
3. Persona evaluates the rebuttal:
     - Convincing → DEFLECTED → attack does not land.
     - Partial → WEAKENED → attack lands but rebuttal limits the damage.
     - Unconvincing → UNREBUTTED → attack lands fully.
4. If WEAKENED, the persona may issue ONE refined follow-up (Round 2). Then stop.
```

The output of each cycle uses [../templates/rebuttal-format.md](../templates/rebuttal-format.md).

## Steel-man rule (HARD)

The rebuttal MUST be the **strongest possible argument the idea author would give** — not a token defense. Concretely:
- Cite specific papers / equations / experiments where applicable.
- Use math or logic, not handwaving ("it should work because the loss decreases" is hand-waving; "the gradient norm of the proposed regularizer is bounded by `c·||W||₂`, see Eq. 3 in `<paper>`" is steel-manned).
- Address the attack's specific claim, not a paraphrase.
- If you cannot write a strong steel-man, that is **diagnostic** — the idea is genuinely vulnerable on that attack, mark UNREBUTTED.

A weak rebuttal is information about the idea, not a failure of the rebuttal-writer. Do not invent strength that is not there.

## Budget (HARD caps)

- **Max 2 rebuttal rounds per attack.** Round 1 = first rebuttal + first persona response. Round 2 = refined rebuttal + final persona response. No Round 3.
- **Max 3 attacks per stage** get the full rebuttal treatment. Additional attacks (≥ 4) are listed in the stage output as "additional attacks" with a 1-line note but no rebuttal cycle.
- **Max 16 rebuttal cycles total per idea** (≈ 2 per stage × 8 stages average). Track this in the per-idea report; if you hit the cap, prioritize Stages 2 and 6.

## User-input rebuttal (Section 7.6)

The user may interject at any point with their own rebuttal:

> User: "For Attack 3, my rebuttal is: `<text>`"

When this happens:
1. Treat the user's text as the new steel-manned rebuttal, replacing the auto-generated one.
2. Persona re-evaluates against the user's argument.
3. Persona may issue a follow-up (counts toward the 2-round budget for that attack).
4. Update the attack status in the stage output: ✅ / ⚠️ / ❌.
5. Note in the rebuttal block: `Source: user` (vs `Source: auto-steelman`).

This makes vetting collaborative rather than lecture-style. The user's rebuttal does NOT auto-deflect — the persona still evaluates honestly.

## Failed rebuttal handling

When an attack ends UNREBUTTED:
- Note the attack and the failed rebuttal in the stage output.
- **Downgrade the stage verdict by one step** per `../rules/decision-logic.md §UNREBUTTED downgrade rule`:
  - Stage was on track for PASS → demote to WARN.
  - Stage was on track for WARN → demote to FAIL.
  - Stage was already FAIL → unchanged.
- Multiple UNREBUTTED attacks in one stage compound: 2+ UNREBUTTED → stage cannot exceed WARN; 3+ UNREBUTTED → stage = FAIL regardless of the rest.

## Round-counter discipline

Every rebuttal block records its round number explicitly. If a stage's output shows Round 3 anywhere, the budget rule was violated — re-run the stage with proper Round-1/Round-2 discipline.
