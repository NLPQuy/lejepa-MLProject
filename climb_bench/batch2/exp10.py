"""Batch-2 Idea 10 — deep supervision on intermediate ViT layers."""

from _common import base_parser, run
from _variants import LeJEPADeepSup


def main():
    p = base_parser("LeJEPA + deep supervision (batch-2 idea 10)")
    p.add_argument("--deepsup_mu", type=float, default=0.0, help="0 = baseline")
    p.add_argument("--deepsup_layers", default="6,9")
    args = p.parse_args()
    layers = [int(x) for x in args.deepsup_layers.split(",") if x]
    model = LeJEPADeepSup(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        n_points=17,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
        deepsup_mu=args.deepsup_mu,
        deepsup_layers=layers,
    )
    run(model, args, tag="exp10-deepsup")


if __name__ == "__main__":
    main()
