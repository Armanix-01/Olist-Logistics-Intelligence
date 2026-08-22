## Extracting all the tables or df
import sys
import pandas as pd
from src.logger.logger import logging
from src.exception.exception import CustomException
from src.entity.config_entity import ExtractionConfig
logging.info("Extraction initiated")
try:
    config= ExtractionConfig().from_config()
    customers_df = pd.read_csv(config.customers_data)
    

except Exception as e:
    raise CustomException(e, sys)