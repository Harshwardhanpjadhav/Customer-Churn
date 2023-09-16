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

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, tp.DATA_INGESTION_INGESTED_DIR)
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, tp.DATA_INGESTION_FEATURE_STORE_DIR, tp.FILE_NAME)
        self.train_file_path: str = os.path.join(
            self.data_ingestion_dir, tp.DATA_INGESTION_INGESTED_DIR, tp.TRAIN_FILE_NAME)
        self.test_file_path: str = os.path.join(
            self.data_ingestion_dir, tp.DATA_INGESTION_INGESTED_DIR, tp.TEST_FILE_NAME)
        self.train_test_split_ratio: float = tp.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = tp.DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, tp.DATA_VALIDATION_DIR_NAME)
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


class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_trainsformation_dir_name = os.path.join(
            training_pipeline_config.artifact_dir, tp.DATA_TRANSFORMATION_DIR_NAME)
        self.data_transforamtion_object_dir_name = os.path.join(
            self.data_trainsformation_dir_name, tp.DATA_TRASNFORMATION_TRANSFORMED_DATA_OBJECT_DIR, tp.PREPROCESSING_PIPELINE_OBJECT)
        self.transformed_train_file_path = os.path.join(
            self.data_trainsformation_dir_name, tp.TRAIN_FILE_NAME.replace("csv", "npy"))
        self.transformed_test_file_path = os.path.join(
            self.data_trainsformation_dir_name, tp.TEST_FILE_NAME.replace("csv", "npy"))


class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, tp.MODEL_TRAINER_DIR_NAME)
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, tp.MODEL_TRAINER_TRAINED_MODEL_DIR, tp.MODEL_FILE_NAME)
        self.expected_accuracy: float = tp.MODEL_TRAINER_EXPECTED_ACCURACY


class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, tp.MODEL_EVALUATION_DIR_NAME)
        self.report_file_path: str = os.path.join(
            self.model_evaluation_dir, tp.MODEL_EVALUATION_REPORT_NAME)
        self.changed_threshold_score: float = tp.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE


class ModelPusherConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, tp.MODEL_PUSHER_DIR_NAME)
        self.model_file_path = os.path.join(
            self.model_evaluation_dir, tp.MODEL_FILE_NAME)
        timestamp = round(datetime.now().timestamp())
        self.saved_model_path = os.path.join(
            tp.SAVED_MODEL_DIR,
            f"{timestamp}",
            tp.MODEL_FILE_NAME)
