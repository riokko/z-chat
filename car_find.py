from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from carsdb import Car, db_session
from car_make_right_number import make_right_number

def find_part(bot, update, user_data):
      
    c = Car

    make_right_number(bot, update, user_data)
    user_data['user_query_result'] = c.query.filter(c.is_deleted == 0).filter(c.licence_plate.like(user_data['user_car'])).all()

# считаем количество совпадений
    number_of_car = len(user_data['user_query_result'])

# если совпадений больше одного, добавляем клавиатуру для корректного ввода авто
    if number_of_car > 1:                           
        for car in user_data['user_query_result']:
            button_list = ReplyKeyboardMarkup(
                [['/find {}'.format(car.licence_plate)] 
                for car in user_data['user_query_result']], 
                one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text('Какой автомобиль?', reply_markup=button_list)

# если одно совпадение, выводим информацию
    if number_of_car == 1:                          
        for car in user_data['user_query_result']:                    
            model_name = '{} {} {} ({}), ГРН {}\n'.format(car.color, car.modelcode_link.body_style, 
                car.modelcode_link.model, car.car_modelcode, car.licence_plate)
            owner_phone = '\nВладелец {}, номер телефона {}'.format(car.car_owner, car.phone_number)
            
            update.message.reply_text(model_name)
            update.message.reply_text(owner_phone)
            if car.photo:
                photo = '\n{}'.format(car.photo)
                update.message.reply_text(photo)

        return True

# если нет совпадений отвечаем фразой
    if number_of_car == 0:                                           
        update.message.reply_text('Такого номера нет в базе')
        return True