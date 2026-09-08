## Extracting all the tables or df
import sys
from src.entity.artifact_entity import ExtractionArtifact
from src.utils.utils import load_csv
from src.logger.logger import logging
from src.exception.exception import CustomException
from src.entity.config_entity import ExtractionConfig


class DataExtractor:
    
        def __init__(self,  config:dict):
            try:
                
                self.config = ExtractionConfig.from_config(config)
            except Exception as e:
                 raise CustomException(e, sys)
            
        def extract(self):
            try:
                logging.info("Extraction initiated")
                return ExtractionArtifact(
                    customers_df= load_csv(self.config.customers_data),
                    geolocation_df= load_csv(self.config.geolocation_data),
                    order_items_df= load_csv(self.config.order_items_data),
                    order_payments_df= load_csv(self.config.order_payments_data),
                    order_reviews_df= load_csv(self.config.order_reviews_data),
                    orders_df= load_csv(self.config.orders_data),
                    products_df= load_csv(self.config.products_data),
                    sellers_df= load_csv(self.config.sellers_data),
                    category_trans_df= load_csv(self.config.category_translation_data)
                )
                
            except Exception as e:
                 raise CustomException(e, sys)
        

