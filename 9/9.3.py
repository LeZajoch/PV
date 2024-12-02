def generatorITVelikanu():
    yield "Alan Turing"
    yield "Ada Lovelace"
    yield "Tim Berners-Lee"

print("Velikani v IT")
for osoba in generatorITVelikanu():
    print(osoba)