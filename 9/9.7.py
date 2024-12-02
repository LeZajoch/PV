def vydej_obedu():
    menu = [
         "vitamínový nápoj",
         "polévka česneková s bramborem",
         "segedínský guláš, houskové knedlíky",
         "jablko",
    ]
    yield [menu[0]]
    yield [menu[1],menu[2],menu[3]]

corutina1 = vydej_obedu();

napoje = next(corutina1)
print(napoje)
jidla = next(corutina1)
print(jidla)