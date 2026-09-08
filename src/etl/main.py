from src.etl.pipeline import ETLpipeline
from src.exception.exception import CustomException
import sys
try:
    pipeline = ETLpipeline()
    pipeline.pipeline()

except Exception as e:
    raise CustomException(e)
