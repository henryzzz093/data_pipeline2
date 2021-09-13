import os
import tempfile

import boto3
import json


# from dotenv import load_dotenv
from data_pipelines.connections.core import BaseConn, CSVConn


class AWSConn(BaseConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.aws_access_key_id = kwargs.get('AWS_ACCESS_KEY')
        self.aws_secret_key_id = kwargs.get('AWS_SECRET_KEY')
        self.session = None

    def connect(self):
        self.session = boto3.Session(
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_key_id
        )
        return self.session.client('sts') # AWS Security Token Service

        

    def close(self):
        pass

class S3Conn(AWSConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3_bucket = kwargs.get('s3_bucket')
        self.s3_key = kwargs.get('s3_key')

    def connect(self):
        super().connect()
        self.s3_client = self.session.client('s3')

    def get_data(self):
        pass

    def load_data(self, data):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = f'{temp_dir}/data.json'
            with open(temp_path, 'w') as f:
                json.dump(data, f)

            self.s3_client.upload_file(temp_path, self.s3_bucket, self.s3_key)



        
        


# if __name__ == '__main__':
#     load_dotenv()
#     my_aws_access = os.getenv('AWS_ACCESS_KEY')
#     my_secret_access = os.getenv('AWS_SECRET_KEY')
#     kwargs = {
#         'AWS_ACCESS_KEY':my_aws_access,
#         'AWS_SECRET_KEY':my_secret_access,
#         's3_bucket': 'test-bucket-henry-093',
#         's3_key':'data-pipelines-2/data.json',
#     }

#     csv_kwargs = {
#         "date": "2021-06"
#     }

#     s3_conn = S3Conn(**kwargs)
#     csv_conn = CSVConn(**csv_kwargs)

    

#     with csv_conn:
#         data = csv_conn.get_data()
#         data = [*data]
#         with s3_conn:   
#             s3_conn.load_data(data)
#     print('Success!')


    
    
