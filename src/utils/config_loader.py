# src/utils/config_loader.py

import os
import yaml
from dotenv import load_dotenv

load_dotenv()


def load_config(config_path: str = "config.yaml") -> dict:
    """Loads the config.yaml file and resolves any ${ENV_VAR} placeholders
    with actual environment variable values."""
    with open(config_path, "r") as f:
        raw = f.read()

    # Replace ${VAR} placeholders with environment variable values
    for key, value in os.environ.items():
        raw = raw.replace(f"${{{key}}}", value)

    config = yaml.safe_load(raw)
    return config
