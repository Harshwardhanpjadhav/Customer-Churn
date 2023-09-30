from src.churn.entity.artifact import ClassificationMetricArtifact
from src.churn.exception import CustomException
from src.churn.utils.main_utilis import write_yaml_file, read_yaml_file
from sklearn.metrics import f1_score,precision_score,recall_score
from src.churn.entity.config import ModelTrainerConfig
from src.churn.logger import logging

import os,sys

def get_classification_score(message,y_true,y_pred,model_trainer_config)->ClassificationMetricArtifact:
    try:
        metrics = {}
        Data_name = message
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classsification_metric =  ClassificationMetricArtifact(
                    f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        
        metrics.update({
            "Name":Data_name,
            "f1_score":model_f1_score,
            "precision_score":model_precision_score,
            "recall_score":model_recall_score
        })
        metric_path = model_trainer_config.model_metric_dir
        logging.info(f"modle file path type{type(metric_path)}")
        write_yaml_file(file_path=metric_path, content=metrics)

        return classsification_metric
    except Exception as e:
        raise CustomException(e,sys)