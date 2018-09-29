import csv

from carsdb import Car, db_session


cars_list = []
c = Car

with open('table.csv', 'r', encoding='utf-8') as f:
    fields = ['licence_plate', 'car_owner', 'hone_number', 'car_model', 'color', 'photo', 'in_the_chat', 'comment']
    reader = csv.DictReader(f, fields, delimiter=';')
    for row in reader:
        cars_list.append(row)

db_session.commit()