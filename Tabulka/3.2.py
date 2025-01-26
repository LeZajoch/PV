cities = {
    "Pardubice": "Pardubicky",
    "Chrudim": "Pardubicky",
    "Litomysl": "Pardubicky",
    "Prelouc": "Pardubicky",
    "Svitavy": "Pardubicky",
    "Pelhrimov": "Vysocina",
    "Jihlava": "Vysocina",
    "Telc": "Vysocina",
    "Trebic": "Vysocina",
    "Humpolec": "Vysocina",
    "Ostrava": "Moravskoslezky",
    "Havirov": "Moravskoslezky",
    "Opava": "Moravskoslezky",
    "Rymarov": "Moravskoslezky",
    "Trinec": "Moravskoslezky",
}
usr_in = input("napiste mesto nebo kraj")
if (usr_in) in cities:
    print(cities[usr_in])
else: cities2 = [city for city, region in cities.items() if region == usr_in]
print(cities2)