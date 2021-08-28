import csv
import json
import logging
from abc import ABC, abstractmethod
from os.path import abspath, dirname

DEFAULT_LOGGER = logging.getLogger(__name__)


class BaseConn(ABC):
    """
    Based connection class that should be inherited.
    """

    def __init__( # constructor for BaseConn class, initialize variables
        self,
        host=None,
        login=None,
        password=None,
        schema=None,
        extra=None,
        logger=DEFAULT_LOGGER,
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

    def connect(self):
        """
        Establishes connection to file
        """
        self.conn = open(self.filepath, self.file_type) # open up a connection toward the selected path and files
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
        self.date = kwargs.get("date")  #?
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
        for line in self.conn.readlines():   # file.readlines() return each lines from the file
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
        self.is_source = kwargs.get(
            'is_source', True
        )

        if self.is_source: # if is_source == True
            self.file_type = 'r'
            file_dir = 'input'
            filename = 'raw_data'
        
        else:
            self.file_type = 'a'
            file_dir = 'output'
            filename = 'output_data'

        self.filepath = dirname(abspath(__file__)).replace(
            'connections', f"data/{file_dir}/{filename}.jsonl"
        )
        
    def get_data(self):
        pass


    def load_data(self, data, *args, **kwargs):
        """
        Contains logic to write data to json file.
        """ 
        self.conn.write(data)

            





        
        


if __name__ == '__main__':

    source_class = CSVConn(date="2021-06-30")

    sink_kwargs = {'is_source': False}
    sink_class = JsonlConn(**sink_kwargs) #set this to true for testing TextConn
    

    with source_class, sink_class :
        for row in source_class.get_data():
            # print(row)
            # sink_class.load_data(row)
            # sink_class.load_data(row, write_header)
            # write_header = False
            #json.dump(json.loads(json.dumps(row)), f) #json.dumps turns ordered dict to a string
                                                      #json.loads turns string to a dictionary
                                                      #json.dump save dictionary to json file

            sink_class.load_data(row)
