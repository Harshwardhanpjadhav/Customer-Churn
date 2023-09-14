import os
SAVED_MODEL_DIR =os.path.join("saved_models")

# Target column name form dataset
TAREGT_COLUMN_NAME: str = 'Churn Category'

# Name of the pipeline
PIPELINE_NAME: str = 'Customer-Churn'

# Name of the artifact DIR
ARTIFACT_DIR: str = 'artifact'

# Dataset file constant name
FILE_NAME: str = 'telecom_customer_churn.csv'

# Train File constant name
TRAIN_FILE_NAME: str = "train.csv"

# Test File constant name
TEST_FILE_NAME: str = "test.csv"

# Preprocessing PKL constant file name
PREPROCESSING_PIPELINE_OBJECT = "preprocessing.pkl"

# Model PKL file constant name
MODEL_FILE_NAME = "model.pkl"

# Schema file path constant
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLUMNS= 'drop_columns'

# Data ingestion constant
DATA_INGESTION_COLLECTION_NAME: str = "churn"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store" 
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# Data Validation Constant 
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR_NAME: str = "validated"
DATA_VALIDATION_INVALID_DIR_NAME: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR_NAME: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME_CAT: str = "cat_report.yaml" 
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME_NUM: str = "num_report.yaml"

# Data Transforamtion Constant
DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformation'
DATA_TRASNFORMATION_TRANSFORMED_DATA_DIR: str = 'transformed' 
DATA_TRASNFORMATION_TRANSFORMED_DATA_OBJECT_DIR: str = 'transformed_object'

# Model Trainer Constant
MODEL_TRAINER_DIR_NAME: str = 'model_trainer' 
MODEL_TRAINER_TRAINED_MODEL_DIR: str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = 'model.pkl' 
MODEL_TRAINER_EXPECTED_ACCURACY: float= 0.7