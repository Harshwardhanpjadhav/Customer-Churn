import yaml
import os
import sys
import dill
import numpy as np
import pandas as pd


from src.churn.logger import logging
from src.churn.exception import CustomException


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os. remove(file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                yaml.dump(content, file)

    except Exception as e:
        raise CustomException(e, sys)


def numerical_col(df: pd.DataFrame) -> pd.DataFrame:
    try:
        num_col = [
            features for features in df.columns if df[features].dtype != "O"]
        logging.info(num_col)
        df = df[num_col]
        return df
    except Exception as e:
        raise CustomException(sys,e)

def categorical_col(df: pd.DataFrame) -> pd.DataFrame:
    try:
        cat_col = [
            features for features in df.columns if df[features].dtype == "O"]
        logging.info(cat_col)
        df = df[cat_col]
        return df
    except Exception as e:
        raise CustomException(sys,e)
