# src/utils/logger.py

import logging
import colorlog
import os
from datetime import datetime


def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] %(levelname)-8s%(reset)s %(message)s",
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        }
    )
    file_formatter = logging.Formatter("[%(asctime)s] %(levelname)-8s %(message)s")

    logger = logging.getLogger("migration")
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if already set up
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(color_formatter)

        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
