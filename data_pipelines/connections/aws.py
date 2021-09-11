import boto3 
from connections.core import BaseConn


class AWSConn(BaseConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect(self):
        pass

    def close(self):
        pass

def S3Conn(AWSConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect(self):
        pass

    def get_data(self):
        pass

    def load_data(self):
        pass


