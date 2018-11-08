from telegram.ext import (Updater, ConversationHandler, CommandHandler, MessageHandler, 
    Filters, RegexHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from carsdb import Car, Admin, Zmodels, db_session
from car_make_right_number import make_right_number

# объявляем константы
SELECTED, CHANGE_NUMBER, CHANGE_OWNER, CHANGE_COLOR, CHAT_PRESENCE, ADD = range(6)

# кнопки для выбора 
edition_button = ReplyKeyboardMarkup(
        [
        ['Номер телефона', 'Владельца'], 
        ['Цвет автомобиля', 'Присутсвие в чате'],
        ['Не надо ничего менять']
        ], one_time_keyboard=True, resize_keyboard=True)

button_list_yes_or_no = ReplyKeyboardMarkup(
        [['Да'], ['Нет']], 
        one_time_keyboard=True, resize_keyboard=True)


def select_edition(bot, update, user_data):
    c = Car
    make_right_number(bot, update, user_data)

    admin_query = Admin.query.filter(Admin.tg_id == user_data['chat_id']).all()
    if admin_query == []:
        text_to_non_admin = """У вас нет прав для редактирования. Запросите у администратора группы права.
\nДля этого вам понадобится ваш ID в Телеграме. Вот он: {}.""".format(user_data['chat_id'])
        update.message.reply_text(text_to_non_admin)

        return ConversationHandler.END

    else:   
        if user_data['user_car'] == '%%':
            update.message.reply_text('Нужно что-то ввести после /edit')

        else:
            query_result = c.query.filter(c.is_deleted == 0).filter(c.licence_plate.like(user_data['user_car'])).all()
            user_data['user_query_result'] = query_result

            number_of_car = 0
            for car in user_data['user_query_result']:
                number_of_car += 1

            if number_of_car == 1:
                model_name = '{} {} {} ({}), ГРН {}'.format(car.color, car.modelcode_link.body_style, 
                        car.modelcode_link.model, car.car_modelcode, car.licence_plate)
                owner_phone = 'Владелец {}, номер телефона {}'.format(car.car_owner, car.phone_number)
                update.message.reply_text("""Вы хотите отредактировать информацию по автомобилю:
\n\n{} \n{}\n\n
Что нужно поменять?""".format(model_name, owner_phone), 
                    reply_markup=edition_button, resize_keyboard=True)

                return SELECTED

            if number_of_car > 1:                           
                for car in user_data['user_query_result']:
                    car_list = ReplyKeyboardMarkup(
                        [['/edit {}'.format(car.licence_plate)] 
                        for car in user_data['user_query_result']], 
                        one_time_keyboard=True, resize_keyboard=True)
                update.message.reply_text('Какой автомобиль?', reply_markup=car_list)
                make_right_number(bot, update, user_data)

            else:                                           
                
                update.message.reply_text('Такого номера нет в базе. Хотите добавить?', 
                    reply_markup=button_list_yes_or_no)
                return ADD


def selected_edition(bot, update, user_data):
        selection = update.message.text

        if selection == 'Номер телефона':                  
            update.message.reply_text('Напишите новый номер телефона.')

            return CHANGE_NUMBER 

        if selection == 'Владельца':
            update.message.reply_text('Напишите имя нового владельца.')

            return CHANGE_OWNER

        if selection == 'Цвет автомобиля':
            update.message.reply_text('Какой новый цвет у автомобиля?')

            return CHANGE_COLOR

        if selection == 'Присутсвие в чате':
            update.message.reply_text('Владелец автомобиля в чате?', 
                reply_markup=button_list_yes_or_no)

            return CHAT_PRESENCE

        if selection == 'Не надо ничего менять':
            update.message.reply_text('Ну ок. Пишите если что.', 
                reply_markup=ReplyKeyboardRemove())
            user_data.clear()
            return ConversationHandler.END


def change_phone_number(bot, update, user_data):
    new_phone_number = update.message.text

    for car in user_data['user_query_result']:  
        car.phone_number = new_phone_number
        db_session.commit()
        new_phone_number_replytext = """У {} изменён номер телефона.
Теперь нужно звонить по {}""".format(car.licence_plate, car.phone_number)
        update.message.reply_text("""{}\n\n
Хотите ещё что-нибудь поменять?""".format(new_phone_number_replytext), 
            reply_markup=edition_button)

        return SELECTED


def change_owner_name(bot, update, user_data):
    new_owner_name = update.message.text
                       
    for car in user_data['user_query_result']:  
        car.car_owner = new_owner_name
        db_session.commit()
        new_owner_name_replytext = """У {} изменено имя владельца.
Теперь владелец автомобиля {}""".format(car.licence_plate, car.car_owner)
        update.message.reply_text("""{}\n\n
Хотите ещё что-нибудь поменять?""".format(new_owner_name_replytext), 
            reply_markup=edition_button)

        return SELECTED


def change_car_color(bot, update, user_data):
    new_car_color = update.message.text
                       
    for car in user_data['user_query_result']:  
        car.color = new_car_color
        db_session.commit()
        new_car_color_replytext = """У {} изменен цвет автомобиля.
Новый цвет автомобиля — {}.""".format(car.licence_plate, car.color)
        update.message.reply_text("""{}\n\n
Хотите ещё что-нибудь поменять?""".format(new_car_color_replytext), 
            reply_markup=edition_button)

        return SELECTED


def change_chat_presence(bot, update, user_data):
    new_chat_presence = update.message.text

    if new_chat_presence == 'Да':
        new_chat_presence = True
    else: 
        new_chat_presence = False

    for car in user_data['user_query_result']:  
        car.in_the_chat = new_chat_presence
        db_session.commit()

        if car.in_the_chat == 1:
            new_chat_presence_replytext = 'Владелец {} теперь в чате'.format(car.licence_plate)
        if car.in_the_chat == 0:
            new_chat_presence_replytext = 'Владелец {} ушёл из чата'.format(car.licence_plate)

        update.message.reply_text('{}\n\n'
            'Хотите ещё что-нибудь поменять?'.format(new_chat_presence_replytext), 
            reply_markup=edition_button)
        return SELECTED


def add_func(bot, update, user_data):
    add_new_car = update.message.text
    if add_new_car == 'Да':
        update.message.reply_text('Скоро научусь', reply_markup=ReplyKeyboardRemove())
        user_data.clear()
        return ConversationHandler.END

    if add_new_car == 'Нет':
        cancel(bot, update, user_data)


def cancel(bot, update, user_data):
    update.message.reply_text('Ну ок. Пишите если что.', 
        reply_markup=ReplyKeyboardRemove())
    user_data.clear()
    return ConversationHandler.END

edit_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('edit', select_edition, pass_user_data=True)],
    states={
        SELECTED: [MessageHandler(Filters.text, selected_edition, pass_user_data=True)],
        CHANGE_NUMBER: [MessageHandler(Filters.text, change_phone_number, pass_user_data=True)],
        CHANGE_OWNER: [MessageHandler(Filters.text, change_owner_name, pass_user_data=True)],
        CHANGE_COLOR: [MessageHandler(Filters.text, change_car_color, pass_user_data=True)],
        CHAT_PRESENCE: [MessageHandler(Filters.text, change_chat_presence, pass_user_data=True)],
        ADD: [MessageHandler(Filters.text, add_func, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )