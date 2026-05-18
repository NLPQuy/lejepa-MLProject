# Prompts for Executing the LeJEPA Ablation Coding Plan

File này chứa các prompt có thể copy trực tiếp cho một coding model để thực thi `scripts/ablation_code_plan.md` theo từng giai đoạn.

Nguyên tắc khi dùng:

- Chạy từng prompt một, theo thứ tự.
- Mỗi prompt đều yêu cầu model đọc đúng phần tương ứng trong `scripts/ablation_code_plan.md`; không cần đọc lại toàn bộ plan trong session mới.
- Sau mỗi prompt, yêu cầu model kiểm tra `git diff` và chạy verification được nêu trong prompt.
- Không dùng prompt phase sau nếu phase trước chưa ổn.
- Nếu model gặp file/entrypoint không tồn tại, nó phải dừng và cập nhật plan thay vì tự bịa pipeline mới.
- Ưu tiên code nhỏ, kiểm thử được, không rewrite training framework.

---

## Prompt 0 — Repo Orientation

```text
Bạn đang làm trong repo LeJEPA. Trước khi code, hãy đọc các file sau:

- AGENTS.md
- scripts/ablation_code_plan.md
- scripts/ablation_plan.md
- stable-pretraining/stable_pretraining/methods/lejepa.py
- stable-pretraining/stable_pretraining/tests/integration/test_lejepa_inet10.py

Mục tiêu của lượt này chỉ là orientation, không sửa file.

Hãy trả lời ngắn:

1. Ablation pipeline hiện đang thiếu entrypoint nào?
2. Những knobs nào đã được LeJEPA hỗ trợ sẵn?
3. Những knobs nào cần sửa model?
4. Phase đầu nên code file nào trước?

Không viết code trong lượt này.
```

---

## Prompt 1 — Implement Ablation Spec Renderer Skeleton

```text
Trước khi làm, hãy đọc phần Phase 1 trong scripts/ablation_code_plan.md và bám sát phần đó.

Hãy thực thi Phase 1 trong scripts/ablation_code_plan.md.

Mục tiêu:

- Tạo ablation spec renderer skeleton.
- Chưa sửa stable-pretraining.
- Chưa tạo training script.
- Chưa chạy GPU.

Tạo các file:

- scripts/ablations.py
- scripts/ablations/__init__.py
- scripts/ablations/common.py
- scripts/ablations/specs.py
- scripts/ablations/commands.py

Yêu cầu:

1. Dùng argparse, không thêm dependency mới.
2. Định nghĩa dataclass AblationSpec, CommandOptions, RenderedCommand.
3. Port toàn bộ ablations từ scripts/ablation_plan.md vào specs.py.
4. Có BASE_OVERRIDES chung.
5. Support 2 kiểu sweep:
   - cartesian grid
   - explicit cases cho views ablation
6. CLI support:
   - python scripts/ablations.py list
   - python scripts/ablations.py show <key>
   - python scripts/ablations.py render <key>
   - python scripts/ablations.py render all
7. Render command tạm thời target:
   python scripts/train_lejepa_ablation.py --multirun ...
   dù script này chưa tồn tại.
8. Mỗi spec phải có status:
   - ready
   - needs_model_support
   - needs_config_support
   - blocked
9. Renderer phải in warning nếu spec chưa ready.
10. Không tạo generated shell scripts trong phase này.

Verification:

Chạy:

python scripts/ablations.py list
python scripts/ablations.py show epps
python scripts/ablations.py render epps
python scripts/ablations.py render views
python scripts/ablations.py render all

Sau đó báo lại:

- file đã tạo
- output chính của các command
- số configs của từng ablation
- bất kỳ limitation còn lại
```

---

## Prompt 2 — Add Write Scripts Command

```text
Trước khi làm, hãy đọc các phần Phase 1, script rendering, và generated scripts trong scripts/ablation_code_plan.md.

Tiếp tục từ Prompt 1. Hãy mở rộng ablation renderer.

Mục tiêu:

- Thêm khả năng ghi shell scripts từ specs.
- Không sửa model/training pipeline.

Yêu cầu:

1. Thêm command:
   python scripts/ablations.py write-scripts
2. Thêm options:
   --output scripts/generated
   --ready-only
   --force
3. Generated scripts có dạng:
   scripts/generated/run_<ablation_key>.sh
4. Script bắt đầu bằng:
   #!/usr/bin/env bash
   set -euo pipefail
5. Nếu file tồn tại và không có --force, không overwrite.
6. Với --ready-only, bỏ qua spec chưa ready.
7. Với spec explicit cases, ghi nhiều command tuần tự trong cùng file.
8. Không chạy generated scripts.

Verification:

python scripts/ablations.py write-scripts --output /tmp/lejepa_ablation_scripts --ready-only --force
ls /tmp/lejepa_ablation_scripts
sed -n '1,120p' /tmp/lejepa_ablation_scripts/run_epps.sh

Báo lại diff và kết quả verification.
```

---

## Prompt 3 — Create Minimal Training Entrypoint

```text
Trước khi làm, hãy đọc phần Phase 2 và Phase 3 trong scripts/ablation_code_plan.md.

Hãy thực thi Phase 2/3 trong scripts/ablation_code_plan.md: tạo training entrypoint tối thiểu.

Mục tiêu:

- Tạo scripts/train_lejepa_ablation.py chạy được smoke nhỏ.
- Reuse stable-pretraining components.
- Chưa implement các model knobs phức tạp.

Trước khi code, đọc:

- stable-pretraining/stable_pretraining/tests/integration/test_lejepa_inet10.py
- stable-pretraining/stable_pretraining/methods/lejepa.py
- stable-pretraining/stable_pretraining/data/transforms.py
- stable-pretraining/stable_pretraining/data/datasets.py
- stable-pretraining/stable_pretraining/manager.py

Yêu cầu:

1. Dùng hydra.main.
2. Default config nằm trong script hoặc dataclass/OmegaConf, miễn chạy được without YAML.
3. Support các config keys tối thiểu:
   - dataset_name
   - max_epochs
   - max_steps
   - batch_size
   - num_workers
   - backbone
   - pretrained
   - resolution
   - local_resolution
   - n_views
   - n_global_views
   - lr
   - weight_decay
   - precision
   - accelerator
   - devices
   - drop_path_rate
   - bstat_lambda
   - bstat_num_slices
   - bstat_t_max
   - bstat_n_points
   - seed
4. Default smoke dataset phải là imagenette/frgfm/imagenette hoặc một dataset nhỏ đã dùng trong test.
5. Build MultiViewTransform bằng stable_pretraining.data.transforms.
6. Build DataModule bằng stable_pretraining.data.DataModule.
7. Build LeJEPA từ stable_pretraining.methods.lejepa.LeJEPA.
8. Monkey-patch hoặc adapter forward giống test_lejepa_inet10.py để batch dict -> LeJEPA.forward.
9. Set module.optim với AdamW + LinearWarmupCosineAnnealing như test.
10. Build Lightning Trainer.
11. Run stable_pretraining.Manager.
12. Không implement W&B trong phase này, hoặc để logger false/null mặc định.
13. Nếu dataset download/network không khả dụng, cung cấp synthetic/debug fallback qua dataset_name=synthetic.

Verification bắt buộc:

python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 accelerator=cpu devices=1 precision=32

Nếu synthetic chưa có, implement synthetic path.

Sau đó chạy:

python scripts/ablations.py render epps

Đảm bảo rendered command target script mới.

Báo lại:

- smoke command có pass không
- loss có finite không
- file đã tạo/sửa
- limitations
```

---

## Prompt 4 — Connect Renderer to Training Entrypoint

```text
Trước khi làm, hãy đọc các phần command rendering, smoke workflow, và training entrypoint trong scripts/ablation_code_plan.md.

Tiếp tục sau khi scripts/train_lejepa_ablation.py chạy smoke được.

Mục tiêu:

- Làm scripts/ablations.py render command tương thích thật với train_lejepa_ablation.py.

Yêu cầu:

1. Kiểm tra toàn bộ key trong BASE_OVERRIDES/specs có được train_lejepa_ablation.py nhận không.
2. Nếu key chưa được support nhưng không cần cho ready specs, renderer phải bỏ qua hoặc warning rõ.
3. Ready specs ban đầu chỉ nên gồm:
   - epps
   - drop_path
   - views nếu n_views/n_global_views/batch_size hoạt động
4. Các spec còn lại giữ needs_model_support.
5. Thêm --smoke option cho render:
   python scripts/ablations.py render epps --smoke
6. --smoke override:
   - dataset_name=synthetic
   - max_steps=3
   - batch_size=4
   - num_workers=0
   - backbone=vit_tiny_patch16_224
   - bstat_num_slices=16 nếu không sweep field đó
   - accelerator=cpu
   - devices=1
   - precision=32
7. Render all --smoke không được sinh command quá nặng.

Verification:

python scripts/ablations.py list
python scripts/ablations.py render epps --smoke
python scripts/ablations.py render drop_path --smoke
python scripts/ablations.py render views --smoke

Chạy ít nhất một command smoke render ra từ renderer.

Báo lại diff và kết quả.
```

---

## Prompt 5 — Add Projector Builder Support

```text
Trước khi làm, hãy đọc mục projector builder trong Phase 4 của scripts/ablation_code_plan.md.

Hãy implement projector builder cho LeJEPA theo scripts/ablation_code_plan.md.

Mục tiêu:

- Unlock projector_depth ablation.
- Không thay đổi behavior mặc định.

Files cần đọc:

- stable-pretraining/stable_pretraining/methods/lejepa.py
- stable-pretraining/stable_pretraining/backbone/mlp.py
- stable-pretraining/stable_pretraining/tests/integration/test_lejepa_inet10.py

Yêu cầu:

1. Thêm function build_projector trong stable_pretraining.methods.lejepa.
2. Support:
   - Linear
   - MLP2
   - MLP
   - MLP4
3. Thêm LeJEPA.__init__ args:
   - projector_arch="MLP"
   - projector_dim=512
   - projector_hidden_dim=2048
   - projector_norm="batch_norm"
4. Nếu projector được truyền trực tiếp, giữ behavior cũ.
5. Nếu projector=None, dùng build_projector.
6. Mặc định phải tương đương gần nhất với projector cũ.
7. Không đổi public output fields.
8. Update train_lejepa_ablation.py để nhận:
   - projector_arch
   - projector_dim
   - projector_hidden_dim
   - projector_norm
9. Update ablation spec: projector_depth status thành ready nếu pass smoke.

Tests:

Tạo hoặc cập nhật:

- stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py

Test instantiate + forward cho:

- projector_arch=Linear
- projector_arch=MLP2
- projector_arch=MLP
- projector_arch=MLP4

Use vit_tiny_patch16_224, n_slices=8, CPU tensors.

Verification:

pytest stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py
python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 projector_arch=MLP2 accelerator=cpu devices=1 precision=32
python scripts/ablations.py render projector_depth --smoke

Báo lại diff và kết quả.
```

---

## Prompt 6 — Add SIGReg Target Support

```text
Trước khi làm, hãy đọc mục sigreg_target trong Phase 4 của scripts/ablation_code_plan.md.

Hãy implement sigreg_target cho LeJEPA.

Mục tiêu:

- Unlock sigreg_target ablation: proj, embed, both.

Yêu cầu:

1. Thêm LeJEPA.__init__ arg:
   sigreg_target="proj"
2. Validate allowed values:
   - proj
   - embed
   - both
3. Sửa _compute_loss để nhận all_features và all_projected.
4. Invariance loss vẫn tính trên projected representations.
5. SIGReg:
   - proj: apply on flattened projected output
   - embed: apply on flattened backbone features
   - both: average SIGReg(proj) và SIGReg(embed)
6. Không đổi default behavior.
7. Update train_lejepa_ablation.py nhận sigreg_target.
8. Update specs status sigreg_target thành ready nếu tests pass.

Tests:

Add tests trong test_lejepa_ablation_options.py:

- sigreg_target=proj
- sigreg_target=embed
- sigreg_target=both
- invalid value raises ValueError

Verification:

pytest stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py
python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 sigreg_target=both accelerator=cpu devices=1 precision=32
python scripts/ablations.py render sigreg_target --smoke

Báo lại diff và kết quả.
```

---

## Prompt 7 — Add Predictor Head Support

```text
Trước khi làm, hãy đọc mục predictor support trong Phase 4 của scripts/ablation_code_plan.md.

Hãy implement predictor head ablation cho LeJEPA.

Mục tiêu:

- Unlock predictor ablation: none, linear, mlp.
- Không đưa stop-gradient hoặc teacher-student behavior ngầm định.

Yêu cầu:

1. Thêm builder:
   build_predictor(kind, dim, hidden_dim=2048, norm_layer="batch_norm")
2. Support:
   - none -> nn.Identity or None path
   - linear -> nn.Linear(dim, dim)
   - mlp -> MLP(dim, [hidden_dim, dim], norm_layer=...)
3. Thêm LeJEPA.__init__ args:
   - predictor="none"
   - predictor_hidden_dim=2048
   - predictor_norm="batch_norm"
4. Loss behavior:
   - z = projector(features)
   - p = predictor(z) nếu predictor != none
   - invariance loss dùng p so với center từ z global views
   - không detach target trừ khi có explicit config riêng; phase này không thêm detach.
   - SIGReg vẫn áp dụng trên z/proj, không trên p.
5. Default predictor=none phải giữ behavior cũ.
6. Update train script.
7. Update specs predictor status thành ready nếu tests pass.

Tests:

Add tests:

- predictor=none
- predictor=linear
- predictor=mlp
- invalid predictor raises
- predictor params receive gradients for linear/mlp

Verification:

pytest stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py
python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 predictor=mlp accelerator=cpu devices=1 precision=32
python scripts/ablations.py render predictor --smoke

Báo lại diff và kết quả.
```

---

## Prompt 8 — Add Register Token Support

```text
Trước khi làm, hãy đọc mục register tokens trong Phase 4 của scripts/ablation_code_plan.md.

Hãy implement reg_tokens support cho LeJEPA.

Mục tiêu:

- Unlock reg_tokens ablation nếu timm backbone hỗ trợ.

Yêu cầu:

1. Thêm LeJEPA.__init__ arg:
   reg_tokens=0
2. Khi tạo timm model, truyền reg_tokens nếu > 0.
3. Nếu timm model không support reg_tokens và reg_tokens > 0, raise error rõ ràng.
4. Nếu reg_tokens=0, giữ behavior cũ.
5. Update train script nhận reg_tokens.
6. Update specs status chỉ thành ready nếu chosen backbone vit_large_patch14_224 support reg_tokens.
7. Nếu không support ổn định, giữ status needs_model_support và ghi note rõ.

Tests:

- reg_tokens=0 pass.
- reg_tokens=1 hoặc 2 pass nếu timm support.
- nếu không support, test error message.

Verification:

pytest stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py
python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 reg_tokens=1 accelerator=cpu devices=1 precision=32
python scripts/ablations.py render reg_tokens --smoke

Báo lại support thực tế của timm trong environment này.
```

---

## Prompt 9 — Add Aggregator Support

```text
Trước khi làm, hãy đọc mục aggregator support trong Phase 4 của scripts/ablation_code_plan.md.

Hãy implement aggregator support cho LeJEPA.

Mục tiêu:

- Support aggregation modes:
  - cls
  - mean
  - cls_mean
- Không implement cls2 trong phase này nếu cần hook/intermediate features phức tạp.

Yêu cầu:

1. Thêm LeJEPA.__init__ arg:
   aggregator="cls"
2. Default cls phải giữ behavior cũ càng gần càng tốt.
3. Thêm helper encode/images path:
   - nếu aggregator=cls và không cần tokens, có thể dùng backbone(images)
   - nếu aggregator=mean/cls_mean, dùng backbone.forward_features(images)
4. Helper aggregate_tokens:
   - cls: token đầu hoặc pooled output
   - mean: mean patch tokens, bỏ CLS/register tokens nếu biết được
   - cls_mean: concat cls token + mean patch tokens
5. Projector input dim phải đúng:
   - nếu cls_mean doubles dim, projector builder phải nhận input dim phù hợp.
6. Nếu không infer được dim cleanly, dùng LazyLinear trong projector builder hoặc dummy forward có kiểm soát.
7. Update train script nhận aggregator.
8. Update specs aggregation:
   - ready for cls,mean,cls_mean
   - cls2 blocked/future

Tests:

- aggregator=cls
- aggregator=mean
- aggregator=cls_mean
- check embedding/projector dimensions
- invalid aggregator raises

Verification:

pytest stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py
python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 aggregator=mean accelerator=cpu devices=1 precision=32
python scripts/ablations.py render aggregation --smoke

Báo lại nếu cls2 vẫn blocked.
```

---

## Prompt 10 — Add Patch Masking Support

```text
Trước khi làm, hãy đọc mục patch masking support trong Phase 4 của scripts/ablation_code_plan.md.

Hãy implement patch_mask_ratio support cho LeJEPA bằng cách reuse stable-pretraining backbone masking.

Mục tiêu:

- Unlock patch_masking ablation.

Files cần đọc:

- stable-pretraining/stable_pretraining/backbone/patch_masking.py
- stable-pretraining/stable_pretraining/backbone/vit.py
- stable-pretraining/stable_pretraining/tests/unit/test_masked_encoder.py
- stable-pretraining/stable_pretraining/methods/lejepa.py

Yêu cầu:

1. Thêm LeJEPA.__init__ args:
   - patch_mask_ratio=0.0
   - patch_mask_block_size=1
   - patch_mask_crop_ratio=0.0
   - patch_size=None
2. Nếu patch_mask_ratio=0.0, giữ path cũ.
3. Nếu patch_mask_ratio>0, dùng PatchMasking + MaskedEncoder nếu khả thi.
4. Aggregation phải hoạt động với visible token sequence.
5. Local/global resolution khác nhau phải không crash.
6. Eval mode không mask hoặc masking module eval phải trả all patches.
7. Update train script nhận patch_mask_ratio và related args.
8. Update specs patch_masking status thành ready nếu tests pass.

Tests:

- patch_mask_ratio=0.0
- patch_mask_ratio=0.3
- train mode forward finite loss
- eval mode returns embedding
- local view size smaller than global does not crash

Verification:

pytest stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py
python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 patch_mask_ratio=0.3 accelerator=cpu devices=1 precision=32
python scripts/ablations.py render patch_masking --smoke

Báo lại mọi shape assumptions trong implementation.
```

---

## Prompt 11 — Add Result Summarization

```text
Trước khi làm, hãy đọc mục results summarization trong scripts/ablation_code_plan.md.

Hãy thêm summarization command cho ablation runner.

Mục tiêu:

- Gom logs sau sweep thành CSV/Markdown.
- Reuse stable-pretraining utilities nếu có thể.

Files cần đọc:

- stable-pretraining/stable_pretraining/utils/read_csv_logger.py
- stable-pretraining/stable_pretraining/utils/log_reader.py
- stable-pretraining/stable_pretraining/cli.py

Yêu cầu:

1. Thêm command:
   python scripts/ablations.py summarize <log_dir>
2. Options:
   --output scripts/generated/results
   --metric val/knn_top1
   --mode max
3. Nếu không tìm thấy logs, error rõ.
4. Nếu có .hydra/config.yaml trong run dirs, parse để lấy swept params.
5. Output:
   - all_ablation_summary.csv
   - all_ablation_summary.md
6. Không phụ thuộc W&B API.
7. Nếu stable-pretraining đã có CSVLogAutoSummarizer dùng được, reuse.

Verification:

- Tạo temp fake logs nhỏ nếu chưa có real logs.
- Chạy summarize trên fake logs.
- Kiểm tra CSV/MD được tạo.

Báo lại format output và limitations.
```

---

## Prompt 12 — Update Existing Docs

```text
Trước khi làm, hãy đọc mục documentation updates trong scripts/ablation_code_plan.md.

Hãy cập nhật docs sau khi ablation runner/training entrypoint đã có.

Files:

- scripts/ablation_plan.md
- scripts/ablation_code_plan.md nếu cần
- AGENTS.md
- CLAUDE.md

Yêu cầu:

1. Trong scripts/ablation_plan.md, thêm section "Executable Ablation Pipeline".
2. Ghi command mới:
   - python scripts/ablations.py list
   - python scripts/ablations.py render epps
   - python scripts/ablations.py write-scripts --ready-only
   - python scripts/train_lejepa_ablation.py ... smoke ...
3. Đánh dấu các old markdown launch files là legacy/manual nếu vẫn còn.
4. Ghi rõ không dùng scripts/je.py vì không tồn tại trong checkout hiện tại.
5. Update AGENTS.md phần Research / Training Entrypoints để nhắc ablation runner mới.
6. Không rewrite toàn bộ docs, chỉ thêm/cập nhật phần liên quan.

Verification:

grep -n "scripts/je.py" scripts/ablation_plan.md AGENTS.md
python scripts/ablations.py list

Báo lại docs đã cập nhật.
```

---

## Prompt 13 — Final Smoke Audit

```text
Trước khi làm, hãy đọc các mục final target behavior và verification preference trong scripts/ablation_code_plan.md.

Hãy audit toàn bộ ablation implementation.

Mục tiêu:

- Không thêm feature mới.
- Chỉ kiểm tra và sửa bug nhỏ nếu cần.

Checklist:

1. git status --short
2. python scripts/ablations.py list
3. python scripts/ablations.py render all --smoke
4. python scripts/ablations.py write-scripts --output /tmp/lejepa_ablation_scripts --ready-only --force
5. Chạy smoke training nhỏ:
   python scripts/train_lejepa_ablation.py dataset_name=synthetic max_steps=3 batch_size=4 num_workers=0 backbone=vit_tiny_patch16_224 bstat_num_slices=16 accelerator=cpu devices=1 precision=32
6. Chạy unit tests liên quan:
   pytest stable-pretraining/stable_pretraining/tests/unit/test_lejepa_ablation_options.py
7. Nếu có root tests bị ảnh hưởng:
   pytest tests/

Yêu cầu trả lời:

- Tóm tắt files changed.
- Specs nào ready.
- Specs nào vẫn blocked và vì sao.
- Commands đã pass.
- Commands chưa chạy được và lý do.
```

---

## Prompt 14 — If a Model Gets Stuck

```text
Trước khi làm, hãy đọc phần liên quan trong scripts/ablation_code_plan.md để xác định phase, intended design, và constraints liên quan.

Bạn đang thực thi scripts/ablation_code_plan.md nhưng bị kẹt.

Không tiếp tục viết workaround lớn.

Hãy làm các bước sau:

1. Chạy git diff để xem đã sửa gì.
2. Chạy command/test nhỏ nhất tái hiện lỗi.
3. Đọc lại đúng file liên quan, không đọc cả repo.
4. Xác định lỗi thuộc nhóm nào:
   - missing dependency
   - wrong config key
   - batch shape mismatch
   - model API mismatch
   - dataset unavailable
   - GPU-only path
   - Hydra parsing issue
5. Nếu lỗi là missing support thật, mark spec là blocked/needs_model_support.
6. Nếu lỗi là bug nhỏ, sửa nhỏ và chạy lại test.
7. Trả lời ngắn với:
   - lỗi
   - nguyên nhân
   - file liên quan
   - patch đã làm hoặc đề xuất patch
   - command verification

Không tạo training framework mới.
Không đổi tên package.
Không xóa generated artifacts/caches.
Không sửa LaTeX/paper files.
```

---

## Recommended Execution Order

1. Prompt 0
2. Prompt 1
3. Prompt 2
4. Prompt 3
5. Prompt 4
6. Prompt 5
7. Prompt 6
8. Prompt 7
9. Prompt 8
10. Prompt 9
11. Prompt 10
12. Prompt 11
13. Prompt 12
14. Prompt 13

Nếu compute hoặc thời gian ít, dừng sau Prompt 4. Lúc đó repo đã có renderer + smoke training path, đủ để bắt đầu chạy các ablation đang supported.
