"""Batch-2 Idea 1 — SAM sharpness-aware minimization."""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    args = base_parser("LeJEPA + SAM (batch-2 idea 1)").parse_args()
    if args.sam_rho == 0.0:
        args.optimizer = "adamw"
    else:
        args.optimizer = "sam"
    args.precision = "bf16-mixed"  # manual SAM steps: avoid the fp16 GradScaler
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp1-sam")


if __name__ == "__main__":
    main()
