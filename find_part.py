from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from carsdb import Car, db_session
from RusEng_letters import ruseng_letters

def find_part(bot, update):
      
    c = Car
    
    user_phrase = update.message.text
    user_phrase = user_phrase.upper().split(' ')[1:]
    user_phrase = ''.join(user_phrase)

    for symbol in ruseng_letters:                   # проверяем, если первый символ — русская буква
        if user_phrase[0] == symbol:
            user_phrase_eng = '' 
            for symbol in user_phrase:
                user_phrase_eng += ruseng_letters.get(symbol) # заменяем русские буквы на английские
            user_phrase = user_phrase_eng
    
        else:                                       # если английская, то делаем ничего
            user_phrase = user_phrase

    user_phrase = '%{}%'.format(user_phrase)

    data_upload = c.query.filter(c.licence_plate.like(user_phrase)).first()
    if data_upload == []:                           # если фильтр из базы — пустой список
        reply_phrase = 'Такого номера нет в базе'
        update.message.reply_text(reply_phrase)

    else:                                           # если есть совпадения
        owner_phone = 'Владелец {}, номер телефона {}'.format(data_upload.car_owner, data_upload.phone_number)
        photo = '{}'.format(data_upload.photo)
        update.message.reply_text(photo)
        update.message.reply_text(owner_phone)    