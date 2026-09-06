from src.entity.config_entity import ETLTransformConfig
from src.utils.utils import  save_df
import pandas as pd

class ETLtransformer:
    def __int__(self, ETLTransformConfig: ETLTransformConfig):
        self.config = ETLTransformConfig


    

    def transform_customers_df(self):
        customers_df = self.config.data_frames.customers_df    
        categorical_features = [each for each in customers_df.columns if customers_df[each].dtype=="str"]
        customers_df["customer_city"] = customers_df["customer_city"].str.lower()
        for each in categorical_features:
            customers_df[each]=customers_df[each].str.strip()
        
        save_df(path=self.config.cleaned_data_path / "cleaned_customers_dataset.csv", df=customers_df)

    def transform_geolocation_df(self):
        geolocation_df = self.config.data_frames.geolocation_df
        geolocation_df["geolocation_city"] = geolocation_df["geolocation_city"].str.strip().str.lower()
        save_df(path=self.config.cleaned_data_path / "cleaned_geolocation_dataset.csv", df= geolocation_df)


    def transform_order_items_df(self):
        order_items_df = self.config.data_frames.order_items_df
        column_to_datetime = "shipping_limit_date"
        order_items_df[column_to_datetime] = pd.to_datetime(order_items_df[column_to_datetime])
        save_df(path= self.config.cleaned_data_path / "cleaned_order_items_dataset.csv", df= order_items_df)
    def transform_order_payments_df(self):
        order_payments_df = self.config.data_frames.order_payments_df
        order_payments_df["payment_type"]= order_payments_df["payment_type"].str.strip().str.lower()
        save_df(path=self.config.cleaned_data_path / "cleaned_order_payments_dataset.csv", df= order_payments_df)


    def transform_order_reviews_df(self):
        order_reviews_df = self.config.data_frames.order_reviews_df
        columns_to_datetime= ("review_creation_date", "review_answer_timestamp")
        for each in columns_to_datetime:
            order_reviews_df[each]= pd.to_datetime(order_reviews_df[each])
        columns_to_strip_and_lower = ("review_comment_title", "review_comment_message")
        for each in columns_to_strip_and_lower:
            order_reviews_df[each]= order_reviews_df[each].str.strip().str.lower()
        save_df(path=self.config.cleaned_data_path / "cleaned_order_reviews_dataset.csv", df=order_reviews_df)

    def transform_orders_df(self):
        orders_df = self.config.data_frames.orders_df
        orders_df["order_status"] = orders_df["order_status"].str.strip().str.lower()
        columns_to_datetime = ("order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date")
        for each in columns_to_datetime:
            orders_df[each] =  pd.to_datetime(orders_df[each])
        save_df(path=self.config.cleaned_data_path / "cleaned_orders_dataset.csv")

    def transform_products_df(self):
        products_df = self.config.data_frames.products_df
        products_df["product_category_name"] = products_df["product_category_name"].str.strip().str.lower()
        products_df.rename(columns={"product_name_lenght": "product_name_length"}, inplace=True)
        products_df.rename(columns={"product_description_lenght":"product_description_length"}, inplace=True)
        save_df(path=self.config.cleaned_data_path / "cleaned_products_dataset.csv", df= products_df)


    def transform_sellers_df(self):
        sellers_df = self.config.data_frames.sellers_df
        sellers_df["seller_city"]= sellers_df["seller_city"].str.strip().str.lower()
        save_df(path= self.config.cleaned_data_path / "cleaned_sellers_dataset.csv", df= sellers_df)


    def transform_category_trans_df(self):
        category_trans_df = self.config.data_frames.category_trans_df
        columns_to_lower_and_strip = ("product_category_name", "product_category_name_english")
        for each in columns_to_lower_and_strip:
            category_trans_df[each]= category_trans_df[each].str.strip().str.lower()
        save_df(path= self.config.cleaned_data_path / "cleaned_category_trans_dataset.csv", df= category_trans_df)


        

        