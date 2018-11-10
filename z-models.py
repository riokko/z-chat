import csv

from carsdb import Car, Zmodels, db_session

models_list = []
z = Zmodels

with open('modelcode.csv', 'r', encoding='utf-8') as g:
    fields = ['modelcode', 'model', 'body_style']
    reader = csv.DictReader(g, fields, delimiter=';')
    for row in reader:
        models_list.append(row)

for model_data in models_list:
    model = Zmodels(model_data['modelcode'], model_data['model'], model_data['body_style'])
    db_session.add(model)


db_session.commit()