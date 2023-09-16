import os
import sys
import pandas as pd
from src.churn.logger import logging
from src.churn.utils import main_utilis as utils
from scipy.stats import ks_2samp, chi2_contingency
from src.churn.exception import CustomException
from src.churn.entity.config import DataValidationConfig
from src.churn.constants.trainingpipeline import SCHEMA_FILE_PATH
from src.churn.utils.main_utilis import write_yaml_file, read_yaml_file
from src.churn.entity.artifact import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config=DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        logging.info("Starts reading Data")
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

    def validate_no_of_columns(self, dataframe=pd.DataFrame) -> bool:
        try:
            logging.info("Started Validating Number of columns >>>>>>")
            no_of_col = len(self._schema_config['columns'])
            logging.info(f"Required number of columns: {no_of_col}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")

            if len(dataframe.columns) == no_of_col:
                return True
            logging.info("validation no of cloumns complete")
            return False

        except Exception as e:
            raise CustomException(e, sys)

    def is_numeric_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            logging.info("Started validating Numeric Col Exists >>>>>>>>>>>>")

            numeric_col = self._schema_config['numeric_columns']

            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numerical_col = []

            for num_col in numeric_col:
                if num_col not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_col.append(num_col)

            logging.info(f"Missing numerical columns: {missing_numerical_col}")

            return numerical_column_present

        except Exception as e:
            raise CustomException(e, sys)

    def is_categorical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            logging.info("Started validating Categorical Col Exists >>>>>")

            cat_col = self._schema_config['categorical_columns']

            df_columns = dataframe.columns

            cat_col_present = True
            missing_cat_col = []

            for col in cat_col:
                if col not in df_columns:
                    cat_col_present = False
                    missing_cat_col.append(col)

            logging.info(f"Missing Categorical Column are {missing_cat_col}")

            return cat_col_present
        except Exception as e:
            raise CustomException(e, sys)

        # Starting Data drift

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            pass

        except Exception as e:
            raise CustomException(e, sys)
