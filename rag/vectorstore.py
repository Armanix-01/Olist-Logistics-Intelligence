import os

from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


def create_vector_store(chunks, embedder):

    vectorstore = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedder,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name="policy_documents",
    )

    return vectorstore
