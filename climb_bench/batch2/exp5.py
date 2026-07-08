"""Batch-2 Idea 5 — PCGrad between invariance and SIGReg."""

from _common import base_parser, run
from _variants import LeJEPAPCGrad


def main():
    p = base_parser("LeJEPA + PCGrad (batch-2 idea 5)")
    p.set_defaults(pcgrad=True)
    args = p.parse_args()
    args.precision = "bf16-mixed"  # manual PCGrad grad-surgery: avoid the fp16 GradScaler
    model = LeJEPAPCGrad(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        n_points=17,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp5-pcgrad")


if __name__ == "__main__":
    main()
