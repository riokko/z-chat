from telegram.ext import (Updater, ConversationHandler, CommandHandler, 
    MessageHandler, Filters, RegexHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from carsdb import Admin, db_session

delete_buttons = ReplyKeyboardMarkup(
        [['Удалить'], ['Не надо ничего удалять']], 
        one_time_keyboard=True, resize_keyboard=True)

DELETE_ADMIN = range(1)

def select_del_admin(bot, update):
    admin_query = Admin.query.filter(Admin.is_active == 1).all()

    for admin in admin_query:
        admin_keyboard = ReplyKeyboardMarkup(
            [['{}'.format(admin.admin_comment)] for admin in admin_query], 
            one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text('Кого хотим удалить из админов?', reply_markup=admin_keyboard)

    return DELETE_ADMIN


def del_admin(bot, update):
    candidate_for_deleting = update.message.text
    admin_query_comment = Admin.query.filter(Admin.admin_comment == candidate_for_deleting).all()
    for admin in admin_query_comment:
        admin.is_active = False
        db_session.commit()
    update.message.reply_text('Этот негодный админ удалён из базы', 
        reply_markup=ReplyKeyboardRemove())
    
    return ConversationHandler.END


def cancel(bot, update):
    update.message.reply_text('Ну ок. Пишите если что.', 
        reply_markup=ReplyKeyboardRemove())
    
    return ConversationHandler.END


del_admin_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('deladmin', select_del_admin)],
    states={
        DELETE_ADMIN: [MessageHandler(Filters.text, del_admin)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )