import os
import sys
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.entity.config import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from src.churn.entity.artifact import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from src.churn.components.data_ingestion import DataIngestion
from src.churn.components.data_validation import DataValidation
from src.churn.components.model_trainer import ModelTrainer
from src.churn.components.model_evaluation import ModelEvaluation
from src.churn.components.model_pusher import ModelPusher

from src.churn.components.data_transformation import DataTransformation





class TrainingPipeline:
    is_pipeline_running=False
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
            logging.info("Calling Data Transformation Component")
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation Completed >>")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        '''
        This function is used to initiate model training.
        Returns : Model training Artifact
        '''
        try:
            logging.info("Calling Model Trainer Component")
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=self.model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model Trainer Completed >>")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact,data_validation_artifact: DataValidationArtifact) -> ModelEvaluationArtifact:
        '''
        This function is used to initiate model evaluation.
        Returns : Model evaluation Artifact
        '''
        try:
            logging.info("Calling model evalutaion component")
            model_evalutaion = ModelEvaluation(
                model_trainer_artifact,
                data_validation_artifact,
                model_evaluation_config=self.model_evaluation_config
                )
            model_evaluation_artifact = model_evalutaion.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_pusher(self, model_eval_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:
            model_pusher = ModelPusher(self.model_pusher_config, model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        try:
            logging.info("Pipeline Started")
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            model_eval_artifact = self.start_model_evaluation( model_trainer_artifact,data_validation_artifact=data_validation_artifact)
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact)
            TrainingPipeline.is_pipeline_running=False
            logging.info("Pipeline Completed")

        except Exception as e:
            raise CustomException(e, sys)
