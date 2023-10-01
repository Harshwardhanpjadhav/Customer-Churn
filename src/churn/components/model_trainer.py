from src.churn.utils.main_utilis import load_numpy_array_data
from src.churn.exception import CustomException
from src.churn.logger import logging
from src.churn.entity.artifact import DataTransformationArtifact, ModelTrainerArtifact
from src.churn.entity.config import ModelTrainerConfig
import os
from src.churn.utils.main_utilis import write_yaml_file, read_yaml_file
import sys
from sklearn.ensemble import AdaBoostClassifier
from src.churn.ml.metrics import get_classification_score
from src.churn.ml.estimator import Churn
from src.churn.utils.main_utilis import save_object, load_object



class ModelTrainer:
    '''
    This class is responsible for training the model and saving it as a pickle file in artifacts folder
    '''
    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def train_test_split(self, train, test):
        '''
        This function is responsible for splitting the data into train and test
        Return : x_train, y_train, x_test, y_test
        '''
        logging.info("Started Train Test split >>>")
        try:

            train_arr = load_numpy_array_data(train)
            test_arr = load_numpy_array_data(test)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )
            return x_train, y_train, x_test, y_test
        except Exception as e:
            raise e

    def perform_hyper_paramter_tunnig(self): ...

    def train_model(self, x_train, y_train):
        '''
        This function is responsible for training the model
        Return : model
        '''
        logging.info("Started Training model >>>")
        try:
            xgb_clf = AdaBoostClassifier(n_estimators=100)
            xgb_clf.fit(x_train, y_train)
            return xgb_clf
        except Exception as e:
            raise e

    def get_metircs(self, model, y_train, x_test, y_test, y_train_pred):
        try:
            '''
            This function is responsible for getting the metrics
            Return : None
            '''
            logging.info("Started metrics >>>")
            all = {}
        #=====================================================
            # For train Prediction
            train_metric_msg = "Train metric accuracy"
            self.classification_train_metric_artifact,train_metrics = get_classification_score(message=train_metric_msg,y_true=y_train, y_pred=y_train_pred)
            all.update(train_metrics)
            if self.classification_train_metric_artifact.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception(
                    "Trained model is not good to provide expected accuracy")
            
        #======================================================
            # For Test Prediction
            test_metric_msg = "Test metric accuracy"
            y_test_pred = model.predict(x_test)
            self.classification_test_metric,test_metrics = get_classification_score(message=test_metric_msg,y_true=y_test, y_pred=y_test_pred)
            all.update(test_metrics)

            metric_path = self.model_trainer_config.model_metric_dir
            dir_path = os.path.dirname(metric_path)
            os.makedirs(dir_path, exist_ok=True)
            
            write_yaml_file(file_path=metric_path, content=all)

        #======================================================
            # Overfitting and Underfitting
            diff = abs(self.classification_train_metric_artifact.f1_score - self.classification_test_metric.f1_score)

            if diff > 0.05:
                raise Exception(
                    "Model is not good try to do more experimentation.")

        except Exception as e:
            raise e
        
#============================================================================================================================================================
#============================================================================================================================================================
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info("Started model trainer>>>")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
        #=================================================================================================
            # Calling train test split
            logging.info("Calling train test split")
            x_train, y_train, x_test, y_test = self.train_test_split(
                train_file_path, test_file_path)
        #=================================================================================================
            # Calling train model
            logging.info("Calling train model")
            model = self.train_model(x_train, y_train)
            y_train_pred = model.predict(x_train)
        #=================================================================================================
            # Calling get metrics
            self.get_metircs(model, y_train,x_test, y_test, y_train_pred)
        #=================================================================================================
            # Saving model
            logging.info("Loading transformed_object_File_path")
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            logging.info("Succesfully created model directory")
            churn = Churn(preprocessor=preprocessor, model=model)
            logging.info(churn)

    #=================================================================================================
            save_object( self.model_trainer_config.trained_model_file_path, obj=churn)
    #=================================================================================================
            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=self.classification_train_metric_artifact,
                test_metric_artifact=self.classification_test_metric)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)
