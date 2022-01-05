import csv
import json
import logging
from abc import ABC, abstractmethod
from os.path import abspath, dirname
import requests

import psycopg2
import mysql.connector as mysql


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        self.log = logger

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.filepath = kwargs.pop("filepath")
        except KeyError as err:
            self.log.warning("filepath kwargs must be set!")
            raise KeyError(err)

        try:
            self.file_permission = kwargs.pop("file_permission")
        except KeyError as err:
            self.log.warning("file_permission kwargs must be set!")
            raise KeyError(err)

        if self.file_permission not in ("r", "w"):
            raise Exception('file_permission kwargs can only be "w" or "r"')

    def connect(self):
        """
        Establishes connection to file
        """
        self.conn = open(
            self.filepath, self.file_permission
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

        if self.file_permission == "w":
            self.write_header = (
                True  # if it is 'w', we only write the header once.
            )

    def get_data(self):
        """
        Contains logic to retrieve data from csv file.
        """
        log_message = f"Retrieving data from: {self.filepath}"
        self.log.info(log_message)
        reader = csv.DictReader(self.conn)
        for row in reader:
            yield row

    def load_data(self, data, *args, **kwargs):
        """
        Contains logic to write data to csv file.
        """
        self.log.info(f"Writing data to: {self.filepath}")
        for row in data:
            writer = csv.DictWriter(self.conn, fieldnames=row.keys())
            if self.write_header:  # allow us to write the header only once
                writer.writeheader()
                self.write_header = False
            writer.writerow(row)


class TextConn(FileConn):
    """
    Connection class used to :
    1. establish connection to text files
    2. get data from text files
    3. load data to text files
    """

    def get_data(self):
        """
        Contains logic to retrieve data from csv file
        """
        self.log.info(f"Retrieving data from: {self.filepath}")
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
        self.log.info(f"Writing data to: {self.filepath}")
        for line in data:
            self.conn.write(line)


class JsonConn(FileConn):
    def get_data(self):
        self.log.info('f"Retrieving data from: {self.filepath}')
        yield json.load(self.conn)

    def load_data(self, data):
        self.log.info(f"Writing data to: {self.filepath}")
        for item in data:
            json.dump(item, self.conn, indent=4)


class JsonlConn(FileConn):
    """
    Connection class used to :
    1. establish connection to json files
    2. get data from json files
    3. load data to json files
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_source = kwargs.get("is_source")

        if self.is_source:  # if is_source == True
            self.file_type = "r"
            file_dir = "input"
            filename = "raw_data"

        else:  # if it is not set to True, we assume it is sink conn
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
        Contains logic to write data to jsonl file.
        """
        self.conn.write(data)


class DBConn(BaseConn):
    """
    Database Connection class used to :
    1. establish connection to Rational Database Management System (RDBMS)
    2. get data from RDBMS
    3. load data to RDBMS
    """

    def __init__(self, **kwargs):
        """
        Constructing the connection by using the following keywords arguments
        """
        super().__init__(**kwargs)
        self.host = kwargs.get("host", "host.docker.internal")
        self.port = kwargs.get("port")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.database = kwargs.get("database")
        self.schema = kwargs.get("schema")
        self.table = kwargs.get("table")

    def close(self):
        """
        Close the connection
        """
        self.conn.close()

    def get_data_full(self):
        pass

    def get_data(self):
        pass

    def load_data(self, data):
        """
        1. setup connection to the cursor
        2. extract column name and row values from the dictionary file # noqa:E501
        3. Insert into the table by using cursor execute SQL statement
        """
        with self.conn.cursor() as cursor:
            for row in data:
                try:
                    columns = ", ".join(
                        row.keys()
                    )  # extract column names from dictionary
                    values = list(row.values())
                    values_template = str(
                        tuple("%s" for val in values)
                    ).replace(
                        "'", ""
                    )  # create a placeholder value template
                    sqlstatement = f"INSERT INTO {self.schema}.{self.table} ({columns}) VALUES {values_template}"  # noqa:E501
                    self.log.info(sqlstatement)
                    cursor.execute(sqlstatement, values)
                    self.conn.commit()

                except (mysql.IntegrityError, psycopg2.IntegrityError) as err:
                    self.log.warning("Duplicate Found! {row}")
                    self.log.warning(err)
                    self.conn.commit()


class PostgresConn(DBConn):
    """
    Inheritance from the database connection to :
    1. establish connection to PostgreSQL Connection (RDBMS)
    2. get data from PostgreSQL
    3. load data to PostgreSQL
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.port = kwargs.get(
            "port", "5432"
        )  # noqa:E501 check to see if the port values exist, if it is not, we set the default port to 5432

    def connect(self):
        """
        connect to the PostgresSQL DB
        """
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database,
        )  # using psycopg2 to create a connection to the database


class MySQLConn(DBConn):
    """
    Inheritance from the database connection to :
    1. establish connection to MySQL Connection (RDBMS)
    2. get data from MySQL
    3. load data to MySQL
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.port = kwargs.get("port", "3306")

    def connect(self):
        """
        To test if we connected to the database
        """
        self.conn = mysql.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database,
        )


class HTTPConn(BaseConn):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = kwargs.get("url")
        self.headers = kwargs.get("headers")
        self.params = kwargs.get("params")
        self.method = kwargs.get("method", "GET")

    def connect(self):
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def _send_request(self, data=None, timeout=None):
        req = requests.Request(
            url=self.url,
            method=self.method,
            params=self.params,
            headers=self.headers,
            json=data,
        )
        prepared = self.session.prepare_request(req)
        response = self.session.send(prepared, timeout=timeout)
        response.raise_for_status()
        return response

    def get_data(self):
        response = self._send_request()
        return response.json()

    def load_data(self, data):
        pass


if __name__ == "__main__":

    from pprint import pprint

    kwargs = {"url": "http://127.0.0.1:5000", "params": {"date": "2021-01-01"}}

    conn = HTTPConn(**kwargs)

    with conn:
        data = conn.get_data()
        pprint(data)
