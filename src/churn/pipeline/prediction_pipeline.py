import os
import sys
import pandas as pd
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.ml.estimator import ModelResolver
from src.churn.utils.main_utilis import load_object
from src.churn.constants.trainingpipeline import SAVED_MODEL_DIR
#===========================================================================================================

class PredictPipeline:
    def __init__(self):
        pass

    def predict_csv(self,dataframe):
        try:
            # create a function to take input as csv and predict the output and return in dataframe
            #  
            model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)     
            labelencoder = load_object("saved_LabelEncoder_obj","labelencoder.pkl")
            model = model_resolver.get_model()
            prediction = model.predict(dataframe)
            
            
        except Exception as e:
            raise CustomException(e,sys)

    def predict_individual(self,dataframe):
        try:
            model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
            if not model_resolver.is_model_exists():
                raise CustomException("Model Not Found")  
            
            labelencoder = load_object("saved_LabelEncoder_obj","labelencoder.pkl")
            model = model_resolver.get_model()
            prediction = model.predict(dataframe)
            prediction  = labelencoder.inverse_transform(prediction)

            return prediction
        except Exception as e:
            raise CustomException(e,sys)
        
    def convert_to_dataframe(self,data):

        df = pd.DataFrame















