# src/utils/logger.py

import logging
import colorlog
import os
import json
from datetime import datetime
from logging.handlers import RotatingFileHandler


class JsonFormatter(logging.Formatter):
    """Formatter to output logs in structured JSON format."""
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/migration_{datetime.now().strftime('%Y%m%d')}.log"
    json_log_filename = f"logs/migration_{datetime.now().strftime('%Y%m%d')}.json"

    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] %(levelname)-8s%(reset)s %(name)s - %(message)s",
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        }
    )
    
    # Standard text file formatter
    file_formatter = logging.Formatter("[%(asctime)s] %(levelname)-8s %(name)s - %(message)s")

    logger = logging.getLogger("migration")
    # Prevent propagation to the root logger
    logger.propagate = False
    
    # Allow INFO level by default, could be configurable later
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if already set up
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(color_formatter)

        # Rotating file handler (10 MB max size, keep 5 backups)
        file_handler = RotatingFileHandler(log_filename, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # JSON Rotating file handler
        json_file_handler = RotatingFileHandler(json_log_filename, maxBytes=10*1024*1024, backupCount=5)
        json_file_handler.setLevel(logging.DEBUG)
        json_file_handler.setFormatter(JsonFormatter())

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(json_file_handler)

    return logger
