"""exp2 — idea 3: adversarial max-sliced SIGReg (game-theoretic worst-case slicing).

Phase 0 (tracker/batch7-analysis.md): works but ~50-100x slower than the baseline
statistic, which undercuts the idea's "M=1 suffices / 1000x cheaper" claim --
per-step cost falls but step count rises. The M=1-RANDOM control arm is therefore
mandatory, not optional:

    exp2.py --sigreg adversarial          # M=1 adversarial
    exp_baseline.py --n_slices 1          # M=1 random  <- the control that matters
    exp_baseline.py                       # M=1024 random
"""

from _common import base_parser, build_sigreg, run
from _variants import build_lejepa


def main():
    p = base_parser("LeJEPA batch-7 exp2 (adversarial max-sliced SIGReg)")
    p.set_defaults(sigreg="adversarial", aux_lr_mult=10.0)  # 10x per batch-7.md Idea 3
    args = p.parse_args()
    model = build_lejepa(
        encoder_name=args.backbone, lamb=args.lamb, n_slices=args.n_slices,
        projector_dim=args.proj_dim, drop_path_rate=args.drop_path_rate,
    )
    model.sigreg = build_sigreg(args)
    run(model, args, tag="exp2-adversarial")


if __name__ == "__main__":
    main()
