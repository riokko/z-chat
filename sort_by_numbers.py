from carsdb import Car
c=Car

def plates (bot,update):
    test ="Вызван /plates"
    print(test)
    #вытаскиваем лишнее:
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
        reply_text = "Машина найдена!"
    elif len(user_phrase) == 0:
        print("Попробуйте напечатать номер автомобиля")
    else:
        reply_text = "Это точно номер автомобиля?"

    reply_text="Машина принадлежит {}".format(u.car_owner)
    print(reply_text)
    update.message.reply_text(reply_text)

