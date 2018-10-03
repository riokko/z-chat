import csv

from carsdb import Car, Zmodels, db_session


cars_list = []
c = Car
z = Zmodels

with open('table.csv', 'r', encoding='utf-8') as f:
    fields = ['licence_plate', 'car_owner', 'phone_number', 'car_modelcode', 'color', 'photo', 'in_the_chat', 'comment', 'modelcode_id']
    reader = csv.DictReader(f, fields, delimiter=';')
    for row in reader:
        owner_modelcode = z.query.filter(z.modelcode == row['car_modelcode']).first()
        row['modelcode_id'] = owner_modelcode.id
        cars_list.append(row)

for car_data in cars_list:
    car = Car(car_data['licence_plate'], car_data['car_owner'], car_data['phone_number'], car_data['car_modelcode'], car_data['color'], car_data['photo'], car_data['in_the_chat'], car_data['comment'], car_data['modelcode_id'])
    db_session.add(car)

db_session.commit()
