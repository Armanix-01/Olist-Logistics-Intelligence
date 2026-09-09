from sqlalchemy import create_engine, text
from src.entity.config_entity import DataIngestionConfig
import pandas as pd
import pandas as pd

class DataIngestion:
    def __init__(self, config: dict):
        self.config = DataIngestionConfig(config)

        self.engine = create_engine(
            f"postgresql://{self.config.db_user}:"
            f"{self.config.db_password}@"
            f"{self.config.db_host}:"
            f"{self.config.db_port}/"
            f"{self.config.db_name}"
        )

    def fetch_data(self):
        with open(self.config.sql_for_ing, "r", encoding="utf-8") as file:
            query = file.read()

        with self.engine.connect() as conn:
            raw_df = pd.read_sql(text(query), conn)

        return raw_df
    
        