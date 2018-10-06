from telegram import ForceReply
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

from carsdb import Car, Zmodels, db_session
from dict_ruseng_letters import ruseng_letters 

CHANGE_NUMBER = range(1)


def make_right_number(bot, update, user_data):
      
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

         
    user_phrase = '%{}%'.format(user_phrase_eng)
    user_data['user_car'] = user_phrase
    query_result = c.query.filter(c.licence_plate.like(user_phrase)).all()

    number_of_car = 0
    for car in query_result:
        number_of_car += 1

    if number_of_car == 1:                          
        for car in query_result:                    
            update.message.reply_text('Напишите новый номер телефона.')

            return CHANGE_NUMBER 
    else:                                           
        update.message.reply_text('Такого номера нет в базе')

def change_phone_number(bot, update, user_data):
    c = Car
    user_phrase = user_data['user_car']
    new_phone_number = update.message.text
    query_result = c.query.filter(c.licence_plate.like(user_phrase)).all()

    number_of_car = 0
    for car in query_result:
        number_of_car += 1
    
    if number_of_car == 1:                          
        for car in query_result:  
            car.phone_number = new_phone_number
            db_session.commit()
            new_phone_number_replytext = 'У {} новый контактный номер телефона: {}'.format(car.licence_plate, car.phone_number)
            update.message.reply_text(new_phone_number_replytext)

def cancel(bot, update, user_data):
    update.message.reply_text("Ну ок. Пиши если что.")

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('edit', make_right_number, pass_user_data=True)],
    states={
        CHANGE_NUMBER: [MessageHandler(Filters.text, change_phone_number, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )


if __name__ == '__main__':
    edit_func()