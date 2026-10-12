import joblib
import pandas as pd

from api.config import (
    BASE_DIR,
    FINAL_MODEL_PATH,
    PROCESSED_DATA_PATH,
)


def main():
    # 1. Load the fitted pipeline.
    pipeline = joblib.load(FINAL_MODEL_PATH)

    preprocessor = pipeline.named_steps["preprocessor"]

    # 2. Load the dataset used as the background source.
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # 3. Remove the target column.
    target_columns = [
        col
        for col in ("is_late", "is_late_delivery")
        if col in df.columns
    ]

    if not target_columns:
        raise ValueError(
            "Could not find the target column in processed.csv."
        )

    X_background = df.drop(columns=target_columns)

    # 4. Remove accidental CSV index columns if any exist.
    X_background = X_background.loc[
        :,
        ~X_background.columns.str.match(
            r"^Unnamed:\s*\d+$",
            case=False,
        ),
    ]

    # 5. Create a reproducible pool of 500 rows.
    background_pool = X_background.sample(
        n=min(500, len(X_background)),
        random_state=42,
    )

    # 6. Verify that the actual preprocessor accepts these rows.
    transformed = preprocessor.transform(background_pool)

    print("Background pool shape:", background_pool.shape)
    print("Transformed shape:", transformed.shape)

    # 7. Save the background pool.
    output_path = (
        BASE_DIR
        / "artifacts"
        / "explainability"
        / "shap_background_pool.parquet"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    background_pool.to_parquet(
        output_path,
        index=False,
    )

    print("SHAP background pool saved successfully.")
    print("Path:", output_path)


if __name__ == "__main__":
    main()