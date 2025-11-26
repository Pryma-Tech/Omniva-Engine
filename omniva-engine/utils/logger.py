"""Unified logging system for Omniva Engine."""
# TODO: Add structured logging, JSON logs, per-module log separation.

import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "omniva.log")

logger = logging.getLogger("omniva")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.propagate = False


def get_logs_tail(lines: int = 200) -> str:
    """
    Return last X lines of omniva.log.
    TODO: Add search, filtering, advanced formatting.
    """
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            all_lines = file.readlines()
        return "".join(all_lines[-lines:])
    except Exception:
        return "No logs available (placeholder)"
