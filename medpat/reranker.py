from sentence_transformers import CrossEncoder

from medpat.schema import RetrievedChunk

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_chunks(
        question: str,
        chunks: list[RetrievedChunk],
        top_k: int = 5
) -> list[RetrievedChunk]:
    pairs = [(question, chunk.text) for chunk in chunks]

    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        chunk
        for chunk, score in ranked[:top_k]
    ]
