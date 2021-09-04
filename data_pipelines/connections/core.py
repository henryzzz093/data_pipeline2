import csv
import json
import logging
import os
from abc import ABC, abstractmethod
from os.path import abspath, dirname

import psycopg2


class BaseConn(ABC):
    """
    Based connection class that should be inherited.
    """

    def __init__(  # constructor for BaseConn class, initialize variables
        self,
        host=None,
        login=None,
        password=None,
        schema=None,
        extra=None,
        *args,
        **kwargs,
    ):
        self.host = host
        self.login = login
        self.password = password
        self.schema = schema
        self.extra = extra
        self.log = logging.getLogger(__name__)

    @abstractmethod
    def connect(self):
        """
        abstract method that should be overwritten by child class
        """
        pass

    @abstractmethod
    def close(self):
        """
        abstract method that should be overwritten by child class
        """
        pass

    def __enter__(self):
        """
        context manager
        """
        self.connect()

    def __exit__(self, *args, **kwargs):
        """
        context manager
        """
        self.close()

    @abstractmethod
    def get_data(self, **kwargs):
        """
        abstract method that should be overwritten by child class
        """
        pass

    @abstractmethod
    def load_data(self, **kwargs):
        """
        abstract method that should be overwritten by child class
        """
        pass


class FileConn(BaseConn):
    def connect(self):
        """
        Establishes connection to file
        """
        self.conn = open(
            self.filepath, self.file_type
        )  # open up a connection toward the selected path and files
        self.log.info("connection success")

    def close(self):
        """
        Closes conenction to file.
        """
        self.conn.close()
        self.log.info("connection closed")


class CSVConn(FileConn):
    """
    Connection class used to :
    1. establish connection to csv files
    2. get data from csv files
    3. load data to csv files
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date = kwargs.get("date")  # ?
        self.is_source = kwargs.get("is_source", True)

        if self.is_source:
            self.file_type = "r"  # read
            file_dir = "input"
            filename = "raw_data"
        else:
            self.file_type = "a"  # noqa:E501 append if file exist it will just append, write function will overwrite the file if the file does exist.
            file_dir = "output"
            filename = "output_data"

        self.filepath = dirname(abspath(__file__)).replace(
            "connections", f"data/{file_dir}/{filename}.csv"
        )

    def get_data(self):
        """
        Contains logic to retrieve data from csv file.
        """
        self.log.info(f"Retrieving data for: {self.date}")
        reader = csv.DictReader(self.conn)
        for row in reader:
            if self.date in row["Date"]:  # filtering
                yield row

    def load_data(self, data, write_header, *args, **kwargs):
        """
        Contains logic to write data to csv file.
        """

        writer = csv.DictWriter(self.conn, fieldnames=data.keys())
        if write_header:
            self.log.info("Writting header")
            writer.writeheader()
        writer.writerow(data)


class TextConn(FileConn):
    """
    Connection class used to :
    1. establish connection to text files
    2. get data from text files
    3. load data to text files
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = kwargs.get("date")  # store the date  # for txt file?
        self.is_source = kwargs.get(
            "is_source", True
        )  # store the is_source, or set default to True

        if self.is_source:  # if is_source == True
            self.file_type = "r"  # read
            file_dir = "input"
            filename = "raw_data"
        else:
            self.file_type = "w"  # noqa:E501 append if file exist it will just append, write function will overwrite the file if the file does exist.
            file_dir = "output"
            filename = "output_data"

        self.filepath = dirname(abspath(__file__)).replace(
            "connections", f"data/{file_dir}/{filename}.txt"
        )

    def get_data(self):
        """
        Contains logic to retrieve data from csv file
        """
        self.log.info(f"Retrieving data for: {self.data}")
        for (
            line
        ) in (
            self.conn.readlines()
        ):  # file.readlines() return each lines from the file
            yield line

    def load_data(self, data, *args, **kwargs):
        """
        Contains logic to write data to text file.
        """
        for line in data:
            self.conn.write(line)


class JsonlConn(FileConn):
    """
    Connection class used to :
    1. establish connection to json files
    2. get data from json files
    3. load data to json files
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_source = kwargs.get("is_source", True)

        if self.is_source:  # if is_source == True
            self.file_type = "r"
            file_dir = "input"
            filename = "raw_data"

        else:
            self.file_type = "a"
            file_dir = "output"
            filename = "output_data"

        self.filepath = dirname(abspath(__file__)).replace(
            "connections", f"data/{file_dir}/{filename}.jsonl"
        )

    def get_data(self):
        pass

    def load_data(self, data, *args, **kwargs):
        """
        Contains logic to write data to json file.
        """
        self.conn.write(data)


class DBConn(BaseConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.host = kwargs.get("host", "host.docker.internal")
        self.port = kwargs.get("port")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.database = kwargs.get("database")
        self.schema = kwargs.get("schema")
        self.table = kwargs.get("table")

    def close(self):
        self.conn.close()

    @abstractmethod
    def get_data_full(self):
        pass


class PostgresConn(DBConn):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.port = kwargs.get("port", "5432")

    def connect(self):
        print(
            self.host, self.port, self.username, self.password, self.database
        )
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database,
        )

    def get_data(self):
        pass

    def get_data_full(self):
        pass

    def load_data(self, data):
        with self.conn.cursor() as cursor:  # setup the conn as cursor
            for row in data:
                try:
                    columns = ", ".join(
                        list(row.keys())
                    )  # extract column names from dictionary
                    values = list(
                        row.values()
                    )  # extract the values from dictionary
                    values_template = str(
                        tuple("%s" for val in values)
                    ).replace(
                        "'", ""
                    )  # create a placeholder value template
                    sql = f"INSERT INTO {self.schema}.{self.table} ({columns}) VALUES {values_template}"
                    cursor.execute(sql, values)
                    self.conn.commit()
                except psycopg2.IntegrityError as err:
                    self.log.warning(f"Duplicate Found! {row}")
                    self.log.warning(err)
                    self.conn.commit()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    kwargs = {
        "port": "5432",
        "username": os.getenv("PG_USERNAME"),
        "password": os.getenv("PG_PASSWORD"),
        "database": "test",
    }
    sink_class = PostgresConn(**kwargs)

    kwargs = {"date": "2021-07"}
    source_class = CSVConn(**kwargs)

    with source_class, sink_class:
        data1 = source_class.get_data()
        data2 = transform_data(data1)
        sink_class.load_data(data2)
