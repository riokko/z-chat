from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup
from datetime import datetime


import logging

import settings
import sort_by_numbers
from find_part import find_part
from edit_func import edit_conv_handler
from del_func import del_conv_handler
from help_start import help_func, start_func

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("find", find_part, pass_user_data=True))
    dp.add_handler(edit_conv_handler)
    dp.add_handler(del_conv_handler)
    dp.add_handler(CommandHandler("plates", sort_by_numbers.plates))
    dp.add_handler(CommandHandler("help", help_func, pass_user_data=True))
    dp.add_handler(CommandHandler("start", help_func, pass_user_data=True))
    #dp.add_handler(RegexHandler("^(Добавить новую машину)$",add_info, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()