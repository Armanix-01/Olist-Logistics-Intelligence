from dataclasses import dataclass
from pandas import DataFrame



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