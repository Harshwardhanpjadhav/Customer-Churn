from dataclasses import dataclass
from datetime import datetime
import os
from src.churn.constants import trainingpipeline as tp

class TrainingPipelineConfig:
    '''
    This class is used to create the training pipeline configuration object.
    '''
    def __init__(self, timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name: str = tp.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(tp. ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp
     