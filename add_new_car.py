from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

from carsdb import Car, Zmodels, db_session
from make_right_number import make_right_number

SELECTED, ADD_NUMBER, ADD_PERSON, ADD_TELEPHONE, ADD_MODEL, ADD_COLOUR, ADD_PHOTO, ADD_PRESENCE, ADD_COMMENT = range(9)

def make_them_type (bot, update):
    test ="Вызван /add"
    #получаем текст пользователя
    user_phrase=update.message.text
    if len(user_phrase) > 0:
        reply_text = "Внесем новый автомобиль в базу данных"
    elif len(user_phrase) == 0:
        reply_text = "Вызовите функцию /add"
    print(reply_text)
    update.message.reply_text("Выберите данные для внесения в базу:",reply_markup=adding_keyboard)

def adding_keyboard(bot,update,user_data):
    c=Car
    edition_button = ReplyKeyboardMarkup(
        [['Номер машины', 'Владелец','Номер телефона'], 
        ['Модель автомобиля', 'Цвет', 'Фото'],
        ['Присутствие в чате','Комментарий','ID']],
        one_time_keyboard=True)
    update.message.reply_text('Вы хотите добавить данные информацию по новому автомобилю')
    update.message.reply_text('Что нужно добавить?', reply_markup=edition_button)

    return SELECTED

def selected_addition(bot, update,user_data):
        selection = update.message.text

        if selection == "Номер машины":                  
            update.message.reply_text("Введите номер автомобиля:")

            return ADD_NUMBER

        elif selection == "Владелец":
            update.message.reply_text("Введите имя владельца:")

            return ADD_PERSON

        elif selection == "Телефон":
            update.message.reply_text("Введите номер телефона:")

            return ADD_TELEPHONE

        elif selection == "Модель":
            update.message.reply_text("Введите модель автомобиля:")

            return ADD_MODEL 

        elif selection == "Цвет":
            update.message.reply_text("Введите цвет автомобиля:")

            return ADD_COLOUR

        elif selection == "Фото":
            update.message.reply_text("Приложите ссылку на фото автомобиля:")

            return ADD_PHOTO

        elif selection == "В чате?":
            update.message.reply_text("Напишите да для отображения в чате:")

            return ADD_PRESENCE

        elif selection == "Комментарий:":
            update.message.reply_text("Комментарий:")  

            return ADD_COMMENT


def add_licence_plate(bot, update, user_data):
    
    user_phrase=update.message.text
    for car in user_phrase:
        car = Car(['licence_plate'])
        db_session.add(car)
        db_session.commit()
        new_licence_plate_replytext = 'В базе новый регистрационный номер: {}'.format(car.licence_plate)
        update.message.reply_text = new_licence_plate_replytext

        return ConversationHandler.END


def add_owner (bot, update, user_data):
    
    user_phrase=update.message.text
    for car in user_phrase:
        owner = Car(['car_owner'])
        db_session.add(owner)
        db_session.commit()
        new_owner_replytext = 'В базу внесен новый владелец: {}'.format(car.car_owner)
        update.message.reply_text = new_owner_replytext

        return ConversationHandler.END

def add_mobile (bot, update, user_data):
    
    user_phrase=update.message.text
    for car in user_phrase:
        car = Car(['phone_number'])
        db_session.add(car)
        db_session.commit()
        new_mobile_replytext = 'В базу внесен новый номер телефона: {}'.format(car.phone_number)
        update.message.reply_text = new_mobile_replytext

        return ConversationHandler.END

def add_models (bot, update, user_data):
    
    user_phrase=update.message.text
    for car in user_phrase:
        car = Car(['car_modelcode'])
        db_session.add(car)
        db_session.commit()
        new_model_replytext = 'В базу внесена новая модель автомобиля: {}'.format(car.car_modelcode)
        update.message.reply_text = new_model_replytext

        return ConversationHandler.END

def add_colours (bot, update, user_data):
    
    user_phrase=update.message.text
    Car(['color']) = user_phrase
    db_session.add(car)
    db_session.commit()
    new_colour_replytext = 'В базу внесен новый цвет автомобиля: {}'.format(car.color)
    update.message.reply_text = new_colour_replytext

    return ConversationHandler.END

def add_pictures (bot, update, user_data):
    
    user_phrase=update.message.text
    for car in user_phrase:
        car = Car(['photo'])
        db_session.add(car)
        db_session.commit()
        new_photo_replytext = 'В базу внесена новая фотография автомобиля: {}'.format(car.photo)
        update.message.reply_text = new_photo_replytext

        return ConversationHandler.END

def add_chat_in (bot, update, user_data):
    
    user_phrase=update.message.text
    for car in user_phrase:
        car = Car(['in_the_chat'])
        db_session.add(car)
        db_session.commit()
        new_chat_in_replytext = 'В базу внесен новый участник. {}'.format(car.in_the_chat)
        update.message.reply_text = new_chat_in_replytext

        return ConversationHandler.END

def add_comments (bot, update, user_data):
    
    user_phrase=update.message.text
    for car in user_phrase:
        car = Car(['comment'])
        db_session.add(car)
        db_session.commit()
        new_comment_replytext = 'В базе новый комментарий. {}'.format(car.comment)
        update.message.reply_text = new_comment_replytext

        return ConversationHandler.END

def cancel(bot, update):
    update.message.reply_text("Хорошо, отлично")

    return ConversationHandler.END


adding_handler = ConversationHandler(
    entry_points=[CommandHandler('add', adding_keyboard, pass_user_data=True)],
    states={

        SELECTED: [MessageHandler(Filters.text, selected_addition, pass_user_data=True)],
        ADD_NUMBER: [MessageHandler(Filters.text, add_licence_plate, pass_user_data=True)],
        ADD_PERSON: [MessageHandler(Filters.text, add_owner, pass_user_data=True)],
        ADD_TELEPHONE: [MessageHandler(Filters.text, add_mobile, pass_user_data=True)],
        ADD_MODEL: [MessageHandler(Filters.text, add_models, pass_user_data=True)],
        ADD_COLOUR: [MessageHandler(Filters.text, add_colours, pass_user_data=True)],
        ADD_PHOTO: [MessageHandler(Filters.text, add_pictures, pass_user_data=True)],
        ADD_PRESENCE: [MessageHandler(Filters.text, add_chat_in, pass_user_data=True)],
        ADD_COMMENT: [MessageHandler(Filters.text, add_comments, pass_user_data=True)],
    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )
