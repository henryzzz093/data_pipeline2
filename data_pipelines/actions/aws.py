from data_pipelines.actions.core import SourceToSink
from data_pipelines.connections.core import HTTPConn, PostgresConn
from data_pipelines.connections.aws import S3Conn


class AppDataBaseToS3(SourceToSink):
    source_class = HTTPConn
    sink_class = S3Conn


class S3ToDatawarehouse(SourceToSink):
    source_class = S3Conn
    sink_class = PostgresConn


if __name__ == "__main__":
    source_kwargs_1 = {
        "url": "http://127.0.0.1:5000",
        "params": {"date": "2021-01-02", "table_name": "customers"},
    }
    sink_kwargs_1 = {
        "s3_key": "data.json",
        "s3_bucket": "data-pipeline-datalake-henry",
    }

    kwargs_1 = {"source_kwargs": source_kwargs_1, "sink_kwargs": sink_kwargs_1}

    source_kwargs_2 = {
        "s3_key": "data.json",
        "s3_bucket": "data-pipeline-datalake-henry",
    }

    sink_kwargs_2 = {
        "host": "localhost",
        "port": 5438,
        "username": "henry",
        "password": "henry",
        "database": "henry",
        "table": "customers",
        "schema": "henry",
    }

    kwargs_2 = {"source_kwargs": source_kwargs_2, "sink_kwargs": sink_kwargs_2}

    extract = AppDataBaseToS3(**kwargs_1)
    load = S3ToDatawarehouse(**kwargs_2)
    extract.run()
    load.run()
