import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

from dict_ruseng_letters import ruseng_letters, not_used_letters_in_rus_licence_plate
'''
функция для бота Z-чата. 
из присланной фразы пользователя убирает лишние пробелы, 
меняет кириллические символы на латинские, составляет
номер ГРН так, как написано в базе данных
'''

def make_right_number(bot, update, user_data): 
# выделяем из фразы только запрос пользователя, исключаем пробелы, нижний регистр переводим в верхний    

    user_phrase = update.message.text
    user_phrase = user_phrase.upper().split(' ')[1:]
    user_phrase = ''.join(user_phrase)
    user_data['user'] = update.message.from_user
    user_data['chat_id'] = update.message.chat_id


# переводим введеный номер в формат БД (латинскими символами)
    user_phrase_eng = ''
    for symbol in user_phrase:
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



def check_input_car_licence(bot, update, user_data):
    inputed_car_licence = update.message.text
    inputed_car_licence = inputed_car_licence.upper().split(' ')[1:]
    inputed_car_licence = ''.join(inputed_car_licence)
    user_data['chat_id'] = update.message.chat_id

    wrong_symbols_in_inputed_car_licence = ''
    for symbol in inputed_car_licence:
        if symbol in not_used_letters_in_rus_licence_plate:
            wrong_symbols_in_inputed_car_licence += symbol
    
    quantity_of_wrong_symbols = len(wrong_symbols_in_inputed_car_licence)

    if quantity_of_wrong_symbols == 1:
        update.message.reply_text('Введён символ «{}». Такого символа нет в русских номерах.'.format(wrong_symbols_in_inputed_car_licence))
   
    if quantity_of_wrong_symbols > 1:
        update.message.reply_text('Введены некорректные символы — {}'.format(wrong_symbols_in_inputed_car_licence))

    if quantity_of_wrong_symbols == 0:
        inputed_car_licence_eng = ''

        for symbol in inputed_car_licence:
            if symbol in ruseng_letters:
                inputed_car_licence_eng += ruseng_letters.get(symbol)
            else:
                inputed_car_licence_eng += symbol
    user_data['checked_car_licence'] = inputed_car_licence_eng


def check_phone_number(bot, update, user_data):
    
    inputed_phone_number = update.message.text
    
    if re.search('[a-zA-Zа-яА-Я]', inputed_phone_number):
        update.message.reply_text('Это не номер телефона, в нем не может быть букв. Введите ещё раз или пропустите этот шаг.')
        return PHONE_NUMBER
    
    else:
        phone_number = re.sub('[^\+?\d]','', inputed_phone_number).strip()
        
        if phone_number[0] == '0' and phone_number[1] == '0':
            update.message.reply_text('Номер телефона не может начинаться на 0. Введите ещё раз или пропустите этот шаг.')
            add_phone_number(bot, update, user_data)
        
        else:
            phone_number = phone_number.lstrip('8')
            pattern = re.compile('^\+?7?[2-9]\d{9,12}$')
            phone_number = pattern.match(phone_number)

            if phone_number == None:
                update.message.reply_text('Номер телефона не может быть меньше 11 символов.')
            else:
                phone_number = '+7' + phone_number[0] if phone_number[0][0] != '+' else phone_number[0]
                phone_number = phone_number[0:2] + ' (' + phone_number[2:5] + ') ' + phone_number[5:8] + '-' + phone_number[8:10] + '-' + phone_number[10:]
    
    user_data['cheked_phone_number'] = phone_number







