
# api/explanation_service.py

import numpy as np
import pandas as pd
import shap


class ExplanationService:
    def __init__(
        self,
        pipeline,
        background_df: pd.DataFrame,
    ):
        """
        Initialize SHAP using an already-fitted sklearn pipeline.

        Args:
            pipeline: Fitted pipeline containing 'preprocessor'
                     and 'best_model' steps.
            background_df: Representative background data containing
                           only the original model input columns.
        """

        if background_df.empty:
            raise ValueError(
                "Background data cannot be empty."
            )

        # Reuse the fitted preprocessing and model components.
        self.preprocessor = pipeline.named_steps["preprocessor"]
        self.model = pipeline.named_steps["best_model"]

        # This service assumes class 1 means late delivery.
        if not np.array_equal(
            self.model.classes_,
            np.array([0, 1]),
        ):
            raise ValueError(
                "Expected a binary classifier with classes [0, 1]."
            )

        # Get names of the transformed features.
        self.feature_names = (
            self.preprocessor.get_feature_names_out()
        )

        # Transform background data only once.
        background_transformed = (
            self.preprocessor.transform(background_df)
        )

        if hasattr(background_transformed, "toarray"):
            background_transformed = (
                background_transformed.toarray()
            )

        background_transformed = pd.DataFrame(
            background_transformed,
            columns=self.feature_names,
        )

        # Explain class 1 probability: late delivery.
        self.explainer = shap.TreeExplainer(
            self.model,
            data=background_transformed,
            feature_perturbation="interventional",
            model_output="probability",
        )

    def explain(
        self,
        input_df: pd.DataFrame,
        top_k: int = 5,
    ) -> dict:
        """
        Explain one order's predicted late-delivery probability.

        Returns:
            {
                "shap_baseline_probability": float,
                "explanation": [
                    {
                        "feature": str,
                        "shap_value": float,
                        "direction": str
                    }
                ]
            }
        """

        if input_df.empty:
            raise ValueError(
                "Input data cannot be empty."
            )

        if len(input_df) != 1:
            raise ValueError(
                "Explain one order at a time."
            )

        if top_k < 1:
            raise ValueError(
                "top_k must be at least 1."
            )

        # Apply the same fitted preprocessing used by the model.
        transformed = self.preprocessor.transform(input_df)

        if hasattr(transformed, "toarray"):
            transformed = transformed.toarray()

        transformed = pd.DataFrame(
            transformed,
            columns=self.feature_names,
        )

        # Calculate SHAP values for this particular order.
        shap_explanation = self.explainer(transformed)

        values = np.asarray(shap_explanation.values)

        expected_shape = (1, len(self.feature_names))

        if values.shape != expected_shape:
            raise ValueError(
                f"Unexpected SHAP output shape: {values.shape}. "
                f"Expected: {expected_shape}"
            )

        # Extract all feature contributions.
        all_contributions = values[0]

        # Extract and validate the baseline.
        base_values = np.asarray(
            shap_explanation.base_values
        )

        if base_values.size != 1:
            raise ValueError(
                "Unexpected SHAP baseline shape: "
                f"{base_values.shape}"
            )

        baseline = float(base_values.item())

        # Validate SHAP additivity against class 1 probability.
        model_probability = float(
            self.model.predict_proba(transformed)[0, 1]
        )

        reconstructed_probability = (
            baseline + float(all_contributions.sum())
        )

        if not np.isclose(
            reconstructed_probability,
            model_probability,
            atol=1e-4,
        ):
            raise ValueError(
                "SHAP additivity check failed. "
                f"Baseline + SHAP = "
                f"{reconstructed_probability:.6f}; "
                f"model probability = {model_probability:.6f}."
            )

        # Rank features by absolute contribution.
        contributions = pd.DataFrame({
            "feature": self.feature_names,
            "shap_value": all_contributions,
        })

        contributions["absolute_impact"] = (
            contributions["shap_value"].abs()
        )

        contributions = contributions.sort_values(
            "absolute_impact",
            ascending=False,
        ).head(min(top_k, len(contributions)))

        # Convert results into JSON-friendly Python types.
        explanations = []

        for _, row in contributions.iterrows():
            shap_value = float(row["shap_value"])

            if shap_value > 0:
                direction = "increases_late_probability"
            elif shap_value < 0:
                direction = "decreases_late_probability"
            else:
                direction = "no_effect"

            explanations.append({
                "feature": str(row["feature"]),
                "shap_value": shap_value,
                "direction": direction,
            })

        return {
            "shap_baseline_probability": baseline,
            "explanation": explanations,
        }
