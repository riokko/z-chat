#from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
#добавили RegexHandler, новый тип обработчика событий, основанный на регулярных выражениях
#регулярные выражения = специальный синтаксис, разметка,позволяющая взять определенную часть строки
#from telegram import ReplyKeyboardMarkup

#from carsdb import Car, Zmodels, db_session


def find_part(bot, update):
      
    c = Car
    z = Zmodels

#получаем данные пользователя и выкидываем лишнее
'''
def get_info (bot,update):
    test ="Вызван /add"
    print(test)
    symbols=["-","=","_",".","/","&","?","*","#","~","$","^","(",")"]
    #получаем текст пользователя
    user_phrase=update.message.text
    for symbol in symbols:
        user_phrase = user_phrase.replace(symbol,"")
    #проверяем на лишние пробелы и разбиваем на части
    user_phrase = user_phrase.strip().split(" ")
    user_phrase = user_phrase[-1]

    if user_phrase:
        u=c.query.filter(Car.licence_plate==user_phrase).first()
        reply_text = "Такая машина уже есть"
    elif len(user_phrase) == 0:
        print("Введите, пожалуйста, новые данные")
    else:
        reply_text = "Это точно номер автомобиля?"

    reply_text="Владелец машины - {}".format(u.car_owner)
    print(reply_text)
    update.message.reply_text(reply_text)
'''