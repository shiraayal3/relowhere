import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from logger import logger
from scraper.config import RAW_DATA_FOLDER, FILE_EXTENSIONS_TO_DOWNLOAD


CHUNK_SIZE = 8192  # 8KB


def save_raw_data(data: str, data_type: str, data_name: str):
    file_name = f"{str(datetime.date(datetime.now()))}_{data_type}_{data_name}"
    file_path = Path(RAW_DATA_FOLDER) / file_name
    with open(file_path, "wb") as f:
        f.write(data)


def save_raw_data_in_chunks(
    response_data: requests.models.Response,
    data_type: str,
    data_name: str,
    chunk_size: int = CHUNK_SIZE,
):
    file_name = f"{str(datetime.date(datetime.now()))}_{data_type}_{data_name}"
    file_path = Path(RAW_DATA_FOLDER) / file_name
    with open(file_path, "wb") as f:
        for chunk in response_data.iter_content(chunk_size=chunk_size):
            f.write(chunk)


def download_file(url: str, file_name: str):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        save_raw_data_in_chunks(response, "file", file_name)
        logger.info(f"Downloaded: {file_name}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading {file_name}:\n{e}")


def scrape_datasets(base_url: str, base_name: str):
    response = requests.get(base_url)
    if response.status_code != 200:
        logger.error(
            f"Unable to scrape {base_url} with status code {response.status_code}:\n{response.reason}"
        )
        return

    save_raw_data(response.content, "html", base_name)

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href and any(
            [href.endswith(file_extension) for file_extension in FILE_EXTENSIONS_TO_DOWNLOAD]
        ):
            file_name = href.split("/")[-1]
            save_raw_data(str(link).encode(), "html_a", file_name)
            download_file("http:" + href, file_name)
