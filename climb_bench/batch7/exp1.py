"""exp1 — idea 2: Hyvarinen score matching, rewritten as a two-player KL surrogate.

The encoder descends KL(P_z || N(0,I)); the score net descends Hyvarinen ISM on a
detached z. See plan-batch-7.md 3.1 for why the original joint-minimization form
drove the encoder the wrong way, and tracker/batch7-analysis.md for the Phase-0
measurement (ep 51 -> 0.48, CONVERGE).
"""

from _common import base_parser, build_sigreg, run
from _variants import build_lejepa


def main():
    p = base_parser("LeJEPA batch-7 exp1 (KL score SIGReg)")
    p.set_defaults(sigreg="klscore")
    args = p.parse_args()
    model = build_lejepa(
        encoder_name=args.backbone, lamb=args.lamb, n_slices=args.n_slices,
        projector_dim=args.proj_dim, drop_path_rate=args.drop_path_rate,
    )
    model.sigreg = build_sigreg(args)
    run(model, args, tag="exp1-klscore")


if __name__ == "__main__":
    main()
