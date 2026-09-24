from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.pre_processing import PreProcessing
from src.components.model_trainer import ModelTrainer
from src.config.paths import Configuration

config:dict = Configuration().get_config()
print(config)
ingestion = DataIngestion(config= config)
ingestion_artifact = ingestion.initiate_data_ingestion()
transformation = DataTransformation(config= config, 
                                    data_ingestion_artifact= ingestion_artifact)
transformation_artifact = transformation.feature_eng()
preprocessing = PreProcessing(config=config, data_trans_artifact= transformation_artifact)
preprocessing_artifact = preprocessing.preprocessing_training_data()
model_trainer = ModelTrainer(config=config, preprocessing_artifact= preprocessing_artifact)
model_trainer_artifact = model_trainer.start_training()
