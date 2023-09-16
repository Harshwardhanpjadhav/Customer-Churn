import os
import sys
from pandas import DataFrame
from src.churn.logger import logging
from src.churn.exception import CustomException
from sklearn.model_selection import train_test_split
from src.churn.entity.config import DataIngestionConfig
from src.churn.entity.artifact import DataIngestionArtifact
from src.churn.data_access import GetChurnData


class DataIngestion:
    """
    DataIngestion class for exporting data to a feature store, performing a train-test split,
    and initiating data ingestion.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def export_data_to_feature_store(slef) -> DataFrame:
        """
            Export data to a feature store as a DataFrame and save it as a CSV file.
            Returns:
                DataFrame: The exported data as a DataFrame.
        """
        try:
            logging.info(
                "Started Exporting data to Feature store file path >>>")
            churn = GetChurnData()
            dataframe = churn.export_collection_as_dataframe(
                collection_name=slef.data_ingestion_config.collection_name)
            feature_store_file_path = slef.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(
                "Exporting data to Feature store file path complete >>>")
            return dataframe

        except Exception as e:
            raise CustomException(e, sys)

    def train_test_split(self, dataframe: DataFrame):
        """
            Perform train-test split on the given DataFrame and save the resulting sets as CSV files.
            Args:
                dataframe (DataFrame): The input DataFrame to be split.
            Returns:
                None
        """
        try:
            logging.info("Started train test split >>>")
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)

            dir_path = os.path.dirname(
                self.data_ingestion_config.train_file_path)

            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(
                self.data_ingestion_config.train_file_path, index=False, header=True)

            test_set.to_csv(
                self.data_ingestion_config.test_file_path, index=False, header=True)

            logging.info("train test split complete >>>")

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
            Perform data ingestion by exporting data to a feature store, performing a train-test split,
            and returning a DataIngestionArtifact.
            Returns:
                DataIngestionArtifact: An artifact containing file paths to the training and testing datasets.
        """
        try:
            logging.info("Started Data Ingestion >>>")

            dataframe = self.export_data_to_feature_store()

            self.train_test_split(dataframe=dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(
                "Data Ingestion Complete returning artifact to pipeline >>>")
            logging.info(
                f"Data Ingestion Artifact loction {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)
