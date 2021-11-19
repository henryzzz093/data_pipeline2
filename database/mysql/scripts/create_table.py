import sqlalchemy as db
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Stocks(Base):
    __tablename__ = "stocks"
    __table_args__ = {"schema": "henry"}

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATE)
    open = db.Column(db.Numeric)
    high = db.Column(db.Numeric)
    low = db.Column(db.Numeric)
    close = db.Column(db.Numeric)
    adj_close = db.Column(db.Numeric)
    volume = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {"schema": "henry"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(50))
    address = db.Column(db.VARCHAR(200))
    phone = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(50))
    created_at = db.Column(db.DateTime, server_default=func.now())


class Products(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "henry"}

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.VARCHAR(50))
    product_price = db.Column(db.Integer)


class Stores(Base):
    __tablename__ = "stores"
    __table_args__ = {"schema": "henry"}

    store_id = db.Column(db.Integer, primary_key=True)
    store_address = db.Column(db.VARCHAR(50))


class Transactions(Base):
    __tablename__ = "transaction"
    __table_args__ = {"schema": "henry"}

    transaction_id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime())
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.store_id"))


dbapi = "mysql+pymysql"
username = "henry"
password = "henry"
host = "host.docker.internal"
port = "3307"
database = "henry"

connection_string = f"{dbapi}://{username}:{password}@{host}:{port}/{database}"


# if __name__ == "__main__":
#     engine = db.create_engine(connection_string, echo=True)
#     Base.metadata.create_all(engine)
