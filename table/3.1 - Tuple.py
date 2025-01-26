#1 - tuple
thistuple = ("b", "a", "c")
print(thistuple)

#2
tu = (1, 8, 3, 2, 10)
print(tu)

#3
tuplee = (1, 2, 5, "a", 3, 8, 2, 10, 4)
print("id tuple: ", tuplee.index("a"), ",", tuplee.index(8))

#4
tuu = ("a", "b", "a", "b")
print(tuu)

#5
atu = ("aa", "nevim", None, "baf", None)
print(atu)

#6
tupleea = ("abc", "aad", ("aaaa", "bbbb"), "ahoooj")
print(tupleea)

#7
tuplll = ("a", "b", "0.0", "asdasa.0", "157")
print(tuplll)
tuplll = ('300', *tuplll[1:])
print(tuplll)

#8
tuap = (1, 8, 3, "asda", "nechci", 5)
print(len(tuap))

#9
tupl1 = (1, 2, 3)
print(tupl1)
tupl2 = (1, "a", 2)
tupl3 = tupl1 + tupl2
print(tupl3)

#10
tup = (1, "a", 3, "va", 99, "a")
print(tup)
idx = tup.index("a")
nt = tup[:idx] + tup[idx+1:]
print(nt)

#11
atiup = (1, 5, "asdas", 33, "aqi")
etup = "ahooj"
aau = atiup[:1] + (etup,) + atiup[2:]
print(aau)

#12
autop = (1, 3, "aas")
hlautop = 5

if hlautop not in autop:
    print(hlautop, "není v tuplu.")
else:
    print(hlautop, "je v tuplu.")

#13
tupls = (5, 3, "asda", "neni", 55)
al = tupls[2]
print("treti prvek je:", al)