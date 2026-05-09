#!/usr/bin/env python
"""Smoke test: run 50 training steps to verify no crash/OOM."""
import os
os.environ["LEJEPA_SMOKE"] = "1"

import lightning.pytorch as pl

_orig = pl.Trainer.__init__

def _patched(self, *a, **kw):
    kw["limit_train_batches"] = 50
    kw["limit_val_batches"] = 0
    kw["max_epochs"] = 1
    # Remove ModelCheckpoint from callbacks to allow enable_checkpointing=False
    if "callbacks" in kw:
        kw["callbacks"] = [c for c in kw["callbacks"] 
                          if not isinstance(c, pl.callbacks.ModelCheckpoint)]
    kw["enable_checkpointing"] = False
    _orig(self, *a, **kw)

pl.Trainer.__init__ = _patched

import train_eval_vit_b as T
T.run_pretraining()
