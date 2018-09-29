from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import settings
import sort_by_numbers

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY)#, request_kwargs=settings.PROXY)
    
    logging.info('Бот запускается')

    dp = mybot.dispatcher
#    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("plates", sort_by_numbers.plates))

    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()