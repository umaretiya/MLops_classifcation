from kaggle.api.kaggle_api_extended import KaggleApi
import os ,json 
from pathlib import Path 
from os import environ
from dotenv import load_dotenv
from sklearn import datasets

       
path = os.path.join('D:\PycharmProjects\DS_ML_Self\MLops_classifcation','.env')
load_dotenv(path)

api =  KaggleApi()
api.authenticate()

download_url = "https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset?select=UCI_Credit_Card.csv"
# DATASET = "uciml/default-of-credit-card-clients-dataset"
# FILE_NAME = "UCI_Credit_Card.csv"

class KaggleDataset:
    
    def __init__(self,download_zip_path):

        self.download_dir_path = download_zip_path
        
    def kaggle_jason_file(self):
        api_key = {"username":environ.get("KAGGLE_USERNAME"),"key":environ.get("KAGGLE_KEY")}
        __file__ = 'kaggle.json'
        config = "kaggle.json"
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(ROOT_DIR, config)
        with open(CONFIG_PATH,'w') as kaggle:
            json.dump(api_key,kaggle)

    def kaggle_data(self,dataset,file_name):
        # dataset = "uciml/default-of-credit-card-clients-dataset"
        # file_name = "UCI_Credit_Card.csv"
        api.dataset_download_file(
            dataset = dataset,
            file_name=file_name,
            path=self.download_dir_path
        )
    

# KaggleDataset.kaggle_jason_file()
# KaggleDataset.kaggle_data()
