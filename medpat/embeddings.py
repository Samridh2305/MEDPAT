from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    """SentenceTransformer embeddings with a deterministic fallback for offline demos."""

    def __init__(
            self,
            model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ) -> None:
        self.model_name = model_name
        self._model = None
        self._model = SentenceTransformer(model_name)

    def encode(
            self,
            texts: list[str]
    ) -> list[list[float]]:
        vectors = self._model.encode(texts, normalize_embeddings=True)
        return [
            vector.tolist()
            for vector in vectors
        ]

