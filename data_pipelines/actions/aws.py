from data_pipelines.actions.core import SourceToSink
from data_pipelines.connections.core import HTTPConn, PostgresConn
from data_pipelines.connections.aws import S3Conn


class AppDataBaseToS3(SourceToSink):
    source_class = HTTPConn
    sink_class = S3Conn


class S3ToDatawarehouse(SourceToSink):
    source_class = S3Conn
    sink_class = PostgresConn
