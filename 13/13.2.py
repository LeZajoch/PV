with open("helloworld.txt", "r") as f:
    print(f.read())
    f.seek(0)               #skok na zacatek souboru
    print(f.readline())
    f.seek(0)
    print(f.read(3))
    f.seek(0)
    y = 1
    for x in f.readlines():
        print(y,x)
        y = y + 1