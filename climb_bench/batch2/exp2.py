"""Batch-2 Idea 2 — QK-Norm in ViT attention."""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    p = base_parser("LeJEPA + QK-Norm (batch-2 idea 2)")
    p.add_argument("--qk_norm", action="store_true", help="off = baseline")
    args = p.parse_args()
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        qk_norm=args.qk_norm,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp2-qknorm")


if __name__ == "__main__":
    main()
