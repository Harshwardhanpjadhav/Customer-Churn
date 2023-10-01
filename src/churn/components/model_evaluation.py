import os,sys
from datetime import datetime
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.entity.config import ModelEvaluationConfig,ModelTrainerConfig
from src.churn.entity.artifact import ModelEvaluationArtifact,ModelTrainerArtifact
from src.churn.constants.trainingpipeline import ARTIFACT_DIR_PATH
from src.churn.utils.main_utilis import read_yaml_file

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

        metric_file_path = os.path.join("Model_Trainer","Metrics","metrics.yaml")
        try:
            logging.info("Started getting previous timestamp >>>")
            timestamps = list(os.listdir(ARTIFACT_DIR_PATH))
            timestamps = sorted(timestamps, key=lambda x: datetime.strptime(x, '%d_%m_%Y_%H_%M_%S'))
            previous_timestamp = timestamps[-2]
            previous_timestamp= os.path.join(ARTIFACT_DIR_PATH,f"{previous_timestamp}",metric_file_path)
            logging.info(f"previous_timestamp : {previous_timestamp}")
            return previous_timestamp
        except Exception as e:
            raise CustomException(e,sys)
        
    def evaluate_model(self,previous_timestamp):
        '''
        This function is responsible for evaluating the model
        '''
        self.previous_timestamp = previous_timestamp
        self.previous_model_metric = read_yaml_file(previous_timestamp)

        logging.info("Started Model Evaluation >>>")
        try:
            prev_accur =  self.previous_model_metric["Train metric accuracy"]
            logging.info(f"previous accuracy{prev_accur}")
            logging.info("Model Evaluation Completed >>>")
            val = prev_accur['F1 Score : ']
            logging.info(f"f1score{val}")

        except Exception as e:
            raise CustomException(e,sys)



    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
         previousfilepath = self.get_previous_timestamp()
         self.evaluate_model(previousfilepath)


         
