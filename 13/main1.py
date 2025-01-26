import pickle

from school import SchoolProfile

profile1 = SchoolProfile("Petr","Bejcek","bejcek2","MA","SPSEJECNA","MS")

# Serializace objektu a uložení do souboru
with open("my_favorite_friend.dat", "wb") as f:
    pickle.dump(profile1, f)

print("Profil byl úspěšně serializován a uložen do my_favorite_friend.dat")