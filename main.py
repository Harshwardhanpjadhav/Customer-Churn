import sys
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.pipeline.training_pipeline import TrainingPipeline 


if __name__ == '__main__':
    try:
        train = TrainingPipeline()
        train.run_pipeline()
    except Exception as e:
        raise CustomException(e,sys)
