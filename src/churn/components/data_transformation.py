from src.churn.logger import logging
from src.churn.exception import CustomException
import os,sys
import pandas as pd
import numpy as np
from src.churn.entity.artifact import DataValidationArtifact,DataTransformationArtifact
from src.churn.entity.config import DataTransformationConfig


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(sys,e)
        

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        logging.info("Startes reading Data")
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

