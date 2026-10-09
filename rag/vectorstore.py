import os

from rag.embeddings import set_up_embedder
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from rag.document_loader import doc_loader
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "policy_documents"


def create_vector_store(chunks, embedder):

    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedder,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=COLLECTION_NAME,
    )


def get_existing_vector_store(embedder):

    return QdrantVectorStore.from_existing_collection(
        embedding=embedder,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=COLLECTION_NAME,
    )

