"""exp4 — idea 1: flow-matching invariance (replaces the per-pair MSE alignment).

SIGReg untouched (stock sliced Epps-Pulley). Joint minimization is legitimate here,
unlike exp3: both z_0 and z_1 are encoder outputs, and the degenerate
"collapse everything" solution is exactly what the SIGReg term prevents.
"""

from _common import base_parser, run
from _variants import LeJEPAFMInv


def main():
    p = base_parser("LeJEPA batch-7 exp4 (flow-matching invariance)")
    p.add_argument("--fm_sigma", type=float, default=0.01)
    args = p.parse_args()
    model = LeJEPAFMInv(
        encoder_name=args.backbone, lamb=args.lamb, n_slices=args.n_slices,
        n_points=17, projector_dim=args.proj_dim, drop_path_rate=args.drop_path_rate,
        fm_sigma=args.fm_sigma,
    )
    run(model, args, tag="exp4-fminv")


if __name__ == "__main__":
    main()
