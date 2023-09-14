import os
import sys
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.entity.config import TrainingPipelineConfig
from src.churn.entity.artifact import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from src.churn.pipeline.training_pipeline import TrainingPipeline as tp


class TrainingPipeline:
    '''
    This class is used to create the training pipeline object.
    '''

    # Inintializing class variable to track whether the pipeline is running
    is_pipeline_running = False

    def __init__(self):
        # Initialize the training pipeline configuration (This does not store the configuration)
        training_pipeline_config = TrainingPipelineConfig()

    # Initiate data ingestion
    # This will return a DataIngestionArtifact
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            # Performing data ingestion
            pass

        except Exception as e:
            # If an exception occurs during data ingestion, raise a custom exception with error 'e'
            raise CustomException(e, sys)

    # Initiate data validation
    # This will return a DataValidationArtifact
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            # Performing data validation using the provided data ingestion artifact
            pass

        except Exception as e:
            # If an exception occurs during data validation, raise a custom exception with error 'e'
            raise CustomException(e, sys)

    # Initiate data transformation
    # This will return a DataTransformationArtifact
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            # Performing data transformation using the provided data validation artifact
            pass

        except Exception as e:
            # If an exception occurs during data transformation, raise a custom exception with error 'e'
            raise CustomException(e, sys)

    # Initiating model trainer module
    # This will return a ModelTrainerArtifact
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            # Training a machine learning model using the provided data transformation artifact
            pass

        except Exception as e:
            # If an exception occurs during model training, raise a custom exception with error 'e'
            raise CustomException(e, sys)

    # Initiating model evaluation module
    # This will return a ModelEvaluationArtifact
    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact, data_validation_artifact: DataValidationArtifact) -> ModelEvaluationArtifact:
        try:
            # Evaluating the trained model using the provided artifacts
            pass

        except Exception as e:
            # If an exception occurs during model evaluation, raise a custom exception with error 'e'
            raise CustomException(e, sys)

    # Initiating model pusher module
    # This will return a ModelPusherArtifact

    def start_model_pusher(self, model_eval_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:
            # Pushing the trained model to a destination using the model evaluation artifact
            pass

        except Exception as e:
            # If an exception occurs during model pushing, raise a custom exception with error 'e'
            raise CustomException(e, sys)

    # This will execute the entire pipeline by arranging the different stages

    def run_pipeline(self):
        try:
            pass

        except Exception as e:
            # If an exception occurs during pipeline execution, raise a custom exception with error 'e'
            raise CustomException(e, sys)
