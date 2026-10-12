import pandas as pd
import joblib

from api.config import FINAL_MODEL_PATH, PROCESSED_DATA_PATH


# Load the same saved pipeline.
pipeline = joblib.load(FINAL_MODEL_PATH)
preprocessor = pipeline.named_steps["preprocessor"]

# Load a few rows from the same dataset.
df = pd.read_csv(PROCESSED_DATA_PATH, nrows=5)

# Remove the target, whichever name your dataset uses.
target_columns = [
    col for col in ("is_late", "is_late_delivery")
    if col in df.columns
]

X = df.drop(columns=target_columns)

expected = list(preprocessor.feature_names_in_)

print("Expected input columns:", len(expected))
print("Actual input columns:", len(X.columns))
print("Missing columns:", sorted(set(expected) - set(X.columns)))
print("Extra columns:", sorted(set(X.columns) - set(expected)))

# Test the exact saved preprocessor.
try:
    transformed = preprocessor.transform(X)
    print("\nPreprocessor transform: SUCCESS")
    print("Transformed shape:", transformed.shape)
except Exception as exc:
    print("\nPreprocessor transform: FAILED")
    print(type(exc).__name__, exc)

# Test the complete pipeline as well.
try:
    predictions = pipeline.predict(X)
    print("\nFull pipeline prediction: SUCCESS")
    print("Predictions:", predictions)
except Exception as exc:
    print("\nFull pipeline prediction: FAILED")
    print(type(exc).__name__, exc)