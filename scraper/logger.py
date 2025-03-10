import logging

LOG_FILE_NAME = "scrape.log"

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE_NAME,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
