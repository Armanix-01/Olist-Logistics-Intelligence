from typing import TypedDict, Annotated
from pydantic import Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from agent.schemas import Plan


from agent.schemas import Plan, SubQuestion


class AgentState(TypedDict, total=False):

    question: str

    plan: Plan

    ready_tasks: list[SubQuestion]

    task_results: Annotated[
        dict[str, str],
        lambda old, new: {**old, **new}
    ]
    answer:str

from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class TaskState(TypedDict, total=False):

    task_id: str

    question: str

    agent: str

    depends_on: list[str]

    # Results from tasks this task depends on
    context: dict[str, str]

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

    result: str

    task_results: Annotated[
        dict[str, str],
        lambda old, new: {**old, **new}
    ]