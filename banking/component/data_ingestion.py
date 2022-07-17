from posixpath import split
from banking.exception import BankingException
from banking.logger import logging 
from banking.entity.artifact_entity import DataIngestionArtifact
from banking.entity.config_entity import DataIngestionConfig

from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np 
import pandas as pd 

import os, sys
import zipfile,tarfile


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*25}Data ingestion Started {'<<'*25}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise BankingException(e, sys) from e

    def download_bankig_data(self):
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir
            
            os.makedirs(tgz_download_dir,exist_ok=True)
            
            bankig_file_name = os.path.basename(download_url)
            tgz_file_path = os.path.join(tgz_download_dir,bankig_file_name)
            
            logging.info(f"Downloading file from: [{download_url}] into: [{tgz_file_path}]")
            """"
            kaggle datasets need to re work and set logic accordingly
            also zip file 
            """
            return tgz_file_path
        except Exception as e:
            raise BankingException(e, sys) from e
        
    def exctracted_tgz_file(self, tgz_file_path):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            
            os.makedirs(raw_data_dir, exist_ok=True)
            logging.info(f"Exctracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            
            with tarfile.open(tgz_file_path) as banking_tgz_file_obj:
                banking_tgz_file_obj.extractall(path=raw_data_dir)
            logging.info(f"Exctracted completed")
            
        except Exception as e:
            raise BankingException(e, sys) from e
        
    def split_data_as_train_test(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            banking_file_path = os.path.join(raw_data_dir,file_name)
            
            logging.info(f"Rading csv file: [{banking_file_path}]")
            banking_data_frame = pd.read_csv(banking_file_path)
            """_summary_
            X,y need to set : pending.........
            """
            strat_train_set=None
            strat_test_set = None
            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
            
            for train_index,test_index in split.split(banking_data_frame,banking_data_frame.iloc[:,-1]):
                strat_train_set = banking_data_frame.loc[train_index]
                strat_test_set = banking_data_frame.loc[test_index]
            
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting traing set to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)
                
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting traing set to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
                
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message=f"Data ingestion completed successfully.")
            logging.info(f"Data Ingestion artifact: [{data_ingestion_artifact}]")
            return data_ingestion_artifact
            
        except Exception as e:
            raise BankingException(e, sys) from e
        
    def initiate_data_ingestion(self):
        try:
            tgz_file_path = self.download_bankig_data()
            self.exctracted_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise BankingException(e, sys) from e