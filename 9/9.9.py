def chatbot():
    yield "Ahoj jak se mas?"

    odpoved = yield

    if(odpoved =="Konec"):
        yield "Loucim se"
    else:
        yield "Nerozumim otazce"


chat = chatbot()  #nastartuje corutinu

print(next(chat))  #spusti prvni cast a pozdravi

next(chat)  #spusti druhou cast, ktera ocekava data
print(chat.send("Konec"))  #posle data a nacte si vysledek

chat.close()  #ukonci corutinu