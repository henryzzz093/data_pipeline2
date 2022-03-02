import sqlalchemy as sa

from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

Base = declarative_base()


class BaseTable:
    """
    defind the basetable structure
    """

    @declared_attr
    def __tablename__(cls):  # pass in the class
        return cls.__name__.lower()

    __table_args__ = {"schema": "henry"}
    id = sa.Column(sa.INTEGER, primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP, server_default=func.now())


class Customers(BaseTable, Base):  # queston about the second parameter
    """
    contains the table structure of Customer table
    """

    name = sa.Column(sa.VARCHAR(50))
    address = sa.Column(sa.VARCHAR(200))
    phone = sa.Column(sa.VARCHAR(50))
    email = sa.Column(sa.VARCHAR(50))
    transactions = relationship(
        "Transactions", backref="customers"
    )  # define the relationship


class Products(BaseTable, Base):
    """
    contains the table structure of Products table
    """

    name = sa.Column(sa.VARCHAR(50))
    price = sa.Column(sa.FLOAT)
    transaction_details = relationship(
        "TransactionDetails", backref="products"
    )


class Transactions(BaseTable, Base):
    """
    contains the table structure of Transactions table
    """

    transaction_date = sa.Column(sa.TIMESTAMP)
    customer_id = sa.Column(sa.INTEGER, sa.ForeignKey("henry.customers.id"))
    transaction_details = relationship(
        "TransactionDetails", backref="transactions"
    )


class TransactionDetails(BaseTable, Base):
    """
    contains the table structure of TransactionDetails table
    """

    __tablename__ = "transaction_details"
    transaction_id = sa.Column(
        sa.INTEGER, sa.ForeignKey("henry.transactions.id")
    )
    product_id = sa.Column(sa.INTEGER, sa.ForeignKey("henry.products.id"))
    quantity = sa.Column(sa.INTEGER)
