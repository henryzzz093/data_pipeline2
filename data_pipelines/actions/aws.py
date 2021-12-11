from data_pipelines.actions.core import SourceToSink
from data_pipelines.connections.core import HTTPConn
from data_pipelines.connections.aws import S3Conn


class AppDataBaseToS3(SourceToSink):
    source_class = HTTPConn
    sink_class = S3Conn


if __name__ == "__main__":
    source_kwargs = {
        "url": "http://127.0.0.1:5000",
        "params": {"date": "2021-01-02", "table_name": "customers"},
    }
    sink_kwargs = {
        "s3_key": "data.json",
        "s3_bucket": "data-pipeline-datalake-henry",
    }

    kwargs = {"source_kwargs": source_kwargs, "sink_kwargs": sink_kwargs}
    test = AppDataBaseToS3(**kwargs)
    test.run()
