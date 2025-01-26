rivers = {
    "Vltava": ("Černý Kříž", "Solenice", "Zebrakov", "Predni Chlum"),
    "Morava": ("Kralicky Sneznik", "Velka Morava", "Dolni Morava", "Horni Hedec"),
    "Labe": ("Spindleruv mlyn", "Vrchlabi", "Hostinne", "Dvur Kralove")
}
usr_in = input("Napište řeku nebo město: ")


if usr_in in rivers:
    print(rivers[usr_in])
else:

    rivers2 = [river for river, cities in rivers.items() if usr_in in cities]
    if rivers2:
        print(rivers2)
    else:
        print("Řeka nebo město nebylo nalezeno.")
