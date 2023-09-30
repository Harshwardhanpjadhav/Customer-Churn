import os
SAVED_MODEL_DIR =os.path.join("saved_models")

# Target column name form dataset
TAREGT_COLUMN_NAME: str = 'Customer Status'

# Name of the pipeline
PIPELINE_NAME: str = 'churn'

# Name of the artifact DIR
ARTIFACT_DIR: str = 'artifact'

# Dataset file constant name
FILE_NAME: str = 'telecom_customer_churn.csv'

# Train File constant name
TRAIN_FILE_NAME: str = "train.csv"
# Test File constant name
TEST_FILE_NAME: str = "test.csv"

# Schema file path constant
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLUMNS= 'drop_columns'

# Data ingestion constant
DATA_INGESTION_COLLECTION_NAME: str = "churn"
DATA_INGESTION_DIR_NAME: str = "Data_Ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "Feature_Store" 
DATA_INGESTION_INGESTED_DIR: str = "Train_Test_Data"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# Data Validation Constant 
DATA_VALIDATION_DIR_NAME: str = "Data_Validation"
DATA_VALIDATION_VALID_DIR_NAME: str = "Valid"
DATA_VALIDATION_INVALID_DIR_NAME: str = "Invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR_NAME: str = "Drift_Report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME_CAT: str = "Categorical_Features.yaml" 
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME_NUM: str = "Numerical_Features.yaml"

# Data Transforamtion Constant
DATA_TRANSFORMATION_DIR_NAME: str = 'Data_Transformation'
DATA_TRASNFORMATION_TRANSFORMED_DATA_DIR: str = 'Transformed' 
DATA_TRASNFORMATION_TRANSFORMED_DATA_OBJECT_DIR: str = 'transformed_object'
PREPROCESSING_PIPELINE_OBJECT = "preprocessing.pkl"

# Model Trainer Constant
MODEL_TRAINER_DIR_NAME: str = 'Model_Trainer' 
MODEL_TRAINER_TRAINED_MODEL_DIR: str = 'Trained_Model'
MODEL_FILE_NAME = "model.pkl"
MODEL_METRIC_DIR: str = "Metrics"
METRIC_FILE_NAME = "metrics.yaml"
MODEL_TRAINER_EXPECTED_ACCURACY: float= 0.7

# Model Evaluation Constant
MODEL_EVALUATION_DIR_NAME: str = "Model_Evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_EVALUATION_REPORT_NAME= "report.yaml"

# Model pusher
MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODEL_DIR