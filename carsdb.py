from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.pool import SingletonThreadPool

engine = create_engine('sqlite:///cars.db')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    licence_plate = Column(String(15), nullable=False, unique=True)
    car_owner = Column(String(50))
    phone_number = Column(String(20))
    car_modelcode = Column(String(5))
    color = Column(String(30))
    photo = Column(String(250))
    in_the_chat = Column(String(3))
    comment = Column(Text)
    modelcode_id = Column(Integer, ForeignKey('zmodels.id'))

    def __init__(self, licence_plate=None, car_owner=None, phone_number=None,
        car_modelcode=None, color=None, photo=None, in_the_chat=None, comment=None, modelcode_id=None):
        self.licence_plate = licence_plate
        self.car_owner = car_owner
        self.phone_number = phone_number
        self.car_modelcode = car_modelcode
        self.color = color
        self.photo = photo
        self.in_the_chat = in_the_chat
        self.comment = comment
        self.modelcode_id = modelcode_id

    def __repr__(self):
        return '{}, номер {}, владелец {}, номер телефона: {}, фотография автомобиля {}, находится в чате: {}'.format(self.color, self.licence_plate, self.car_owner, self.phone_number, self.photo, self.in_the_chat)

class Zmodels(Base):
    __tablename__ = 'zmodels'
    id = Column(Integer, primary_key=True)
    modelcode = Column(String(5))
    model = Column(String(5))
    body_style = Column(String(15))
    cars_link = relationship('Car', backref='modelcode_link')

    def __init__(self, modelcode=None, model=None, body_style=None):
        self.modelcode = modelcode
        self.model = model
        self.body_style = body_style

    def __repr__(self):
        return '{} {} ({})'.format(self.body_style, self.model, self.modelcode)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)