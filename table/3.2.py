kraje = ["Středočeský kraj", "Královéhradecký kraj", "Pardubický kraj"]
mesta = ["Benesov", "Mělník", "Kolín", "Jičín", "Chrudim"]

try:
    x = int(input("zadej 1 - mesta, 2 - kraje:"))
    if x == 1:
        y = int(input("zadej mesto: 1 - Benešov, 2 - Mělník, 3 - Kolín, 4 - Jičín nebo 5 - Chrudim"))
        if y == 1:
            print("zadal si:", mesta[0], "v kraji:", kraje[0])
        elif y == 2:
            print("zadal si:", mesta[1], "v kraji:", kraje[0])
        elif y == 3:
            print("zadal si:", mesta[2], "v kraji:", kraje[0])
        elif y == 4:
            print("zadal si:", mesta[3], "v kraji:", kraje[1])
        elif y == 5:
            print("zadal si:", mesta[4], "v kraji:", kraje[2])
        else:
            print("nezadal si mesto ze zadani!! ")

    elif x == 2:
        y = int(input("zadej kraj: 1 - Středočeský kraj, 2 - Královéhradecký kraj, 3 - Pardubický kraj"))
        if y == 1:
            print("zadal si:", kraje[0], "a tady je:", mesta[0], ",", mesta[1], ",", mesta[2])
        elif y == 2:
            print("zadal si:", kraje[1], "a tady je:", mesta[3])
        elif y == 3:
            print("zadal si:", kraje[2], "a tady je:", mesta[4])
        else:
            print("nezadal si mesto ze zadani!! ")
    else:
        print("zadej cislo 1 nebo 2 !")
except:
    print("Chyba! priste zadej cislo 1 nebo 2 !!")
 