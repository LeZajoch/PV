import pickle
import datetime
import os

# Název souboru pro ukládání dat
INFO_FILE = "info.dat"

# Základní formát informací
info = {'pocet_spusteni': 0, 'posledni_spusteni': None}

# Kontrola, zda soubor existuje a načítání dat (deserializace)
if os.path.exists(INFO_FILE):
    with open(INFO_FILE, "rb") as file:
        info = pickle.load(file)
else:
    print("Soubor info.dat neexistuje. Vytvářím nový záznam.")

# Aktualizace informací o spuštění
info['pocet_spusteni'] += 1
info['posledni_spusteni'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Výpis informací na obrazovku
print(f"Počet spuštění: {info['pocet_spusteni']}")
print(f"Poslední spuštění: {info['posledni_spusteni']}")

# Serializace dat do binárního souboru
with open(INFO_FILE, "wb") as file:
    pickle.dump(info, file)

print("Informace byly aktualizovány a uloženy.")
