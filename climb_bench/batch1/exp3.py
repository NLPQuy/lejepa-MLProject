"""Batch-1 Idea 3 — Coding-rate (log-det) volume term complementing SIGReg.

loss = inv + lamb*sigreg + coding_beta * (-coding_rate(projections))
coding_beta=0 reproduces the baseline (sanity check).

Usage (Kaggle offline):
    python exp3.py --backbone vit_small_patch16_224 --max_epochs 400 \
        --batch_size 128 --num_workers 4 --coding_beta 0.01 \
        --data_local_path {DATA} --checkpoint_dir {CKPT}/exp3-codingrate-vits --no_wandb
"""

from _common import base_parser, run
from _variants import LeJEPACodingRate


def main():
    p = base_parser("LeJEPA + coding-rate (batch-1 idea 3)")
    p.add_argument("--coding_beta", type=float, default=0.01, help="0.0 = baseline")
    p.add_argument("--coding_eps", type=float, default=0.5)
    args = p.parse_args()

    model = LeJEPACodingRate(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        n_points=17,
        projector_dim=args.proj_dim,
        coding_beta=args.coding_beta,
        coding_eps=args.coding_eps,
    )
    run(model, args, tag="exp3-codingrate")


if __name__ == "__main__":
    main()
