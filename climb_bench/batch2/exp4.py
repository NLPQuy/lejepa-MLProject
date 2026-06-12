"""Batch-2 Idea 4 — Schedule-Free AdamW."""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    args = base_parser("LeJEPA + Schedule-Free AdamW (batch-2 idea 4)").parse_args()
    args.optimizer = "schedulefree"
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp4-schedulefree")


if __name__ == "__main__":
    main()
