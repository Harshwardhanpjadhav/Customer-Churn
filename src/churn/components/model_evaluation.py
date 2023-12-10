import os
import sys
import mlflow
import pandas as pd
from src.churn.logger import logging
from src.churn.exception import CustomException
from src.churn.entity.config import ModelEvaluationConfig, ModelTrainerConfig
from src.churn.entity.artifact import ModelEvaluationArtifact, ModelTrainerArtifact,DataValidationArtifact
from src.churn.constants.trainingpipeline import TAREGT_COLUMN_NAME
from src.churn.utils.main_utilis import load_object
from src.churn.ml.metrics import get_classification_score
from src.churn.ml.estimator import ModelResolver
from sklearn import preprocessing 
from src.churn.utils.main_utilis import write_yaml_file, read_yaml_file

from urllib.parse import urlparse



class ModelEvaluation:
    def __init__(self,
                 model_trainer_artifact: ModelTrainerArtifact,
                 data_validation_artifact:DataValidationArtifact,
                 model_evaluation_config:ModelEvaluationConfig,
                ):
        try:
            self.model_evaluation_config=model_evaluation_config
            self.data_validation_artifact=data_validation_artifact
            self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            #valid train and test file dataframeclear
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)
            df = pd.concat([train_df,test_df])

            y_true = df[TAREGT_COLUMN_NAME]
            label_encoder = preprocessing.LabelEncoder() 
            y_true = label_encoder.fit_transform(y_true) 
            df.drop(TAREGT_COLUMN_NAME,axis=1,inplace=True)

            train_model_file_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()
            is_model_accepted=True

            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    trained_model_path=train_model_file_path,
                    train_model_metric_artifact=self.model_trainer_artifact.train_metric_artifact,
                    best_model_metric_artifact=None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            

            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)
            train_model = load_object(file_path=train_model_file_path)
            
            y_trained_pred = train_model.predict(df)
            y_latest_pred  =latest_model.predict(df)

            trained_metric,_ = get_classification_score("Train",y_true, y_trained_pred)
            latest_metric,_ = get_classification_score("Test",y_true, y_latest_pred)
            logging.info(trained_metric)

            improved_accuracy = trained_metric.f1_score-latest_metric.f1_score
            if self.model_evaluation_config.changed_threshold_score < improved_accuracy:
                #0.02 < 0.03
                is_model_accepted=True
                logging.info("New Model is Best")
                logging.info("Saving the new model.pkl")
                logging.info(f"Old model accuracy {trained_metric.f1_score}")
                logging.info(f"New model accuracy {latest_metric.f1_score}")
            else:
                is_model_accepted=False
                logging.info("Old Model is Best")
                logging.info("Saving the old model.pkl")
                logging.info(f"Old model accuracy {trained_metric.f1_score}")
                logging.info(f"New model accuracy {latest_metric.f1_score}")

            model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=improved_accuracy, 
                    best_model_path=latest_model_path, 
                    trained_model_path=train_model_file_path, 
                    train_model_metric_artifact=trained_metric, 
                    best_model_metric_artifact=latest_metric)

            model_eval_report = model_evaluation_artifact.__dict__

#=======================================================================================================
            # MFLOW
            model = load_object(file_path=latest_model_path)

            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            with mlflow.start_run() as run:

                f1_score = trained_metric.f1_score
                precision_score = trained_metric.precision_score
                recall_score = trained_metric.recall_score


                mlflow.log_metric("F1 Score",f1_score)
                mlflow.log_metric("Recall Score",recall_score)
                mlflow.log_metric("Precision score",precision_score)

                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(
                        model, "model", registered_model_name="AdaBoostClassifier"
                    )
                else:
                    mlflow.sklearn.log_model(model, "model")

#=======================================================================================================
            write_yaml_file(self.model_evaluation_config.report_file_path, model_eval_report)
            logging.info(model_evaluation_artifact)
            logging.info("Model Evaluation Completed >>>")
            return model_evaluation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)

