## Here you will make artifact_entity.py and config_entity.py
#In artifact_entity: basically this will decide the pipeline or 
# major process output file. Ex: 
# @dataclass
# class DataValidationArtifact:
#     validation_status:bool
#     valid_train_file_path:str
#     valid_test_file_path:str
#     invalid_train_file_path:str
#     invalid_test_file_path:str
#     drift_report_file_path:str


# In config_entity we basically setup the requirements for 
#pipeline or process. Ex:
      
# class DataIngestionConfig:
#     def __init__(self, training_pipeline_config:TrainingPipelineConfig):
#         self.data_ingestion_dir = os.path.join(
#             training_pipeline_config.artifact_dir,
#             training_pipeline.DATA_INGESTION_DIR_NAME
#         )
#         self.feature_store_file_path= os.path.join(
#             self.data_ingestion_dir,
#             training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
#             training_pipeline.FILE_NAME
#         )
#         self.training_file_path= os.path.join(
#             self.data_ingestion_dir,
#             training_pipeline.DATA_INGESTION_INGESTED_DIR,
#             training_pipeline.TRAIN_FILE_NAME
#         )
#         self.testing_file_path= os.path.join(
#             self.data_ingestion_dir,
#             training_pipeline.DATA_INGESTION_INGESTED_DIR,
#             training_pipeline.TEST_FILE_NAME
#         )
#         self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
#         self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
#         self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME