from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:

    def __init__(self, model_name="all-MiniLM-L6-v2", device="cpu"):
        self.model = SentenceTransformer(model_name, device=device)

    def encode(self, text: str) -> list[float]:
        if not text:
            return []

        emb = self.model.encode(text)

        # normalize for cosine similarity stability
        norm = np.linalg.norm(emb)
        if norm == 0:
            return emb.tolist()

        return (emb / norm).tolist()

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()
    