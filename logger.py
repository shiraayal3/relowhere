import logging

from config import LOG_FILE_PATH

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
