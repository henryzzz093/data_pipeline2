from re import S
from data_pipelines.actions.core import SourceToSink
from data_pipelines.connections.core import HTTPConn
from data_pipelines.connections.gdrive import GDriveConn

class AppDataBaseToGDrive(SourceToSink):
    source_class = HTTPConn
    sink_class = GDriveConn

if __name__ == "__main__":
    source_kwargs = {
        "url": "http://127.0.0.1:5000",
        "params": {"date": "2022-01-18", "table_name": "customers"},
    }

    sink_kwargs = {
        "connection_id": "gdrive_default",
        "file_ext": "csv",
        "folder_name": "Testing1"
    }

    kwargs = {"source_kwargs":source_kwargs, "sink_kwargs":sink_kwargs}


    actionclass = AppDataBaseToGDrive(**kwargs)
    actionclass.run()
    
