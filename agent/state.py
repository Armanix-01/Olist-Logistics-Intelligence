from typing import TypedDict


class AgentState(TypedDict, total=False):
    # User's original question
    question: str

    # SQL-related
    sql_query: str
    query_result: list

    # RAG-related
    retrieved_context: str

    # ML prediction-related
    prediction_result: dict

    # Final response
    answer: str