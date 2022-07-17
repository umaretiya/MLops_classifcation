from distutils.command.config import config

from django import conf
from banking.exception import BankingException
from banking.logger import logging
from banking.entity.artifact_entity import DataIngestionArtifact
from banking.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from banking.component.data_ingestion import DataIngestion
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