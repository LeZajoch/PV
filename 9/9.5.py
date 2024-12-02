def generatorRaselininychJezerCR():
    yield "Černé jezero"
    yield "Čertovo jezero"
    yield "Jezero Laka"
    yield "Mechové jezírko na Rejvízu"
    yield "Rašeliniště Borkovická blata"
    #raise StopIteration()

print("Raselina jezera v CR")
jezera = generatorRaselininychJezerCR()
while True:
    try:
        jezero = next(jezera)
        print(jezero)
    except StopIteration:
        break
