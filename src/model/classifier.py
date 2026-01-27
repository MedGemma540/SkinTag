"""Classifier on top of MedSigLIP embeddings."""

import torch
import torch.nn as nn


class EmbeddingClassifier(nn.Module):
    """Lightweight classifier on pre-computed embeddings."""

    def __init__(self, embedding_dim: int, num_classes: int, hidden_dim: int = 256):
        super().__init__()
        self.classifier = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, num_classes),
        )

    def forward(self, embeddings):
        return self.classifier(embeddings)


class ZeroShotClassifier:
    """Zero-shot classification using image-text similarity."""

    def __init__(self, extractor, class_descriptions: list[str]):
        self.extractor = extractor
        self.class_descriptions = class_descriptions
        self.text_embeddings = self._encode_classes()

    def _encode_classes(self):
        return self.extractor.extract_text(self.class_descriptions)

    def predict(self, images):
        """Predict class by finding most similar text description."""
        image_embeddings = self.extractor.extract(images)
        # Normalize
        image_embeddings = image_embeddings / image_embeddings.norm(dim=-1, keepdim=True)
        text_embeddings = self.text_embeddings / self.text_embeddings.norm(dim=-1, keepdim=True)
        # Cosine similarity
        similarity = image_embeddings @ text_embeddings.T
        return similarity.argmax(dim=-1)
