from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from carsdb import Car, Zmodels, db_session
from make_right_number import make_right_number

SELECTED, ADD_NUMBER, ADD_PERSON, ADD_TELEPHONE, ADD_MODEL, ADD_COLOUR, ADD_PHOTO, ADD_PRESENCE, ADD_COMMENT, KEY_OPTIONS = range(10)

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
        [['Номер машины']],
        one_time_keyboard=True)
    update.message.reply_text('Вы хотите добавить данные информацию по новому автомобилю')
    update.message.reply_text('Внесите первые данные:', reply_markup=edition_button)

    return SELECTED

def selected_addition(bot, update,user_data):
        selection = update.message.text

        if selection == "Регистрационный номер нового автомобиля":                  
            update.message.reply_text("Введите номер автомобиля:")

            return ADD_NUMBER

def add_licence_plate(bot, update, user_data):
    
    user_phrase=update.message.text 
    new_car = Car()
    new_car.licence_plate = user_phrase
    db_session.add(new_car)
    db_session.commit()
    new_licence_plate_replytext = 'В базе появился новый регистрационный номер: {}'.format(new_car.licence_plate)
    edition_button = ReplyKeyboardMarkup(
        [['Владелец','Номер телефона'], 
        ['Модель автомобиля', 'Цвет', 'Фото'],
        ['Присутствие в чате','Комментарий','ID']],
        one_time_keyboard=True)
    update.message.reply_text('Вы хотите дополнить данные по автомобилю ?')
    update.message.reply_text(new_licence_plate_replytext,reply_markup=edition_button)
    user_data["licence_plate"] = new_car.licence_plate

    return KEY_OPTIONS

def selecting_new_data (bot,update,user_data):    
        selection = update.message.text

        if selection == "Владелец":
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



def add_owner (bot, update, user_data):
    
    car=Car.query.filter(Car.licence_plate==user_data["licence_plate"]).first()
    user_phrase=update.message.text
    car.car_owner=user_phrase
    db_session.add(car)
    db_session.commit()
    new_owner_replytext = 'В базу внесен новый владелец: {}'.format(car.car_owner)
    edition_button = ReplyKeyboardMarkup(
        [['Номер телефона','Модель автомобиля'], 
        [ 'Цвет', 'Фото'],
        ['Присутствие в чате','Комментарий','ID']],
        one_time_keyboard=True)
    update.message.reply_text('Вы хотите добавить другие данные?')
    update.message.reply_text(new_owner_replytext, reply_markup=edition_button)

    return KEY_OPTIONS

def add_mobile (bot, update, user_data):
    
    car=Car.query.filter(Car.licence_plate==user_data["licence_plate"]).first()
    user_phrase=update.message.text
    car.phone_number=user_phrase
    db_session.add(car)
    db_session.commit()
    new_phone_replytext = 'Телефон владельца новой машины: {}'.format(car.phone_number)
    edition_button = ReplyKeyboardMarkup(
        [['Номер телефона','Модель автомобиля'], 
        [ 'Цвет', 'Фото'],
        ['Присутствие в чате','Комментарий','ID']],
        one_time_keyboard=True)
    update.message.reply_text('Выберите опцию для дополнения: ')
    update.message.reply_text(new_phone_replytext,reply_markup=edition_button)

    return KEY_OPTIONS

def add_models (bot, update, user_data):

        car=Car.query.filter(Car.licence_plate==user_data["licence_plate"]).first()
        user_phrase=update.message.text
        car.car_modelcode=user_phrase
        db_session.add(car)
        db_session.commit()
        new_model_replytext = 'Модель новой машины: {}'.format(car.car_modelcode)
        edition_button = ReplyKeyboardMarkup(
            [['Номер телефона','Модель автомобиля'], 
            [ 'Цвет', 'Фото'],
            ['Присутствие в чате','Комментарий','ID']],
            one_time_keyboard=True)
        update.message.reply_text('Вы хотите добавить другие данные?')
        update.message.reply_text(new_model_replytext,reply_markup=edition_button)

        return KEY_OPTIONS

def add_colors (bot, update, user_data):
    
    car=Car.query.filter(Car.licence_plate==user_data["licence_plate"]).first()
    user_phrase=update.message.text
    car.color=user_phrase
    db_session.add(car)
    db_session.commit()
    new_color_replytext = 'Цвет новой машины: {}'.format(car.color)
    edition_button = ReplyKeyboardMarkup(
        [['Номер телефона','Модель автомобиля'], 
        [ 'Цвет', 'Фото'],
        ['Присутствие в чате','Комментарий','ID']],
        one_time_keyboard=True)
    update.message.reply_text('Вы хотите добавить другие данные?')
    update.message.reply_text(new_color_replytext,reply_markup=edition_button)

    return KEY_OPTIONS

def add_pictures (bot, update, user_data):
    
    car=Car.query.filter(Car.licence_plate==user_data["licence_plate"]).first()
    user_phrase=update.message.text
    car.photo=user_phrase
    db_session.add(car)
    db_session.commit()
    new_picture_replytext = 'Фото новой машины: {}'.format(car.photo)
    edition_button = ReplyKeyboardMarkup(
        [['Номер телефона','Модель автомобиля'], 
        [ 'Цвет', 'Фото'],
        ['Присутствие в чате','Комментарий','ID']],
        one_time_keyboard=True)
    update.message.reply_text('Вы хотите добавить другие данные?')
    update.message.reply_text(new_picture_replytext,reply_markup=edition_button)

    return KEY_OPTIONS

def add_present_in_chat (bot, update, user_data):
    
    car=Car.query.filter(Car.licence_plate==user_data["licence_plate"]).first()
    user_phrase=update.message.text
    car.in_the_chat=user_phrase
    db_session.add(car)
    db_session.commit()
    new_presence_replytext = 'Присутствие в чате: {}'.format(car.in_the_chat)
    edition_button = ReplyKeyboardMarkup(
        [['Номер телефона','Модель автомобиля'], 
        [ 'Цвет', 'Фото'],
        ['Присутствие в чате','Комментарий','ID']],
        one_time_keyboard=True)
    update.message.reply_text('Вы хотите добавить другие данные?')
    update.message.reply_text(new_presence_replytext,reply_markup=edition_button)

    return KEY_OPTIONS

def add_comments (bot, update, user_data):
    
    car=Car.query.filter(Car.licence_plate==user_data["licence_plate"]).first()
    user_phrase=update.message.text
    car.comment=user_phrase
    db_session.add(car)
    db_session.commit()
    new_comment = 'Комметарии: {}'.format(car.comment)
    edition_button = ReplyKeyboardMarkup(
        [['Номер телефона','Модель автомобиля'], 
        [ 'Цвет', 'Фото'],
        ['Присутствие в чате','Комментарий','ID']],
        one_time_keyboard=True)
    update.message.reply_text('Вы хотите добавить другие данные?')
    update.message.reply_text(new_comment_replytext,reply_markup=edition_button)

    return KEY_OPTIONS

def cancel(bot, update):
    update.message.reply_text("Хорошо, отлично")

    return ConversationHandler.END


adding_licence_handler = ConversationHandler(
    entry_points=[CommandHandler('add', adding_keyboard, pass_user_data=True)],
    states={

        SELECTED: [MessageHandler(Filters.text, selected_addition, pass_user_data=True)],
        ADD_NUMBER: [MessageHandler(Filters.text, add_licence_plate, pass_user_data=True)],
        KEY_OPTIONS: [MessageHandler(Filters.text, selecting_new_data, pass_user_data=True)],
        ADD_PERSON: [MessageHandler(Filters.text, add_owner, pass_user_data=True)],
        ADD_TELEPHONE: [MessageHandler(Filters.text, add_mobile, pass_user_data=True)],
        ADD_MODEL: [MessageHandler(Filters.text, add_models, pass_user_data=True)],
        ADD_COLOUR: [MessageHandler(Filters.text, add_colors, pass_user_data=True)],
        ADD_PHOTO: [MessageHandler(Filters.text, add_pictures, pass_user_data=True)],
        ADD_PRESENCE: [MessageHandler(Filters.text, add_present_in_chat, pass_user_data=True)],
        ADD_COMMENT: [MessageHandler(Filters.text, add_comments, pass_user_data=True)],

    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )