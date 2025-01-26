import pickle
# Načtení objektu ze souboru
try:
    with open("my_favorite_friend.dat", "rb") as file:
        loaded_profile = pickle.load(file)

    # Výpis obsahu objektu
    print("Načtený profil:")
    print(loaded_profile.toString())

except FileNotFoundError:
    print("Soubor my_favorite_friend.dat neexistuje. Nejprve spusťte skript main1.py.")
except Exception as e:
    print(f"Nastala chyba při načítání souboru: {e}")
