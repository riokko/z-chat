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
        u=c.query.filter(Car.licence_plate==user_phrase).all()
        reply_plates = "Машина найдена!"
    else:
        reply_plates = "Это точно номер автомобиля?"

    #print(reply_plates)
    #reply_text="Машина принадлежит {}".format(self.car_owner)
    #update.message.reply_text(*)


#проверить что список непустой
#взять первый автомобиль
#и вместо селф будет u 
#и текст откорректировать