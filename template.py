import os
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='w'
)

# Name of the Project
project_name = "churn"

list_files = [

    # Root Folder files 👇
    ".github/workflows/.gitkeep",
    "config/schema.yaml",
    "templates/index.html",
    "requirements.txt",
    "research/trails.ipynb",
    ".env",

    # Src Project Folders and Files 👇
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/data_access/__init__.py",
    f"src/{project_name}/ml/__init__.py",
    f"src/{project_name}/confiuration/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/constants/trainingpipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/artifact/__init__.py",
    f"src/{project_name}/entity/config/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
]

for file_path in list_files:
    # Using Path Function so that path system  works on every os system
    filepath = Path(file_path)
    # os.path.split(filepath) give -> directory name and file name as output
    filedir, filename = os.path.split(filepath)

    if filedir != "":  # Checks if filedir name is not empty string
        os.makedirs(filedir, exist_ok=True)  # creates directory
        logging.info(f"creating directory: {filedir} for file: {filename}")

    # Creates file
    if (not os.path.exists(file_path) or (os.path.getsize(filepath) == 0)):
        # checks condition if file not exists and checks size of path
        with open(file_path, "w") as f:
            logging.info(f"creating file: {file_path}")
            pass
    else:
        logging.info(f"file already exists: {filepath}")
