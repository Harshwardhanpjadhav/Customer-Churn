import os 
import sys
import pandas 
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.ml.estimator import ModelResolver
from src.churn.utils.main_utilis import load_object
from src.churn.constants.trainingpipeline import SAVED_MODEL_DIR

class Prediction_pipeline:
    def __init__(self):
        pass

    def predict(self,data):
        try:
            model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
            if not model_resolver.is_model_exists():
                raise CustomException("Model Not Found")
            
            best_model_path = model_resolver.get_best_model_path()

            model = load_object(file_path=best_model_path)

            y_pred = model.predict(data)

            

            return y_pred

        except Exception as e:
            raise CustomException(e,sys)
        

    def predictAll(self,dataframe):
        try:
            model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
            if not model_resolver.is_model_exists():
                raise CustomException("Model Not Found")
            
            best_model_path = model_resolver.get_best_model_path()

            model = load_object(file_path=best_model_path)

            y_pred = model.predict(dataframe)

        except Exception as e:
            raise CustomException(e,sys)