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
        self.artifact_dir: str = os.path.join(tp. ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp


class DataIngestionConfig:
    '''
        file location for data ingestion  
    '''
    def __init__(self,trainingpipelineconfig:TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(trainingpipelineconfig.artifact_dir,tp.DATA_INGESTION_INGESTED_DIR)
        self.feature_store_file_path  = os.path.join(self.data_ingestion_dir,tp.DATA_INGESTION_FEATURE_STORE_DIR,tp.FILE_NAME)
        self.train_file_path = os.path.join(self.data_ingestion_dir,tp.DATA_INGESTION_INGESTED_DIR,tp.TRAIN_FILE_NAME)
        self.test_file_path = os.path.join(self.data_ingestion_dir,tp.DATA_INGESTION_INGESTED_DIR,tp.TEST_FILE_NAME)
        self.train_test_split_ratio:float = tp.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = tp.DATA_INGESTION_COLLECTION_NAME