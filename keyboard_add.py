from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
#добавили RegexHandler, новый тип обработчика событий, основанный на регулярных выражениях
#регулярные выражения = специальный синтаксис, разметка,позволяющая взять определенную часть строки
from telegram import ReplyKeyboardMarkup

from carsdb import Car, Zmodels, db_session

ADD_INFO = range(1)

def get_info (bot, update, user_data):
    test ="Вызван /add"
    symbols=["-","=","_",".","/","&","?","*","#","~","$","^","(",")"]
    #получаем текст пользователя
    user_phrase=update.message.text
    for symbol in symbols:
        user_phrase = user_phrase.replace(symbol,"")
    #проверяем на лишние пробелы и разбиваем на части
    user_phrase = user_phrase.strip().split(" ")
    user_phrase = user_phrase[-1]

    if user_phrase:
        f=c.query.filter(Car.licence_plate==user_phrase).first()
        reply_text = "Такая машинка уже есть в нашей базе"
    elif len(user_phrase) == 0:
        print("Введите номер автомобиля, пожалуйста")
            return ADD_INFO
    else:
        reply_text = "Что-то я сомневаюсь, что бывают такие номера"


def add_info (bot, update, user_data):
    new_user = Car(car_data['licence_plate'])
    db_session.add(new_user)
    db_session.commit()
    new_user_replytext = 'У нас пополнение, встречайте: {}'.format(car.licence_plate)
            update.message.reply_text(new_user_replytext_replytext)

            return ConversationHandler.END


if __name__ == '__main__':
    keyboard_add()
