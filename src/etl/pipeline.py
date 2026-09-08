from src.config.paths import PROJECT_ROOT, Configuration
from src.entity import artifact_entity, config_entity
from src.etl.extract import DataExtractor
from src.etl.transform import ETLtransformer
from src.etl.load import ETLLoader



class ETLpipeline:
    def __init__(self):
        self.config=  Configuration().get_config()



    def pipeline(self):
        extracted_res=DataExtractor(config= self.config).extract()
        transform_res=ETLtransformer(config=self.config, ExtractionArtifact=extracted_res).transform()
        ETLLoader(config= self.config, transform_artifact= transform_res ).load()



        


