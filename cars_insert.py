import csv

from carsdb import Car, Zmodels, db_session


cars_list = []
models_list = []
c = Car
z = Zmodels

with open('table.csv', 'r', encoding='utf-8') as f:
    fields = ['licence_plate', 'car_owner', 'phone_number', 'car_index', 'color', 'photo', 'in_the_chat', 'comment']
    reader = csv.DictReader(f, fields, delimiter=';')
    for row in reader:
        cars_list.append(row)

for car_data in cars_list:
    car = Car(car_data['licence_plate'], car_data['car_owner'], car_data['phone_number'], car_data['car_index'], car_data['color'], car_data['photo'], car_data['in_the_chat'], car_data['comment'])
    db_session.add(car)

with open('modelcode.csv', 'r', encoding='utf-8') as g:
    fields = ['index', 'model', 'body_style']
    reader = csv.DictReader(g, fields, delimiter=';')
    for row in reader:
        models_list.append(row)

for model_data in models_list:
    model = Zmodels(model_data['index'], model_data['model'], model_data['body_style'])
    db_session.add(model)

db_session.commit()