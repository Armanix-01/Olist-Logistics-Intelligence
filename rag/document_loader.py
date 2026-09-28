from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter




def doc_loader(path: Path):

    text = path.read_text(encoding="utf-8")

    docs = [
        Document(
            page_content=text,
            metadata={
                "source": "docs/policy.txt"
            }
        )
    ]


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=70
    )

    chunks = splitter.split_documents(docs)
    return chunks

