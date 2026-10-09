from agent.schemas import  Plan
from agent.llms import general_llm, query_llm
from agent.state import AgentState, TaskState
from agent.prompts import  QUERY_AGENT_PROMPT, PREDICTION_AGENT_PROMPT, RETRIEVER_AGENT_PROMPT, FINAL_ANSWER_PROMPT, PLANNER_PROMPT
from agent.tools.query_tools import QUERY_TOOLS
from agent.tools.retriever_tool import retriever_tool
from agent.tools.prediction_tools import prediction_tool
from agent.tools.custom_sql_tools import run_custom_sql_query
from langgraph.prebuilt import ToolNode
from langgraph.types import Send

##Planner node
planner_llm = general_llm.with_structured_output(Plan)
def planner(state: AgentState) -> dict:
    question = state["question"]

    messages = [
        {
            "role": "system",
            "content": PLANNER_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    plan = planner_llm.invoke(messages)

    return {
        "plan": plan
    }

##Orchestrator node
def orchestrator(state: AgentState) -> dict:

    plan = state["plan"]

    completed_results = state.get(
        "task_results",
        {}
    )

    ready_tasks = []

    for task in plan.subquestions:

        if task.id in completed_results:
            continue

        dependencies_completed = all(
            dependency_id in completed_results
            for dependency_id in task.depends_on
        )

        if dependencies_completed:
            ready_tasks.append(task)

    return {
        "ready_tasks": ready_tasks
    }



def route_tasks(state: AgentState):

    ready_tasks = state.get("ready_tasks", [])
    task_results = state.get("task_results", {})

    sends = []

    for task in ready_tasks:

        dependency_results = {
            dependency_id: task_results[dependency_id]
            for dependency_id in task.depends_on
        }

        task_state = {
            "task_id": task.id,
            "question": task.question,
            "agent": task.agent,
            "depends_on": task.depends_on,
            "context": dependency_results,
        }

        

        if task.agent == "query":

            sends.append(
                Send(
                    "query_agent",
                    task_state
                )
            )

        elif task.agent == "prediction":

            sends.append(
                Send(
                    "prediction_agent",
                    task_state
                )
            )

        elif task.agent == "retriever":

            sends.append(
                Send(
                    "retriever_agent",
                    task_state
                )
            )

    return sends


query_agent_tools = QUERY_TOOLS + [run_custom_sql_query]
query_llm_with_tools = query_llm.bind_tools(tools= query_agent_tools)
query_tool_node = ToolNode(query_agent_tools)

def query_agent(state: TaskState) -> dict:

    messages = state.get("messages", [])

    if not messages:
        messages = [
            {
                "role": "system",
                "content": QUERY_AGENT_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Task:
{state["question"]}

Information from dependent tasks:
{state.get("context", {})}
"""
            }
        ]

    response = query_llm_with_tools.invoke(messages)

    if not state.get("messages"):
        return {
            "messages": messages + [response]
        }

    return {
        "messages": [response]
    }


prediction_tools = prediction_tool
prediction_llm_with_tools = general_llm.bind_tools(
    prediction_tool
)
prediction_tool_node = ToolNode(
    prediction_tool)
def prediction_agent(state: TaskState) -> dict:

    messages = state.get("messages", [])

    if not messages:
        messages = [
            {
                "role": "system",
                "content": PREDICTION_AGENT_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Task:
{state["question"]}

Information from dependent tasks:
{state.get("context", {})}
"""
            }
        ]

    response = prediction_llm_with_tools.invoke(messages)

    if not state.get("messages"):
        return {
            "messages": messages + [response]
        }

    return {
        "messages": [response]
    }

retriever_tools = retriever_tool
retriever_llm_with_tools = general_llm.bind_tools(
    retriever_tool
)
retriever_tool_node = ToolNode(
    retriever_tool
)
def retriever_agent(state: TaskState) -> dict:

    messages = state.get("messages", [])

    if not messages:
        messages = [
            {
                "role": "system",
                "content": RETRIEVER_AGENT_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Task:
{state["question"]}

Information from dependent tasks:
{state.get("context", {})}
"""
            }
        ]

    response = retriever_llm_with_tools.invoke(messages)

    if not state.get("messages"):
        return {
            "messages": messages + [response]
        }

    return {
        "messages": [response]
    }

def finalize_task(state: TaskState) -> dict:

    last_message = state["messages"][-1]

    return {
        "result": last_message.content
    }

def collect_result(state: TaskState) -> dict:

    return {
        "task_results": {
            state["task_id"]: state["result"]
        }
    }
def final_answer(state: AgentState) -> dict:

    question = state["question"]

    task_results = state.get(
        "task_results",
        {}
    )

    context = "\n\n".join(
        f"Task {task_id}:\n{result}"
        for task_id, result in task_results.items()
    )

    messages = [
        {
            "role": "system",
            "content": FINAL_ANSWER_PROMPT
        },
        {
            "role": "user",
            "content": f"""
        Original question:
        {question}

        Results from completed tasks:
        {context}

        Use ONLY the information provided in the task results.
        Synthesize them into a clear answer to the original question.
        Do not mention internal task IDs or the multi-agent architecture.
        """
        }
            ]

    response = general_llm.invoke(messages)

    return {
        "answer": response.content
    }


##ROUTING FUNCTIONS
def route_query_agent(state: TaskState):

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "query_tool_node"

    return "finalize_task"


def route_prediction_agent(state: TaskState):

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "prediction_tool_node"

    return "finalize_task"


def route_retriever_agent(state: TaskState):

    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "retriever_tool_node"

    return "finalize_task"