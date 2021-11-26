import sqlalchemy as sa

from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

Base = declarative_base()


class BaseTable:
    @declared_attr
    def __tablename__(cls):  # pass in the class
        return cls.__name__.lower()

    __table_args__ = {"schema": "henry"}
    id = sa.Column(sa.INTEGER, primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP, server_default=func.now())


class Customers(BaseTable, Base):
    name = sa.Column(sa.VARCHAR(50))
    address = sa.Column(sa.VARCHAR(200))
    phone = sa.Column(sa.VARCHAR(50))
    email = sa.Column(sa.VARCHAR(50))
    transactions = relationship("Transactions", backref="customers")


class Products(BaseTable, Base):
    name = sa.Column(sa.VARCHAR(50))
    price = sa.Column(sa.FLOAT)
    transaction_details = relationship(
        "TransactionDetails", backref="products"
    )


class Transactions(BaseTable, Base):

    transaction_date = sa.Column(sa.TIMESTAMP)
    customer_id = sa.Column(sa.INTEGER, sa.ForeignKey("henry.customers.id"))
    transaction_details = relationship(
        "TransactionDetails", backref="transactions"
    )


class TransactionDetails(BaseTable, Base):

    __tablename__ = "transaction_details"
    transaction_id = sa.Column(
        sa.INTEGER, sa.ForeignKey("henry.transactions.id")
    )
    product_id = sa.Column(sa.INTEGER, sa.ForeignKey("henry.products.id"))
    quantity = sa.Column(sa.INTEGER)


if __name__ == "__main__":
    dbapi = "mysql+pymysql"
    username = "henry"
    password = "henry"
    host = "localhost"
    port = "3307"
    database = "henry"

    connection_string = (
        f"{dbapi}://{username}:{password}@{host}:{port}/{database}"
    )

    engine = sa.create_engine(connection_string, echo=True)
    Base.metadata.create_all(engine)
