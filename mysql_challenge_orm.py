import pandas as pd
from os import environ
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# MySQL URI
mysql_uri = environ.get('MYSQL_URI')

# Name of database to connect
db_name = "redtech30"

# Create the engine
engine = create_engine(mysql_uri + db_name)

# Create the base
Base = declarative_base()


class Sales(Base):
    """
    A model for the "Sales" table
    """
    __tablename__ = " sales"
    __table_args__ = {"schema": "redtech30"}

    # The columns of the table
    order_num = Column(Integer, primary_key=True)
    order_type = Column(String(255))
    cust_name = Column(String(255))
    prod_number = Column(Integer)
    prod_name = Column(String(255))
    quantity = Column(Integer)
    price = Column(Float)
    discount = Column(Float)
    order_total = Column(Float)

    # String representation
    def __repr__(self):
        return f"[Sale(order_num={self.order_num}, \
                    order_type={self.order_type}, \
                    cust_name={self.cust_name}, \
                    prod_number={self.prod_number}, \
                    prod_name={self.prod_name}, \
                    quantity={self.quantity}, \
                    price={self.price}, \
                    discount={self.discount}, \
                    order_total={self.order_total}))]"


# Add the model to the engine
Base.metadata.create_all(engine)

# File to be added to the database
file_name = "data/red30.csv"

# Read file
df = pd.read_csv(file_name)

# Add file to the database
df.to_sql(name=Sales.__tablename__, con=engine,
          if_exists="replace", index=False)

# Create a sessionmaker object
session = sessionmaker()
session.configure(bind=engine)
transaction = session()

# Query for the highest purchase
highest_purchase = transaction.query(func.max(Sales.order_total)).scalar()
print(highest_purchase)

# Query for the topmost orders
topmost_order = transaction.query(Sales).filter(
    Sales.order_total == transaction.query(func.max(Sales.order_total)).scalar())
# topmost_orders = transaction.query(Sales).order_by(
#     Sales.order_total.desc()).limit(20)

# Display the output on the console
for row in topmost_order:
    print(row)
