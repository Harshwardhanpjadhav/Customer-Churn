from src.churn.logger import logging
from src.churn.exception import CustomException
import os
import sys
import pandas as pd
import numpy as np
from src.churn.entity.artifact import DataValidationArtifact, DataTransformationArtifact,DataIngestionArtifact
from src.churn.entity.config import DataTransformationConfig
from src.churn.constants.trainingpipeline import TAREGT_COLUMN_NAME, SCHEMA_FILE_PATH
from src.churn.utils.main_utilis import read_yaml_file,save_numpy_array_data,save_object

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer,make_column_selector
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
                    ('numerical_pipe', numerical, make_column_selector(dtype_include='number')),
                    ('categorical_pipe', categorical, make_column_selector(dtype_include=object))
                ]
            )

            logging.info("Preorocessing object Created")
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:

            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)
            
            logging.info('Obtaining preprocessing object >>>')
            preprocessing_obj = self.get_data_transformation_object()
            logging.info('Preprocessing object Created Cuccessfully')
            
            input_feature_train_df = train_df.drop(columns=TAREGT_COLUMN_NAME,axis=1)
            target_feature_train_df=train_df[TAREGT_COLUMN_NAME]

            logging.info(f"Input Datatype {type(input_feature_train_df)}")
            logging.info(f"Output train Datatype {type(target_feature_train_df)}")
            logging.info(f"Input shape {input_feature_train_df.shape}")
            logging.info(f'Output train shape {target_feature_train_df.shape}')

            input_feature_test_df=test_df.drop(columns=TAREGT_COLUMN_NAME,axis=1)
            target_feature_test_df=test_df[TAREGT_COLUMN_NAME]

            logging.info(f"Input test Datatype {type(input_feature_test_df)}")
            logging.info(f"Output test Datatype {type(target_feature_test_df)}")
            logging.info(f"Input test shape {input_feature_test_df.shape}")
            logging.info(f'Output test shape {target_feature_test_df.shape}')
            
            
            ## Transformating using preprocessor obj
            logging.info("Applying preprocessing object on Input and Testing datasets >>>")
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            logging.info("Input preprocessing completed >>>")

            logging.info(f"Input train Datatype {type(input_feature_train_arr)}")
            logging.info(f"Input test Datatype {type(input_feature_test_arr)}")

            logging.info(f"Input train shape {input_feature_train_arr.shape}")
            logging.info(f"Input test shape {input_feature_test_arr.shape}")


            labelencoder = LabelEncoder()
            target_feature_train_array = labelencoder.fit_transform(target_feature_train_df)
            target_feature_test_array = labelencoder.transform(target_feature_test_df)
            logging.info(type(target_feature_train_array))
            logging.info(type(target_feature_test_array))
            logging.info(target_feature_train_array.shape)
            logging.info(target_feature_test_array.shape)


            logging.info("Started Concanocatoin Input and Output column")
            train_arr = np.c_[input_feature_train_arr, target_feature_train_array]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_array]

            logging.info("Started saving numpy data")
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.data_transformation_object_file_path, preprocessing_obj,)
            logging.info("Completed saving numpy data")

            logging.info("started DataTransformationArtifact ")
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.data_transformation_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)
