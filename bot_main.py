from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from telegram.ext.dispatcher import run_async
#from datetime import datetime


import logging

import settings
import sort_by_numbers
from car_find import find_part
from car_edit import edit_conv_handler
from car_del import del_conv_handler
from help_start_tgid import help_func, tg_id_func
from adding_licence_plate import adding_licence_handler
from admin_add import add_admin_conv_handler
from admin_del import del_admin_conv_handler

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def echo(bot, update):
  bot.sendMessage(update.message.chat_id, text=update.message.text)

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("find", find_part, pass_user_data=True))
    dp.add_handler(edit_conv_handler)
    dp.add_handler(del_conv_handler)
    dp.add_handler(adding_licence_handler)
    dp.add_handler(add_admin_conv_handler)
    dp.add_handler(del_admin_conv_handler)
    dp.add_handler(CommandHandler("plates", sort_by_numbers.plates))
    dp.add_handler(CommandHandler("help", help_func, pass_user_data=True))
    dp.add_handler(CommandHandler("start", help_func, pass_user_data=True))
    dp.add_handler(CommandHandler("myid", tg_id_func, pass_user_data=True))
    #dp.add_handler(RegexHandler("^(Добавить новую машину)$",add_info, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()