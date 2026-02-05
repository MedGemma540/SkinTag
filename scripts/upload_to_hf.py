"""Upload updated models and artifacts to HuggingFace with versioning.

Creates a v1-original branch for rollback, then updates main with:
- Latest classifier PKLs and metadata from 5-dataset pipeline run
- Fixed classifier_deep_mlp.pkl alias for web app compatibility
- Updated README.md model card
"""
import sys
from pathlib import Path
from huggingface_hub import HfApi, CommitOperationAdd, create_branch

REPO_ID = "skintaglabs/siglip-skin-lesion-classifier"
CACHE_DIR = Path("results/cache")
FINETUNED_DIR = CACHE_DIR / "clinical_v20260204_161741"

api = HfApi()

# --- Step 1: Create v1-original branch for rollback ---
print("Step 1: Creating v1-original branch for rollback...")
try:
    create_branch(REPO_ID, branch="v1-original", repo_type="model")
    print("  Created branch: v1-original")
except Exception as e:
    if "already exists" in str(e).lower() or "409" in str(e):
        print("  Branch v1-original already exists (ok)")
    else:
        print(f"  Warning: {e}")

# --- Step 2: Prepare Misc/ file uploads ---
print("\nStep 2: Preparing Misc/ files for upload...")
operations = []

# Files from results/cache/ (frozen pipeline outputs)
misc_files = {
    "classifier.pkl": "classifier.pkl",
    "classifier_baseline.pkl": "classifier_baseline.pkl",
    "classifier_condition.pkl": "classifier_condition.pkl",
    "classifier_condition_deep.pkl": "classifier_condition_deep.pkl",
    "classifier_condition_logistic.pkl": "classifier_condition_logistic.pkl",
    "classifier_deep.pkl": "classifier_deep.pkl",
    "classifier_logistic.pkl": "classifier_logistic.pkl",
    "classifier_xgboost.pkl": "classifier_xgboost.pkl",
    "condition_training_results.json": "condition_training_results.json",
    "evaluation_results.json": "evaluation_results.json",
    "finetune_results.json": "finetune_results.json",
    "metadata.csv": "metadata.csv",
    "test_metadata.csv": "test_metadata.csv",
    "training_results.json": "training_results.json",
}

for local_name, remote_name in misc_files.items():
    local_path = CACHE_DIR / local_name
    if local_path.exists():
        operations.append(CommitOperationAdd(
            path_in_repo=f"Misc/{remote_name}",
            path_or_fileobj=str(local_path),
        ))
        size_mb = local_path.stat().st_size / 1_000_000
        print(f"  + Misc/{remote_name} ({size_mb:.2f} MB)")
    else:
        print(f"  - SKIP {local_name} (not found)")

# Fix web app naming mismatch: classifier_deep.pkl -> also as classifier_deep_mlp.pkl
deep_pkl = CACHE_DIR / "classifier_deep.pkl"
if deep_pkl.exists():
    operations.append(CommitOperationAdd(
        path_in_repo="Misc/classifier_deep_mlp.pkl",
        path_or_fileobj=str(deep_pkl),
    ))
    print(f"  + Misc/classifier_deep_mlp.pkl (web app alias)")

# Fine-tuned classifiers from retraining pipeline
finetuned_classifiers = FINETUNED_DIR / "classifiers_finetuned"
if finetuned_classifiers.exists():
    for f in finetuned_classifiers.iterdir():
        if f.suffix == ".pkl":
            operations.append(CommitOperationAdd(
                path_in_repo=f"Misc/{f.name}",
                path_or_fileobj=str(f),
            ))
            size_mb = f.stat().st_size / 1_000_000
            print(f"  + Misc/{f.name} ({size_mb:.2f} MB)")

# Fine-tuned XGBoost from cache root (if not already covered)
xgb_finetuned = CACHE_DIR / "classifier_xgboost_finetuned.pkl"
if xgb_finetuned.exists():
    operations.append(CommitOperationAdd(
        path_in_repo="Misc/classifier_xgboost_finetuned.pkl",
        path_or_fileobj=str(xgb_finetuned),
    ))
    print(f"  + Misc/classifier_xgboost_finetuned.pkl")

# Embeddings (large files)
for emb_name in ["embeddings.pt", "embeddings_finetuned_train.pt", "embeddings_finetuned_test.pt"]:
    emb_path = CACHE_DIR / emb_name
    if emb_path.exists():
        operations.append(CommitOperationAdd(
            path_in_repo=f"Misc/{emb_name}",
            path_or_fileobj=str(emb_path),
        ))
        size_mb = emb_path.stat().st_size / 1_000_000
        print(f"  + Misc/{emb_name} ({size_mb:.1f} MB)")

# --- Step 3: Prepare updated README.md ---
print("\nStep 3: Preparing updated README.md...")

readme_content = """---
license: mit
language:
- en
metrics:
- f1
- accuracy
- roc_auc
base_model: google/siglip-so400m-patch14-384
pipeline_tag: image-classification
tags:
- dermatology
- medical
- skin-lesion
- melanoma-detection
- vision
---

# SigLIP Skin Lesion Classifier

Fine-tuned SigLIP vision model for skin lesion classification and triage. Part of the [SkinTag](https://github.com/skintaglabs/main) project for equitable melanoma detection.

## Model Details

**Base Model:** [google/siglip-so400m-patch14-384](https://huggingface.co/google/siglip-so400m-patch14-384) (878M parameters)

**Fine-tuning:** Last 4 vision transformer layers unfrozen (~7% trainable parameters), with classification head. Trained with Fitzpatrick-balanced sampling for fairness across skin tones.

**Training Data:** 47,277 images from 5 dermatology datasets:

| Dataset | Samples | Type | Skin Tone Coverage |
|---------|---------|------|--------------------|
| HAM10000 | 10,015 | Dermoscopic | Limited |
| DDI/Stanford | 656 | Clinical | Fitzpatrick I-VI |
| Fitzpatrick17k | 16,518 | Clinical | Fitzpatrick I-VI |
| PAD-UFES-20 | 2,298 | Smartphone | Brazilian population |
| BCN20000 | 17,790 | Dermoscopic | European population |

## Performance

### Binary Triage (Benign vs Malignant)

| Model | AUC | Accuracy | F1 |
|-------|-----|----------|----|
| Fine-tuned XGBoost | 0.960 | 92.0% | 0.866 |
| Fine-tuned MLP | 0.945 | 91.2% | 0.856 |
| Frozen XGBoost (baseline) | 0.916 | 88.2% | 0.794 |

**Clinical Thresholds:**
- At 95% sensitivity: 82.5% specificity
- At 90% sensitivity: 88.3% specificity

### Condition Estimation (10-class)

10 categories: Melanoma, BCC, SCC, Actinic Keratosis, Melanocytic Nevus, Seborrheic Keratosis, Dermatofibroma, Vascular Lesion, Non-Neoplastic, Other/Unknown.

### Fairness

Tested across Fitzpatrick skin types I-VI with <5% sensitivity gap. See evaluation_results.json for per-group metrics.

## Versioning

| Branch | Description | Model Format |
|--------|-------------|--------------|
| `main` | Production (current) -- EndToEndSigLIP v1 format | config.json + model_state.pt + head_state.pt |
| `v1-original` | Snapshot of original upload for rollback | Same as main at time of branch creation |

To load a specific version:
```python
from huggingface_hub import snapshot_download
# Latest (main)
snapshot_download("skintaglabs/siglip-skin-lesion-classifier")
# Rollback to v1
snapshot_download("skintaglabs/siglip-skin-lesion-classifier", revision="v1-original")
```

## Files

### Root (Model Weights)
- `config.json` -- Architecture configuration (model_name, hidden_dim, n_classes, dropout, unfreeze_layers)
- `head_state.pt` -- Classification head weights (~1.2 MB)
- `model_state.pt` -- Full fine-tuned model weights (~3.5 GB)

### Misc/ (Pipeline Artifacts)
- `classifier.pkl`, `classifier_logistic.pkl`, `classifier_deep.pkl` -- Binary classifiers (frozen embeddings)
- `classifier_deep_mlp.pkl` -- Alias for classifier_deep.pkl (web app compatibility)
- `classifier_xgboost.pkl` -- XGBoost binary classifier (frozen embeddings)
- `classifier_xgboost_finetuned.pkl` -- XGBoost on fine-tuned embeddings (AUC 0.960)
- `xgboost_finetuned_binary.pkl`, `mlp_finetuned_binary.pkl` -- Fine-tuned pipeline classifiers
- `xgboost_finetuned_condition.pkl` -- 10-class condition classifier (fine-tuned)
- `classifier_condition.pkl`, `classifier_condition_deep.pkl`, `classifier_condition_logistic.pkl` -- Condition classifiers
- `embeddings.pt` -- Frozen SigLIP embeddings (~109 MB)
- `embeddings_finetuned_train.pt`, `embeddings_finetuned_test.pt` -- Fine-tuned embeddings
- `metadata.csv`, `test_metadata.csv` -- Dataset metadata with labels
- `evaluation_results.json`, `training_results.json` -- Metrics

## Usage

### End-to-End Inference (Recommended)
```python
from src.model.deep_classifier import EndToEndClassifier
model = EndToEndClassifier.load_for_inference("path/to/downloaded/model")
probs = model.predict_proba(images)  # Returns [benign_prob, malignant_prob]
```

### Embedding + Classifier Head
```python
from transformers import AutoModel, AutoImageProcessor
import pickle

# Extract embeddings with frozen SigLIP
processor = AutoImageProcessor.from_pretrained("google/siglip-so400m-patch14-384")
model = AutoModel.from_pretrained("google/siglip-so400m-patch14-384")
embeddings = model.vision_model(pixel_values=processed_images).pooler_output

# Classify with downloaded head
with open("Misc/classifier.pkl", "rb") as f:
    clf = pickle.load(f)
predictions = clf.predict_proba(embeddings.numpy())
```

### Full Implementation
See the [SkinTag repository](https://github.com/skintaglabs/main) for the complete pipeline including web app, mobile distillation, and evaluation.

## Citation

```bibtex
@misc{skintag2026,
  title={SkinTag: AI-Powered Skin Lesion Triage for Equitable Melanoma Detection},
  author={SkinTag Labs},
  year={2026},
  url={https://github.com/skintaglabs/main}
}
```

**Base model (SigLIP):**
```bibtex
@misc{zhai2023sigmoid,
  title={Sigmoid Loss for Language Image Pre-Training},
  author={Xiaohua Zhai and Basil Mustafa and Alexander Kolesnikov and Lucas Beyer},
  year={2023},
  eprint={2303.15343},
  archivePrefix={arXiv},
  primaryClass={cs.CV}
}
```

## Attribution

- **Base Model:** [SigLIP](https://huggingface.co/google/siglip-so400m-patch14-384) by Google (Apache 2.0)
- **Fine-tuning:** SkinTag Labs (MIT)

## Medical Disclaimer

This model is for research and triage screening only, not clinical diagnosis. Users should consult healthcare professionals for medical advice.

## License

MIT License (fine-tuned weights). Base model (SigLIP) is licensed under Apache 2.0 by Google.
"""

operations.append(CommitOperationAdd(
    path_in_repo="README.md",
    path_or_fileobj=readme_content.encode("utf-8"),
))
print("  + README.md (updated model card)")

# --- Step 4: Upload all files in one commit ---
print(f"\nStep 4: Uploading {len(operations)} files to main branch...")
print("  (This may take several minutes for large embedding files)")

api.create_commit(
    repo_id=REPO_ID,
    repo_type="model",
    operations=operations,
    commit_message="Update pipeline artifacts from 5-dataset retraining run (2026-02-05)\n\n"
        "- Updated all Misc/ classifiers and metadata from expanded pipeline\n"
        "- Added fine-tuned classifiers (XGBoost AUC 0.960, MLP AUC 0.945)\n"
        "- Added classifier_deep_mlp.pkl alias for web app compatibility\n"
        "- Updated fine-tuned and frozen embeddings for 47,277 samples\n"
        "- Updated README.md model card with versioning info and latest results",
)

print("\nDone! All files uploaded to main branch.")
print(f"  Repo: https://huggingface.co/{REPO_ID}")
print(f"  Rollback: https://huggingface.co/{REPO_ID}/tree/v1-original")
