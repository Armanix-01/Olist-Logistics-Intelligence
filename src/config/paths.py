import os
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
class Configuration:
    def __init__(self):
        config_path= os.path.join(PROJECT_ROOT, "configs", "config.yaml")
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

    def get_config(self):
        return self.config