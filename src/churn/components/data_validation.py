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

#This class defines data validation process for the data ingested.
class DataValidation:
    #This constructor is used to assign values to local variables of class DataValidation
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                    data_validation_config=DataValidationConfig):
        try:
            #Assigning local variables or data members
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            #if there is issue in assigning the local var or data member of class
            #then this will raise a custom exception
            raise CustomException(e, sys)
    
    
    #This fun is used to read data from given file path and returns a pandas dataframe
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        logging.info("Starts reading Data")  #creates a log as this fun starts reading data
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            #if the file is not readed properly it will raise a custom exception.
            raise CustomException(e, sys)

    #This function is to confirm if the columns in data frame are equal to the no. of columns from schema file
    def validate_no_of_columns(self, dataframe=pd.DataFrame) -> bool:
        try:
            logging.info("Started Validating Number of columns >>>>>>")
            no_of_col = len(self._schema_config['columns'])
            logging.info(f"Required number of columns: {no_of_col}")#log for required no. of col    
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")#log for columns in dataframea

            #if the columns of df are equal to columns from schema then true otherwise false
            if len(dataframe.columns) == no_of_col:
                return True 
            logging.info("validation no of cloumns complete") # log for confirmation of validation .
            return False

        except Exception as e:
            #if above code shows error while validating columns then it will raise a custom exception
            raise CustomException(e, sys)


    #This columns returns true if numeric column exist otherwise false and takes dataframe as input.
    def is_numeric_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            logging.info("Started validating Numeric Col Exists >>>>>>>>>>>>")#log for starting validation

            numeric_col = self._schema_config['numeric_columns'] #extracts numerical columns from schema file 
                                                                 # and adds it to 'numeric_col' variable 

            dataframe_columns = dataframe.columns  # Extracts columns from dataframe

            numerical_column_present = True #flagging the column present as true to check it afterwards
            missing_numerical_col = [] # Created a empty list for missing numerical columns
            
            # This for loop says that -->
            # if numerical columns are not present in dataframe's column then flag numerical_column_present as false
            # and add that column to 'missing_num_col' list. 
            for num_col in numeric_col:
                if num_col not in dataframe_columns:
                    numerical_column_present = False
                    missing_numerical_col.append(num_col)

            logging.info(f"Missing numerical columns: {missing_numerical_col}")#log for missing numerical columns

            # This will return true if all the numerical columns are present otherwise false.
            return numerical_column_present

        except Exception as e:
             # Raise a custom exception with the original exception and system information
            raise CustomException(e, sys)

    #This columns returns true if categorical column exist otherwise false and takes dataframe as input.
    def is_categorical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try :
            logging.info("Started validating Categorical Col Exists >>>>>")#log for starting validation 

            cat_col = self._schema_config['categorical_columns']# extracts categorical columns from schema file 
                                                            # and adds it to 'cat_col' variable 

            df_columns = dataframe.columns #Extracts columns of dataframe

            cat_col_present = True   # flagging this var true to check afterwards
            missing_cat_col = []     # creating a empty list to append missing categorical columns
 
            # This for loop says that -->
            # if the categorical columns are not present in dataframe then flag 'cat_col_present' as false
            # and append that column to missing_cat_col list .
            for col in cat_col:
                if col not in df_columns:
                    cat_col_present = False
                    missing_cat_col.append(col)

            # Creating a log for missing categorical columns.
            logging.info(f"Missing Categorical Column are {missing_cat_col}")

            #This will return true if all the categorical columns are present otherwise false.
            return cat_col_present
        except Exception as e:
             # Raise a custom exception with the original exception and system information
            raise CustomException(e, sys)


    def detect_numeric_drift(self, base_df, current_df, threshold=0.05) -> bool:
        logging.info("Started Detect Dataset Drift >>>>>")# log of starting of dataset drift detecting
        try:
            status = True       #status is flagged as true to check afterward
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                P_value = is_same_dist.pvalue
                logging.info(f"{P_value} and {threshold}")
                if threshold <= P_value:
                    is_found = False
                else:
                    is_found = True
                    status = False

                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found

                }})

            drift_report_file_path = self.data_validation_config.drift_report_file_num

            # Create directory
            dir_path = os.path.dirname(drift_report_file_path)

            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status

        except Exception as e:
            # Raise a custom exception with the original exception and system information
            raise CustomException(e, sys)

    def detect_categorical_drift(self, base_df, current_df, threshold=0.05) -> bool:
        status = True
        report = {}
        for co in base_df.columns:
            freq_table_train = base_df[co].value_counts()
            freq_table_operational = current_df[co].value_counts()
            expected_freqs = freq_table_train / freq_table_train.sum()
            chi2_stat, p_val, dof, _ = chi2_contingency(
                [freq_table_operational, expected_freqs * len(current_df)])

            if p_val <= threshold:
                is_found = True
            else:
                is_found = False
                status = True

                report.update({co: {
                    "p_value": float(p_val),
                    "drift_status": is_found

                }})

        drift_report_file_path = self.data_validation_config.drift_report_file_cat

        dir_path = os.path.dirname(drift_report_file_path)

        write_yaml_file(file_path=drift_report_file_path, content=report)

        return status

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:

            error_message = ""

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            logging.info("-------- Calling Read Data --------")
            train_dataframe = DataValidation.read_data(train_file_path)
            logging.info("Train Data Read sccessfull")
            test_dataframe = DataValidation.read_data(test_file_path)
            logging.info("Test Data Read sccessfull")

            logging.info("------ validate_no_of_columns --------")
            status = self.validate_no_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all columns"
            else:
                logging.info("Train dataset contains all columns")

            status = self.validate_no_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"test Datase Does not contain all columns"

            else:
                logging.info("Test dataset contains all columns")

            # is_numeric_columns_exist
            logging.info("------ is_numeric_columns_exist --------")
            status = self.is_numeric_columns_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all numeric columns"
            else:
                logging.info("Train dataset contains all numeric columns")

            status = self.is_numeric_columns_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all numeric columns"
            else:
                logging.info("Test dataset contains all numeric columns")

            # is_categorical_columns_exist
            logging.info("------ is_categorical_columns_exist --------")
            status = self.is_categorical_columns_exist(
                dataframe=train_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all categorical columns"
            else:
                logging.info("Train dataset contains all categorical columns")

            status = self.is_categorical_columns_exist(
                dataframe=test_dataframe)
            if not status:
                error_message = f"Train Datase Does not contain all categorical columns"
            else:
                logging.info("Test dataset contains all categorical columns")

            if len(error_message) > 0:
                raise Exception(error_message)

            train_df_nu = utils.numerical_col(df=train_dataframe)
            test_df_nu = utils.numerical_col(df=test_dataframe)

            train_df_cat = utils.categorical_col(df=train_dataframe)
            test_df_cat = utils.categorical_col(df=test_dataframe)

            status = self.detect_categorical_drift(
                base_df=train_df_cat,
                current_df=test_df_cat

            )

            status = self.detect_numeric_drift(
                base_df=train_df_nu,
                current_df=test_df_nu

            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file
            )

            logging.info(
                f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)