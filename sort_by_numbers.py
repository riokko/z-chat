from carsdb import Car
c=Car

def plates (bot,update):
    test ="Вызван /plates"
    #вытаскиваем лишнее:
    symbols=["-","=","_",".","/","&","?","*","#","~","$","^","(",")"]
    #получаем текст пользователя
    user_text=update.message.user_text
    for symbol in symbols:
        user_phrase = user_phrase.replace(symbol,"")
    #проверяем на лишние пробелы и разбиваем на части
    user_phrase = user_phrase.strip().split(" ")
    user_phrase = user_phrase[1:]

    if user_phrase:
        c.query.filter(Car.licence_plate==user_phrase).all()
    else:
        reply_plates = "Это точно номер автомобиля?"

    print(reply_plates)
    reply_text="Машина принадлежит {}".format(self.car_owner)
    update.message.reply_text(reply_plates)
