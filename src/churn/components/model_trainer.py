from src.churn.utils.main_utilis import load_numpy_array_data
from src.churn.exception import CustomException
from src.churn.logger import logging
from src.churn.entity.artifact import DataTransformationArtifact,ModelTrainerArtifact
from src.churn.entity.config import ModelTrainerConfig
import os,sys
from xgboost import XGBClassifier
from src.churn.ml.metrics import get_classification_score
# from src.churn.ml.estimator import ChurnModel -->after estimatior module
from src.churn.utils.main_utilis import save_object,load_object


class ModelTrainer:

    def __init__(self,model_trainer_config:ModelTrainerConfig,
        data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def train_test_split(self,train,test):
        try:
            train_arr = load_numpy_array_data(train)
            test_arr = load_numpy_array_data(test)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            return x_train,y_train,x_test,y_test
        except Exception as e:
            raise e

    def perform_hyper_paramter_tunnig(self):...

    def train_model(self,x_train,y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf
        except Exception as e:
            raise e
        
    def get_accuracy(self,model,y_train,x_test,y_test,y_train_pred):
        try:
            # For train Prediction
            train_metric_msg = "Train metric accuracy"
            self.classification_train_metric =  get_classification_score(message=train_metric_msg,y_true=y_train, y_pred=y_train_pred)

            if self.classification_train_metric.f1_score<=self.model_trainer_config.expected_accuracy:
                raise Exception("Trained model is not good to provide expected accuracy")
            
            # For Test Prediction
            test_metric_msg = "Test metric accuracy"
            y_test_pred = model.predict(x_test)
            self.classification_test_metric = get_classification_score(message=test_metric_msg,y_true=y_test, y_pred=y_test_pred)


            #Overfitting and Underfitting
            diff = abs(self.classification_train_metric.f1_score-self.classification_test_metric.f1_score)
            
            if diff>self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Model is not good try to do more experimentation.")
            
        except Exception as e:
            raise e
            

    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:

            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            x_train,y_train,x_test,y_test=self.train_test_split(train_file_path,test_file_path)

            model = self.train_model(x_train, y_train)
            y_train_pred = model.predict(x_train)

            self.get_accuracy(model, x_train,y_train,x_test,y_test,y_train_pred)


            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            sensor_model = SensorModel(preprocessor=preprocessor,model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=sensor_model)

            #model trainer artifact

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path, 
            train_metric_artifact=self.classification_train_metric,
            test_metric_artifact=self.classification_test_metric)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise (e,sys)