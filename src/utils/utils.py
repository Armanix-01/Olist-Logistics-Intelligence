import pandas as pd
from src.logger.logger import logging

def load_csv(path:str):
    logging.info
    return pd.read_csv(path)
