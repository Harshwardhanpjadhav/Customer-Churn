from dataclasses import dataclass
from datetime import datetime
import os
from src.churn.constants import trainingpipeline as tp


class TrainingPipelineConfig:
    '''
    This class is used to create the training pipeline configuration object.
    '''

    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = tp.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(tp.ARTIFACT_DIR, timestamp)
        # self.timestamp: str = timestamp


class DataIngestionConfig:
    '''
        file location for data ingestion  
    '''

    def __init__(self, trainingpipelineconfig: TrainingPipelineConfig):
        self.data_ingestion_di: str = os.path.join(
            trainingpipelineconfig.artifact_dir, tp.DATA_INGESTION_INGESTED_DIR)
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, tp.DATA_INGESTION_FEATURE_STORE_DIR, tp.FILE_NAME)
        self.train_file_path: str = os.path.join(
            self.data_ingestion_dir, tp.DATA_INGESTION_INGESTED_DIR, tp.TRAIN_FILE_NAME)
        self.test_file_path: str = os.path.join(
            self.data_ingestion_dir, tp.DATA_INGESTION_INGESTED_DIR, tp.TEST_FILE_NAME)
        self.train_test_split_ratio: float = tp.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = tp.DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:
    def __init__(self, trainingpipelineconfig: TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(
            trainingpipelineconfig.artifact_dir, tp.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir, tp.DATA_VALIDATION_VALID_DIR_NAME)
        self.valid_train_file_path: str = os.path.join(
            self.valid_data_dir, tp.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir, tp.TEST_FILE_NAME)
        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir, tp.DATA_VALIDATION_INVALID_DIR_NAME)
        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir, tp.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir, tp.TEST_FILE_NAME)
        self.drift_report_file: str = os.path.join(
            self.data_validation_dir, tp.DATA_VALIDATION_DRIFT_REPORT_DIR_NAME)
        self.drift_report_file_cat: str = os.path.join(
            self.drift_report_file, tp.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME_CAT)
        self.drift_report_file_num: str = os.path.join(
            self.drift_report_file, tp.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME_NUM)

