from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

from carsdb import Car, Zmodels, db_session
from make_right_number import make_right_number

SELECTED, ADD_NUMBER = range(2)

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
        elif selection == "Телефон":
            update.message.reply_text("Введите номер телефона:")
        elif selection == "Модель":
            update.message.reply_text("Введите модель автомобиля:")
        elif selection == "Цвет":
            update.message.reply_text("Введите цвет автомобиля:")
        elif selection == "Фото":
            update.message.reply_text("Приложите ссылку на фото автомобиля:")
        elif selection == "В чате?":
            update.message.reply_text("Напишите да для отображения в чате:")
        elif selection == "Комментарий:":
            update.message.reply_text("Комментарий:")  


def add_licence_plate(bot, update, user_data):
    
    user_phrase=update.message.text
    for car_data in user_phrase:
        car = Car(car_data ['licence_plate'])
        db_session.add(car)
        db_session.commit()
        new_licence_plate_replytext = 'В базе новый регистрационный номер: {}'.format(car.licence_plate)
        update.message.reply_text = new_licence_plate_replytext

        return ConversationHandler.END

def cancel(bot, update):
    update.message.reply_text("Хорошо, отлично")

    return ConversationHandler.END


adding_handler = ConversationHandler(
    entry_points=[CommandHandler('add', adding_keyboard, pass_user_data=True)],
    states={
        ADD_NUMBER: [MessageHandler(Filters.text, add_licence_plate, pass_user_data=True)],
        SELECTED: [MessageHandler(Filters.text, selected_addition, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )
