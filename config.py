import os
from pathlib import Path

DEFAULT_DATA_PATH = str(Path.home() / "relowhere_data")
BASE_DATA_DIR = os.getenv("RELOWHERE_DATA_DIR", DEFAULT_DATA_PATH)

LOGS_FOLDER = str(Path(BASE_DATA_DIR) / "logs")
LOG_FILE_NAME = "relowhere.log"
LOG_FILE_PATH = str(Path(LOGS_FOLDER) / LOG_FILE_NAME)

Path(LOGS_FOLDER).mkdir(parents=True, exist_ok=True)
