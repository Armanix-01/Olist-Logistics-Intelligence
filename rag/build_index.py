from pathlib import Path
from rag.document_loader import doc_loader
from rag.embeddings import set_up_embedder
from rag.vectorstore import create_vector_store

PROJECT_DIR = Path(__file__).resolve().parents[1]
file_path = PROJECT_DIR / "docs" / "policy.txt"


chunks = doc_loader(path=file_path)
embedder = set_up_embedder()
create_vector_store(chunks=chunks, embedder=embedder)
print("vectore store build successfully")

