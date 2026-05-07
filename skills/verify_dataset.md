# Verify Dataset Skill

**Goal**: Verify that the ImageNet dataset has been correctly downloaded and extracted into the `ImageFolder` structure required by `train_eval_vit_l.py`.

## Instructions
1. Run the `check_data.py` script located in the project root.
2. Supply the path to the dataset directory using the `--data-dir` flag (default is `/workspace/data/imagenet`).

```bash
python check_data.py --data-dir <path_to_data>
```

## Success Criteria
- The script returns `[SUCCESS] ImageNet data structure looks valid and ready for training!`
- If the script returns `[FAIL]`, you must identify why the data is missing or incorrectly formatted (e.g., zip not extracted, wrong path) and fix it before proceeding to training.
- Do not run `train_eval_vit_l.py` until the data is verified.
