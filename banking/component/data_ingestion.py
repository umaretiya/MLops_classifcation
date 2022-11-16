from banking.exception import BankingException
from banking.logger import logging 
from banking.entity.artifact_entity import DataIngestionArtifact
from banking.entity.config_entity import DataIngestionConfig
from banking.component.kaggle_data import KaggleDataset
from banking.constant import *
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split
import numpy as np 
import pandas as pd 

import os, sys,shutil
import zipfile


class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*25}Data ingestion Started {'<<'*25}")
            self.data_ingestion_config = data_ingestion_config
        
        except Exception as e:
            raise BankingException(e, sys) from e

    def download_bankig_data(self):
        try:
            
            # download_url = self.data_ingestion_config.dataset_download_url
    
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir # target dir 
            
            os.makedirs(tgz_download_dir,exist_ok=True)
            # banking_file_name = self.data_ingestion_config.dataset_file_name
            
            tgz_file_name = self.data_ingestion_config.dataset_zip_file_name # zipfile name 
            source_data_dir = ROOT_DIR
            src = os.path.join(source_data_dir, tgz_file_name)
            # kaggel = KaggleDataset(tgz_download_dir)
            
            # kaggel.kaggle_jason_file()
            # kaggel.kaggle_data(download_url, banking_file_name)
        
            shutil.copy(src, tgz_download_dir)
            zip_file_path = os.path.join(tgz_download_dir,tgz_file_name)
          
            return zip_file_path
        
        except Exception as e:
            raise BankingException(e, sys) from e 

            
    def exctracted_tgz_file(self, zip_file_path):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            os.makedirs(raw_data_dir, exist_ok=True)
            logging.info(f"raw data dir created")
            
            with zipfile.ZipFile(zip_file_path, 'r') as zipref:
                zipref.extractall(raw_data_dir)
            file_name = os.listdir(raw_data_dir)[0]
            
            banking_file_path = os.path.join(raw_data_dir,file_name)
            banking_data_frame = pd.read_csv(banking_file_path)
            banking_data_frame.rename(mapper={'default.payment.next.month':"default"},axis=1,inplace=True)
            banking_data_frame.to_csv(banking_file_path,index=False)
        except Exception as e:
            raise BankingException(e, sys) from e 
        
    def split_data_as_train_test(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            banking_file_path = os.path.join(raw_data_dir,file_name)
            
            logging.info(f"Rading csv file: [{banking_file_path}]")
            banking_data_frame = pd.read_csv(banking_file_path)
            # banking_data_frame.rename(mapper={'default.payment.next.month':"default"},axis=1,inplace=True)
            
            # X = banking_data_frame.drop(labels=['default'], axis=1)
            # y = banking_data_frame['default']
            strat_train_set=None
            strat_test_set = None
            # split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
            
            # for train_index,test_index in split.split(banking_data_frame,banking_data_frame.iloc[:,-1]):
            #     strat_train_set = banking_data_frame.loc[train_index]
            #     strat_test_set = banking_data_frame.loc[test_index]
            strat_train_set,strat_test_set = train_test_split(banking_data_frame,test_size=0.3, random_state=42)
            
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
            zip_file_path = self.download_bankig_data()
            self.exctracted_tgz_file(zip_file_path=zip_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise BankingException(e, sys) from e