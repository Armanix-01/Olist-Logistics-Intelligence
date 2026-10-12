from fastapi import FastAPI, HTTPException

from api.schemas import (
    PredictionRequest,
    PredictionResponse
)
from fastapi.responses import StreamingResponse
from api.schemas import AgentRequest
import json
from api.prediction_service import PredictionService
from api.exceptions import PredictionException
from api.logger import logger
from api.schemas import AgentRequest
from agent.graph import graph
import pandas as pd

from api.config import BASE_DIR
from api.explanation_service import ExplanationService
from api.llm_explanation_service import (
    generate_prediction_explanation,
)

app = FastAPI(
    title="Olist Delivery Prediction API",
    description="API for predicting late deliveries",
    version="1.0.0"
)


prediction_service = PredictionService()


@app.get("/")
def root():

    return {
        "message": "Olist Delivery Prediction API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



##SHAP service
SHAP_BACKGROUND_PATH = (
    BASE_DIR
    / "artifacts"
    / "explainability"
    / "shap_background_pool.parquet"
)
background_pool = pd.read_parquet(
    SHAP_BACKGROUND_PATH
)

background_df = background_pool.sample(
    n=min(100, len(background_pool)),
    random_state=42,
)



explanation_service = ExplanationService(
    pipeline=prediction_service.model,
    background_df=background_df,
)

@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(request: PredictionRequest):
    try:
        logger.info("Received prediction request")

        input_data = request.model_dump()

        # 1. Get the prediction result.
        prediction_result = prediction_service.predict(input_data)

        # 2. Calculate SHAP contributions.
        input_df = pd.DataFrame([input_data])

        shap_result = explanation_service.explain(
            input_df,
            top_k=5,
        )

        # 3. Generate the LLM explanation.
        llm_explanation = generate_prediction_explanation(
            prediction=int(prediction_result["is_late"]),
            probability=float(
                prediction_result["late_probability"]
            ),
            shap_result=shap_result,
        )

        # 4. Construct a new response dictionary.
        response_data = {
            **prediction_result,
            "shap_baseline_probability": (
                shap_result["shap_baseline_probability"]
            ),
            "explanation": shap_result["explanation"],
            "llm_explanation": llm_explanation,
        }

        logger.info(
            "Prediction, SHAP, and LLM explanation completed"
        )

        return response_data

    except PredictionException as e:
        logger.error(
            "PredictionException: %s",
            e.message,
        )

        raise HTTPException(
            status_code=500,
            detail=e.message,
        )

    except Exception:
        logger.exception("Unexpected API error")

        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


# --------------------------------------------------
# Agent endpoint
# --------------------------------------------------



def agent_event_stream(question: str):

    initial_state = {
        "question": question
    }

    # Initial update for the frontend
    yield f"data: {json.dumps({'type': 'status', 'message': 'Planning your question...'})}\n\n"

    try:
        for namespace, event in graph.stream(
            initial_state,
            stream_mode="updates",
            subgraphs= True
        ):
            for node_name, update in event.items():
                
                status_messages = {
    "planner": "Breaking your question into tasks...",
    "orchestrator": "Organizing the tasks...",

    "query_worker": "Processing your database question...",
    "query_agent": "Analyzing Olist database data...",
    "query_tool_node": "Executing database tools...",

    "prediction_worker": "Processing delivery prediction...",
    "prediction_agent": "Analyzing delivery risk...",
    "prediction_tool_node": "Running the delivery prediction...",

    "retriever_worker": "Searching the knowledge base...",
    "retriever_agent": "Searching the knowledge base...",
    "retriever_tool_node": "Retrieving relevant information...",

    "final_answer": "Preparing your final answer..."
}

                if node_name == "final_answer":
                    answer = update.get("answer", "")

                    yield (
                        "data: "
                        + json.dumps({
                            "type": "answer",
                            "answer": answer
                        })
                        + "\n\n"
                    )

                elif node_name in status_messages:
                    yield (
                        "data: "
                        + json.dumps({
                            "type": "status",
                            "message": status_messages[node_name]
                        })
                        + "\n\n"
                    )

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    except Exception:
        logger.exception("Agent streaming failed")

        yield (
            "data: "
            + json.dumps({
                "type": "error",
                "message": "The agent could not complete your request."
            })
            + "\n\n"
        )


@app.post("/agent/stream")
def stream_agent(request: AgentRequest):

    return StreamingResponse(
        agent_event_stream(request.question),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )