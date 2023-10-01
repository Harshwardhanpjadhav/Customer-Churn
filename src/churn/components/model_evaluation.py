import os,sys
from datetime import datetime
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.entity.config import ModelEvaluationConfig,ModelTrainerConfig
from src.churn.entity.artifact import ModelEvaluationArtifact,ModelTrainerArtifact
from src.churn.constants.trainingpipeline import ARTIFACT_DIR_PATH

class ModelEvaluation:
    def __init__(self,model_evalutaion_config:ModelEvaluationConfig,
                 model_trainer_artifact:ModelTrainerArtifact,
                 model_trainer_config:ModelTrainerConfig):
        try:
            self.model_evalutaion_config = model_evalutaion_config
            self.model_trainer_artifact = model_trainer_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_previous_timestamp(self):
        '''
        This function is responsible for getting the previous timestamp
        '''
        try:
            logging.info("Started getting previous timestamp >>>")
            timestamps = list(os.listdir(ARTIFACT_DIR_PATH))
            timestamps = sorted(timestamps, key=lambda x: datetime.strptime(x, '%d_%m_%Y_%H_%M_%S'))
            previous_timestamp = timestamps[-2]
            previous_timestamp= os.path.join(ARTIFACT_DIR_PATH,f"{previous_timestamp}",self.model_trainer_config.model_metric_dir)
            logging.info(f"previous_timestamp : {previous_timestamp}")
            return previous_timestamp
        except Exception as e:
            raise CustomException(e,sys)
        
    def evaluate_model(self):
        '''
        This function is responsible for evaluating the model
        '''
        logging.info("Started Model Evaluation >>>")
        try:

            logging.info("Model Evaluation Completed >>>")
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        self.get_previous_timestamp()
