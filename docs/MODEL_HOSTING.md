# Model Hosting with Hugging Face

SkinTag uses Hugging Face Hub for hosting and distributing trained model artifacts.

## Quick Start

### Using Models from Hugging Face

Set environment variable to enable HF downloads:

```bash
export USE_HF_MODELS=true
export HF_REPO_ID=MedGemma540/skintag-models  # Optional: override default repo
make app
```

The app will automatically download models from Hugging Face on first startup.

### Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_HF_MODELS` | `false` | Enable downloading from Hugging Face |
| `HF_REPO_ID` | `MedGemma540/skintag-models` | Hugging Face repository |
| `HF_CLASSIFIER_FILE` | `classifier_deep_mlp.pkl` | Main classifier filename |
| `HF_CONDITION_FILE` | `classifier_condition.pkl` | Condition classifier filename |
| `HF_TOKEN` | - | HF API token (for private repos) |
| `HF_HOME` | `~/.cache/huggingface` | Cache directory |

## Uploading Models to Hugging Face

### 1. Install Hugging Face CLI

```bash
pip install huggingface_hub[cli]
```

### 2. Login

```bash
huggingface-cli login
```

### 3. Upload Models

```bash
# Upload classifier
huggingface-cli upload MedGemma540/skintag-models \
    results/cache/classifier_deep_mlp.pkl \
    classifier_deep_mlp.pkl

# Upload condition classifier
huggingface-cli upload MedGemma540/skintag-models \
    results/cache/classifier_condition.pkl \
    classifier_condition.pkl
```

### 4. Make Repository Public (Optional)

Go to https://huggingface.co/MedGemma540/skintag-models/settings

## Model Architecture

Models stored on Hugging Face:

- `classifier_deep_mlp.pkl`: Deep MLP classifier (SigLIP embeddings → binary classification)
- `classifier_condition.pkl`: Condition classifier (SigLIP embeddings → 10-class diagnosis)
- `finetuned_model/`: End-to-end fine-tuned model (optional, higher accuracy)

## Local Development

For local development without Hugging Face:

```bash
# Train models locally
make train-all

# Run app with local cache
make app
```

Models are cached in `results/cache/` and loaded automatically.

## Caching

Downloaded models are cached locally:

- **Location**: `$HF_HOME/skintag/` (default: `~/.cache/huggingface/skintag/`)
- **Behavior**: Downloaded once, reused on subsequent runs
- **Clear cache**: `rm -rf ~/.cache/huggingface/skintag/`

## Private Repositories

For private model repositories:

```bash
export HF_TOKEN=hf_your_token_here
export USE_HF_MODELS=true
make app
```

Or pass token in code (see `src/utils/model_hub.py`).

## Integration

The download logic is in `src/utils/model_hub.py`:

```python
from src.utils.model_hub import download_model_from_hf

model_path = download_model_from_hf(
    repo_id="MedGemma540/skintag-models",
    filename="classifier_deep_mlp.pkl",
    cache_subdir="skintag"
)
```

Automatic caching ensures models are only downloaded once.
