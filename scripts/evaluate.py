"""Evaluation script for robustness assessment."""

import yaml
from pathlib import Path


def main():
    # Load config
    config_path = Path(__file__).parent.parent / "configs" / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    print(f"Config: {config}")

    # TODO: Implement evaluation
    # 1. Load test set
    # 2. Apply augmentations to create robustness test sets
    # 3. Evaluate per-group accuracy
    # 4. Generate robustness report


if __name__ == "__main__":
    main()
