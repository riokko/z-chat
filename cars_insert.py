import csv

from carsdb import Car, Zmodels, Admin, db_session


cars_list = []
c = Car
z = Zmodels

with open('table.csv', 'r', encoding='utf-8') as f:
    fields = ['licence_plate', 'car_owner', 'phone_number', 'car_modelcode', 'color', 'photo', 'in_the_chat', 'is_deleted', 'comment', 'modelcode_id']
    reader = csv.DictReader(f, fields, delimiter=';')
    def make_bool(string):
        if string == 'True':
            return bool(1)
        return bool(0)
    for row in reader:
        owner_modelcode = z.query.filter(z.modelcode == row['car_modelcode']).first()
        row['modelcode_id'] = owner_modelcode.id
        row['in_the_chat'] = make_bool(row['in_the_chat'])
        row['is_deleted'] = make_bool(row['is_deleted'])
        cars_list.append(row)

for car_data in cars_list:

    car = Car(car_data['licence_plate'], car_data['car_owner'], car_data['phone_number'], 
        car_data['car_modelcode'], car_data['color'], car_data['photo'], car_data['in_the_chat'], 
        car_data['is_deleted'], car_data['comment'], car_data['modelcode_id'])
    db_session.add(car)

db_session.commit()

admin = Admin(67039566, "недоальпина", True)
db_session.add(admin)
db_session.commit()