# Idea 5 Vetting — Kernelize SIGReg projections (RKHS slicing)
**Source**: batch-1.md · Pattern P2 · Tier 2 · Scope enhance-existing
**Claim**: +0.5 / +2.0 / +4.0 pp, Feas 4/5, Effort M.

---

## Stage 1 — Problem Framing
> Persona: **Advisor**.

**Attack**: "What concrete *nonlinear* deviation from N(0,I) are you worried about? Without naming the failure mode you're targeting, this is 'kernelise because kernelising is cool'."
- *Steel-man rebuttal*: Random projections of post-encoder embeddings tend to be marginally Gaussian by CLT regardless of the joint distribution. So linear-slice SIGReg can be satisfied while the joint still has e.g. clustered modes that hurt linear probe. Kernel-SIGReg checks higher-order structure (cf. MMD with Gaussian kernel detects all moments).
- *Response*: ⚠️ **WEAKENED**. The CLT-shielding-linear-marginals argument is real but the magnitude is unknown empirically — could be tiny.

**Stage verdict**: ⚠️ **WARN**.

---

## Stage 2 — Prior Work Attack
**Attack 1**: "Kernel VICReg (Adouane 2025, arXiv:2509.07289) already kernelised VICReg's variance term. Your idea is the same trick on SIGReg."
- *Rebuttal*: True — that's the explicit citation. Climb-mode: this *is* the transfer.
- *Response*: ✅ **DEFLECTED**.

**Attack 2**: "Kernel mean embedding-based normality tests (Gretton MMD 2012) are the actual antecedent. RFF→sliced-Epps is just an MMD approximation in disguise."
- *Rebuttal*: Partially. The slicing keeps SIGReg's O(N·M) cost; MMD is O(N²). The combination of (RFF lift) + (sliced univariate test) is not the same as MMD computationally.
- *Response*: ⚠️ **WEAKENED**.

**Stage verdict**: ⚠️ **WARN**.

---

## Stage 4 — Theory (lite)
**Attack**: "Cramér-Wold guarantees apply to the *original* random variable Z. Once you apply a nonlinear φ, you're targeting Gaussianity of φ(Z), which is *not* the same as isotropic Gaussianity of Z. The LeJEPA paper's downstream-risk theorem (Z ~ N(0,I) optimises probe risk) does not transfer."
- *Steel-man rebuttal*: True. You lose the theoretical guarantee. The empirical claim becomes: even without the guarantee, kernel-SIGReg may be a better *practical* normalizer because it's a stricter normality test. But you've traded theory for empirical guessing — that's the whole point of LeJEPA you're undoing.
- *Response*: ❌ **UNREBUTTED**. This *directly attacks the LeJEPA value prop*.

**Rebuttal-cycle summary**: 0 DEFLECTED · 0 WEAKENED · 1 UNREBUTTED.
**Stage verdict**: ❌ **FAIL** (downgraded by UNREBUTTED).

---

## Stage 5 — Feasibility
- M effort, σ heuristic well-known. ✅ **PASS**.

---

## Stage 6 — Killer Baseline ⚔️
**Attack**: "The killer baseline is: keep linear SIGReg + add a *second* normality test (Anderson-Darling, already in `lejepa.univariate`) on linear slices. Combining two univariate tests catches more failure modes than swapping to RFF and is theoretically clean."
- *Steel-man rebuttal*: Stacking univariate tests preserves the Cramér-Wold guarantee and is free compute-wise. RFF-SIGReg only wins if there is a deviation that *no* linear univariate test catches but some kernelised one does. That's a much narrower claim.
- *Response*: ❌ **UNREBUTTED**. The "stack two univariate tests" baseline is strictly dominant in theory and roughly free in compute.

**Rebuttal-cycle summary**: 0 DEFLECTED · 0 WEAKENED · 1 UNREBUTTED.
**Stage verdict**: ❌ **FAIL**.

---

## Stage 8 — Decision Gate

Tally: 2 FAIL (Stage 4, Stage 6) · 2 WARN (Stage 1, Stage 2) · rest PASS.

Per `decision-logic.md` rule 8 (2 FAIL → REFRAME or KILL).

**Verdict**: ☠️ **KILL** 🟡

**Rationale**: The theory FAIL is the killing blow — kernel-SIGReg explicitly breaks the LeJEPA Cramér-Wold guarantee (its main selling point) and the cheaper "stack two univariate tests" baseline dominates. There is no reframing that fixes both.

**Salvageable substrate**: the *combine-multiple-univariate-tests* baseline that emerged in Stage 6 is interesting and free — propose it as a **new idea** (Idea 7) in the next batch.

---

## Cycle audit
Total cycles: 5. 1 DEFLECTED · 2 WEAKENED · 2 UNREBUTTED.
