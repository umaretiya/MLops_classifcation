from banking.exception import BankingException
from banking.logger import logging
from banking.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from banking.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from banking.component.data_ingestion import DataIngestion
from banking.component.data_validation import DataValidation
from banking.component.data_transformation_clf import DataTransformation
from banking.config.configuration import Configuration 
from banking.constant import EXPERIMENT_DIR_NAME,EXPERIMENT_FILE_NAME
from collections import namedtuple 
from datetime import datetime 
from threading import Thread
import os, sys,pandas as pd, numpy as np


Experiment = namedtuple("Experiment",["experiment_id","initialization_timestamp","artifact_time_stamp",
                                      "running_status","start_time","stop_time","execution_time","message",
                                      "experiment_file_path","accuracy","is_model_accepted"])


class Pipeline(Thread):
    experiment = Experiment(*([None]*11))
    experiment_file_path = None 
    
    def __init__(self, config:Configuration):
        try:
            os.makedirs(config.trainig_pipeline_config.artifact_dir, exist_ok=True)
            Pipeline.experiment_file_path = os.path.join(config.trainig_pipeline_config.artifact_dir,EXPERIMENT_DIR_NAME,EXPERIMENT_FILE_NAME)
            super().__init__(daemon=False, name="pipeline")
            self.config = config
        except Exception as e:
            raise BankingException(e, sys) from e 
    
    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise BankingException(e, sys) from e      
         
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact) 
            return data_validation
        except Exception as e:
            raise BankingException(e, sys) from e  
        
    def start_data_transformation(self,
                                  data_ingestion_artifact:DataIngestionArtifact,
                                  data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation = DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise BankingException(e, sys) from e 