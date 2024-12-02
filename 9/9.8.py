def vydej_obedu():
    menu = [
         "vitamínový nápoj",
         "polévka česneková s bramborem",
         "segedínský guláš, houskové knedlíky",
         "jablko",
    ]
    yield [menu[0]]                                         #vypis piti
    yield ("vyber menu A/B")
    yield [menu[2],menu[3]]                                 #vypis obou jidel
    vyber = yield                                           #prijeti hodnoty od uzivatele
    if vyber == "A":                                        #rozhodovaci logika
        vyber = menu[2]
    else:
        vyber = menu[3]
    yield ("vybral jsi si: " + vyber)                       #vypis



corutina1 = vydej_obedu();

napoje = next(corutina1)
print(napoje)
nabidka = next(corutina1)
print(nabidka)
jidlo = next(corutina1)
print(jidlo)
next(corutina1)
vypis = corutina1.send("A")
print(vypis)

corutina1.close()