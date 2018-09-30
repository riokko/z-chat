from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.pool import SingletonThreadPool

engine = create_engine('sqlite:///cars.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    licence_plate = Column(String(15), nullable=False)
    car_owner = Column(String(50))
    phone_number = Column(String(20))
    car_model = Column(String(5))
    color = Column(String(30))
    photo = Column(String(250))
    in_the_chat = Column(String(3))
    comment = Column(Text)

    def __init__(self, licence_plate=None, car_owner=None, phone_number=None,
        car_model=None, color=None, photo=None, in_the_chat=None, comment=None):
        self.licence_plate = licence_plate
        self.car_owner = car_owner
        self.phone_number = phone_number
        self.car_model = car_model
        self.color = color
        self.photo = photo
        self.in_the_chat = in_the_chat
        self.comment = comment

    def __repr__(self):
        return '{} Z4 {}, номер {}, владелец {}, номер телефона: {}, фотография автомобиля {}, находится в чате: {}'.format(self.color, self.car_model, self.licence_plate, self.car_owner, self.phone_number, self.photo, self.in_the_chat)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)