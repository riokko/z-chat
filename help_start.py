from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

def help_func(bot, update, user_data):
    help_reply = 'Я умею искать, редактировать, добавлять и удалять информацию об автомобиле.\n\nДля этого используйте функции:\n/find номер автомобиля\n/edit номер автомобиля\n/add номер автомобиля\n/del номер автомобиля'
    update.message.reply_text(help_reply)


def start_func(bot, update, user_data):
    start_reply = 'Привет!\n\nЯ умею искать, редактировать, добавлять и удалять информацию об автомобиле.\n\nДля этого используйте функции:\n/find номер автомобиля\n/edit номер автомобиля\n/add номер автомобиля\n/del номер автомобиля'
    update.message.reply_text(start_reply)