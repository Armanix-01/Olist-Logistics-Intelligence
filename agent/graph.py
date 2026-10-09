# agent/graph.py

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from agent.state import AgentState, TaskState

from agent.nodes import (
    planner,
    orchestrator,

    route_tasks,

    query_agent,
    query_tool_node,
    route_query_agent,

    prediction_agent,
    prediction_tool_node,
    route_prediction_agent,

    retriever_agent,
    retriever_tool_node,
    route_retriever_agent,

    finalize_task,
    collect_result,

    final_answer,
)

def build_query_worker():

    builder = StateGraph(TaskState)

    builder.add_node(
        "query_agent",
        query_agent
    )

    builder.add_node(
        "query_tool_node",
        query_tool_node
    )

    builder.add_node(
        "finalize_task",
        finalize_task
    )

    builder.add_node(
        "collect_result",
        collect_result
    )

    builder.add_edge(
        START,
        "query_agent"
    )

    builder.add_conditional_edges(
        "query_agent",
        route_query_agent,
        {
            "query_tool_node": "query_tool_node",
            "finalize_task": "finalize_task",
        }
    )

    builder.add_edge(
        "query_tool_node",
        "query_agent"
    )

    builder.add_edge(
        "finalize_task",
        "collect_result"
    )

    builder.add_edge(
        "collect_result",
        END
    )

    return builder.compile()


def build_prediction_worker():

    builder = StateGraph(TaskState)

    builder.add_node(
        "prediction_agent",
        prediction_agent
    )

    builder.add_node(
        "prediction_tool_node",
        prediction_tool_node
    )

    builder.add_node(
        "finalize_task",
        finalize_task
    )

    builder.add_node(
        "collect_result",
        collect_result
    )

    builder.add_edge(
        START,
        "prediction_agent"
    )

    builder.add_conditional_edges(
        "prediction_agent",
        route_prediction_agent,
        {
            "prediction_tool_node": "prediction_tool_node",
            "finalize_task": "finalize_task",
        }
    )

    builder.add_edge(
        "prediction_tool_node",
        "prediction_agent"
    )

    builder.add_edge(
        "finalize_task",
        "collect_result"
    )

    builder.add_edge(
        "collect_result",
        END
    )

    return builder.compile()

def build_retriever_worker():

    builder = StateGraph(TaskState)

    builder.add_node(
        "retriever_agent",
        retriever_agent
    )

    builder.add_node(
        "retriever_tool_node",
        retriever_tool_node
    )

    builder.add_node(
        "finalize_task",
        finalize_task
    )

    builder.add_node(
        "collect_result",
        collect_result
    )

    builder.add_edge(
        START,
        "retriever_agent"
    )

    builder.add_conditional_edges(
        "retriever_agent",
        route_retriever_agent,
        {
            "retriever_tool_node": "retriever_tool_node",
            "finalize_task": "finalize_task",
        }
    )

    builder.add_edge(
        "retriever_tool_node",
        "retriever_agent"
    )

    builder.add_edge(
        "finalize_task",
        "collect_result"
    )

    builder.add_edge(
        "collect_result",
        END
    )

    return builder.compile()

def route_after_orchestrator(state: AgentState):

    plan = state["plan"]

    task_results = state.get(
        "task_results",
        {}
    )

    all_completed = all(
        task.id in task_results
        for task in plan.subquestions
    )

    if all_completed:
        return "final_answer"

    return route_tasks(state)


def build_graph():

    query_worker = build_query_worker()
    prediction_worker = build_prediction_worker()
    retriever_worker = build_retriever_worker()

    builder = StateGraph(AgentState)

    # -------------------------
    # Parent graph nodes
    # -------------------------

    builder.add_node(
        "planner",
        planner
    )

    builder.add_node(
        "orchestrator",
        orchestrator
    )

    builder.add_node(
        "query_worker",
        query_worker
    )

    builder.add_node(
        "prediction_worker",
        prediction_worker
    )

    builder.add_node(
        "retriever_worker",
        retriever_worker
    )

    builder.add_node(
        "final_answer",
        final_answer
    )

    # -------------------------
    # Main flow
    # -------------------------

    builder.add_edge(
        START,
        "planner"
    )

    builder.add_edge(
        "planner",
        "orchestrator"
    )

    # -------------------------
    # Dynamic routing
    # -------------------------

    builder.add_conditional_edges(
        "orchestrator",
        route_after_orchestrator,
        [
            "query_worker",
            "prediction_worker",
            "retriever_worker",
            "final_answer",
        ]
    )

    # -------------------------
    # Workers return to
    # orchestrator
    # -------------------------

    builder.add_edge(
        "query_worker",
        "orchestrator"
    )

    builder.add_edge(
        "prediction_worker",
        "orchestrator"
    )

    builder.add_edge(
        "retriever_worker",
        "orchestrator"
    )

    # -------------------------
    # Final answer
    # -------------------------

    builder.add_edge(
        "final_answer",
        END
    )

    return builder.compile()


graph = build_graph()
