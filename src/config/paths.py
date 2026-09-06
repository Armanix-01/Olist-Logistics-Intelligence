import os
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
class Configuration:
    def __init__(self):
        config_path = PROJECT_ROOT / "configs" / "config.yaml"

        with config_path.open() as f:
            self.config = yaml.safe_load(f)

    def get_config(self) ->dict:
        return self.config