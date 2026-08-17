import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from qdrant_client import QdrantClient
from ingestion.chunker import generate_patient_chunks

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "medical_records")
EMBEDDING_MODEL = "text-embedding-3-small"

def get_ensemble_retriever(k: int = 5) -> EnsembleRetriever:
    # Dense retriever — Qdrant
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    dense_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )

    # Sparse retriever — BM25
    chunks = generate_patient_chunks()
    texts = [chunk["text"] for chunk in chunks]
    bm25_retriever = BM25Retriever.from_texts(texts)
    bm25_retriever.k = k

    # Ensemble — equal weights
    ensemble_retriever = EnsembleRetriever(
        retrievers=[dense_retriever, bm25_retriever],
        weights=[0.5, 0.5],
    )

    return ensemble_retriever