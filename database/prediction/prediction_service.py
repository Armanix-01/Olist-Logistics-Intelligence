from functools import lru_cache
import joblib

from database.prediction.prediction_query import get_prediction_data
from database.prediction.prediction_features import create_prediction_features
from database.connection import PROJECT_ROOT


MODEL_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "models"
    / "final_model.pkl"
)


@lru_cache(maxsize=1)
def get_model():
    return joblib.load(MODEL_PATH)


def prediction(order_id: str):

    query_res = get_prediction_data(
        order_id=order_id
    )

    if query_res is None:
        raise ValueError(
            f"Order {order_id} was not found in the database."
        )

    df = create_prediction_features(query_res)

    model = get_model()

    result = model.predict(df)

    return result


# from database.prediction.prediction_query import get_prediction_data
# from database.prediction.prediction_features import create_prediction_features
# from database.connection import PROJECT_ROOT

# import joblib


# MODEL_PATH = (
#     PROJECT_ROOT
#     / "artifacts"
#     / "models"
#     / "final_model.pkl"
# )


# class PredictionService:

#     def __init__(self):

#         print("Loading prediction model...")

#         self.model = joblib.load(MODEL_PATH)

#         print("Prediction model loaded successfully")


#     def prediction(self, order_id: str):

#         print("STEP 1: Getting prediction data")

#         query_res = get_prediction_data(
#             order_id=order_id
#         )

#         print("STEP 2: Query result")
#         print(query_res)

#         if query_res is None:
#             raise ValueError(
#                 f"Order {order_id} was not found."
#             )

#         print("STEP 3: Creating prediction features")

#         df = create_prediction_features(
#             query_res
#         )

#         print("STEP 4: Features")
#         print(df)

#         print("STEP 5: Making prediction")

#         result = self.model.predict(df)

#         probability = self.model.predict_proba(df)[0][1]

#         print("STEP 6: Prediction completed")
#         print("Prediction:", result)
#         print("Probability:", probability)

#         return {
#             "is_late": int(result[0]),
#             "late_probability": float(probability)
#         }


# if __name__ == "__main__":

#     service = PredictionService()

#     result = service.prediction(
#         order_id="53cdb2fc8bc7dce0b6741e2150273451"
#     )

#     print("\nFINAL RESULT:")
#     print(result)