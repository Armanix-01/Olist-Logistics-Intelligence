import pandas as pd
from pandas import DataFrame
from src.logger.logger import logging
import joblib
import os
import sys
import numpy as np
from pathlib import Path
import yaml

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
    return joblib.load(path)




def save_numpy_array_data(
    file_path: str,
    array: np.ndarray
):

    dir_path = os.path.dirname(file_path)

    os.makedirs(
        dir_path,
        exist_ok=True
    )

    np.save(
        file_path,
        array
    )


def load_numpy_array_data(
    file_path: str
) -> np.ndarray:

    return np.load(
        file_path
    )



def read_yaml(file_path: Path):
    with file_path.open() as f:
        data = yaml.safe_load(f)

    return data
