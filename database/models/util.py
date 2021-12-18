import sqlalchemy as sa
import numpy as np
import datetime as dt
from faker import Faker
from jinja2 import Environment, PackageLoader

from database.models.core import (
    Base,
    Products,
    Customers,
    TransactionDetails,
    Transactions,
)
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PRODUCT_LIST = [
    {"name": "hat", "price": 10.99},
    {"name": "cap", "price": 6.99},
    {"name": "shirt", "price": 50.99},
    {"name": "sweater", "price": 69.99},
    {"name": "shorts", "price": 49.99},
    {"name": "jeans", "price": 39.99},
    {"name": "neakers", "price": 32.99},
    {"name": "boots", "price": 199.99},
    {"name": "coats", "price": 249.99},
    {"name": "accessories", "price": 149.99},
]


class DBConn:
    def __init__(self, **kwargs):
        """
        initialize the attributes of a class.
        """
        self.host = kwargs.get("host", "host.docker.internal")
        self.username = kwargs.get("username", "henry")
        self.password = kwargs.get("password", "henry")
        self.database = kwargs.get("database", "henry")
        self.schema = kwargs.get("schema", "henry")
        self.log = logger

    def _get_conn_str(self, database_type):
        """
        return the connection string based on database types
        """

        if database_type == "postgres":
            dbapi = "postgresql"
            port = 5438

        elif database_type == "mysql":
            dbapi = "mysql+pymysql"
            port = 3307

        return f"{dbapi}://{self.username}:{self.password}@{self.host}:{port}"  # noqa: E501

    def get_conn(self, database_type):
        """
        setup the connection to database
        """

        conn_str = self._get_conn_str(database_type)
        connection = sa.create_engine(conn_str, echo=True)
        return connection

    @property
    def _database_types(self):
        return ["mysql", "postgres"]

    def get_session(self, database_type):
        conn = self.get_conn(database_type)
        Session = sa.orm.sessionmaker(bind=conn)
        return Session()


class DataGenerator:
    def __init__(self):
        self.fake = Faker()

    def _get_dates(self):
        start_date = dt.date(2021, 1, 1)  # set the start date
        end_date = dt.datetime.now().date()  # set the end date
        diff = (end_date - start_date).days  # calculate the delta

        for i in range(0, diff):
            date = start_date + dt.timedelta(days=i)  # get each of the data
            date = date.strftime("%Y-%m-%d")  # convert it into datetime string
            yield date

    @property
    def _name(self):
        return self.fake.name()

    @property
    def _address(self):
        return self.fake.address()

    @property
    def _phone(self):
        return self.fake.phone_number()

    def _get_email(self, name):
        first_name = name.split()[0]
        last_name = name.split()[-1]

        index = np.random.randint(0, 3)
        domains = ["gmail", "yahoo", "outlook"]
        email = f"{first_name}.{last_name}@{domains[index]}.com"
        return email.lower()

    @property
    def _product_id(self):
        product_ids = list(
            range(1, len(PRODUCT_LIST) + 1)
        )  # a list of [0, ... len(Product_list)+1]
        index = np.random.randint(0, len(product_ids))
        return product_ids[
            index
        ]  # return a random number from 0 to length of string

    @property
    def _quantity(self):
        return np.random.randint(1, 10)

    def get_data(self):

        for date in self._get_dates():

            for _ in range(np.random.randint(1, 15)):

                name = self._name

                data = {
                    "customers": {
                        "name": name,
                        "address": self._address,
                        "phone": self._phone,
                        "email": self._get_email(name),
                    },
                    "transactions": {
                        "transaction_date": date,
                    },
                    "transaction_details": {
                        "product_id": self._product_id,
                        "quantity": np.random.randint(1, 10),
                    },
                }

                yield data


class DBSetup(DBConn):
    def _create_tables(self):
        for database_type in self._database_types:
            conn = self.get_conn(database_type)
            if database_type == "postgres":
                if not conn.dialect.has_schema(conn, self.schema):
                    conn.execute(sa.schema.CreateSchema(self.schema))
            if database_type == "mysql":
                conn.execute(f"CREATE DATABASE IF NOT EXISTS {self.schema}")

            Base.metadata.create_all(conn)

    def reset(self):
        for database_type in self._database_types:
            conn = self.get_conn(database_type)
            Base.metadata.drop_all(conn)

            sql = f"DROP SCHEMA IF EXISTS {self.schema}"
            if database_type == "postgres":
                conn.execute(f"{sql} CASCADE")
            else:
                conn.execute(sql)

    def load_transaction(self, data, session):

        customers = data.get("customers")
        transactions = data.get("transactions")
        transaction_details = data.get("transaction_details")

        row = Customers(  # maintain the relationship between each tables
            **customers,
            transactions=[
                Transactions(
                    **transactions,
                    transaction_details=[
                        TransactionDetails(**transaction_details)
                    ],
                )
            ],
        )

        session.add(row)
        session.commit()

    def _seed_transactions(self):
        my_fake_data = DataGenerator()
        session = self.get_session("mysql")
        for line in my_fake_data.get_data():
            self.load_transaction(line, session)

    @property
    def _product_list(self):
        return PRODUCT_LIST

    def _seed_products(self):
        for database_type in self._database_types:  #
            session = self.get_session(database_type)
            for row in self._product_list:
                product = Products(**row)  # pass in as a kwargs
                session.add(product)  # insert data into both databases
                session.commit()

    def run(self):
        self.reset()
        self._create_tables()
        self._seed_products()
        self._seed_transactions()


class ApplicationDataBase(DBConn):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jinja_env = Environment(
            loader=PackageLoader("database", "templates")
        )

    db_type = "mysql"

    def _get_template(self, filename, **kwargs):
        temp = self.jinja_env.get_template(filename)
        return temp.render(**kwargs)

    def get_data(self, date, table_name):
        kwargs = {"date": date}
        sql = self._get_template(f"{table_name}.sql", **kwargs)
        return self.run_query(sql)

    def run_query(self, sql):
        conn = self.get_conn("mysql")
        result = conn.execute(sql)
        return [dict(row) for row in result.fetchall()]


if __name__ == "__main__":

    kwargs = {"host": "localhost"}

    app = ApplicationDataBase(**kwargs)
    data1 = app.get_data("2021-08-03", "customers")
    data2 = app.get_data("2021-05-01", "transactions")
    data3 = app.get_data("2021-07-21", "transaction_details")
    print(data1)
    print("******")
    print(data2)
    print("******")
    print(data3)
