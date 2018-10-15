from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup
from datetime import datetime


import logging

import settings
import sort_by_numbers
from add_new_car import adding_handler
from find_part import find_part
from edit_func import conv_handler

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("find", find_part, pass_user_data=True))
    dp.add_handler(CommandHandler("add",make_them_type))
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("plates", sort_by_numbers.plates))
    #dp.add_handler(RegexHandler("^(Добавить новую машину)$",add_info, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()