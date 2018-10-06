import telebot
from telebot import types
from telegram.ext import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MeesageHandler, Filers, RegexHandler 
#добавили RegexHandler, новый тип обработчика событий, основанный на регулярных выражениях
#регулярные выражения = специальный синтаксис, разметка,позволяющая взять определенную часть строки


def greet_user(bot,update):
    emo = get_user_emo(user_data)
    user_data["emo"] = emo
    text = "Привет, {} !".format(emo)
    m_keyboard = ReplyKeyboardMarkup([['/cat']])
    update.message.reply_text(text, reply_markup=my_keyboard) 
    