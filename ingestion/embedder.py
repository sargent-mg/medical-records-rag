import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from ingestion.chunker import generate_patient_chunks

load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "medical_records")
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536
BATCH_SIZE = 100

def get_qdrant_client():
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

def setup_collection(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIM,
            distance=Distance.COSINE,
        ),
    )
    print(f"Created collection: {COLLECTION_NAME}")

def embed_and_store(chunks: list[dict]):
    client = get_qdrant_client()
    setup_collection(client)

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    texts = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "patient_id": chunk["patient_id"],
            "full_name": chunk["full_name"],
            "chunk_type": chunk["chunk_type"],
        }
        for chunk in chunks
    ]

    print(f"Embedding {len(texts)} chunks in batches of {BATCH_SIZE}...")

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

    for i in range(0, len(texts), BATCH_SIZE):
        batch_texts = texts[i:i + BATCH_SIZE]
        batch_metadatas = metadatas[i:i + BATCH_SIZE]
        vector_store.add_texts(texts=batch_texts, metadatas=batch_metadatas)
        print(f"  Embedded {min(i + BATCH_SIZE, len(texts))}/{len(texts)}")

    print(f"Done — {len(texts)} chunks stored in Qdrant")
    return vector_store

if __name__ == "__main__":
    chunks = generate_patient_chunks()
    embed_and_store(chunks)