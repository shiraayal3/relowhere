from pathlib import Path

from config import BASE_DATA_DIR

RAW_DATA_FOLDER = str(Path(BASE_DATA_DIR) / "raw_data")
Path(RAW_DATA_FOLDER).mkdir(parents=True, exist_ok=True)

FILE_EXTENSIONS_TO_DOWNLOAD = [".csv", ".xlsx"]
