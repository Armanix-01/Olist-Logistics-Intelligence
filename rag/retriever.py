from rag.vectorstore import create_vector_store
from rag.document_loader import doc_loader
from pathlib import Path
from rag.embeddings import set_up_embedder
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
file_path = PROJECT_DIR / "docs" / "policy.txt"


chunks = doc_loader(path=file_path)
embedder = set_up_embedder()
vectorstore = create_vector_store(chunks=chunks, embedder=embedder)
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)
