import os
import sys
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.entity.config import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from src.churn.entity.artifact import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from src.churn.components.data_ingestion import DataIngestion
from src.churn.components.data_validation import DataValidation


class TrainingPipeline:

    def __init__(self):
        '''
        This constructor is used to assign values to local variables of class TrainingPipeline
        '''
        training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=training_pipeline_config)
        self.data_validation_config = DataValidationConfig(
            training_pipeline_config=training_pipeline_config)
        self.data_transformation_config = DataTransformationConfig(
            training_pipeline_config=training_pipeline_config)
        self.model_trainer_config = ModelTrainerConfig(
            training_pipeline_config=training_pipeline_config)
        self.model_evaluation_config = ModelEvaluationConfig(
            training_pipeline_config=training_pipeline_config)
        self.model_pusher_config = ModelPusherConfig(
            training_pipeline_config=training_pipeline_config)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        '''
        This function is used to initiate data ingestion.
        Returns : Data Ingestion Artifact
        '''
        try:
            logging.info("Calling Data Ingestion Component")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Data Ingestion Completed >>")

            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        '''
        This function is used to initiate data validation.
        Returns : Data validation Artifact
        '''
        try:
            logging.info("Calling Data Validation Component")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact =  data_validation.initiate_data_validation()
            logging.info("Data Validation Completed >>")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        '''
        This function is used to initiate data transformation.
        Returns : Data transformation Artifact
        '''
        try:
            pass

        except Exception as e:
            raise CustomException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        '''
        This function is used to initiate model training.
        Returns : Model training Artifact
        '''
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact, data_validation_artifact: DataValidationArtifact) -> ModelEvaluationArtifact:
        '''
        This function is used to initiate model evaluation.
        Returns : Model evaluation Artifact
        '''
        try:
            pass

        except Exception as e:
            raise CustomException(e, sys)

    def start_model_pusher(self, model_eval_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        '''
        This function is used to initiate model pushing.
        Returns : Model pushing Artifact
        '''
        try:
            pass

        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        try:
            logging.info("Pipeline Started")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)

        except Exception as e:
            raise CustomException(e, sys)
