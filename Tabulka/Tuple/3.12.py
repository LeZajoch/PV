test_tuple = (1, 2, 3, 1, "a", 2)
x = "a"
y = "b"
if x in test_tuple:
    print(f"variable: "+ x + " is in tuple")
else:
    print(f""+ x + "is not in tuple")
if y not in test_tuple:
    print(f"variable: "+ y + " is not in tuple")
else:
    print(f""+ y + "is in tuple")
