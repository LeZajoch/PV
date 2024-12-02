def generatorRaselininychJezerCR():
    yield "Černé jezero"
    yield "Čertovo jezero"
    raise StopIteration()
    yield "Jezero Laka"
    yield "Mechové jezírko na Rejvízu"
    yield "Rašeliniště Borkovická blata"


print("Raselina jezera v CR")
for jezero in generatorRaselininychJezerCR():
    print(jezero)
