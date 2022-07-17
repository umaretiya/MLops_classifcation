import os

class Config(object):
    SECRET_KY = os.environ.get('SECRET_KEY') or  b'c7\xb3\xfav\x13\xae\x91\xab\xadFua\x9b\xef\x05'