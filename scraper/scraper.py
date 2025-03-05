import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import logging

BASE_URL = "https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html"
DOWNLOAD_FOLDER = "datasets/"
DOWNLOAD_LOG_FILE_NAME = "download_log.log"
FILE_TYPES_TO_DOWNLOAD = [".csv", ".xlsx"]

CHUNK_SIZE = 8192 # 8KB

# init
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

download_log_file = os.path.join(DOWNLOAD_FOLDER, DOWNLOAD_LOG_FILE_NAME)
logging.basicConfig(filename=download_log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _save_file_in_chunks(file_path: str, response: requests.models.Response):
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            f.write(chunk)

def _download_dataset(url: str, file_path: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    _save_file_in_chunks(file_path, response)

def download_dataset(url: str, download_folder: str = DOWNLOAD_FOLDER):
    file_name = url.split("/")[-1]
    file_path = os.path.join(download_folder, file_name)

    try:
        _download_dataset(url, file_path)
        logging.info(f"Downloaded: {file_name}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading {file_name}:\n{e}")

def scrape_datasets(base_url: str):
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        logging.error(f"Unable to scrape {base_rul} with status code {response.status_code}:\n{response.reason}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href and any([href.endswith(file_type) for file_type in FILE_TYPES_TO_DOWNLOAD]):
            download_dataset("http:" + href)
