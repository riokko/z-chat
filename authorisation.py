'''
Идентификация — это процедура распознавания субъекта по его идентификатору 
(проще говоря, это определение имени, логина или номера).

Аутентификация – это процедура проверки подлинности (пользователя проверяют 
с помощью пароля, письмо проверяют по электронной подписи и т.д.)

Авторизация – это предоставление доступа к какому-либо ресурсу 
(например, к электронной почте).
'''

from telegram.ext import (Updater, ConversationHandler, CommandHandler, 
    MessageHandler, Filters, RegexHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, 
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)

import logging
import settings

from carsdb import Admin, db_session

from edit_func import select_edition

def admin_request(bot, update, user_data):
    user_data['user'] = update.message.from_user

    user = user_data['user']
    user_data['names_username'] = '{} {} @{}'.format(user['first_name'], 
                                    user['last_name'], user['username'])

    send_text = ('{} хочет что-то отредактировать в БД.'
        '\nРазрешить?'.format(user_data['names_username']))
    
    keyboard = [[InlineKeyboardButton("Да", 
                callback_data='Вы разрешили доступ {}'.format(user_data['names_username'])),
                InlineKeyboardButton("Нет", 
                callback_data='Вы запретили доступ {}'.format(user_data['names_username']))
                ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(text=send_text, chat_id=67039566, reply_markup=reply_markup)


def press_button(bot, update, user_data):
    query = update.callback_query

    bot.edit_message_text(text="{}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    
    if query.data == 'Вы разрешили доступ {}'.format(user_data['names_username']):

        admin_query = Admin.query.filter(Admin.tg_id.like(user_data['chat_id'])).all()
        if admin_query == []:
            new_admin = Admin()
            new_admin.admin_name = (query.message.chat.first_name + ' ' + 
                                    query.message.chat.last_name)
            new_admin.tg_id = query.message.chat.id
            new_admin.is_active = 1
            db_session.add(new_admin)
            db_session.commit()
            
            select_edition(bot, update, user_data)
        else:
            for admin in admin_query:
                admin.is_active = 1
                db_session.commit()
                select_edition(bot, update, user_data)
'''
def authentication(bot, update, user_data):

    user = user_data['user']
    admin_query = Admin.query.filter(Admin.tg_id.like(user['id'])).all()
    for adm in admin_query:

        if user['id'] == adm.tg_id:   
            print('ok')

        else:
           update.message.reply_text('Вы не можете редактировать данные')
'''