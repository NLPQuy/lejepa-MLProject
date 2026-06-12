"""Batch-2 Idea 6 — convolutional stem for ViT-S."""

from _common import base_parser, run
from _variants import apply_conv_stem, build_lejepa


def main():
    p = base_parser("LeJEPA + conv stem (batch-2 idea 6)")
    p.add_argument("--conv_stem", action="store_true", help="off = baseline")
    args = p.parse_args()
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    if args.conv_stem:
        apply_conv_stem(model)
    run(model, args, tag="exp6-convstem")


if __name__ == "__main__":
    main()
