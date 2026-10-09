from langchain_core.tools import tool
from database.prediction.prediction_service import prediction
from agent.schemas import OrderLookupInput
@tool(args_schema= OrderLookupInput)
def predict_delivery_delay(order_id: str):
    """
    Predict whether a specific order is likely to be delivered late.

    This uses the trained machine learning model and
    information available for the order at prediction time.

    Use this when the user asks whether an order is likely
    to be late.

    Args:
        order_id: The unique ID of the order.

    Returns:
        Machine learning prediction where:
        1 means predicted late delivery.
        0 means predicted on-time delivery.
    """
    result = prediction(order_id)

    return {
        "order_id": order_id,
        "is_late": int(result[0])
    }

prediction_tool = [predict_delivery_delay]