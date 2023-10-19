import os
import gdown
from zipfile import ZipFile
from cnnClassifier import logger
from cnnClassifier.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(
            self,
            config: DataIngestionConfig
            ):
        self.config = config

    def download_file(self) -> None:
        """downloads file from the url"""
        try:
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs(self.config.unzip_dir, exist_ok=True)
            logger.info(
                f"Downloading data from {dataset_url} into the file {zip_download_dir}"
                )
            file_id = dataset_url.split('/')[-2]
            prefix = "https://drive.google.com/uc?/export=download&id="
            gdown.download(prefix + file_id, str(zip_download_dir))
            logger.info(f"Downloaded data from {dataset_url} into the file {zip_download_dir}")

        except Exception as e:
            raise e

    def extract_file(self) -> None:
        """ Extracts zip file into the data directory"""
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with ZipFile(self.config.local_data_file, "r") as f:
            f.extractall(unzip_path)