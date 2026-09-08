from src.exception.exception import CustomException
from src.logger.logger import logging
import sys
import os
from dotenv import load_dotenv
from src.config.paths import PROJECT_ROOT, Configuration
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
load_dotenv()



@dataclass(frozen=True)
class ExtractionConfig:

    
    
    raw_data_path: Path
    customers_data: Path
    geolocation_data: Path
    order_items_data: Path
    order_payments_data: Path
    order_reviews_data: Path
    orders_data: Path
    products_data: Path
    sellers_data: Path
    category_translation_data: Path
    
    REQUIRED_KEYS:ClassVar[list[str]] = [
        "customers",
        "geolocation",
        "order_items",
        "order_payments",
        "order_reviews",
        "orders",
        "products",
        "sellers",
        "category_translation",
    ]

    @classmethod
    def from_config(cls, config: dict) -> "ExtractionConfig":
        try:
            logging.info("Initializing ExtractionConfig")
            
            cls._validate(config)

            files = config["files"]

            raw = PROJECT_ROOT / config["data"]["raw"]
            raw.mkdir(parents=True, exist_ok=True)
            
            return cls(
                
                raw_data_path=raw,
                customers_data=raw / files["customers"],
                geolocation_data=raw / files["geolocation"],
                order_items_data=raw / files["order_items"],
                order_payments_data=raw / files["order_payments"],
                order_reviews_data=raw / files["order_reviews"],
                orders_data=raw / files["orders"],
                products_data=raw / files["products"],
                sellers_data=raw / files["sellers"],
                category_translation_data=raw / files["category_translation"],
            )
        except Exception as e:
            raise CustomException(e, sys)

    @classmethod
    def _validate(cls, config: dict) -> None:
        try:

            if "data" not in config:
                raise KeyError("Missing 'data' section")

            if "raw" not in config["data"]:
                raise KeyError("Missing 'data.raw'")

            if "files" not in config:
                raise KeyError("Missing 'files' section")

            for key in cls.REQUIRED_KEYS:
                if key not in config["files"]:
                    raise KeyError(
                        f"Missing 'files.{key}'"
                    )
        except Exception as e:
            raise CustomException(e, sys)



class ETLTransformConfig:
    def __init__(self,  config:dict):
        try:
            
            
            self.cleaned_data_path= PROJECT_ROOT / config["data"]["cleaned"]
            self.cleaned_data_path.mkdir(parents=True, exist_ok=True)

        except Exception as e:
            raise CustomException(e, sys)

class ETLLoadConfig:

    def __init__(self, config: dict):

        self.db_user = config["database"]["user"]
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = config["database"]["host"]
        self.db_port = config["database"]["port"]
        self.db_name = config["database"]["name"]
        self.schema_path = PROJECT_ROOT / "src" / "sql" / "schema.sql"