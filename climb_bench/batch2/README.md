# LeJEPA Batch 2

Batch-local optimizer and architecture experiments for Imagenette. Official
`stable_pretraining` sources are not modified; new mechanisms live in
`_common.py`, `_variants.py`, and `_vendor/`.

## Experiments

- `exp_baseline.py`: stock LeJEPA, AdamW + warmup cosine.
- `exp1.py`: SAM, enabled with `--sam_rho 0.05`; `--sam_rho 0` is baseline.
- `exp2.py`: QK-Norm, enabled with `--qk_norm`; flag absent is baseline.
- `exp3.py`: Muon optimizer for 2-D weights with AdamW fallback.
- `exp4.py`: vendored Schedule-Free AdamW; validation switches to averaged iterate.
- `exp5.py`: PCGrad between `inv_loss` and `lambda * sigreg_loss`.
- `exp6.py`: conv stem, enabled with `--conv_stem`; flag absent is baseline.
- `exp7.py`: SWA tail averaging; validation logs averaged-weight use when active.
- `exp8.py`: LLRD, enabled with `--llrd_gamma 0.75`; `0` is baseline.
- `exp9.py`: linear stochastic-depth schedule.
- `exp10.py`: deep supervision; `--deepsup_mu 0` is baseline.

## Kaggle Offline

Use `run-batch2.py`. It sets `PYTHONPATH` to both `stable-pretraining` and this
batch directory, sets `SPT_LIGHT_IMPORT=0`, and stubs `requests_cache` when the
system package is absent. Commands are double-commented for jupytext safety.

## Vendored Sources

- `_vendor/muon.py`: minimal Muon reimplementation from KellerJordan/Muon, MIT.
- `_vendor/schedulefree.py`: minimal AdamWScheduleFree reimplementation from
  facebookresearch/schedule_free, MIT.
- `_vendor/sam.py`: adapted from davda54/sam, MIT.

## Local Smoke

The local full data pipeline is intentionally not required here. Smoke at the
model/optimizer level in the `lejepa` conda env, for example:

```bash
conda run -n lejepa python -m py_compile climb_bench/batch2/*.py climb_bench/batch2/_vendor/*.py
```

For experiment parity, compare each off-switch against `exp_baseline.py` on the
same seed and a short synthetic/model-level run before launching 400 epochs.
