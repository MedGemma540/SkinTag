"""Training script for skin lesion classifier."""

import yaml
from pathlib import Path


def main():
    # Load config
    config_path = Path(__file__).parent.parent / "configs" / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    print(f"Config: {config}")

    # TODO: Implement training loop
    # 1. Load dataset
    # 2. Extract embeddings (once)
    # 3. Train classifier on embeddings
    # 4. Save model


if __name__ == "__main__":
    main()
