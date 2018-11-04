#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    user = update.message.from_user
    names_username = '{} {} @{}'.format(user['first_name'], user['last_name'], user['username'])
    send_text = '{} хочет что-то отредактировать в БД. Разрешить?'.format(names_username)

    
    keyboard = [[InlineKeyboardButton("Да", callback_data='Вы разрешили доступ {}'.format(names_username)),
                 InlineKeyboardButton("Нет", callback_data='Вы запретили доступ {}'.format(names_username))]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(send_text, reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="{}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()