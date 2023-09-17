from src.churn.logger import logging
from src.churn.exception import CustomException
import os
import sys
import pandas as pd
import numpy as np
from src.churn.entity.artifact import DataValidationArtifact, DataTransformationArtifact
from src.churn.entity.config import DataTransformationConfig
from src.churn.constants.trainingpipeline import TAREGT_COLUMN_NAME, SCHEMA_FILE_PATH
from src.churn.utils.main_utilis import read_yaml_file

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler, OneHotEncoder, MinMaxScaler, LabelEncoder, StandardScaler


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(sys, e)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        logging.info("Startes reading Data")
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_transformation_object(self) -> Pipeline:
        try:

            numerical_col = self._schema_config['numeric_columns']
            logging.info(numerical_col)
            categorical_col = self._schema_config['categorical_columns']
            categorical_col = categorical_col.remove('Customer Status')

            logging.info("creating numerical Pipeline ")
            numerical = Pipeline(
                steps=[
                    ('Missing_numeric', SimpleImputer(strategy='mean')),
                    ('scaling', StandardScaler())
                ]
            )

            logging.info("creating categorical Pipeline ")
            categorical = Pipeline(
                steps=[
                    ('Missing_cat', SimpleImputer(strategy='most_frequent')),
                    ("OHE", OneHotEncoder(handle_unknown="ignore", drop='first')),
                    ('scaling', StandardScaler(with_mean=False))

                ])
            
            logging.info("creating object")
            preprocessor = ColumnTransformer(
                [
                    ('numerical', numerical, numerical_col),
                    ('categorical', categorical, categorical_col)
                ]
            )

            logging.info("Preorocessing object Created")
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:

            train = DataTransformation.read_data(
                self.data_validation_artifact.valid_train_file_path)
            test = DataTransformation.read_data(
                self.data_validation_artifact.valid_test_file_path)

            preprocessor = self.get_data_transformation_object()

            logging.info(type(train))
            logging.info(type(test))

            input_train = train.drop(columns=[TAREGT_COLUMN_NAME], axis=1)
            output_train = train[TAREGT_COLUMN_NAME]


            logging.info(type(input_train))
            logging.info(type(output_train))

            input_test = test.drop(columns=[TAREGT_COLUMN_NAME], axis=1)
            output_test = test[TAREGT_COLUMN_NAME]

            train_tf = preprocessor.fit_transform(input_train)
            test_tf = preprocessor.transform(input_test)

            # train_tf = pd.DataFrame(train_tf)
            # test_tf = pd.DataFrame(test_tf)

            logging.info(train_tf)

        except Exception as e:
            raise CustomException(e, sys)
