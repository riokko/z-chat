from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup

from carsdb import Car, Zmodels, db_session
from dict_ruseng_letters import ruseng_letters # добавляем словарь кириллические символы - латинские символы

def find_part(bot, update):
      
    c = Car
    z = Zmodels

# выделяем из фразы только запрос пользовтеля, исключаем пробелы, нижний регистр переводим в верхний    
    user_phrase = update.message.text
    user_phrase = user_phrase.upper().split(' ')[1:]
    user_phrase = ''.join(user_phrase)

# переводим введеный номер в формат БД (латинскими символами)
    user_phrase_eng = ''
    for symbol in user_phrase:
        if symbol in ruseng_letters:
            user_phrase_eng += ruseng_letters.get(symbol)
        else:
            user_phrase_eng += symbol

# возвращаем текст для поиска в БД            
    user_phrase = '%{}%'.format(user_phrase_eng)
#осуществляем поиск по всей БД
    query_result = c.query.filter(c.licence_plate.like(user_phrase)).all()

# считаем количество совпадений
    number_of_car = 0
    for car in c.query.filter(c.licence_plate.like(user_phrase)).all():
        number_of_car += 1
    

# если совпадений больше одного, добавляем клавиатуру для корректного ввода авто
    if number_of_car > 1:                           
        for car in query_result:
            button_list = ReplyKeyboardMarkup([['/find {}'.format(car.licence_plate)] for car in query_result], one_time_keyboard=True)
            update.message.reply_text('Какой автомобиль?', reply_markup=button_list)
            find_part()

# если одно совпадение, выводим информацию
    if number_of_car == 1:                          
        for car in query_result:                    
            model_name = '{} {} {} ({})\n'.format(car.color, car.modelcode_link.body_style, 
                car.modelcode_link.model, car.car_modelcode)
            owner_phone = 'Владелец {}, номер телефона {}'.format(car.car_owner, car.phone_number)
            photo = '\n {}'.format(car.photo)
            update.message.reply_text(model_name)
            update.message.reply_text(owner_phone)
            if photo:
                update.message.reply_text(photo)

# если нет совпадений отвечаем фразой
    else:                                           
        update.message.reply_text('Такого номера нет в базе')



if __name__ == '__main__':
    find_part()