import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format= "[%(asctime)s]: %(message)s")

project_name = "cnnClassifier"

list_of_files = [
    "./.github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "dvc.yaml",
    "config/config.yaml",
    "params.yaml",
    "setup.py",
    "requirements.txt",
    "research/03.1_splitting_data.ipynb",
    "templates/index.html",
    "main.py"
    ]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info("Creating directory: {} for the file: {}".format(filedir, filename))

    if (not os.path.exists(filepath) or (os.path.getsize(filepath) == 0)):
        with open (filepath, "w") as f:
            # This code is left empty on purpose to create empty files
            pass
        logging.info("Creating empty file for the file: {}".format(filename))

    else:
        logging.info("{} already exists".format(filename))