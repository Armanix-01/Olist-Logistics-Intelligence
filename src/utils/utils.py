import pandas as pd
from pandas import DataFrame
from src.logger.logger import logging

def load_csv(path:str):
    logging.info(f"csv file loading from {path}")
    return pd.read_csv(path)


def save_df(path:str, df:DataFrame):
    
    df.to_csv(path_or_buf=path)
    