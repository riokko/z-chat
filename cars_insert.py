import csv

from carsdb import Car, db_session


cars_list = []
c = Car

with open('table.csv', 'r', encoding='utf-8') as f:
    fields = ['licence_plate', 'car_owner', 'phone_number', 'car_model', 'color', 'photo', 'in_the_chat', 'comment']
    reader = csv.DictReader(f, fields, delimiter=';')
    for row in reader:
        cars_list.append(row)

for car_data in cars_list:
    car = Car(car_data['licence_plate'], car_data['car_owner'], car_data['phone_number'], car_data['car_model'], car_data['color'], car_data['photo'], car_data['in_the_chat'], car_data['comment'])
    db_session.add(car)


db_session.commit()