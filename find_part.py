from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from carsdb import Car, Zmodels, db_session
from dict_ruseng_letters import ruseng_letters

def find_part(bot, update):
      
    c = Car
    z = Zmodels
    
    user_phrase = update.message.text
    user_phrase = user_phrase.upper().split(' ')[1:]
    user_phrase = ''.join(user_phrase)

    user_phrase_eng = ''
    for symbol in user_phrase:
        if symbol in ruseng_letters:
            user_phrase_eng += ruseng_letters.get(symbol)
        else:
            user_phrase_eng += symbol

    user_phrase = '%{}%'.format(user_phrase)
    query_result = c.query.filter(c.licence_plate.like(user_phrase)).first()

    #print('data: {}'.format(data_upload))
    
    if query_result:                                    # если есть совпадения
        model_name = '{} {} {} ({})'.format(query_result.color, query_result.modelcode_link.body_style, 
            query_result.modelcode_link.model, query_result.car_modelcode,)
        owner_phone = 'Владелец {}, номер телефона {}'.format(query_result.car_owner, query_result.phone_number)
        photo = '{}'.format(query_result.photo)
        if photo:
            update.message.reply_text(photo)
        update.message.reply_text(owner_phone)    

    if query_result == None:                            # если фильтр из базы — пустой список
        reply_phrase = 'Такого номера нет в базе'
        update.message.reply_text(reply_phrase)
