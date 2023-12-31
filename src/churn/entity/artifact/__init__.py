from dataclasses import dataclass

# These data classes provide a structured way to store and pass around information and 
# results within machine learning pipeline
# Each class is designed to encapsulate specific types of information or artifacts

# Data Ingestion Artifact includes information related to data ingestion
@dataclass
class DataIngestionArtifact:
    trained_file_path: str  # Path to the training data file
    test_file_path: str     # Path to the test data file

# Data Validation Artifact includes information about data validation and potential issues
@dataclass
class DataValidationArtifact:
    validation_status: bool           # Indicates whether data validation was successful or not
    valid_train_file_path: str        # Path to the valid training data file
    valid_test_file_path: str         # Path to the valid test data file
    invalid_train_file_path: None      # Path to the invalid training data file (if any issues found)
    invalid_test_file_path: None       # Path to the invalid test data file (if any issues found)
    drift_report_file_path: str       # Path to a report on data drift

# Data Transformation Artifact includes information related to data transformation
@dataclass
class DataTransformationArtifact:
    transformed_preprocessing_object_file_path: str  # Path to the transformed data object
    transformed_labelencoder_object_file_path: str  # Path to the transformed data object
    transformed_train_file_path: str   # Path to the transformed training data file
    transformed_test_file_path: str    # Path to the transformed test data file

# Classification Metric Artifact includes classification metrics
@dataclass
class ClassificationMetricArtifact:
    f1_score: float         # F1-score for the classification model
    precision_score: float  # Precision score for the classification model
    recall_score: float     # Recall score for the classification model

# Model Trainer Artifact includes information related to model training module
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str       # Path to the trained machine learning model file
    metric_artifact: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
  

# Model Evaluation Artifact includes information related to model evaluation
@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    trained_model_path: str
    train_model_metric_artifact: ClassificationMetricArtifact
    best_model_metric_artifact: ClassificationMetricArtifact

# Model Pusher Artifact includes information related to pushing/deploying the model
@dataclass
class ModelPusherArtifact:
    saved_model_path: str     # Path to the saved model file
    model_file_path: str  

# These artifacts are used to initialize training pipeline and components   
