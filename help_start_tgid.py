from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from carsdb import Admin

def help_func(bot, update, user_data):
    user_data['chat_id'] = update.message.chat_id
    admin_query = Admin.query.filter(Admin.tg_id == user_data['chat_id']).all()

    if admin_query == []:
        help_reply = """Я умею искать информацию об автомобиле.

Для этого используйте команду «/find номер_автомобиля.»
Ещё вы можете узнать, свой ID Телеграма — /myid."""

    else:
        help_reply = """Привет, админ!

Я умею искать, редактировать, добавлять и удалять информацию об автомобиле.

Для этого используйте команды:
/find номер_автомобиля
/edit номер_автомобиля
/add номер_автомобиля
/del номер_автомобиля

А ещё я могу управлять списком админов, кто может добавлять, удалять и редактировать информацию. 
Для этого воспользуйтесь командами: 
/addadmin ID_Телеграма
/deladmin 

Список всех админов выводится по команде: /adminlist

Чтобы узнать номер ID Телеграма, есть команда /myid."""
    update.message.reply_text(help_reply)

def tg_id_func(bot, update, user_data):
    tg_id = update.message.chat_id
    update.message.reply_text("Ваш Телеграм ID — %s." % tg_id)

def admin_list_func(bot, update):
    admin_query = Admin.query.filter(Admin.is_active == 1).all()
    adminlist_text = ""

    for admin in admin_query:
        tgid_text = 'ID Телеграма: {}, комментарий: {}\n'.format(admin.tg_id, admin.admin_comment)
        adminlist_text += tgid_text
    update.message.reply_text(adminlist_text)