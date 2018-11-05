from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from carsdb import Car, Zmodels, db_session
from make_right_number import make_right_number


delete_buttons = ReplyKeyboardMarkup(
        [['Удалить'], ['Не надо ничего удалять']], 
        one_time_keyboard=True)

DELETE = range(1)

def select_delete(bot, update, user_data):
    c = Car
    make_right_number(bot, update, user_data)

    if user_data['user_car'] == '%%':
        update.message.reply_text('Нужно что-то ввести после /del')

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
            update.message.reply_text('Вы хотите удалить информацию об автомобиле:'
                    '\n\n{} \n{}\n\n'
                    'Подтвердите свой выбор'.format(model_name, owner_phone), 
                    reply_markup=delete_buttons)

            return DELETE

        if number_of_car > 1:                           
            for car in user_data['user_query_result']:
                car_list = ReplyKeyboardMarkup(
                    [['/del {}'.format(car.licence_plate)] 
                    for car in user_data['user_query_result']], one_time_keyboard=True
                    )
            update.message.reply_text('Какой автомобиль?', reply_markup=car_list)

        if number_of_car == 0:                                           
            
            update.message.reply_text('Такого номера нет в базе')
            return ConversationHandler.END

def delete_func(bot, update, user_data):
    user_choice = update.message.text
    if user_choice == 'Удалить':
        for car in user_data['user_query_result']:  
            car.is_deleted = True
            db_session.commit()
            delete_replytext = 'Информация об автомобиле {} удалена из базы'.format(car.licence_plate)
            update.message.reply_text(delete_replytext)

            user_data.clear()
            return ConversationHandler.END

    if user_choice == 'Не надо ничего удалять':
        for car in user_data['user_query_result']: 
            not_delete_replytext = 'Информация об автомобиле {} оставлена в базе'.format(car.licence_plate)
            update.message.reply_text(not_delete_replytext)
        
            user_data.clear()
            return ConversationHandler.END

def cancel(bot, update, user_data):
    update.message.reply_text('Ну ок. Пишите если что.', 
        reply_markup=ReplyKeyboardRemove())
    user_data.clear()
    return ConversationHandler.END

del_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('del', select_delete, pass_user_data=True)],
    states={
        DELETE: [MessageHandler(Filters.text, delete_func, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )