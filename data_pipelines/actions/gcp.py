from data_pipelines.actions.core import SourceToSink
from data_pipelines.connections.core import HTTPConn
from data_pipelines.connections.gdrive import GDriveConn


class AppDataBaseToGDrive(SourceToSink):
    source_class = HTTPConn
    sink_class = GDriveConn
