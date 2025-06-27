import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging() -> None:
    """Configure logging for the application."""
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    runtime = Path("runtime")
    runtime.mkdir(exist_ok=True)
    log_file = runtime / "server.log"

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    logging.basicConfig(level=level, handlers=[console_handler, file_handler])

