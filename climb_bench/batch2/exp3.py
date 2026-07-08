"""Batch-2 Idea 3 — Muon optimizer for matrix weights."""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    args = base_parser("LeJEPA + Muon (batch-2 idea 3)").parse_args()
    args.optimizer = "muon"
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp3-muon")


if __name__ == "__main__":
    main()
