from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Car(Base):
    __tablename__ = 'car'
    # Даём определения столбцам будущей таблицы
    id = Column(Integer, primary_key=True)
    licence_plate = Column(String(9), nullable=False)
    car_owner = Column(String(50))
    phone_number = Column(String(20))
    car_model = Column(String(5))
    color = Column(String(30))
    photo = Column(String(250))
    in_the_chat = Column(String(3))
    comment = Column(String(400))

engine = create_engine('sqlite:///attempt2.db')
Base.metadata.create_all(engine)