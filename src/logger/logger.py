import os
import logging
from datetime import datetime

log_file_name= f"{datetime.now().strftime("%d-%m-%Y %H-%M-%S")}"
logs_path= os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)
log_file_path = os.path.join(logs_path, log_file_name)
logging.basicConfig(
    filemode="w",
    filename=log_file_path,
    format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt= "%d-%m-%Y %H-%M-%S", 
    level= logging.INFO
)

# logging.info("Checking if logging is working properly")