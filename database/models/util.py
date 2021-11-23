import sqlalchemy as sa
from database.models.core import Products


class DBSetup:
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "host.docker.internal")
        self.username = kwargs.get("username", "henry")
        self.password = kwargs.get("password", "henry")
        self.database = kwargs.get("database", "henry")
        self.schema = kwargs.get("schema", "henry")

    def _get_conn_str(self, database_type):
        if database_type == "postgres":
            dbapi = "postgresql"
            port = 5438

        elif database_type == "mysql":
            dbapi = "mysql+pymysql"
            port = 3307

        return f"{dbapi}://{self.username}:{self.password}@{self.host}:{port}/{self.database}"  # noqa: E501

    def _get_conn(self, database_type):
        conn_str = self._get_conn_str(database_type)
        connection = sa.create_engine(conn_str, echo=True)
        return connection

    @property
    def _database_types(self):
        return ["mysql", "postgres"]

    def _create_tables(self):
        for database_type in self._database_types:
            conn = self._get_conn(database_type)
            if database_type == "postgres":
                if not conn.dialect.has_schema(conn, self.schema):
                    conn.execute(sa.schema.CreateSchema(self.schema))

    def _get_session(self, database_type):
        conn = self.get_conn(database_type)
        Session = sa.orm.sessionmaker(bind=conn)
        return Session()

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
            session = self._get_conn(database_type)
        for row in self._product_list:
            product = Products(**row)
            session.add(product)
            session.commit()

    def run(self):
        self._create_tables()
        self._seed_products()


if __name__ == "__main__":

    kwargs = {"host": "localhost"}

    setup = DBSetup(**kwargs)
    setup.run()

    print("Success")
