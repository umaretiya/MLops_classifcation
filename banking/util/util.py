import yaml
import os, sys
from banking.exception import BankingException




def read_yaml_file(file_path):
    """_summary_
    read a yaml file and return as dict
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise BankingException(e, sys) from e