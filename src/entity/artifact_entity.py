from dataclasses import dataclass
from pandas import DataFrame
import numpy as np
import pandas as pd



@dataclass
class ExtractionArtifact:

    customers_df:DataFrame
    geolocation_df:DataFrame
    orders_df:DataFrame
    order_items_df:DataFrame
    order_payments_df:DataFrame
    order_reviews_df:DataFrame
    products_df:DataFrame
    sellers_df:DataFrame
    category_trans_df:DataFrame



@dataclass
class ETLTransformArtifact:
    customers_df: DataFrame
    geolocation_df: DataFrame
    orders_df: DataFrame
    order_items_df: DataFrame
    order_payments_df: DataFrame
    order_reviews_df: DataFrame
    products_df: DataFrame
    sellers_df: DataFrame
    category_trans_df: DataFrame

    def as_dict(self):
        return {
            "customers": self.customers_df,
            "sellers": self.sellers_df,
            "geolocation": self.geolocation_df,
            "category_name_translation": self.category_trans_df,
            "products": self.products_df,
            "orders": self.orders_df,
            "order_items": self.order_items_df,
            "order_payments": self.order_payments_df,
            "order_reviews": self.order_reviews_df,
            
            
            
        }

@dataclass
class ETLLoadArtifact:
    pass


@dataclass
class DataIngestionArtifact:
    Ingested_df:DataFrame


@dataclass
class DataTransformationArtifact:
    transformed_df:DataFrame


@dataclass
class PreProcessingArtifact:
    x_train: pd.DataFrame | np.ndarray
    y_train: pd.Series | np.ndarray
    x_test: pd.DataFrame | np.ndarray
    y_test: pd.Series | np.ndarray