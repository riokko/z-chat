from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardRemove

from carsdb import Admin, db_session

ADMIN_NAME = range(1)

def add_admin(bot, update, args, user_data):
    new_admin_tgid = int(args[0])
    user_data['new_admin_tgid'] = new_admin_tgid
    admin_query = Admin.query.filter(Admin.tg_id.like(new_admin_tgid)).all()

    if admin_query == []:
        new_admin = Admin()
        new_admin.tg_id = new_admin_tgid
        new_admin.is_active = 1
        db_session.add(new_admin)
        db_session.commit()

    else:
        for admin in admin_query:
            admin.is_active = 1
            db_session.commit()
    
    added_admin_text = "Добавил админа в базу. Добавьте комментарий к админу."
    update.message.reply_text(added_admin_text)

    return ADMIN_NAME

def add_admin_name(bot, update, user_data):
    inputed_comment = update.message.text
    number_of_symbols = len(inputed_comment)

    admin_query = Admin.query.filter(Admin.tg_id.like(user_data['new_admin_tgid'])).all()
    for admin in admin_query:
        admin.admin_comment = inputed_comment
        db_session.commit()
        inputed_comment_text = """Добавил комментарий. Теперь у нас есть новый админ: 
\n{}, {}""".format(admin.tg_id, admin.admin_comment)
        update.message.reply_text(inputed_comment_text)

    user_data.clear()
    return ConversationHandler.END

def cancel(bot, update, user_data):
    update.message.reply_text('Ну ок. Пишите если что.', 
        reply_markup=ReplyKeyboardRemove())
    user_data.clear()
    return ConversationHandler.END


add_admin_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('addadmin', add_admin, pass_args=True, pass_user_data=True)],
    states={
        ADMIN_NAME: [MessageHandler(Filters.text, add_admin_name, pass_user_data=True)]
    },
    fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )