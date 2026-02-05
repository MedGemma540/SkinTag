"""Upload v2 fine-tuned model to separate branch and access guide to main."""
from pathlib import Path
from huggingface_hub import HfApi, CommitOperationAdd, create_branch

REPO_ID = "skintaglabs/siglip-skin-lesion-classifier"
V2_DIR = Path("results/cache/clinical_v20260204_161741/siglip_finetuned")
V2_CLASSIFIERS = Path("results/cache/clinical_v20260204_161741/classifiers_finetuned")

api = HfApi()

# --- Step 1: Create v2-field-augmented branch ---
print("Step 1: Creating v2-field-augmented branch...")
try:
    create_branch(REPO_ID, branch="v2-field-augmented", repo_type="model")
    print("  Created branch: v2-field-augmented")
except Exception as e:
    if "already exists" in str(e).lower() or "409" in str(e):
        print("  Branch v2-field-augmented already exists (ok)")
    else:
        print(f"  Warning: {e}")

# --- Step 2: Upload v2 model to v2-field-augmented branch ---
print("\nStep 2: Uploading v2 fine-tuned model to v2-field-augmented branch...")
v2_ops = []

# v2 model files
v2_config = V2_DIR / "config.json"
v2_weights = V2_DIR / "siglip_finetuned.pt"

if v2_config.exists():
    v2_ops.append(CommitOperationAdd(
        path_in_repo="v2/config.json",
        path_or_fileobj=str(v2_config),
    ))
    print(f"  + v2/config.json")

if v2_weights.exists():
    size_gb = v2_weights.stat().st_size / 1_000_000_000
    v2_ops.append(CommitOperationAdd(
        path_in_repo="v2/siglip_finetuned.pt",
        path_or_fileobj=str(v2_weights),
    ))
    print(f"  + v2/siglip_finetuned.pt ({size_gb:.1f} GB)")

# v2 fine-tuned classifiers
if V2_CLASSIFIERS.exists():
    for f in V2_CLASSIFIERS.iterdir():
        if f.suffix == ".pkl":
            v2_ops.append(CommitOperationAdd(
                path_in_repo=f"v2/classifiers/{f.name}",
                path_or_fileobj=str(f),
            ))
            print(f"  + v2/classifiers/{f.name}")

if v2_ops:
    print(f"\n  Uploading {len(v2_ops)} files to v2-field-augmented branch...")
    print("  (3.5 GB model -- this will take several minutes)")
    api.create_commit(
        repo_id=REPO_ID,
        repo_type="model",
        revision="v2-field-augmented",
        operations=v2_ops,
        commit_message="Add v2 FineTunableSigLIP model with field augmentations\n\n"
            "- FineTunableSigLIP architecture (hidden_dim=512, unfreeze_layers=4)\n"
            "- Trained with field condition augmentations (blur, noise, lighting, compression)\n"
            "- Fine-tuned XGBoost AUC: 0.960, MLP AUC: 0.945\n"
            "- At 95% sensitivity: 82.5% specificity",
    )
    print("  v2 model uploaded successfully!")

# --- Step 3: Create and upload ACCESS_GUIDE.md to main ---
print("\nStep 3: Creating ACCESS_GUIDE.md...")

guide = """\
# File Access Guide

Quick reference for which files to use from this repository.

## For Web App / Mobile Inference (Production)

The web app loads the **EndToEndSigLIP v1** model from the root of the `main` branch.

| File | Size | Purpose |
|------|------|---------|
| `config.json` | 0.1 KB | Model architecture config (model_name, hidden_dim=256, n_classes, dropout, unfreeze_layers) |
| `model_state.pt` | 3.5 GB | Full fine-tuned SigLIP model weights (EndToEndSigLIP format) |
| `head_state.pt` | 1.2 MB | Classification head weights only (for head-only loading) |

**How to load:**
```python
from src.model.deep_classifier import EndToEndClassifier
model = EndToEndClassifier.load_for_inference("path/to/downloaded/dir")
```

## For Classifier-Only Inference (Lightweight)

Use frozen SigLIP embeddings + a classifier head. No fine-tuned model download needed.

| File | Size | Purpose | AUC |
|------|------|---------|-----|
| `Misc/classifier_deep_mlp.pkl` | 1.2 MB | Deep MLP binary classifier (frozen embeddings) | 0.916 |
| `Misc/classifier_xgboost.pkl` | 1.9 MB | XGBoost binary classifier (frozen embeddings) | 0.916 |
| `Misc/classifier_condition.pkl` | 121 KB | 10-class condition classifier (frozen embeddings) | -- |

**How to load:**
```python
from transformers import AutoModel, AutoImageProcessor
import pickle

processor = AutoImageProcessor.from_pretrained("google/siglip-so400m-patch14-384")
model = AutoModel.from_pretrained("google/siglip-so400m-patch14-384")
embeddings = model.vision_model(pixel_values=images).pooler_output

with open("Misc/classifier_deep_mlp.pkl", "rb") as f:
    clf = pickle.load(f)
probs = clf.predict_proba(embeddings.numpy())
```

## For Best Accuracy (v2 Fine-Tuned Pipeline)

The v2 model uses `FineTunableSigLIP` architecture with field augmentations. Available on the `v2-field-augmented` branch.

| File | Branch | Size | Purpose | AUC |
|------|--------|------|---------|-----|
| `v2/siglip_finetuned.pt` | v2-field-augmented | 3.5 GB | Fine-tuned SigLIP (FineTunableSigLIP, hidden_dim=512) | -- |
| `v2/config.json` | v2-field-augmented | 0.1 KB | v2 architecture config | -- |
| `v2/classifiers/xgboost_finetuned_binary.pkl` | v2-field-augmented | 1.1 MB | XGBoost on fine-tuned embeddings | 0.960 |
| `v2/classifiers/mlp_finetuned_binary.pkl` | v2-field-augmented | 2.9 MB | MLP on fine-tuned embeddings | 0.945 |
| `v2/classifiers/xgboost_finetuned_condition.pkl` | v2-field-augmented | 7.9 MB | 10-class condition (fine-tuned) | -- |

**How to download v2:**
```python
from huggingface_hub import snapshot_download
path = snapshot_download(
    "skintaglabs/siglip-skin-lesion-classifier",
    revision="v2-field-augmented",
    allow_patterns=["v2/*"]
)
```

**How to load v2:**
```python
from scripts.full_retraining_pipeline import FineTunableSigLIP
import torch, json

with open("v2/config.json") as f:
    cfg = json.load(f)
model = FineTunableSigLIP(
    model_name=cfg["model_name"],
    hidden_dim=cfg["hidden_dim"],
    n_classes=cfg["n_classes"],
    dropout=cfg["dropout"],
    unfreeze_layers=cfg["unfreeze_layers"],
)
model.load_state_dict(torch.load("v2/siglip_finetuned.pt", map_location="cpu"))
model.eval()
```

## Research / Reproducibility

Embeddings and metadata for reproducing results without re-running the pipeline.

| File | Size | Purpose |
|------|------|---------|
| `Misc/embeddings.pt` | 109 MB | Frozen SigLIP embeddings (47,277 samples) |
| `Misc/embeddings_finetuned_train.pt` | 174 MB | Fine-tuned embeddings (train split) |
| `Misc/embeddings_finetuned_test.pt` | 44 MB | Fine-tuned embeddings (test split) |
| `Misc/metadata.csv` | 3.2 MB | Full dataset metadata with labels |
| `Misc/test_metadata.csv` | 650 KB | Test split metadata |
| `Misc/evaluation_results.json` | 77 KB | Evaluation metrics (per-group fairness, thresholds) |
| `Misc/training_results.json` | 0.9 KB | Training metrics summary |

## Versioning / Rollback

| Branch | Description |
|--------|-------------|
| `main` | Current production (v1 EndToEndSigLIP + updated classifiers) |
| `v1-original` | Snapshot before 2026-02-05 update (for rollback) |
| `v2-field-augmented` | v2 FineTunableSigLIP with field augmentations (best accuracy) |

```python
from huggingface_hub import snapshot_download
# Production (main)
snapshot_download("skintaglabs/siglip-skin-lesion-classifier")
# Rollback
snapshot_download("skintaglabs/siglip-skin-lesion-classifier", revision="v1-original")
# Best accuracy
snapshot_download("skintaglabs/siglip-skin-lesion-classifier", revision="v2-field-augmented")
```
"""

guide_ops = [CommitOperationAdd(
    path_in_repo="ACCESS_GUIDE.md",
    path_or_fileobj=guide.encode("utf-8"),
)]

api.create_commit(
    repo_id=REPO_ID,
    repo_type="model",
    operations=guide_ops,
    commit_message="Add ACCESS_GUIDE.md with file reference for all use cases",
)
print("  ACCESS_GUIDE.md uploaded to main!")

print("\nAll done!")
print(f"  Main: https://huggingface.co/{REPO_ID}")
print(f"  v2 branch: https://huggingface.co/{REPO_ID}/tree/v2-field-augmented")
print(f"  Access guide: https://huggingface.co/{REPO_ID}/blob/main/ACCESS_GUIDE.md")
