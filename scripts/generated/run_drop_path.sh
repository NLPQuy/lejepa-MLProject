#!/usr/bin/env bash
set -euo pipefail

# drop_path: Drop Path Rate
# status: ready
# configs: 5
HYDRA_FULL_ERROR=1 python3 scripts/train_lejepa_ablation.py --multirun \
  dataset_name=inet100 \
  max_epochs=50 \
  backbone=vit_large_patch14_224 \
  batch_size=512 \
  bstat_name=epps_pulley \
  bstat_num_slices=1024 \
  bstat_t_max=3 \
  bstat_n_points=17 \
  bstat_lambda=0.05 \
  embedding_dim=512 \
  projector_dim=512 \
  projector_arch=MLP \
  lr=0.0005 \
  weight_decay=0.05 \
  teacher_student=false \
  n_views=8 \
  n_global_views=2 \
  multi_crop=true \
  resolution=238 \
  local_resolution=98 \
  patch_size=14 \
  patch_mask_ratio=0.3 \
  autostop=false \
  drop_path_rate=0,0.05,0.1,0.2,0.4
