import sqlalchemy as sa
from database.models.core import (
    Base,
    Products,
    Customers,
    TransactionDetails,
    Transactions,
)
from jinja2 import Environment, PackageLoader
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DBConn:
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "host.docker.internal")
        self.username = kwargs.get("username", "henry")
        self.password = kwargs.get("password", "henry")
        self.database = kwargs.get("database", "henry")
        self.schema = kwargs.get("schema", "henry")
        self.jinja_env = Environment(
            loader=PackageLoader("database", "templates")
        )
        self.log = logger

    def _get_conn_str(self, database_type):
        if database_type == "postgres":
            dbapi = "postgresql"
            port = 5438

        elif database_type == "mysql":
            dbapi = "mysql+pymysql"
            port = 3307

        return f"{dbapi}://{self.username}:{self.password}@{self.host}:{port}"  # noqa: E501

    def get_conn(self, database_type):
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


class DBSetup:
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

    @property
    def _product_list(self):
        return [
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

    def _seed_products(self):
        for database_type in self._database_types:
            session = self.get_session(database_type)
            for row in self._product_list:
                product = Products(**row)  # pass in as a kwargs
                session.add(product)
                session.commit()

    def run(self):
        self._create_tables()
        self._seed_products()


class ApplicationDataBase(DBConn):

    db_type = "mysql"

    def load_transaction(self, data):
        customers = data.get("customers")
        transactions = data.get("transactions")
        transaction_details = data.get("transaction_details")

        purchase = Customers(
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

        session = self.get_session(self.db_type)
        session.add(purchase)
        session.commit()

    def load_transactions(self, data):
        pass


if __name__ == "__main__":

    kwargs = {"host": "localhost"}

    data = {
        "customers": {
            "name": "test",
            "address": "test",
            "phone": 12345,
            "email": "test",
        },
        "transactions": {
            "transaction_date": "2021-10-01",
        },
        "transaction_details": {
            "product_id": 3,
            "quantity": 4,
        },
    }

    db = ApplicationDataBase(**kwargs)
    db.load_transaction(data)
