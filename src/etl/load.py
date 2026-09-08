from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from src.entity.config_entity import ETLLoadConfig
from src.entity.artifact_entity import ETLTransformArtifact
from src.logger.logger import logging


class ETLLoader:

    def __init__(
        self,
        config: dict,
        transform_artifact: ETLTransformArtifact
    ):
        self.config = ETLLoadConfig(config= config)
        self.transform_artifact = transform_artifact
        
        self.engine = create_engine(
            f"postgresql://{self.config.db_user}:"
            f"{self.config.db_password}@"
            f"{self.config.db_host}:"
            f"{self.config.db_port}/"
            f"{self.config.db_name}"
)

    def create_tables(self):
        with open(self.config.schema_path, "r", encoding="utf-8") as file:
            schema = file.read()

        with self.engine.begin() as conn:
            for statement in schema.split(";"):
                statement = statement.strip()
                if statement:
                    conn.execute(text(statement))

    def load(self):
        self.create_tables()

        #loading
        with self.engine.begin() as conn:
            for table_name, df in self.transform_artifact.as_dict().items():
                logging.info("Loading table '%s' (%d rows)", table_name, len(df))

                df.to_sql(
                        name=table_name,
                        con=conn,
                        if_exists="append",
                        index=False,
                )

            logging.info("Loaded table '%s' successfully", table_name)