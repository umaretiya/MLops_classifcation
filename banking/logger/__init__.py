
import logging
from datetime import datetime
import os 
import pandas as pd
from banking.constant import get_current_time_stamp

LOG_DIR = "logs"

def get_log_file_name():
    return f"log_{get_current_time_stamp()}.log"

LOG_FILE_NAME = get_log_file_name()
os.makedirs(LOG_DIR,exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode="w",
                    format='[%(asctime)s]^; %(levelname)s^; %(lineno)d^; %(filename)s^; %(funcName)s()^; %(message)s',
                    level=logging.INFO)

def get_log_dataframe(file_path):
    data = []
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))
            
    log_df = pd.DataFrame(data)
    column = ["TimeStamp","LogLevel","LineNumber","FileName","FunctionName","Message"]
    log_df.columns = column
    
    log_df['log_message'] = log_df['TimeStamp'].astype(str) + ":$" + log_df["Message"]
    return log_df[["log_message"]]