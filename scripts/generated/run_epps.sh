#!/usr/bin/env bash
set -euo pipefail

# epps: Epps-Pulley Parameters
# status: ready
# configs: 27
HYDRA_FULL_ERROR=1 python scripts/train_lejepa_ablation.py --multirun \
  dataset_name=inet100 \
  max_epochs=50 \
  backbone=vit_large_patch14_224 \
  batch_size=512 \
  bstat_name=epps_pulley \
  bstat_lambda=0.05 \
  embedding_dim=512 \
  projector_dim=512 \
  projector_arch=MLP \
  lr=0.0005 \
  weight_decay=0.05 \
  teacher_student=false \
  n_views=8 \
  n_global_views=2 \
  drop_path_rate=0.1 \
  multi_crop=true \
  resolution=238 \
  local_resolution=98 \
  patch_size=14 \
  patch_mask_ratio=0.3 \
  autostop=false \
  bstat_num_slices=512,1024,4096 \
  bstat_t_max=1,3,5 \
  bstat_n_points=5,17,41
