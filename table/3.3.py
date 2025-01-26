reky = [
    {
        "nazev": "vltava",
        "pramen": "sumava",
        "mesta": ("Praha", "CB", "Cesky Krumlov"),
    },
    {
        "nazev": "labe",
        "pramen": "krkonose",
        "mesta": ("Pardubice", "HK", "Decin"),
    },
    {
        "nazev": "Odra",
        "pramen": "Vychodni Beskydy",
        "mesta": ("Bohunin", "Olomouc", "Opava"),
    },
]

def najdi_reky_podle_mesta(mesto):
    nalezeno = []
    for reka in reky:
        if mesto in reka["mesta"]:
            nalezeno.append(reka["nazev"])
    return nalezeno

def najdi_mesta_podle_reky(reka):
    for r in reky:
        if r["nazev"] == reka:
            return r["mesta"]
    return []

while True:
    print("1 - Vyhledat řeku podle města")
    print("2 - Vyhledat města podle řeky")
    print("3 - Konec")
    volba = input("Vyberte možnost (1/2/3): ")

    if volba == "1":
        mesto = input("Zadejte název města: ")
        nalezeno = najdi_reky_podle_mesta(mesto)
        if nalezeno:
            print(f"Řeka(y) protékající městem {mesto}: {', '.join(nalezeno)}")
        else:
            print(f"Žádná řeka neprotéká městem {mesto}.")
    elif volba == "2":
        reka = input("Zadejte název řeky: ")
        mesta = najdi_mesta_podle_reky(reka)
        if mesta:
            print(f"Řeka {reka} protéká městy: {', '.join(mesta)}")
        else:
            print(f"Řeka {reka} není v evidenci.")
    elif volba == "3":
        break
    else:
        print("Neplatná volba. Zvolte 1, 2 nebo 3.")
