"""exp3 — idea 7: FM-SIGReg (transport-based marginal-shape regularizer).

Ships the two-player form (--fm_form b) on the OT path with the KL surrogate
averaged over t in [0.3, 0.7]. Phase 0 (tracker/batch7-analysis.md) showed the
t-band IS the mechanism: [0.1,0.3] diverges (1/t noise), [0.5,0.9] collapses
(p_t -> N(0,I), no signal), [0.3,0.7] converges to ep 0.59.

--fm_form a reproduces the addendum's as-written spec, which FAILS Phase 0. Kept
as the falsification arm, not as a shipping default.
"""

from _common import base_parser, build_sigreg, run
from _variants import build_lejepa


def main():
    p = base_parser("LeJEPA batch-7 exp3 (FM-SIGReg)")
    p.set_defaults(sigreg="fm", fm_form="b", fm_path="ot")
    args = p.parse_args()
    model = build_lejepa(
        encoder_name=args.backbone, lamb=args.lamb, n_slices=args.n_slices,
        projector_dim=args.proj_dim, drop_path_rate=args.drop_path_rate,
    )
    model.sigreg = build_sigreg(args)
    run(model, args, tag=f"exp3-fmsigreg-{args.fm_form}{args.fm_path}")


if __name__ == "__main__":
    main()
