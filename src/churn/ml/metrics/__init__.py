from src.churn.entity.artifact import ClassificationMetricArtifact
from src.churn.exception import CustomException
from src.churn.utils.main_utilis import write_yaml_file, read_yaml_file
from sklearn.metrics import f1_score,precision_score,recall_score
from src.churn.entity.config import ModelTrainerConfig
from src.churn.
import os,sys

def get_classification_score(y_true,y_pred,model_trainer_config:ModelTrainerConfig)->ClassificationMetricArtifact:
    try:
        metrics = {}
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classsification_metric =  ClassificationMetricArtifact(
                    f1_score=model_f1_score,
                    precision_score=model_precision_score, 
                    recall_score=model_recall_score)
        
        metrics.update({
            "f1_score":model_f1_score,
            "precision_score":model_precision_score,
            "recall_score":model_recall_score
        })
        write_yaml_file(file_path=model_trainer_config, content=metrics)

        return classsification_metric
    except Exception as e:
        raise CustomException(e,sys)