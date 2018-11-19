from telegram.ext import (Updater, ConversationHandler, CommandHandler, 
    MessageHandler, Filters, RegexHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from carsdb import Car, Admin, Zmodels, db_session
from car_make_right_number import check_input_car_licence, check_phone_number
from car_edit import button_list_yes_or_no

(YES_OR_NO, NAME, PHONE_NUMBER, CAR_MODELCODE, CAR_COLOR, 
    CHAT_PRESENCE, ADD_COMMENT) = range(7)
c = Car
z = Zmodels


car_model_keyboard = ReplyKeyboardMarkup(
    [
    ['Z/B: родстер Z1 ', 'E36/7: родстер Z3'], 
    ['E36/8: купе Z3', 'E52: родстер Z8'],
    ['E85: родстер Z4', 'E86: купе Z4'],
    ['E89: родстер Z4', 'G29: родстер Z4']
    ], one_time_keyboard=True, resize_keyboard=True)

def add_licence_plate_of_car(bot, update, user_data):
    user_data['chat_id'] = update.message.chat_id
    admin_query = Admin.query.filter(Admin.tg_id == user_data['chat_id']).all()
    if admin_query == []:
        text_to_non_admin = """У вас нет прав для редактирования. Запросите у администратора группы права.
\nДля этого вам понадобится ваш ID в Телеграме. Вот он: {}.""".format(user_data['chat_id'])
        update.message.reply_text(text_to_non_admin)

        return ConversationHandler.END

    else:   
        check_input_car_licence(bot, update, user_data)

        if user_data['checked_car_licence'] == '':
            update.message.reply_text('Нужно что-то ввести после /add')

        else:
            confirm_entry_text = """Вы ходите добавить новый автомобиль в базу. 
Подтвердите, что введённый номер корректный:

{}""".format(user_data['checked_car_licence'])
            update.message.reply_text(confirm_entry_text, 
                reply_markup=button_list_yes_or_no)
            return YES_OR_NO


def yes_or_no_selecting(bot, update, user_data):
    choice_text = update.message.text
    added_car = c.query.filter(c.licence_plate == user_data['checked_car_licence']).first()
    if choice_text == 'Да':
        new_car = Car()
        new_car.licence_plate = user_data['checked_car_licence']
        db_session.add(new_car)
        db_session.commit()
        new_licence_plate_replytext = """В базе появился новый регистрационный номер: {}.

Теперь введите имя владельца.""".format(new_car.licence_plate)
        update.message.reply_text(new_licence_plate_replytext)
        return NAME
    if choice_text == 'Нет':
        update.message.reply_text('Введите новый номер автомобиля через команду /add.')
        return ConversationHandler.END


def add_owner_name(bot, update, user_data):
    added_car = c.query.filter(c.licence_plate == user_data['checked_car_licence']).first()
    new_owner_name = update.message.text
    added_car.car_owner = new_owner_name
    added_car.is_deleted = False
    db_session.commit()
    new_owner_name_replytext = """У {} добавлено имя владельца: {}. 

Введите номер телефона владельца или пропустите этот шаг нажав /skip""".format(added_car.licence_plate, added_car.car_owner)
    update.message.reply_text(new_owner_name_replytext)

    return PHONE_NUMBER


def add_phone_number(bot, update, user_data):
    check_phone_number(bot, update, user_data)
    added_car = c.query.filter(c.licence_plate == user_data['checked_car_licence']).first()
    added_car.phone_number = user_data['cheked_phone_number']
    db_session.commit()
    phone_number_replytext = """У {} добавлен номер телефона — {}. 

Сейчас выберете кузов автомобиля.""".format(added_car.licence_plate, added_car.phone_number)
    update.message.reply_text(phone_number_replytext, reply_markup=car_model_keyboard)

    return CAR_MODELCODE


def skip_phone_number(bot, update, user_data):
    skip_phone_number_replytext = """Вы всегда сможете отредактировать эту информацию. 

Сейчас выберете кузов автомобиля."""
    update.message.reply_text(skip_phone_number_replytext, reply_markup=car_model_keyboard)

    return CAR_MODELCODE

def add_car_model(bot, update, user_data):
    users_car_modelcode = update.message.text
    users_car_modelcode = users_car_modelcode.split(':')[0]
    added_car = c.query.filter(c.licence_plate == user_data['checked_car_licence']).first()
    added_car.car_modelcode = users_car_modelcode
    owner_modelcode = z.query.filter(z.modelcode == users_car_modelcode).first()
    added_car.modelcode_id = owner_modelcode.id
    db_session.commit()
    car_modelcode_replytext = """Записал, что у {} кузов {}. 

Какой у автомобиля цвет?""".format(added_car.licence_plate, added_car.car_modelcode)
    update.message.reply_text(car_modelcode_replytext)

    return CAR_COLOR

def add_color(bot, update, user_data):
    users_color = update.message.text
    users_color = users_color.lower()
    added_car = c.query.filter(c.licence_plate == user_data['checked_car_licence']).first()
    added_car.color = users_color
    db_session.commit()
    car_color_replytext = """Записал, что у {} цвет кузова — {}. 

Владелец автомобиля в чате?""".format(added_car.licence_plate, added_car.color) 
    update.message.reply_text(car_color_replytext, reply_markup=button_list_yes_or_no)

    return CHAT_PRESENCE

def add_chat_presense(bot, update, user_data):
    chat_presense_users_text = update.message.text
    if chat_presense_users_text == 'Да':
        chat_presense_users_text = True
    else: 
        chat_presense_users_text = False
    added_car = c.query.filter(c.licence_plate == user_data['checked_car_licence']).first()
    added_car.in_the_chat = chat_presense_users_text
    db_session.commit()

    if added_car.in_the_chat == 1:
        chat_presence_replytext = """Отметил, что владелец {} есть в чате. 

Добавьте комментарий к автомобилю или пропустите, нажав /skip""".format(added_car.licence_plate)
    if added_car.in_the_chat == 0:
        chat_presence_replytext = """Отметил, что владельца {} нет в чате.
Добавьте комментарий к автомобилю или пропустите, нажав /skip""".format(added_car.licence_plate)

    update.message.reply_text(chat_presence_replytext)

    return ADD_COMMENT


def add_comment(bot, update, user_data):
    added_car = c.query.filter(c.licence_plate == user_data['checked_car_licence']).first()
    added_car.comment = update.message.text
    db_session.commit()
    comment_replytext = """Внёс комментарий к автомобилю: 

{}

Если нужно что-то отредактировать, воспользуйтесь командой /edit номер_автомобиля.""".format(added_car.comment)
    update.message.reply_text(comment_replytext)
    return ConversationHandler.END

def skip_adding_comment(bot, update, user_data):
    nocomment_replytext = """Окей.

Если нужно что-то отредактировать, воспользуйтесь командой /edit номер_автомобиля."""
    update.message.reply_text(nocomment_replytext)
    return ConversationHandler.END

def cancel(bot, update, user_data):
    update.message.reply_text('Ну ок. Пишите если что.', 
        reply_markup=ReplyKeyboardRemove())
    user_data.clear()
    return ConversationHandler.END


add_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add_licence_plate_of_car, pass_user_data=True)],
    states={
        YES_OR_NO: [MessageHandler(Filters.text, yes_or_no_selecting, pass_user_data=True)],
        NAME: [MessageHandler(Filters.text, add_owner_name, pass_user_data=True)],
        PHONE_NUMBER: [MessageHandler(Filters.text, add_phone_number, pass_user_data=True),
            CommandHandler('skip', skip_phone_number, pass_user_data=True)],
        CAR_MODELCODE: [MessageHandler(Filters.text, add_car_model, pass_user_data=True)],
        CAR_COLOR: [MessageHandler(Filters.text, add_color, pass_user_data=True)],
        CHAT_PRESENCE: [MessageHandler(Filters.text, add_chat_presense, pass_user_data=True)],
        ADD_COMMENT: [MessageHandler(Filters.text, add_comment, pass_user_data=True),
            CommandHandler('skip', skip_adding_comment, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )