from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
#добавили RegexHandler, новый тип обработчика событий, основанный на регулярных выражениях
#регулярные выражения = специальный синтаксис, разметка,позволяющая взять определенную часть строки
from telegram import ReplyKeyboardMarkup
from telebot import types
from carsdb import Car, Zmodels, db_session

ADD_INFO = range(1)

#создаю клавиатуру

def try_keyboard(bot, update, user_data):
    c = Car
    add_new_car(bot, update, user_data)
    edition_button = ReplyKeyboardMarkup(
        [['Добавить новую машину']],
        one_time_keyboard=True)

        return ADD_INFO

def add_info (bot, update, user_data):
    new_user = Car(['licence_plate'])
    db_session.add(new_plate)
    db_session.commit()
    new_user_replytext = 'У нас пополнение, встречайте: {}'.format(car.licence_plate)
    update.message.reply_text(new_user_replytext_replytext)
    return ConversationHandler.END

if __name__ == '__main__':
    keyboard_add()
