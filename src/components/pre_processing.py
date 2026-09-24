import logging
import sys

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.entity.artifact_entity import (
    DataTransformationArtifact,
    DataPreprocessingArtifact
)
from src.entity.config_entity import PreProcessingConfig
from src.exception.exception import CustomException
from src.utils.utils import (
    save_artifact,
    save_numpy_array_data
)


class PreProcessing:

    def __init__(
        self,
        config: dict,
        data_trans_artifact: DataTransformationArtifact
    ):

        logging.info("Initializing Data Preprocessing")

        self.config = PreProcessingConfig(config=config, test_size=0.2, random_state= 42)

        self.transformed_data_file_path = (
            data_trans_artifact.transformed_data_file_path
        )

        logging.info(
            "Data preprocessing initialized. "
            "Input file: %s",
            self.transformed_data_file_path
        )

    
    # TRAIN TEST SPLIT
    def train_and_test_split(self):

        try:

            logging.info("Starting train-test split")

            # Load transformed dataframe
            df = pd.read_csv(
                self.transformed_data_file_path
            ).copy()

            logging.info(
                "Input dataframe shape: %s",
                df.shape
            )

            # Separate features and target
            X = df.drop(
                columns=["is_late"]
            )

            y = df["is_late"]

            logging.info(
                "Feature shape: %s", X.shape
            )

            logging.info(
                "Target shape: %s", y.shape
            )

            logging.info(
                "Target distribution:\n%s", y.value_counts(normalize=True)
            )

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=self.config.test_size,
                random_state=self.config.random_state,
                stratify=y
            )

            logging.info(
                "Train shape: X=%s, y=%s",X_train.shape,y_train.shape
            )

            logging.info(
                "Test shape: X=%s, y=%s",
                X_test.shape,
                y_test.shape
            )

            logging.info(
                "Train-test split completed successfully"
            )

            return (
                X_train,
                X_test,
                y_train,
                y_test
            )

        except Exception as e:

            logging.exception(
                "Error occurred during train-test split"
            )

            raise CustomException(
                e,
                sys
            )

    
    # PREPROCESSOR
    
    def preprocessor(self):

        try:

            logging.info(
                "Creating preprocessing pipeline"
            )

            
            # CATEGORICAL FEATURES
            

            categorical_cols = [
                "customer_state",
                "seller_state",
                "payment_type",
                "product_category_name"
            ]

           
            # NUMERICAL FEATURES
            

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
                "Number of numerical features: %d",
                len(numeric_cols)
            )

            logging.info(
                "Number of categorical features: %d",
                len(categorical_cols)
            )

           
            # CATEGORICAL PIPELINE
            

            categorical_pipeline = Pipeline(
                steps=[
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
                            handle_unknown="ignore",
                            sparse_output=False
                        )
                    )
                ]
            )

            
            # NUMERICAL PIPELINE
            

            numeric_pipeline = Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(
                            strategy="median"
                        )
                    ),
                    (
                        "scaler",
                        StandardScaler()
                    )
                ]
            )

            
            # COLUMN TRANSFORMER
            

            preprocessor = ColumnTransformer(
                transformers=[
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
                ]
            )

            logging.info(
                "Preprocessing pipeline created successfully"
            )

            return preprocessor

        except Exception as e:

            logging.exception(
                "Error occurred while creating "
                "preprocessing pipeline"
            )

            raise CustomException(
                e,
                sys
            )

    
    # COMPLETE PREPROCESSING
    

    def preprocessing_training_data(
        self
    ) -> DataPreprocessingArtifact:

        try:

            logging.info(
                "Starting complete data preprocessing"
            )

            
            # TRAIN TEST SPLIT
            

            ( X_train,
                X_test,
                y_train,
                y_test) = self.train_and_test_split()

            
            #  CREATE PREPROCESSOR
            

            preprocessor = self.preprocessor()

            
            #  FIT ONLY ON TRAINING DATA
           

            logging.info(
                "Fitting preprocessor on training data"
            )

            X_train_transformed = (
                preprocessor.fit_transform(X_train)
            )

            logging.info(
                "Transformed training shape: %s",
                X_train_transformed.shape
            )

            
            #  TRANSFORM TEST DATA
            

            logging.info(
                "Transforming test data"
            )

            X_test_transformed = (
                preprocessor.transform(X_test)
            )

            logging.info(
                "Transformed test shape: %s",
                X_test_transformed.shape
            )

            
            #  CONVERT TARGET TO NUMPY
            

            y_train_array = y_train.to_numpy()

            y_test_array = y_test.to_numpy()

            
            #  MAKE SURE X IS NUMPY
            

            X_train_array = (
                X_train_transformed
                if hasattr(X_train_transformed, "shape")
                else X_train_transformed.toarray()
            )

            X_test_array = (
                X_test_transformed
                if hasattr(X_test_transformed, "shape")
                else X_test_transformed.toarray()
            )

            
            #  SAVE X TRAIN
            

            X_train_path = (
                self.config.train_file_dir
                / "x_train.npy"
            )

            save_numpy_array_data(
                file_path=X_train_path,
                array=X_train_array
            )

            logging.info(
                "X_train saved to: %s",
                X_train_path
            )

            
            #  SAVE X TEST
            

            X_test_path = (
                self.config.test_file_dir
                / "x_test.npy"
            )

            save_numpy_array_data(
                file_path=X_test_path,
                array=X_test_array
            )

            logging.info(
                "X_test saved to: %s",
                X_test_path
            )

            
            #  SAVE Y TRAIN
           

            y_train_path = (
                self.config.train_file_dir
                / "y_train.npy"
            )

            save_numpy_array_data(
                file_path=y_train_path,
                array=y_train_array
            )

            logging.info(
                "y_train saved to: %s",
                y_train_path
            )

            
            #  SAVE Y TEST
            

            y_test_path = (
                self.config.test_file_dir
                / "y_test.npy"
            )

            save_numpy_array_data(
                file_path=y_test_path,
                array=y_test_array
            )

            logging.info(
                "y_test saved to: %s",
                y_test_path
            )

            
            #  SAVE PREPROCESSOR
            
            preprocessor_path = (
                self.config.preprocessor_dir
                / "preprocessor.pkl"
            )

            save_artifact(
                artifact=preprocessor,
                path=preprocessor_path
            )

            logging.info(
                "Preprocessor saved to: %s",
                preprocessor_path
            )
           
            # CREATE ARTIFACT
            
            preprocessing_artifact = (
                DataPreprocessingArtifact( 
                    X_train_file_path=str( X_train_path),
                    X_test_file_path=str(X_test_path),
                    y_train_file_path=str(y_train_path),
                    y_test_file_path=str(y_test_path),
                    preprocessor_file_path=str(preprocessor_path)
                )
            )

            logging.info(
                "DataPreprocessingArtifact created successfully"
            )

            logging.info(
                "Data preprocessing completed successfully"
            )

            return preprocessing_artifact

        except Exception as e:

            logging.exception(
                "Error occurred during preprocessing"
            )

            raise CustomException(
                e,
                sys
            )