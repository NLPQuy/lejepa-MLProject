"""Batch-7 baseline — stock LeJEPA (sliced Epps-Pulley SIGReg, MSE invariance).

Reference point for every other exp. All batch-7 knobs default to off, so this
must reproduce the batch-1/2 baseline.
"""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    args = base_parser("LeJEPA baseline (batch-7)").parse_args()
    model = build_lejepa(
        encoder_name=args.backbone, lamb=args.lamb, n_slices=args.n_slices,
        projector_dim=args.proj_dim, drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp_baseline")


if __name__ == "__main__":
    main()
