"""Batch-1 Idea 7 — Energy-preserving DynTanh normalization in the projector.

Replaces the projector's BatchNorm with DynTanh (gamma*tanh(alpha*x)+beta).
No off-switch to baseline (architectural swap); compare against exp_baseline.

Usage (Kaggle offline):
    python exp7.py --backbone vit_small_patch16_224 --max_epochs 400 \
        --batch_size 128 --num_workers 4 --dyntanh_alpha 0.5 \
        --data_local_path {DATA} --checkpoint_dir {CKPT}/exp7-dyntanh-vits --no_wandb
"""

from _common import base_parser, run
from _variants import LeJEPADynTanhProj


def main():
    p = base_parser("LeJEPA + DynTanh projector (batch-1 idea 7)")
    p.add_argument("--dyntanh_alpha", type=float, default=0.5, help="initial DynTanh alpha")
    p.add_argument("--proj_hidden", type=int, default=2048)
    args = p.parse_args()

    model = LeJEPADynTanhProj(
        encoder_name=args.backbone,
        lamb=args.lamb,
        n_slices=args.n_slices,
        n_points=17,
        projector_dim=args.proj_dim,
        projector_hidden_dim=args.proj_hidden,
        dyntanh_alpha=args.dyntanh_alpha,
    )
    run(model, args, tag="exp7-dyntanh")


if __name__ == "__main__":
    main()
