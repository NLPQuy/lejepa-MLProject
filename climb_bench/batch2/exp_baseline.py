"""Batch-2 baseline — plain LeJEPA with AdamW + cosine."""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    args = base_parser("LeJEPA baseline (batch-2)").parse_args()
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp_baseline")


if __name__ == "__main__":
    main()
