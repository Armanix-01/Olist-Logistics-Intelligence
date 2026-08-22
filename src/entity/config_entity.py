from src.exception.exception import CustomException
from src.logger.logger import logging
import sys
from src.config.paths import PROJECT_ROOT, Configuration
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar
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
    def from_config(cls):
        try:
            logging.info("Initializing ExtractionConfig")
            config = Configuration().get_config()
            cls._validate(config)

            files = config["files"]

            raw = PROJECT_ROOT / config["data"]["raw"]
            
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
    def _validate(cls, config):
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
