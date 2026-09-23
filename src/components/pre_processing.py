from src.logger.logger import logging
from src.exception.exception import CustomException
from src.entity.artifact_entity import (
    DataTransformationArtifact,
    PreProcessingArtifact
)
from src.entity.config_entity import PreProcessingConfig

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils.utils import save_artifact

import sys


class PreProcessing:

    def __init__(
        self,
        config: dict,
        data_trans_artifact: DataTransformationArtifact
    ):
        self.config = PreProcessingConfig(config=config)
        self.transformed_df = data_trans_artifact.transformed_df

    def train_and_test_split(self):

        try:
            logging.info("Starting train-test split")

            df = self.transformed_df.copy()

            logging.info(f"Input dataframe shape: {df.shape}")

            x = df.drop(columns=["is_late"])
            y = df["is_late"]

            logging.info(f"Feature shape: {x.shape}")
            logging.info(f"Target shape: {y.shape}")

            logging.info(
                f"Target distribution:\n{y.value_counts(normalize=True)}"
            )

            x_train, x_test, y_train, y_test = train_test_split(
                x,
                y,
                test_size=self.config.test_size,
                random_state=self.config.random_state,
                stratify=y
            )

            logging.info(
                f"Train shape: X={x_train.shape}, y={y_train.shape}"
            )

            logging.info(
                f"Test shape: X={x_test.shape}, y={y_test.shape}"
            )

            logging.info("Train-test split completed")

            return x_train, x_test, y_train, y_test

        except Exception as e:
            logging.exception("Error occurred during train-test split")
            raise CustomException(e, sys)

    def preprocessor(self):

        try:
            logging.info("Creating preprocessing pipeline")

            categorical_cols = [
                "customer_state",
                "seller_state",
                "payment_type",
                "product_category_name"
            ]

            numeric_cols = [
                "number_of_items",
                "number_of_products",
                "number_of_sellers",
                "total_price",
                "total_freight",
                "total_product_weight",
                "total_product_volume",
                "total_payment_value",
                "max_payment_installments",
                "number_of_payments",
                "order_purchase_hour",
                "order_purchase_day_of_week",
                "order_purchase_month",
                "order_purchase_year",
                "order_approval_delay_hours",
                "estimated_delivery_days"
            ]

            logging.info(
                f"Number of numerical features: {len(numeric_cols)}"
            )

            logging.info(
                f"Number of categorical features: {len(categorical_cols)}"
            )

            categorical_pipeline = Pipeline([
                (
                    "imputer",
                    SimpleImputer(
                        strategy="constant",
                        fill_value="unknown"
                    )
                ),
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    )
                )
            ])

            numeric_pipeline = Pipeline([
                (
                    "imputer",
                    SimpleImputer(strategy="median")
                ),
                (
                    "scaler",
                    StandardScaler()
                )
            ])

            preprocessor = ColumnTransformer([
                (
                    "num",
                    numeric_pipeline,
                    numeric_cols
                ),
                (
                    "cat",
                    categorical_pipeline,
                    categorical_cols
                )
            ])

            logging.info("Preprocessing pipeline created successfully")

            return preprocessor

        except Exception as e:
            logging.exception(
                "Error occurred while creating preprocessing pipeline"
            )
            raise CustomException(e, sys)

    def preprocessing_training_data(self):

        try:
            logging.info("Starting preprocessing of training and test data")

            x_train, x_test, y_train, y_test = (
                self.train_and_test_split()
            )

            preprocessor = self.preprocessor()

            logging.info("Fitting preprocessor on training data")

            # Fit ONLY on training data
            x_train_transformed = preprocessor.fit_transform(x_train)

            logging.info(
                f"Transformed training shape: "
                f"{x_train_transformed.shape}"
            )

            logging.info("Transforming test data")

            # Only transform test data
            x_test_transformed = preprocessor.transform(x_test)

            logging.info(
                f"Transformed test shape: "
                f"{x_test_transformed.shape}"
            )

            # Save fitted preprocessor
            preprocessor_path = (
                self.config.preprocessor_dir / "preprocessor.pkl"
            )

            save_artifact(
                artifact=preprocessor,
                path=preprocessor_path
            )

            logging.info(
                f"Preprocessor saved at: {preprocessor_path}"
            )

            logging.info("Preprocessing completed successfully")

            return PreProcessingArtifact(
                x_train=x_train_transformed,
                y_train=y_train,
                x_test=x_test_transformed,
                y_test=y_test
            )

        except Exception as e:
            logging.exception(
                "Error occurred during preprocessing"
            )
            raise CustomException(e, sys)