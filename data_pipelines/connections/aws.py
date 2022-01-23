import tempfile
import boto3
from data_pipelines.connections.core import BaseConn
import json


class AWSConn(BaseConn):
    def __init__(self, **kwargs):
        self.aws_access_key_id = kwargs.get("aws_access_key_id")
        self.aws_secret_access_key = kwargs.get("aws_secret_key_id")
        self.session = None

    def connect(self):
        print(self.aws_access_key_id, self.aws_secret_access_key)
        self.session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def close(self):
        pass


class S3Conn(AWSConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.s3_bucket = kwargs.get("s3_bucket")
        self.s3_key = kwargs.get("s3_key")

    def connect(self):
        super().connect()
        self.s3_client = self.session.client("s3")

    def _write_json(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, default=str)

    def _read_json(self, path):
        with open(path) as f:
            data = json.load(f)
        return data

    def get_data(self, **kwargs):
        """
        1. open up a temp directory as /temp_dir/data.json
        2. use s3_client.download_file to download the file to temp_directory
        3. read the file into the memory as a json
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = f"{temp_dir}/data.json"
            self.s3_client.download_file(
                self.s3_bucket, self.s3_key, temp_path
            )
            return self._read_json(temp_path)

    def load_data(self, data, **kwargs):
        """"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = f"{temp_dir}/data.json"
            self._write_json(temp_path, data)
            self.s3_client.upload_file(temp_path, self.s3_bucket, self.s3_key)


if __name__ == "__main__":
    kwargs = {"s3_key": "data.json", "s3_bucket": "test-bucket-henry-093"}
    myconn = S3Conn(**kwargs)

    with myconn:
        data = myconn.get_data()
        print(data)