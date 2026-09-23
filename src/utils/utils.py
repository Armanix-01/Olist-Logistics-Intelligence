import pandas as pd
from pandas import DataFrame
from src.logger.logger import logging
import joblib

def load_csv(path:str):
    logging.info(f"csv file loading from {path}")
    return pd.read_csv(path)


def save_df(path:str, df:DataFrame):
    logging.info(f"Saving DataFrame to: {path}")
    df.to_csv(path_or_buf=path)


def save_artifact(artifact, path):
    logging.info(f"Saving artifact to: {path}")
    joblib.dump(artifact, path)

def load_artifact(path):
    logging.info(f"Loading artifact from: {path}")
    joblib.load(path)