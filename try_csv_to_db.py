from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import pandas as pd
#def Load_Data(file_name):
#data = csv.reader(file_name, delimiter=',')# skiprows=1, converters={0: lambda s: str(s)})
#return data.tolist()
Base = declarative_base()
class cdb1(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'cdb1'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False)
    number = Column(String(40))
    name = Column(String(250))
    phone_number = Column(String(10))
    model = Column(String(5))
    color = Column(String(15))
    photo = Column(String(250))
    chat = Column(Integer)
    comments = Column(String(400))
engine = create_engine('sqlite:///cdb.db')
Base.metadata.create_all(engine)

file_name = 'table.csv'

df = pd.read_csv(file_name)
df.to_sql(con=engine, index_label='id', name=cdb1.__tablename__, if_exists='replace')