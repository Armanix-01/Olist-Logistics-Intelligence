from fastapi import FastAPI, HTTPException

from api.schemas import (
    PredictionRequest,
    PredictionResponse
)
from api.prediction_service import PredictionService
from api.exceptions import PredictionException
from api.logger import logger


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


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: PredictionRequest):

    try:

        logger.info("Received prediction request")

        result = prediction_service.predict(
            request.model_dump()
        )

        return result

    except PredictionException as e:

        logger.error(
            "PredictionException: %s",
            e.message
        )

        raise HTTPException(
            status_code=500,
            detail=e.message
        )

    except Exception:

        logger.exception(
            "Unexpected API error"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )