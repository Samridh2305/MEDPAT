from hashlib import sha256
from pathlib import Path

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from extraction.lab_values_context import build_lab_context
from llm.service import LLMClient
from medpat.embeddings import EmbeddingModel
from medpat.reranker import rerank_chunks
from medpat.schema import (
    KnowledgeChunk,
    RetrievedChunk,
    RAGResponse
)


def load_knowledge_base() -> list[KnowledgeChunk]:
    kb_folder = Path("knowledge_base")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    all_chunks: list[KnowledgeChunk] = []

    for file in kb_folder.glob("*.md"):
        text = file.read_text(
            encoding="utf-8"
        )

        chunks = splitter.split_text(text)

        for chunk in chunks:
            all_chunks.append(
                KnowledgeChunk(
                    text=chunk,
                    source=file.name,
                )
            )

    return all_chunks


def build_collection(
        persist_directory: str = "chroma_db",
        collection_name: str = "medical_knowledge",
):
    client = chromadb.PersistentClient(
        path=persist_directory
    )

    return client.get_or_create_collection(
        name=collection_name,
        metadata={
            "hnsw:space": "cosine"
        },
    )


def generate_embeddings(
        chunks: list[KnowledgeChunk],
        embedding_model: EmbeddingModel,
):
    texts = [
        chunk.text
        for chunk in chunks
    ]

    return embedding_model.encode(texts)


def index_chunks(
        collection,
        chunks: list[KnowledgeChunk],
        embeddings,
):
    if not chunks:
        return

    ids = [
        _chunk_id(chunk.text)
        for chunk in chunks
    ]

    documents = [
        chunk.text
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": chunk.source
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def retrieve(
        collection,
        embedding_model: EmbeddingModel,
        query: str,
        limit: int = 20,
) -> list[RetrievedChunk]:
    query_vector = embedding_model.encode(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=limit,
        include=[
            "documents",
            "distances",
            "metadatas",
        ],
    )

    documents = results.get(
        "documents",
        [[]],
    )[0]

    distances = results.get(
        "distances",
        [[]],
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]],
    )[0]

    return [
        RetrievedChunk(
            text=document,
            score=1.0 - float(distance),
            source=metadata.get(
                "source",
                "unknown",
            ),
        )
        for document, distance, metadata in zip(
            documents,
            distances,
            metadatas,
        )
    ]


def answer_question(
        collection,
        embedding_model: EmbeddingModel,
        question: str,
        report_text: str,
        lab_values,
        llm: LLMClient,
) -> RAGResponse:

    lab_context= build_lab_context(lab_values)

    retrieval_query = (
        f"""
    Question:
    {question}

    Extracted Lab Values:
    {lab_context}
    """
    )

    retrieved = retrieve(
        collection=collection,
        embedding_model=embedding_model,
        query=retrieval_query,
        limit=20,
    )

    retrieved = rerank_chunks(
        question=question,
        chunks=retrieved,
        top_k=5,
    )

    context = "\n\n".join(
        chunk.text
        for chunk in retrieved
    )

    answer = llm.generate(
        question=question,
        report_text=report_text,
        lab_context= lab_context,
        context=context,
    )

    sources= list({
        chunk.source
        for chunk in retrieved
    })

    return RAGResponse(
        answer=answer,
        sources=sources,
    )


def _chunk_id(chunk: str) -> str:
    return sha256(
        chunk.encode("utf-8")
    ).hexdigest()
