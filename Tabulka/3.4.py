rivers_info = {
    "Vltava": {
        "pramen": "Šumava, Černý potok",
        "ústí": "Labe, Mělník",
        "pokračuje": "Labe"
    },
    "Labe": {
        "pramen": "Krkonoše, Labská bouda",
        "ústí": "Severní moře, Německo",
        "pokračuje": "Labe"
    },
    "Morava": {
        "pramen": "Králický Sněžník",
        "ústí": "Dunaj, Bratislava",
        "pokračuje": "Dunaj"
    },
    "Ohře": {
        "pramen": "Fichtelberg, Německo",
        "ústí": "Labe, Litoměřice",
        "pokračuje": "Labe"
    },
    "Sázava": {
        "pramen": "Žďárské vrchy",
        "ústí": "Vltava, Davle",
        "pokračuje": "Vltava"
    },
    "Berounka": {
        "pramen": "Spojení několika menších řek, Plzeň",
        "ústí": "Vltava, Praha",
        "pokračuje": "Vltava"
    }
}

usr_in = input("Napište řeku: ")


if usr_in in rivers_info:
    print(rivers_info[usr_in])
