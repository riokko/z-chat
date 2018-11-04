from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from carsdb import Car, Zmodels, db_session 
from dict_ruseng_letters import ruseng_letters
'''
функция для бота Z-чата. 
из присланной фразы пользователя убирает лишние пробелы, 
меняет кириллические символы на латинские, составляет
номер ГРН так, как написано в базе данных
'''

def make_right_number(bot, update, user_data): 
    c = Car
    z = Zmodels
# выделяем из фразы только запрос пользователя, исключаем пробелы, нижний регистр переводим в верхний    

    user_data['user_car'] = update.message.text
    user_data['user_car'] = user_data['user_car'].upper().split(' ')[1:]
    user_data['user_car'] = ''.join(user_data['user_car'])
    user_data['user'] = update.message.from_user
    user_data['chat_id'] = update.message.chat_id


# переводим введеный номер в формат БД (латинскими символами)
    user_phrase_eng = ''
    for symbol in user_data['user_car']:
        if symbol in ruseng_letters:
            user_phrase_eng += ruseng_letters.get(symbol)
        else:
            user_phrase_eng += symbol
# возвращаем текст для поиска в БД  
    user_phrase = '%{}%'.format(user_phrase_eng)

# добавляем фразу в кэш user_data
    user_data['user_car'] = user_phrase

if __name__ == '__main__':
    make_right_number()