import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str) : path like input

    Raises:
            ValueError: if yaml file is empty
            e: empty file
    Returns:
            ConfigBox: ConfigBox type"""

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info("yaml file: {} loaded".format(path_to_yaml))
            return ConfigBox(content)

    except BoxValueError:
        raise BoxValueError("yaml file is empty")

    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates a list of directories

    :param path_to_directories (list): list of path of directories
    :param verbose (bool, optional): ignore if multiple dirs is to be created, Defaults to False
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)

        if verbose:
            logger.info(f"Created directory at {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save json data
    :param path (Path): path to json file
    :param data (dict) : data to be saved in json file
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    logger.info(f"json saved at {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    load json files data
    :param path (Path): path to json file
    :return: ConfigBox: data as class attributes instead of dict
    """

    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Save binary file
    :param data: data to be saved in binary
    :param path: path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    loades binary file
    :param path: path to binary file
    :return: Amy object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """
    get size in kb
    :param path: path of the file
    :return: size in kb
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~{size_in_kb} KB"


def decodeImage(imgstring, filename):
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())