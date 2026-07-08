"""Batch-1 Idea 4 — Hypersphere-uniformity term complementing SIGReg.

loss = inv + lamb*sigreg + uniformity_gamma * uniformity(projections)
uniformity_gamma=0 reproduces the baseline (sanity check).

Usage (Kaggle offline):
    python exp4.py --backbone vit_small_patch16_224 --max_epochs 400 \
        --batch_size 128 --num_workers 4 --uniformity_gamma 0.5 \
        --data_local_path {DATA} --checkpoint_dir {CKPT}/exp4-uniformity-vits --no_wandb
"""

from _common import base_parser, run
from _variants import LeJEPAUniformity


def main():
    p = base_parser("LeJEPA + uniformity (batch-1 idea 4)")
    p.add_argument("--uniformity_gamma", type=float, default=0.5, help="0.0 = baseline")
    p.add_argument("--uniformity_t", type=float, default=2.0)
    args = p.parse_args()

    model = LeJEPAUniformity(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        n_points=17,
        projector_dim=args.proj_dim,
        uniformity_gamma=args.uniformity_gamma,
        uniformity_t=args.uniformity_t,
    )
    run(model, args, tag="exp4-uniformity")


if __name__ == "__main__":
    main()
