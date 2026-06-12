"""Batch-2 Idea 7 — SWA tail averaging."""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    args = base_parser("LeJEPA + SWA (batch-2 idea 7)").parse_args()
    args.swa = True
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp7-swa")


if __name__ == "__main__":
    main()
