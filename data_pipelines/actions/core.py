import json
import logging
import os
from abc import ABC, abstractmethod
from os.path import isfile

from airflow.exceptions import AirflowSkipException
from jinja2 import Environment, PackageLoader

from data_pipelines.connections.core import (
    CSVConn,
    JsonlConn,
    PostgresConn,
    TextConn,
    MySQLConn,
)

DEFAULT_LOGGER = logging.getLogger(__name__)


class BaseAction(ABC):
    """
    Base action calss that should be inherited from
    """

    def __init__(self, **kwargs):
        self.log = DEFAULT_LOGGER
        self.jinja_env = Environment(
            loader=PackageLoader("data_pipelines", "templates")
        )

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
        super().__init__(**kwargs)

        source_kwargs = kwargs.get(
            "source_kwargs", {}
        )  # if the key not exist, return the defalt values (emply dict)
        sink_kwargs = kwargs.get("sink_kwargs", {})

        self.source = self.source_class(**source_kwargs)
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

    def load_data(self, data, *args, **kwargs):
        """
        Loads data with the sink class
        """
        self.sink.load_data(data, *args, **kwargs)

    def run(self):
        """
        The core function that is executed by the airflow operator class
        """
        with self.source, self.sink:
            for data in self.source.get_data():
                data = self.transform_data(data)
                self.log.info(str(data))
                self.load_data(data)
            self.log.info("Data Load Success!")


class CSVToCSV(SourceToSink):
    source_class = CSVConn
    sink_class = CSVConn

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._write_header = True
        if self._file_exists:
            self._write_header = False

    @property
    def _file_exists(self):
        return isfile(self.sink.filepath)

    def run(self):
        """
        The core function that is executed by the airflow operator class.
        """
        with self.source:
            data = self.get_data()
            data = [*data]  # unpack the generater
            if data:
                with self.sink:
                    for item in data:
                        item = self.transform_data(item)
                        self.log.info(str(item))
                        self.load_data(item, self._write_header)
                    self.log.info("Data Load Success!")

            else:
                raise AirflowSkipException("No data available!")


class TextToText(SourceToSink):

    source_class = TextConn
    sink_class = TextConn

    def transform_data(self, data):
        return data.upper()

    def run(self):
        """
        The core function that is executed by the airflow operator class.
        """
        with self.source, self.sink:
            for line in self.source.get_data():
                line = self.transform_data(line)
                self.log.info(str(line))
                self.load_data(line)
            self.log.info("Data Load Success!")


class CSVToJsonl(SourceToSink):

    source_class = CSVConn
    sink_class = JsonlConn

    def transform_data(self, data):
        return f"{json.dumps(data)}\n"

    def run(self):
        """
        The core function that is executed by the airflow operator class
        """

        with self.source:
            data = self.get_data()
            data = [*data]  # unpack the generator
            if data:  # if the date exists, then process
                with self.sink:
                    for item in data:
                        item = self.transform_data(item)
                        self.log.info(str(item))
                        self.load_data(item)
                    self.log.info("Data Load Success!")

            else:  # otherwise, raise Airflow Skip Execption and skip the current date
                raise AirflowSkipException("No Data Available on that date !")


class CSVToPostgres(SourceToSink):
    source_class = CSVConn
    sink_class = PostgresConn

    def transform_data(self, data):
        for row in data:
            columns = [key.lower().replace(" ", "_") for key in row.keys()]
            values = list(row.values())
            dict1 = dict(zip(columns, values))
            yield dict1

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

            else:  # otherwise, raise Airflow Skip Execption and skip the current date
                raise AirflowSkipException("No Data Available on that date !")


class CSVTOMySQL(SourceToSink):
    source_class = CSVConn
    sink_class = MySQLConn

    def transform_data(self, data):
        for row in data:
            columns = [key.lower().replace(' ', '_') for key in row.keys()] # get the columns name as a list()
            values = list(row.values())
            mydict = dict(zip(columns, values))
            yield mydict

    def run(self):
        '''
        The core function that is executed by the airflow operator class
        '''
        with self.source:
            data = self.get_data()
            data = [*data]
            if data: 
                with self.sink:
                    data = self.transform_data(data)
                    self.load_data(data)
                self.log.info('Data Load Success!')

            else:
                raise AirflowSkipException('No Data Found on that date !')



if __name__ == "__main__":
    from dotenv import load_dotenv

    source_kwargs = {"date": "2021-07-02"}

    load_dotenv()
    sink_kwargs = {
        # "host": "localhost",
        "port": '3306',
        "username": os.getenv("MySQL_USERNAME"),
        "password": os.getenv("MySQL_PASSWORD"),
        "schema":"sys",
        "database": "sys",
        "table":"test",
    }

    kwargs = {
        "source_kwargs": source_kwargs,
        "sink_kwargs": sink_kwargs,
    }

    action_class = CSVTOMySQL(**kwargs)
    with action_class.source:
        data =  action_class.get_data()
        data = action_class.transform_data(data)
        for item in data:
            print(item)
