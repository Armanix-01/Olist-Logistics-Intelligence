from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

FINAL_MODEL_PATH = BASE_DIR / "artifacts" / "models" / "final_model.pkl"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "processed.csv"
