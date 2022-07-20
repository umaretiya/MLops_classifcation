import yaml
import os, sys
from banking.exception import BankingException
import dill
from banking.constant import *

import numpy as np, pandas as pd , os, sys 


def write_yaml_file(file_path, data:dict):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            yaml.dump(data, yaml_file)
    except Exception as e:
        raise BankingException(e, sys) from e 
    

def read_yaml_file(file_path:str)->dict:
    """_summary_
    read a yaml file and return as dict
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise BankingException(e, sys) from e
    
def save_numpy_array_data(file_path, array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise BankingException(e, sys) from e
    
def load_numpy_array_data(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise BankingException(e, sys) from e 
    
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise BankingException(e, sys) from e 
    
def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise BankingException(e, sys) from e 
    

def load_data(file_path, schema_file_path):
    try:
        dataset_schema = read_yaml_file(schema_file_path)
        # print(f"------load_data util --->>>>>>>>  {dataset_schema}  <<<<<<----dataset_schem-------")
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]
        # print(f"------load_data util --->>>>>>>>  {schema}  <<<<<<----schema-------")
        dataframe = pd.read_csv(file_path)
        # print(f"------load_data util --->>>>>>>>  {len(dataframe)}  <<<<<<----dataframe-------")
        error_message = ""
        # print(f"------load_data util --->>>>>>>>  {list(schema.keys())}  <<<<<<----shcema key-------")
        # print(f"------load_data util --->>>>>>>>  {dataframe.columns}  <<<<<<----shcema key-------")
        for column in dataframe.columns:
            # print(f"------load_data util --->>>>>>>>  {column}  <<<<<<----dataframe.columns-------")
            if column in list(schema.keys()):
                # print(f"------load_data util --if condition->>>>>>>>  {column}  <<<<<<----in dataframe.columns-------")
                # print(f"------load_data util --if condition->>>>>>>>  {schema[column]}  <<<<<<----in dataframe.columns-------")
                dataframe[column].astype(schema[column])
            else:
                error_message = f"{error_message} \nColumn:[{column}] is not in the schema."
        if len(error_message) > 0:
            raise Exception(error_message)
        return dataframe        
    
    except Exception as e:
        raise BankingException(e, sys) from e 
    
# def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    # try:
    #     datatset_schema = read_yaml_file(schema_file_path)

    #     schema = datatset_schema[DATASET_SCHEMA_COLUMNS_KEY]

    #     dataframe = pd.read_csv(file_path)

    #     error_messgae = ""


    #     for column in dataframe.columns:
    #         if column in list(schema.keys()):
    #             dataframe[column].astype(schema[column])
    #         else:
    #             error_messgae = f"{error_messgae} \nColumn: [{column}] is not in the schema."
    #     if len(error_messgae) > 0:
    #         raise Exception(error_messgae)
    #     return dataframe