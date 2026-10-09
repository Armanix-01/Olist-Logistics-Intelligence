from langchain_core.tools import tool
from agent.schemas import RetrieverInput
from rag.retriever import get_retriever

@tool(args_schema=RetrieverInput)
def search_knowledge_base(query: str) -> str:
    """Search business policies, FAQs, documentation,
    and explanations related to the e-commerce platform."""
    retriever = get_retriever()
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found."

    results = []

    for doc in docs:
        results.append(
            f"Content: {doc.page_content}\n"
            f"Source: {doc.metadata.get('source', 'Unknown')}"
        )

    return "\n\n".join(results)

retriever_tool = [search_knowledge_base]