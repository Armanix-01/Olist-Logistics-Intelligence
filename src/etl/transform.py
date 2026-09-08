from src.entity.config_entity import ETLTransformConfig
from src.utils.utils import  save_df
import pandas as pd
from src.logger.logger import logging
from src.entity.artifact_entity import ExtractionArtifact, ETLTransformArtifact
class ETLtransformer:
    def __init__(self, config:dict,ExtractionArtifact: ExtractionArtifact):
        self.config = ETLTransformConfig(config= config)
        self.extracted_dfs = ExtractionArtifact


    def transform(self):
        logging.info("Initializing the ETL transformation")
        cleaned_customers_df=self.transform_customers_df()
        cleaned_geolocation_df=self.transform_geolocation_df()
        cleaned_order_items_df=self.transform_order_items_df()
        cleaned_order_payments_df=self.transform_order_payments_df()
        cleaned_order_reviews_df=self.transform_order_reviews_df()
        cleaned_orders_df=self.transform_orders_df()
        cleaned_products_df=self.transform_products_df()
        cleaned_sellers_df=self.transform_sellers_df()
        cleaned_category_trans_df=self.transform_category_trans_df()
        return ETLTransformArtifact(geolocation_df= cleaned_geolocation_df,
                                    category_trans_df=cleaned_category_trans_df,
                                    orders_df= cleaned_orders_df,
                                    order_reviews_df= cleaned_order_reviews_df,
                                    order_payments_df= cleaned_order_payments_df,
                                    order_items_df= cleaned_order_items_df,
                                    sellers_df= cleaned_sellers_df, 
                                    products_df= cleaned_products_df,
                                    customers_df= cleaned_customers_df)


    def transform_customers_df(self):
        customers_df = self.extracted_dfs.customers_df   
        categorical_features = customers_df.select_dtypes(
        include=["object", "string"]
        ).columns
        customers_df["customer_city"] = customers_df["customer_city"].str.lower()
        for each in categorical_features:
            customers_df[each]=customers_df[each].str.strip()
        
        save_df(path=self.config.cleaned_data_path / "cleaned_customers_dataset.csv", df=customers_df)
        return customers_df

    def transform_geolocation_df(self):
        geolocation_df = self.extracted_dfs.geolocation_df
        geolocation_df["geolocation_city"] = geolocation_df["geolocation_city"].str.strip().str.lower()
        save_df(path=self.config.cleaned_data_path / "cleaned_geolocation_dataset.csv", df= geolocation_df)
        return geolocation_df

    def transform_order_items_df(self):
        order_items_df = self.extracted_dfs.order_items_df
        column_to_datetime = "shipping_limit_date"
        order_items_df[column_to_datetime] = pd.to_datetime(order_items_df[column_to_datetime], errors= "coerce")
        save_df(path= self.config.cleaned_data_path / "cleaned_order_items_dataset.csv", df= order_items_df)
        return order_items_df

    def transform_order_payments_df(self):
        order_payments_df = self.extracted_dfs.order_payments_df
        order_payments_df["payment_type"]= order_payments_df["payment_type"].str.strip().str.lower()
        save_df(path=self.config.cleaned_data_path / "cleaned_order_payments_dataset.csv", df= order_payments_df)
        return order_payments_df

    def transform_order_reviews_df(self):
        order_reviews_df = self.extracted_dfs.order_reviews_df
        columns_to_datetime= ("review_creation_date", "review_answer_timestamp")
        for each in columns_to_datetime:
            order_reviews_df[each]= pd.to_datetime(order_reviews_df[each], errors= "coerce")
        columns_to_strip_and_lower = ("review_comment_title", "review_comment_message")
        for each in columns_to_strip_and_lower:
            order_reviews_df[each]= order_reviews_df[each].str.strip().str.lower()
        save_df(path=self.config.cleaned_data_path / "cleaned_order_reviews_dataset.csv", df=order_reviews_df)
        return order_reviews_df

    
    def transform_orders_df(self):
        orders_df = self.extracted_dfs.orders_df
        orders_df["order_status"] = orders_df["order_status"].str.strip().str.lower()
        columns_to_datetime = ("order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date")
        for each in columns_to_datetime:
            orders_df[each] =  pd.to_datetime(orders_df[each], errors= "coerce")
        save_df(path=self.config.cleaned_data_path / "cleaned_orders_dataset.csv", df= orders_df)
        return orders_df 
    
    def transform_products_df(self):
        products_df = self.extracted_dfs.products_df
        products_df["product_category_name"] = products_df["product_category_name"].str.strip().str.lower()
        products_df.rename(
            columns={
                "product_name_lenght":"product_name_length",
                "product_description_lenght":"product_description_length"
            },
            inplace=True
        )
        save_df(path=self.config.cleaned_data_path / "cleaned_products_dataset.csv", df= products_df)
        return products_df

    def transform_sellers_df(self):
        sellers_df = self.extracted_dfs.sellers_df
        sellers_df["seller_city"]= sellers_df["seller_city"].str.strip().str.lower()
        save_df(path= self.config.cleaned_data_path / "cleaned_sellers_dataset.csv", df= sellers_df)
        return sellers_df

    def transform_category_trans_df(self):
        category_trans_df = self.extracted_dfs.category_trans_df
        columns_to_lower_and_strip = ("product_category_name", "product_category_name_english")
        for each in columns_to_lower_and_strip:
            category_trans_df[each]= category_trans_df[each].str.strip().str.lower()
        save_df(path= self.config.cleaned_data_path / "cleaned_category_trans_dataset.csv", df= category_trans_df)
        return category_trans_df

        

        