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