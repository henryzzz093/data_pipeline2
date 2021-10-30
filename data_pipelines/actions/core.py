import logging
from abc import ABC, abstractmethod

from airflow.exceptions import AirflowSkipException

from data_pipelines.connections.core import (
    CSVConn,
    JsonConn,
    PostgresConn,
    TextConn,
    MySQLConn,
)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BaseAction(ABC):
    """
    Base action calss that should be inherited from ABC

    Attributes:
        log: the log string
    """

    def __init__(self):
        self.log = logger

    @abstractmethod
    def run(self):
        """
        Abstract method that must be overwritten dy child class
        """
        pass


class SourceToSink(BaseAction):
    """
    This class contains the core logic to transport data
    from a source class to a sink class performing all
    applied transformation logic in the process
    """

    def __init__(self, **kwargs):
        super().__init__()

        source_kwargs = kwargs.get(
            "source_kwargs", {}
        )  # if the key not exist, return the defalt values (emply dict)
        sink_kwargs = kwargs.get("sink_kwargs", {})

        self.source = self.source_class(
            **source_kwargs
        )  # instantiate source & sink from the parent class
        self.sink = self.sink_class(**sink_kwargs)

    def get_data(self):
        """
        Pulls data from source class.
        """
        return self.source.get_data()

    def transform_data(self, data):
        """
        Overriden to provide transformation logic
        """
        return data

    def load_data(self, data, **kwargs):
        """
        Loads data with the sink class
        """
        self.sink.load_data(data, **kwargs)

    def run(self):
        """
        The core function that is executed by the airflow operator class
        """
        with self.source, self.sink:
            data = self.get_data()
            data = self.transform_data(data)
            self.load_data(data)
            self.log.info("Data Load Success!")


class CSVToCSV(SourceToSink):
    """
    This class contains the core logic to transport data
    from a source CSV connection to a sink CSV connection performing all
    applied transformation logic in the process
    """

    source_class = (
        CSVConn  # assign the source_class to CSV connection from child class
    )
    sink_class = (
        CSVConn  # assign the sink_class to CSV connection from child class
    )


class TextToText(SourceToSink):
    """
    This class contains the core logic to transport data
    from a source Text connection to a sink Text connection performing all
    applied transformation logic in the process
    """

    source_class = TextConn
    sink_class = TextConn

    def transform_data(self, data):
        """
        Turn all the data to uppercase
        """
        for line in data:
            line = line.upper()
            yield line


class JsonToJson(SourceToSink):
    """
    This class contains the core logic to transport data
    from a source JSON connection to a sink Json connection performing all
    applied transformation logic (if needed) in the process
    """

    source_class = JsonConn
    sink_class = JsonConn


class CSVToPostgres(SourceToSink):
    """
    This class contains the core logic to transport data
    from a source CSV connection to a sink Postgres connection performing all
    applied transformation logic in the process
    """

    source_class = CSVConn
    sink_class = PostgresConn

    def transform_data(self, data):
        """
        Extract the columns name, attributes from the data,
        constructing a new dictionary based on the keys and values
        """
        for row in data:
            yield {
                key.lower().replace(" ", "_"): value
                for key, value in row.items()
            }

    def run(self):
        """
        The core function that is executed by the airflow operator class
        """
        with self.source:
            data = self.get_data()
            data = [*data]  # unpack the generator
            if data:  # if the date exists, then process
                with self.sink:
                    data = self.transform_data(data)
                    self.load_data(data)
                self.log.info("Data Load Success!")

            else:  # otherwise, raise Airflow Skip Execption and skip the current date # noqa:E501
                raise AirflowSkipException("No Data Available on that date !")


class CSVToMySQL(SourceToSink):
    """
    This class contains the core logic to transport data
    from a source CSV connection to a sink MySQL connection performing all
    applied transformation logic in the process
    """

    source_class = CSVConn
    sink_class = MySQLConn

    def transform_data(self, data):
        """
        Extract the columns name, attributes from the data,
        constructing a new dictionary based on the keys and values
        """

        for row in data:
            yield {
                key.lower().replace(" ", "_"): value
                for key, value in row.items()
            }

    def run(self):
        """
        The core function that is executed by the airflow operator class
        """
        with self.source:
            data = self.get_data()
            data = [*data]
            if data:
                with self.sink:
                    data = self.transform_data(data)
                    self.load_data(data)
                self.log.info("Data Load Success!")

            else:
                raise AirflowSkipException("No Data Found on that date !")
