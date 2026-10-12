
# api/llm_explanation_service.py

import json

from agent.llms import general_llm


EXPLANATION_PROMPT = """
You are an AI explanation assistant for an Olist
e-commerce delivery prediction application.

Your task is to explain a machine-learning prediction
using the verified prediction and SHAP results provided.

Rules:
1. Class 1 means late delivery.
2. Class 0 means the model predicts no late delivery.
3. Explain the predicted late-delivery probability clearly.
4. A positive SHAP value pushes the late-delivery
   probability higher relative to the baseline.
5. A negative SHAP value pushes the late-delivery
   probability lower relative to the baseline.
6. Explain only the supplied feature contributions.
7. Do not invent feature values, facts, or explanations.
8. SHAP contributions describe model behavior and do not
   prove that a feature caused the delivery outcome.
9. Do not interpret an individual SHAP value as a standalone
   probability or as a percentage-point change unless
   correctly calculated and explained.
10. The supplied features are only the most influential
    features, not necessarily every factor in the prediction.
11. Distinguish the predicted class from its probability.
12. Keep the response clear, concise, and understandable
    to someone without machine-learning knowledge.

Use this structure:
- Prediction: State the predicted outcome and probability.
- Main factors increasing the late-delivery probability.
- Main factors decreasing the late-delivery probability.
- Important caveat: This is a model estimate, not a guarantee.

If no features contribute in one direction, state that
the supplied top features do not show a meaningful
contribution in that direction.
"""


def generate_prediction_explanation(
    prediction: int,
    probability: float,
    shap_result: dict,
) -> str:
    """
    Generate a natural-language explanation using general_llm.

    Args:
        prediction: Predicted class (0 or 1).
        probability: Predicted probability of late delivery.
        shap_result: Output returned by ExplanationService.explain().

    Returns:
        Natural-language explanation as a string.
    """

    if prediction not in (0, 1):
        raise ValueError(
            "Prediction must be either 0 or 1."
        )

    if not 0.0 <= probability <= 1.0:
        raise ValueError(
            "Probability must be between 0 and 1."
        )

    if "shap_baseline_probability" not in shap_result:
        raise ValueError(
            "SHAP result is missing the baseline probability."
        )

    if "explanation" not in shap_result:
        raise ValueError(
            "SHAP result is missing feature contributions."
        )

    context = {
        "predicted_class": prediction,
        "predicted_outcome": (
            "Late delivery"
            if prediction == 1
            else "Not late"
        ),
        "late_delivery_probability": probability,
        "shap_baseline_probability": (
            shap_result["shap_baseline_probability"]
        ),
        "top_feature_contributions": (
            shap_result["explanation"]
        ),
    }

    messages = [
        {
            "role": "system",
            "content": EXPLANATION_PROMPT,
        },
        {
            "role": "user",
            "content": (
                "Explain this prediction using the following "
                "verified model results:\n\n"
                + json.dumps(context, indent=2)
            ),
        },
    ]

    response = general_llm.invoke(messages)

    if not isinstance(response.content, str):
        raise ValueError(
            "The LLM returned a non-text response."
        )

    explanation = response.content.strip()

    if not explanation:
        raise ValueError(
            "The LLM returned an empty explanation."
        )

    return explanation
