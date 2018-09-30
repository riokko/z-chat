from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from carsdb import Car, db_session

def find_part(bot, update):
      
    c = Car
    
    user_phrase = update.message.text
    user_phrase = user_phrase.split(" ")
    user_phrase = user_phrase[1]
    user_phrase = str(user_phrase)

    user_phrase = '%{}%'.format(user_phrase)

    data_upload = c.query.filter(c.licence_plate.like(user_phrase)).all()

    if data_upload == []:
        return "Нет такого номера в базе"
    else:
        data_upload = str(data_upload)
        data_upload = data_upload[1:-1]
        update.message.reply_text(data_upload)