from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from datetime import datetime


import logging

import settings
import sort_by_numbers
from find_part import find_part

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("find", find_part))
    dp.add_handler(CommandHandler("plates", sort_by_numbers.plates))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()