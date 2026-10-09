from rag.embeddings import set_up_embedder
from rag.vectorstore import get_existing_vector_store


def get_retriever():
    embedder = set_up_embedder()
    vectorstore = get_existing_vector_store(embedder= embedder)
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )


