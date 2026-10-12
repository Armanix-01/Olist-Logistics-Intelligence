import joblib
import pandas as pd

from api.config import FINAL_MODEL_PATH
from api.exceptions import PredictionException
from api.logger import logger


class PredictionService:

    def __init__(self):

        try:
            logger.info(
                "Loading model from: %s",
                FINAL_MODEL_PATH
            )

            self.model = joblib.load(FINAL_MODEL_PATH)

            logger.info("Model loaded successfully")

        except Exception as e:

            logger.exception("Failed to load model")

            raise PredictionException(
                "Failed to load prediction model"
            ) from e

    def predict(self, data: dict):

        try:

            logger.info("Starting prediction")

            df = pd.DataFrame([data])

            prediction = self.model.predict(df)[0]

            probability = self.model.predict_proba(df)[0][1]

            result = {
                "is_late": int(prediction),
                "late_probability": float(probability)
            }

            logger.info(
                "Prediction completed successfully"
            )

            return result

        except Exception as e:

            logger.exception(
                "Prediction failed"
            )

            raise PredictionException(
                "Failed to generate prediction"
            ) from e