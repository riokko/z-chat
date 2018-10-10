from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

from carsdb import Car, Zmodels, db_session
from make_right_number import make_right_number


SELECTED, CHANGE_NUMBER = range(2)

def select_edition(bot, update, user_data):
    c = Car
    make_right_number(bot, update, user_data)
    query_result = c.query.filter(c.licence_plate.like(user_data['user_car'])).all()
    user_data['user_query_result'] = query_result
    edition_button = ReplyKeyboardMarkup(
        [['Номер телефона', 'Владельца'], 
        ['Цвет автомобиля', 'Присутсвие в чате']],
        one_time_keyboard=True)

    number_of_car = 0
    for car in user_data['user_query_result']:
        number_of_car += 1

    if number_of_car == 1:
        model_name = '{} {} {} ({}), ГРН {}\n'.format(car.color, car.modelcode_link.body_style, 
                car.modelcode_link.model, car.car_modelcode, car.licence_plate)
        owner_phone = 'Владелец {}, номер телефона {}'.format(car.car_owner, car.phone_number)
        update.message.reply_text('Вы хотите отредактировать информацию по автомобилю:')
        update.message.reply_text(model_name)
        update.message.reply_text(owner_phone)
        update.message.reply_text('Что нужно поменять?', reply_markup=edition_button)

        return SELECTED

    if number_of_car > 1:                           
        for car in user_data['user_query_result']:
            button_list = ReplyKeyboardMarkup(
                [['/edit {}'.format(car.licence_plate)] 
                for car in user_data['user_query_result']], one_time_keyboard=True
                )
            update.message.reply_text('Какой автомобиль?', reply_markup=button_list)
            make_right_number()

    else:                                           
        update.message.reply_text('Такого номера нет в базе')

def selected_edition(bot, update, user_data):
        selection = update.message.text

        if selection == "Номер телефона":                  
            update.message.reply_text('Напишите новый номер телефона.')

            return CHANGE_NUMBER 

def change_phone_number(bot, update, user_data):
    c = Car
    new_phone_number = update.message.text

    number_of_car = 0
    for car in user_data['user_query_result']:
        number_of_car += 1

    if number_of_car == 1:                          
        for car in user_data['user_query_result']:  
            car.phone_number = new_phone_number
            db_session.commit()
            new_phone_number_replytext = 'У {} изменён номер телефона. Теперь нужно звонить по {}'.format(car.licence_plate, car.phone_number)
            update.message.reply_text(new_phone_number_replytext)

            return ConversationHandler.END

def cancel(bot, update, user_data):
    update.message.reply_text("Ну ок. Пиши если что.")

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('edit', select_edition, pass_user_data=True)],
    states={
        CHANGE_NUMBER: [MessageHandler(Filters.text, change_phone_number, pass_user_data=True)],
        SELECTED: [MessageHandler(Filters.text, selected_edition, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )


if __name__ == '__main__':
    edit_func()