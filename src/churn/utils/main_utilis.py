import yaml #for working with yaml files
import os
import sys
import dill #for adding indexes or serial numbers to our python objects
import numpy as np
import pandas as pd


#   Importing exception and logger classes from
#   src\churn\exception.py,logger.py modules

from src.churn.logger import logging
from src.churn.exception import CustomException

#This function is used to read the data from yaml file .
def read_yaml_file(file_path: str) -> dict:
    try:
        #This will open the yaml file for reading in binary mode
        with open(file_path, "rb") as yaml_file:
            # Using yaml.safe_load to extract yaml content and return in
            # the form of dictonary .
            return yaml.safe_load(yaml_file)
    except Exception as e:
        # If an error occurs it will raise CustomException with 
        # error message and system information
        raise CustomException(e, sys)

#This function is used to write data into a yaml file
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None :
    # --The replace parameter is a boolean flag that determines whether to replace an existing YAML with new content.
    try:
        # Check if the 'replace' flag is set to True
        if replace:
            # If the file already exists, remove it
            if os.path.exists(file_path):
                os. remove (file_path)
            # This will create the directory structure if it does not exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # With following code we can open the file in write mode
            # and use yaml.dump to serialize "content' into the file
            with open(file_path, "w") as file:
                yaml.dump (content, file)

    except Exception as e:
        # If an error occurs during the file operation, raise a custom exception with the error message
        raise CustomException(e, sys)
