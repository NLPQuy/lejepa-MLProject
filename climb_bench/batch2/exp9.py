"""Batch-2 Idea 9 — progressive stochastic-depth schedule."""

from _common import base_parser, run
from _variants import build_lejepa


def main():
    args = base_parser("LeJEPA + stochastic-depth schedule (batch-2 idea 9)").parse_args()
    args.sd_schedule = "linear"
    model = build_lejepa(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        projector_dim=args.proj_dim,
        drop_path_rate=args.drop_path_rate,
    )
    run(model, args, tag="exp9-sdschedule")


if __name__ == "__main__":
    main()
