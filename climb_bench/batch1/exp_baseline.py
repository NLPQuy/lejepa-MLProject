"""Batch-1 baseline — plain LeJEPA (sanity reference for all variants).

Usage (Kaggle offline):
    python exp_baseline.py --backbone vit_small_patch16_224 --max_epochs 400 \
        --batch_size 128 --num_workers 4 --data_local_path {DATA} \
        --checkpoint_dir {CKPT}/exp_baseline-vits --no_wandb
Smoke (CPU):
    python exp_baseline.py --accelerator cpu --num_gpus 1 --precision 32 \
        --max_steps 3 --batch_size 4 --num_workers 0 --data_local_path {DATA}
"""

from _common import base_parser, run
from stable_pretraining.methods.lejepa import LeJEPA


def main():
    args = base_parser("LeJEPA baseline (batch-1)").parse_args()
    model = LeJEPA(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        n_points=17,
        projector_dim=args.proj_dim,
    )
    run(model, args, tag="exp_baseline")


if __name__ == "__main__":
    main()
