"""exp7 — idea 4: RL-learned augmentation policy (REINFORCE on crop parameters).

Heaviest and most fragile arm; built last on purpose.

Two spec deviations, both documented in _variants.py::LeJEPARLCrop:
  * the policy crops on GPU inside forward (transforms run in CPU workers, so the
    "data/transform" surface the ideation doc assumed is not viable);
  * --rl_reward resolves a sign contradiction in the spec. batch-7.md Idea 4 step 3
    rewards EASY crops; its own rationale and the arXiv:2310.03940 evidence it cites
    want HARD crops. Default follows the rationale.

A/B set (plan 3.5) is random crops + b5 saliency -- NOT SelfAugment: refs/selfaugment
turns out to be Ray/HyperOpt offline search over 5 k-fold MoCo checkpoints, an order
of magnitude beyond this batch's budget.

Guards (mandatory before any 400-ep commit) -- watch fit/rl_entropy and fit/rl_reward:
  * entropy must DECREASE from the uniform-prior value. Flat => not learning, reject.
  * mean reward must stay positive and rise. ~0 => reward too noisy, reject.
"""

from _common import base_parser, run
from _variants import LeJEPARLCrop


def main():
    p = base_parser("LeJEPA batch-7 exp7 (RL crop policy)")
    p.add_argument("--rl_n_crops", type=int, default=4)
    p.add_argument("--rl_w", type=float, default=1.0, help="0 => no policy update")
    p.add_argument("--rl_entropy_beta", type=float, default=0.01)
    p.add_argument("--rl_reward", choices=["hard", "easy"], default="hard")
    p.add_argument("--rl_warmup_steps", type=int, default=0)
    args = p.parse_args()
    model = LeJEPARLCrop(
        encoder_name=args.backbone, lamb=args.lamb, n_slices=args.n_slices,
        n_points=17, projector_dim=args.proj_dim, drop_path_rate=args.drop_path_rate,
        rl_n_crops=args.rl_n_crops, rl_w=args.rl_w,
        rl_entropy_beta=args.rl_entropy_beta, rl_reward=args.rl_reward,
        rl_warmup_steps=args.rl_warmup_steps,
    )
    run(model, args, tag=f"exp7-rlcrop-{args.rl_reward}")


if __name__ == "__main__":
    main()
