from src.churn.entity.artifact import ClassificationMetricArtifact
from src.churn.exception import CustomException
from src.churn.utils.main_utilis import write_yaml_file, read_yaml_file
from sklearn.metrics import f1_score,precision_score,recall_score
from src.churn.entity.config import ModelTrainerConfig
from src.churn.logger import logging

import os,sys
def get_classification_score(message,y_true,y_pred)->ClassificationMetricArtifact:
    try:
        metrics:dict = {}
        model_f1_score:float = f1_score(y_true, y_pred)
        model_recall_score:float = recall_score(y_true, y_pred)
        model_precision_score:float =precision_score(y_true,y_pred)

        model_f1_score = float(model_f1_score)
        model_recall_score = float(model_recall_score)
        model_precision_score = float(model_precision_score)

        metrics.update({message:
                        {
                            "F1 Score":model_f1_score,
                            "Recall Score":model_recall_score,
                            "Precisionscore":model_precision_score
                        }})

        classsification_metric_artifact =  ClassificationMetricArtifact(
                    f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        
        return classsification_metric_artifact,metrics
    except Exception as e:
        raise CustomException(e,sys)