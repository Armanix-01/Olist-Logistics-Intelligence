from sqlalchemy import create_engine, text
import pandas as pd

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.utils.utils import load_csv, save_df
from src.logger.logger import logging


class DataIngestion:

    def __init__(self, config: dict):

        logging.info("Initializing Data Ingestion")

        self.config = DataIngestionConfig(config)

        self.engine = create_engine(
            f"postgresql://{self.config.db_user}:"
            f"{self.config.db_password}@"
            f"{self.config.db_host}:"
            f"{self.config.db_port}/"
            f"{self.config.db_name}"
        )

        logging.info("Database engine created successfully")

    def fetch_data(self) -> pd.DataFrame:

        logging.info("Starting data fetching from PostgreSQL")

        with open(
            self.config.sql_for_ing,
            "r",
            encoding="utf-8"
        ) as file:
            query = file.read()

        logging.info("SQL query loaded successfully")

        with self.engine.connect() as conn:
            df = pd.read_sql(
                text(query),
                conn
            )

        logging.info(
            f"Data fetched successfully. Shape: {df.shape}"
        )

        return df

    from pathlib import Path

    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        logging.info("Starting data ingestion")

        raw_df = self.fetch_data()

        ingested_file_path = (
            self.config.ingested_data_dir / "ingested.csv"
        )

        save_df(
            path=ingested_file_path,
            df=raw_df
        )

        logging.info(
            f"Ingested dataframe saved to: {ingested_file_path}"
        )

        artifact = DataIngestionArtifact(
            ingested_data_file_path=str(ingested_file_path)
        )

        logging.info("Data ingestion completed successfully")

        return artifact