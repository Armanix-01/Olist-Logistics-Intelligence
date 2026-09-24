import logging
import pandas as pd
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact
)
from src.utils.utils import save_df, load_csv


class DataTransformation:

    def __init__(
        self,
        config: dict,
        data_ingestion_artifact: DataIngestionArtifact
    ):

        self.config = DataTransformationConfig(config=config)

        self.processed_dataset_path = (
            self.config.processed_dataset_dir / "processed.csv"
        )

        self.ingested_df_path = (
            data_ingestion_artifact.ingested_data_file_path
        )

        logging.info(
            "DataTransformation initialized. "
            "Input file: %s",
            self.ingested_df_path
        )

    def feature_eng(self) -> DataTransformationArtifact:

        logging.info("Starting data transformation and feature engineering.")

        try:
            df = load_csv(
                path=self.ingested_df_path
            ).copy()

            logging.info(
                "Initial dataframe shape: %s",
                df.shape
            )

            
            # Validate required columns
           

            required_columns = [
                "order_purchase_timestamp",
                "order_approved_at",
                "order_estimated_delivery_date",
                "payment_type",
                "product_category_name",
                "is_late"
            ]

            missing_columns = [
                col for col in required_columns
                if col not in df.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"Required columns are missing: {missing_columns}"
                )

            logging.info("Required columns validation successful.")
            timestamp_cols = [
                "order_purchase_timestamp",
                "order_approved_at",
                "order_estimated_delivery_date"
            ]

            for col in timestamp_cols:
                df[col] = pd.to_datetime(
                    df[col],
                    errors="coerce"
                )
            
            #  Remove unnecessary columns
            

            remove_cols = [
                "order_id",
                "customer_id",
                "customer_unique_id",
                "customer_city",
                "seller_city",
                "order_delivered_carrier_date",
                "order_delivered_customer_date",
                "average_review_score"
            ]

            existing_remove_cols = [
                col for col in remove_cols
                if col in df.columns
            ]

            df.drop(
                columns=existing_remove_cols,
                inplace=True
            )

            logging.info(
                "Removed %d unnecessary columns.",
                len(existing_remove_cols)
            )

           
            # Timestamp feature engineering
          

            logging.info("Creating timestamp-based features.")

            df["order_purchase_hour"] = (
                df["order_purchase_timestamp"].dt.hour
            )

            df["order_purchase_day_of_week"] = (
                df["order_purchase_timestamp"].dt.dayofweek
            )

            df["order_purchase_month"] = (
                df["order_purchase_timestamp"].dt.month
            )

            df["order_purchase_year"] = (
                df["order_purchase_timestamp"].dt.year
            )

            df["order_approval_delay_hours"] = (
                df["order_approved_at"]
                - df["order_purchase_timestamp"]
            ).dt.total_seconds() / 3600

            df["estimated_delivery_days"] = (
                df["order_estimated_delivery_date"]
                - df["order_purchase_timestamp"]
            ).dt.total_seconds() / 86400

            logging.info(
                "Timestamp feature engineering completed."
            )

           
            # Handle categorical values
           

            logging.info(
                "Handling categorical features."
            )

            # Missing payment type
            df["payment_type"] = (
                df["payment_type"].fillna("unknown")
            )

            category_mapping = {

                # Home & Furniture
                "moveis_decoracao": "Home & Furniture",
                "cama_mesa_banho": "Home & Furniture",
                "utilidades_domesticas": "Home & Furniture",
                "moveis_escritorio": "Home & Furniture",
                "moveis_cozinha_area_de_servico_jantar_e_jardim": "Home & Furniture",
                "casa_conforto": "Home & Furniture",
                "moveis_sala": "Home & Furniture",
                "moveis_quarto": "Home & Furniture",
                "casa_conforto_2": "Home & Furniture",
                "moveis_colchao_e_estofado": "Home & Furniture",

                # Home Appliances
                "eletrodomesticos": "Home Appliances",
                "portateis_casa_forno_e_cafe": "Home Appliances",
                "eletroportateis": "Home Appliances",
                "eletrodomesticos_2": "Home Appliances",
                "portateis_cozinha_e_preparadores_de_alimentos": "Home Appliances",
                "climatizacao": "Home Appliances",

                # Electronics & Computers
                "eletronicos": "Electronics & Computers",
                "informatica_acessorios": "Electronics & Computers",
                "audio": "Electronics & Computers",
                "pcs": "Electronics & Computers",
                "pc_gamer": "Electronics & Computers",
                "tablets_impressao_imagem": "Electronics & Computers",

                # Telephony
                "telefonia": "Telephony",
                "telefonia_fixa": "Telephony",

                # Fashion
                "fashion_bolsas_e_acessorios": "Fashion",
                "fashion_underwear_e_moda_praia": "Fashion",
                "fashion_roupa_masculina": "Fashion",
                "fashion_calcados": "Fashion",
                "fashion_roupa_feminina": "Fashion",
                "fashion_esporte": "Fashion",
                "fashion_roupa_infanto_juvenil": "Fashion",
                "malas_acessorios": "Fashion",

                # Beauty & Personal Care
                "perfumaria": "Beauty & Personal Care",
                "beleza_saude": "Beauty & Personal Care",
                "fraldas_higiene": "Beauty & Personal Care",

                # Sports & Leisure
                "esporte_lazer": "Sports & Leisure",
                "consoles_games": "Sports & Leisure",
                "instrumentos_musicais": "Sports & Leisure",
                "cool_stuff": "Sports & Leisure",

                # Books & Media
                "livros_tecnicos": "Books & Media",
                "livros_interesse_geral": "Books & Media",
                "livros_importados": "Books & Media",
                "musica": "Books & Media",
                "cds_dvds_musicais": "Books & Media",
                "dvds_blu_ray": "Books & Media",

                # Baby & Kids
                "bebes": "Baby & Kids",
                "brinquedos": "Baby & Kids",

                # Tools & Construction
                "ferramentas_jardim": "Tools & Construction",
                "construcao_ferramentas_construcao": "Tools & Construction",
                "construcao_ferramentas_iluminacao": "Tools & Construction",
                "construcao_ferramentas_jardim": "Tools & Construction",
                "construcao_ferramentas_seguranca": "Tools & Construction",
                "construcao_ferramentas_ferramentas": "Tools & Construction",
                "casa_construcao": "Tools & Construction",

                # Food & Beverages
                "alimentos": "Food & Beverages",
                "alimentos_bebidas": "Food & Beverages",
                "bebidas": "Food & Beverages",

                # Automotive
                "automotivo": "Automotive",

                # Pets
                "pet_shop": "Pets",

                # Agriculture & Garden
                "agro_industria_e_comercio": "Agriculture & Garden",
                "flores": "Agriculture & Garden",

                # Office, Arts & Services
                "papelaria": "Office, Arts & Services",
                "industria_comercio_e_negocios": "Office, Arts & Services",
                "artigos_de_festas": "Office, Arts & Services",
                "artes": "Office, Arts & Services",
                "cine_foto": "Office, Arts & Services",
                "artes_e_artesanato": "Office, Arts & Services",
                "relogios_presentes": "Office, Arts & Services",
                "market_place": "Office, Arts & Services",
                "seguros_e_servicos": "Office, Arts & Services",
                "artigos_de_natal": "Office, Arts & Services",
                "la_cuisine": "Office, Arts & Services",
            }

            df["product_category_name"] = (
                df["product_category_name"]
                .map(category_mapping)
                .fillna("unknown")
            )

            logging.info(
                "Product categories grouped successfully."
            )

            # Drop raw timestamp columns
          

            timestamp_cols = [
                "order_purchase_timestamp",
                "order_approved_at",
                "order_estimated_delivery_date"
            ]

            df.drop(
                columns=timestamp_cols,
                inplace=True
            )

            logging.info(
                "Raw timestamp columns removed."
            )

            
            # Log missing values
          

            missing_values = df.isna().sum()
            missing_values = missing_values[
                missing_values > 0
            ]

            if not missing_values.empty:
                logging.info(
                    "Remaining missing values after feature engineering:\n%s",
                    missing_values
                )
            else:
                logging.info(
                    "No missing values remain after transformation."
                )

            
            # Final dataframe information
           

            logging.info(
                "Final transformed dataframe shape: %s",
                df.shape
            )

            logging.info(
                "Final transformed columns: %s",
                list(df.columns)
            )

           
            # Save transformed dataframe
           

            save_df(
                path=self.processed_dataset_path,
                df=df
            )

            logging.info(
                "Transformed dataframe successfully saved to: %s",
                self.processed_dataset_path
            )

            
            # Create artifact
          

            artifact = DataTransformationArtifact(
                transformed_data_file_path= str(self.processed_dataset_path)
            )

            logging.info(
                "DataTransformationArtifact created successfully."
            )

            logging.info(
                "Data transformation completed successfully."
            )

            return artifact

        except Exception as e:

            logging.exception(
                "Error occurred during data transformation."
            )

            raise e