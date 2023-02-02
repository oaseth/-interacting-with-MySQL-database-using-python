import pandas as pd
from os import environ
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# MySQL URI
mysql_uri = environ.get('MYSQL_URI')

# Name of database to connect
db_name = "landon"

# Create the engine
engine = create_engine(mysql_uri + db_name)

# Create the base
Base = declarative_base()

# Creation of the tables as classes


class Purchase(Base):
    """
    A model for the "Purchase" table
    """
    __tablename__ = "purchases"
    __table_args__ = {"schema": "landon"}

    # Columns of the table
    order_id = Column(Integer, primary_key=True)
    property_id = Column(Integer)
    property_city = Column(String(255))
    property_state = Column(String(255))
    product_id = Column(Integer)
    product_category = Column(String(255))
    product_name = Column(String(255))
    quantity = Column(Integer)
    product_price = Column(Float)
    order_total = Column(Float)

    # String representation
    def __repr__(self):
        return f"[Purchase(order_id={self.order_id}, \
                    property_id={self.property_id}, \
                    property_city={self.property_city}, \
                    property_state={self.property_state}, \
                    product_id={self.product_id}, \
                    product_category={self.product_category}, \
                    product_name={self.product_name}, \
                    quantity={self.quantity}, \
                    product_price={self.product_price}, \
                    order_total={self.order_total}))]"


# Add the model to the engine
Base.metadata.create_all(engine)

# File to be added to the database
file_name = "data/landon.csv"

# Read the file with pandas
df = pd.read_csv(file_name)

# Adding the data to the database
df.to_sql(con=engine, name=Purchase.__tablename__,
          if_exists="append", index=False)

# Construct a sessionmaker object
session = sessionmaker()
# Bind the sessionmaker object to the engine
session.configure(bind=engine)
transaction = session()

# Query and its results
output = transaction.query(Purchase).limit(50).all()
for result in output:
    print(result)
