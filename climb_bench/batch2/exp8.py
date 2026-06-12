"""Batch-2 Idea 8 — layer-wise learning-rate decay."""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    args = base_parser("LeJEPA + LLRD (batch-2 idea 8)").parse_args()
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp8-llrd")


if __name__ == "__main__":
    main()
