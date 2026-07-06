# Plan: Consolidate & analyze LeJEPA ablation results

**Notebook:** `mlinh776/lejepa-ablation-full` (22 versions, 1 ablation per version).
**Status:** ✅ raw output downloaded to `ablation_raw/` (14 zips). Retrieval done —
this plan now covers **merge → aggregate → analyze**.

---

## 0. Verified state of `ablation_raw/`

14 zips, one per version/chunk. Each contains `results/<spec>/job*/…`
(+ `multirun/` hydra logs + `environment*/requirements*` — ignore those).
All 62 jobs completed with a populated `paper_eval`:

| zip(s) | spec | jobs | expected |
|--------|------|------|----------|
| 01-aggregation | `aggregation` | 3 | 3 ✅ |
| 02-drop_path | `drop_path` | 5 | 5 ✅ |
| 03-predictor | `predictor` | 3 | 3 ✅ |
| 04-sigreg_target | `sigreg_target` | 3 | 3 ✅ |
| 05-patch_masking | `patch_masking` | 6 | 6 ✅ |
| 06-projector_depth | `projector_depth` | 4 | 4 ✅ |
| 07-view_chunk0/1/2 | `views` | 4+4+3 = **11** | 11 ✅ |
| 08-epps_chunk0–4 | `epps` | 4+7+4+7+5 = **27** | 27 ✅ |

**Total: 62 jobs, nothing missing.** Job dir names (`job0_<hash>`) are **unique
across chunks** (epps 27/27, views 11/11) → merging chunks won't overwrite.

### ⚠️ Key correction to the earlier plan
`metrics.csv` in these outputs holds **only loss curves**
(`fit/validate loss`, `inv_loss`, `sigreg_loss`) — **no accuracy/kNN column**.
So `scripts/ablations.py summarize --metric val/knn_top1` **cannot work here**.
The downstream metric lives in **`results/<spec>/job*/summary.json`**:

```json
"config": { …varied knob… },
"final_loss": 1.027,
"paper_eval": { "top1": 0.6333, "top5": 0.9366, "best_probe_epoch": 77,
                "probe": "AdamW lr1e-3 wd1e-6 cosine", "n_train": 28407 }
```

→ Aggregation must read `summary.json`, not `metrics.csv`.
(`metrics.csv` stays useful only for loss/convergence curves.)

### Per-spec varied knob + observed top1 range (from summary.json)
| spec | varied config key(s) | top1 range |
|------|----------------------|------------|
| epps | `bstat_num_slices`, `bstat_t_max`, `bstat_n_points` | 0.549 – **0.701** |
| views | `n_views`, `n_global_views`, `batch_size`, `autostop` | 0.568 – **0.728** |
| drop_path | `drop_path_rate` | 0.582 – 0.617 |
| patch_masking | `patch_mask_ratio` | 0.593 – 0.611 |
| projector_depth | `projector_arch` | **0.234** – 0.613 (Linear collapses) |
| sigreg_target | `sigreg_target` | **0.237** – 0.595 (embed/both collapse) |
| predictor | `predictor` | **0.439** – 0.595 |
| aggregation | `aggregator` | 0.558 – 0.595 |

---

## 1. Merge → unified tree  `ablation_results/`

```bash
cd /media/mlinh/Kingston/projects/ML/lab-3_LeJEPA/lejepa-MLProject
mkdir -p ablation_results
for z in ablation_raw/*.zip; do
  d=$(mktemp -d); unzip -oq "$z" 'results/*' -d "$d"
  cp -rn "$d"/results/. ablation_results/; rm -rf "$d"
done
```
**Verify:** `find ablation_results -name summary.json | wc -l` → **62**, and
`ls ablation_results/` → the 8 spec dirs above.
(`cp -rn` = no-clobber; unique hashes mean chunk merges are safe.)

Add `ablation_raw/` and `ablation_results/` to `.gitignore` (large, regenerable).

## 2. Aggregate → one table  (custom pass, reads `summary.json`)

Create `scripts/ablations/collect_summaries.py`: walk
`ablation_results/**/summary.json`, and for each job emit a row =
`{spec, job_hash, <every varied config key>, final_loss, top1, top5,
best_probe_epoch}`. Write two artifacts:

- `ablation_results/ablation_summary.csv` — all 62 rows (flat, for pandas).
- `ablation_results/ablation_summary.md` — grouped by spec, **sorted by top1
  desc within each spec**, baseline row marked (the config matching
  `BASE_OVERRIDES`, e.g. epps num_slices=1024/t_max=3/n_points=17).

**Verify:** CSV has 62 rows; each spec's rows = its expected count; no NaN top1.
(Reuse `scripts/ablations/specs.py::BASE_OVERRIDES` to flag the baseline config.)

## 3. Analyze → trends & comparison to paper

The epps grid (slices 512/1024/4096 × t_max 1/3/5 × n_points 5/17/41) and the
views cases line up with the paper baselines already staged in
`climb_bench/tracker/paper-ablation-baselines.md`. Produce a short findings note:

1. **Per-spec trend** — does top1 move with the knob; flat vs steep; best config.
2. **Collapses to explain** — `projector_depth=Linear` (0.234), `sigreg_target`
   embed/both (0.237), `predictor` non-none — confirm these are real, not
   broken runs (check `final_loss` + loss curves in `metrics.csv`).
3. **Trend vs paper** — compare *direction/shape* only (absolute numbers not
   comparable: ViT-S/imagenet10 vs paper ViT-L/IN-1K). E.g. does our epps
   confirm "t_max≥3 matters, n_points≈flat, more slices≈marginal"?
4. Write to `climb_bench/tracker/batch-ablation-analysis.md` (new) or append a
   "measured" column next to the paper table in `paper-ablation-baselines.md`.

**Success criteria:** every spec has a ranked table + a one-line trend verdict,
and each collapse is confirmed real (low top1 co-occurs with degenerate loss) or
flagged as a run artifact.

---

## 4. Execution order (on your go)
1. Run §1 merge → verify 62 summaries. *(cheap, ~seconds)*
2. Write + run §2 `collect_summaries.py` → CSV + MD. *(minutes)*
3. Draft §3 findings note comparing to the paper table.

Optional going-forward (not needed now): add a Kaggle output-Dataset sink to the
notebook so the next batch is one-command `kaggle datasets download` — avoids the
22 manual web-UI downloads next time.

**Trạng thái §1–§3: ✅ ĐÃ XONG.** `ablation_results/` (62 job) + `ablation_summary.{csv,md}`
+ `climb_bench/tracker/ablation-measured-analysis.md`.

---

# Giai đoạn 4 — Báo cáo ablation theo pipeline paper (visualize → insight → slide)

**Mục tiêu đồ án:** *"Benchmark the methods on different settings of hyperparameters
and components."* Trình bày theo đúng pipeline paper rồi đưa vào slide.

## Pipeline paper (đã khảo sát — `docs/.../body.tex` `tab:ablations`, l.605–684)
Mỗi ablation = **một bảng grid top1** theo trục hyperparameter, gom vào 1 bảng lớn,
caption mang thông điệp **"ổn định qua mọi hyperparameter, không lựa chọn nào gây
collapse; vài cái cải thiện nhẹ (num_slices, projector dim)"**. Cấu trúc:
- (a) Epps-Pulley: `integration domain × num_slices × n_points`  ← **khớp epps của ta**
- (b) Views: `n_views × n_global`  ← **khớp views của ta**
- (c) batch_size · (d) emb/proj dim · (e) reg_tokens
- Bảng riêng `tab:proj_pred`: bỏ predictor / teacher-student (collapse study).

Ta dựng lại pipeline này trên **imagenet10 / ViT-S/16** (khác regime paper ViT-L/IN-1K).

## 4.1 — Code visualize → `scripts/ablations/viz_ablation.py`
Đọc `ablation_results/ablation_summary.csv`, style `figures/matplotlibrc`
(fallback `usetex=False` nếu máy thiếu LaTeX), xuất PNG+PDF vào
`ablation_results/figures/`. Bốn hình bám pipeline paper:

| Hình | Loại | Nội dung | ↔ paper |
|------|------|----------|---------|
| **A** `epps_heatmap` | 3 heatmap (n_points 5/17/41), trục `t_max × num_slices`, annotate top1 | tab(a) |
| **B** `views_heatmap` | heatmap `n_views × n_global` (ô thiếu để trống) | tab(b) |
| **C** `components_bars` | panel bar Δtop1 vs anchor: drop_path, patch_mask, projector_arch, sigreg_target, predictor, aggregator; **collapse tô đỏ**, baseline = đường ngang | tab(a) + proj_pred |
| **D** `sensitivity_tornado` | range (max−min) top1 mỗi ablation, sort desc → 1 hình tóm tắt "stable vs collapse" | thông điệp chính |

**Verify:** 4 hình sinh ra; số trên hình khớp `ablation_summary.csv`; anchor 0.5946
hiện đúng làm mốc.

## 4.2 — Insight → hoàn thiện `ablation-measured-analysis.md`
Viết lại theo framing paper, thêm:
1. **Mục "Comparability" (bắt buộc):** anchor ablation 0.5946 ≠ baseline dự án 0.8949
   vì **khác harness pretrain** (batch 512 vs 128, có/không patch_mask+drop_path,
   schedule 100 vs 400ep). → số ablation **chỉ so Δ nội bộ**, không ghép thang batch1/2.
2. **Đối chiếu trực tiếp paper tab(a)/(b):** khớp (num_slices↑, n_points≈phẳng) vs
   ngược (t_max nhỏ tốt hơn; ít-view tốt hơn) — quy cho regime low-data/ViT-S.
3. **Robustness vs collapse:** xác nhận robust ở hyperparameter chính; **collapse thật**
   khi đặt sai component (projector=Linear, sigreg=embed/both) — nhất quán lý thuyết
   (SIGReg phải áp lên projection đủ chiều), và predictor không cần (khớp paper).
4. **Caveat under-reg:** top config (t_max=1, ít-view) kèm loss thấp + best_ep sớm →
   cần kNN/đường loss để phân biệt "tốt thật" vs "under-regularize may mắn".

## 4.3 — Slide → `slides/slides_main.tex` (Beamer, section "Kết quả")
Đã có sẵn frame ablation **đang bị comment** (l.1961–2008, dùng số paper). Thay bằng
kết quả của ta:
- **Frame 1 — Hyperparameter robustness:** nhúng Fig A (epps) + Fig B (views),
  bullet: khớp/ngược paper + "không collapse trên hyperparameter".
- **Frame 2 — Component & collapse:** nhúng Fig C + Fig D, bullet: 3 collapse thật,
  predictor không cần; **1 dòng caveat comparability** (số là track ablation batch-lớn).
- Giữ nguyên style/theme Beamer; build lại `slides_main.pdf` (`pdflatex`).

## Thứ tự thực hiện + rủi ro
1. **4.1** viết + chạy `viz_ablation.py` → verify 4 hình. *(rủi ro: `usetex` cần LaTeX → có fallback)*
2. **4.2** hoàn thiện note (không cần compute).
3. **4.3** chèn 2 frame + build slide. *(rủi ro: cần `pdflatex`; nếu thiếu, chỉ giao .tex + hình)*

**KHÔNG cần chạy lại baseline** cho giai đoạn này — anchor 0.5946 nội bộ là mốc đúng
để benchmark các setting (đã có sẵn, deterministic). Chỉ chạy lại nếu muốn nối thang
sang batch1/2 (ngoài phạm vi đồ án ablation).
