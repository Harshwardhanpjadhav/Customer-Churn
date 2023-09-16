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

# ================================================================================================================
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        logging.info("Starts reading Data")
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)

# ================================================================================================================
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

# ================================================================================================================
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

# ================================================================================================================
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

# ================================================================================================================
    def detect_numeric_drift(self, base_df, current_df, threshold=0.05) -> bool:
        logging.info("Started Detect Dataset Drift >>>>>")
        try:
            status = True
            num_report = {}
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

                num_report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found

                }})
            
            # logging.info(report)
            # drift_report_file_path = self.data_validation_config.drift_report_file_num

            # # Create directory
            # dir_path = os.path.dirname(drift_report_file_path)
            # logging.info(dir_path)

            # os.makedirs(dir_path, exist_ok=True)
            # logging.info(dir_path)
            

            # write_yaml_file(file_path=drift_report_file_path, content=report)

            return status,num_report

        except Exception as e:
            raise CustomException(e, sys)

# ================================================================================================================
    def detect_categorical_drift(self, base_df, current_df, threshold=0.05) -> bool:
        status = True
        cat_report = {}
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

                cat_report.update({co: {
                    "p_value": float(p_val),
                    "drift_status": is_found

                }})

        

        # drift_report_file_path = self.data_validation_config.drift_report_file_cat

        # dir_path = os.path.dirname(drift_report_file_path)

        # os.makedirs(dir_path, exist_ok=True)

        # write_yaml_file(file_path=drift_report_file_path, content=report)

        return status,cat_report
    
# ================================================================================================================
# ================================================================================================================
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = ""

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

# ================================================================================================================
            logging.info("Calling Read Data >>>")
            train_dataframe = DataValidation.read_data(train_file_path)
            logging.info("Train Data Read sccessfull")
            test_dataframe = DataValidation.read_data(test_file_path)
            logging.info("Test Data Read sccessfull")

# ================================================================================================================
            logging.info("Calling validate no of columns >>>")
            train_column_status = self.validate_no_of_columns(
                dataframe=train_dataframe)
            if not train_column_status:
                error_message = f"Train Datase Does not contain all columns"
            else:
                logging.info("Train dataset contains all columns")
            test_column_status = self.validate_no_of_columns(
                dataframe=test_dataframe)
            if not test_column_status:
                error_message = f"test Datase Does not contain all columns"
            else:
                logging.info("Test dataset contains all columns")

# ================================================================================================================
            logging.info("calling is numeric columns exist")
            train_numeric_status = self.is_numeric_columns_exist(
                dataframe=train_dataframe)
            if not train_numeric_status:
                error_message = f"Train Datase Does not contain all numeric columns"
            else:
                logging.info("Train dataset contains all numeric columns")

            test_numeric_status = self.is_numeric_columns_exist(
                dataframe=test_dataframe)
            if not test_numeric_status:
                error_message = f"Train Datase Does not contain all numeric columns"
            else:
                logging.info("Test dataset contains all numeric columns")

# ================================================================================================================
            logging.info("calling is categorical columns exist")
            train_categorical_status = self.is_categorical_columns_exist(
                dataframe=train_dataframe)
            if not train_categorical_status:
                error_message = f"Train Datase Does not contain all categorical columns"
            else:
                logging.info("Train dataset contains all categorical columns")
            test_categorical_status = self.is_categorical_columns_exist(
                dataframe=test_dataframe)
            if not test_categorical_status:
                error_message = f"Test dataset Does not contain all categorical columns"
            else:
                logging.info("Test dataset contains all categorical columns")

# ================================================================================================================
            if len(error_message) > 0:
                raise Exception(error_message)

            train_df_nu = utils.numerical_col(df=train_dataframe)
            test_df_nu = utils.numerical_col(df=test_dataframe)

            train_df_cat = utils.categorical_col(df=train_dataframe)
            test_df_cat = utils.categorical_col(df=test_dataframe)
# ================================================================================================================
            logging.info("calling categorical data drift")
            num_drift_status,cat_report = self.detect_categorical_drift(base_df=train_df_cat,
                                                                        current_df=test_df_cat)
            
            logging.info(cat_report)
            categorical_report_file_path = self.data_validation_config.drift_report_file_cat
            dir_path = os.path.dirname(categorical_report_file_path)

            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=categorical_report_file_path, content=cat_report)
            logging.info(categorical_report_file_path)

# ================================================================================================================
            logging.info("calling numerical data drift")
            cat_drift_status,num_report = self.detect_numeric_drift(base_df=train_df_nu,
                                                                    current_df=test_df_nu)
            logging.info(num_report)
            numeric_report_file_path = self.data_validation_config.drift_report_file_num
            write_yaml_file(file_path=numeric_report_file_path, content=cat_report)
            logging.info(f'report file path {numeric_report_file_path}')
            
# ================================================================================================================
            valid_dir_path = self.data_validation_config.valid_train_file_path
            valid_train_file_path = self.data_validation_config.valid_train_file_path
            valid_test_file_path = self.data_validation_config.valid_test_file_path

# ================================================================================================================
            if train_column_status and test_column_status and train_numeric_status and  test_numeric_status and train_categorical_status and test_categorical_status and num_drift_status and cat_drift_status:
                status = True
                valid_train_data = train_dataframe
                valid_test_data = test_dataframe
                valid_dir_name = os.path.dirname(valid_dir_path)
                os.makedirs(valid_dir_name, exist_ok=True)
                valid_train_data.to_csv(
                    valid_train_file_path)
                valid_test_data.to_csv(
                    valid_test_file_path)
                
            else:
                status = False


# ================================================================================================================
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file
            )

            logging.info(
                f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)
