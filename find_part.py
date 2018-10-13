from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup

from carsdb import Car, Zmodels, db_session
from make_right_number import make_right_number

def find_part(bot, update, user_data):
      
    c = Car
    z = Zmodels

    make_right_number(bot, update, user_data)
    user_data['user_query_result'] = c.query.filter(c.licence_plate.like(user_data['user_car'])).all()

# считаем количество совпадений
    number_of_car = 0
    for car in user_data['user_query_result']:
        number_of_car += 1
    

# если совпадений больше одного, добавляем клавиатуру для корректного ввода авто
    if number_of_car > 1:                           
        for car in user_data['user_query_result']:
            button_list = ReplyKeyboardMarkup([['/find {}'.format(car.licence_plate)] for car in user_data['user_query_result']], one_time_keyboard=True)
            update.message.reply_text('Какой автомобиль?', reply_markup=button_list)
            find_part()

# если одно совпадение, выводим информацию
    if number_of_car == 1:                          
        for car in user_data['user_query_result']:                    
            model_name = '{} {} {} ({}), ГРН {}\n'.format(car.color, car.modelcode_link.body_style, 
                car.modelcode_link.model, car.car_modelcode, car.licence_plate)
            owner_phone = 'Владелец {}, номер телефона {}'.format(car.car_owner, car.phone_number)
            photo = '\n {}'.format(car.photo)
            update.message.reply_text(model_name)
            update.message.reply_text(owner_phone)
            if photo:
                update.message.reply_text(photo)

        return True

# если нет совпадений отвечаем фразой
    else:                                           
        update.message.reply_text('Такого номера нет в базе')



if __name__ == '__main__':
    find_part()