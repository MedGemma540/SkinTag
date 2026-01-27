"""MedSigLIP embedding extraction."""

import torch
from transformers import AutoModel, AutoProcessor


class EmbeddingExtractor:
    """Extract embeddings using MedSigLIP vision encoder."""

    def __init__(self, model_name: str = "google/siglip-so400m-patch14-384", device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model.eval()

    @torch.no_grad()
    def extract(self, images):
        """Extract embeddings from a batch of images.

        Args:
            images: List of PIL images or tensor batch

        Returns:
            Tensor of shape (batch_size, embedding_dim)
        """
        inputs = self.processor(images=images, return_tensors="pt").to(self.device)
        outputs = self.model.get_image_features(**inputs)
        return outputs

    @torch.no_grad()
    def extract_text(self, texts):
        """Extract text embeddings for zero-shot classification.

        Args:
            texts: List of text descriptions

        Returns:
            Tensor of shape (num_texts, embedding_dim)
        """
        inputs = self.processor(text=texts, return_tensors="pt", padding=True).to(self.device)
        outputs = self.model.get_text_features(**inputs)
        return outputs
