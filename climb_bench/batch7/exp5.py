"""exp5 — idea 5: neural-collapse simplex-ETF prototypes.

The prototypes are the EXACT closed-form simplex ETF and are FROZEN (a buffer, not a
Parameter), per refs/Neural-Collapse. That deletes the L_ETF penalty and the alpha
weight the ideation doc proposed, leaving one term and one weight (--etf_w).
See plan-batch-7.md 3.3.

Prior-art gate CLEARED (2026-07-17): no Cramer-Wold <-> ETF equivalence exists.
SIGReg constrains the MARGINAL law; ETF is about CLASS-CONDITIONAL means. P_z=N(0,I)
holds perfectly with all class means stacked at the origin, so SIGReg genuinely does
not constrain cluster geometry.

Falsification (batch-7.md Idea 5): 3-arm baseline / +L_NC / L_NC-only, plus the
class-mean cosine check on validation -> should approach -1/9 for Imagenette's 10
classes (refs/Neural-Collapse validate_NC.py::compute_ETF).
"""

from _common import base_parser, run
from _variants import LeJEPAETF


def main():
    p = base_parser("LeJEPA batch-7 exp5 (simplex-ETF prototypes)")
    p.add_argument("--etf_w", type=float, default=0.1, help="0 => exact baseline")
    p.add_argument("--etf_k", type=int, default=20)
    p.add_argument("--etf_warmup_steps", type=int, default=0)
    p.add_argument("--sinkhorn_eps", type=float, default=0.05)
    args = p.parse_args()
    model = LeJEPAETF(
        encoder_name=args.backbone, lamb=args.lamb, n_slices=args.n_slices,
        n_points=17, projector_dim=args.proj_dim, drop_path_rate=args.drop_path_rate,
        etf_w=args.etf_w, etf_k=args.etf_k,
        etf_warmup_steps=args.etf_warmup_steps, sinkhorn_eps=args.sinkhorn_eps,
    )
    run(model, args, tag="exp5-etf")


if __name__ == "__main__":
    main()
