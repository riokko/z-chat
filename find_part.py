from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from carsdb import Car, db_session
from RusEng_letters import ruseng_letters

def find_part(bot, update):
      
    c = Car
    
    user_phrase = update.message.text
    user_phrase = user_phrase.upper()
    user_phrase = user_phrase.split(" ")
    user_phrase = user_phrase[1:]
    user_phrase = str(user_phrase)[2:-2]            # переводим фразу в строку, убираем символы [' сначала и '] — с конца

    for symbol in ruseng_letters:                   # проверяем, если первый символ — русская буква
        if user_phrase[0] == symbol:
            user_phrase_eng = "" 
            for symbol in user_phrase:
                user_phrase_eng += ruseng_letters.get(symbol) # заменяем русские буквы на английские
            user_phrase = user_phrase_eng
    
        else:                                       # если английская, то делаем ничего
            user_phrase = user_phrase

    user_phrase = '%{}%'.format(user_phrase)

    data_upload = c.query.filter(c.licence_plate.like(user_phrase)).all()
    if data_upload == []:                           # если фильтр из базы — пустой список
        reply = "Такого номера нет в базе"
        update.message.reply_text(reply)
    else:                                           # если есть совпадения
        data_upload = str(data_upload)              # переводим в строку
        data_upload = data_upload[1:-1]             # убираем символы [ и ]
        update.message.reply_text(data_upload)