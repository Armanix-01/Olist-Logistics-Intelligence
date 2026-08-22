from src.exception.exception import CustomException
from dataclasses import dataclass
import sys
from pandas import DataFrame

@dataclass
class ExtractionArtifact:
    try:
        customers_df:DataFrame
        geolocation_df:DataFrame
        orders_df:DataFrame
        order_items_df:DataFrame
        order_payments_df:DataFrame
        order_reviews_df:DataFrame
        products_df:DataFrame
        sellers_df:DataFrame
        category_trans_df:DataFrame
    except Exception as e:
        raise CustomException(e, sys)
    