from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cars_declarative import Base, Car

engine = create_engine('sqlite:///attempt2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_car = Car(licence_plate='A564EP777', car_owner='Вася Пупкин', phone_number='+7 916 733 66 66',
    car_model='e85', color='серый', in_the_chat='да')
session.add(new_car)
session.commit()