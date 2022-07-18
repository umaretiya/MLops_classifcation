import os
from dotenv import load_dotenv



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or  b'c7\xb3\xfav\x13\xae\x91\xab\xadFua\x9b\xef\x05'
    KAGGLE_USERNAME=os.environ.get("KAGGLE_USERNAME")
    KAGGLE_KEY=os.environ.get("KAGGLE_KEY")
