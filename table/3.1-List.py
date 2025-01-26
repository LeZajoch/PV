# 1 - list
li = ["a", "c", "b"]
print(li)

# 2
li1 = [1, 5, 2, 6, 8]
print(li1)

# 3
li2 = [1, 2, "bb", 6, 9, 8, 3, "aa"]
aiq = li2[2]
print(aiq)

# 4
li3 = [1, 1, 1, 2, 3, 3, "aa", "aa"]
print(li3)

# 5
li4 = [1,1,"baaf", None, "aa", 2, None]
print(li4)

# 6
li5 = [5,3,2,[2,"aaa",3],33]
print(li5)

# 7
li6 = [5,6,9,"aa","asna"]
print(li6)
li6.append(55)
li6.remove(6)
li6.pop(0)
print(li6)

# 8
li7 = [1,65,98,"loloko", "maslolita",99]
poc = len(li7)
print(poc)

# 9
li8 = [5,6,"babicc"]
li8.append(98)
print(li8)
li8.insert(1,99)
print(li8)

# 10
li9 = ["ahokon", "masteriostny", 1987, 2, 8944986, "amostr"]
li9.remove(2)
li9.pop(2)
print(li9)

# 11
li10 = ["ahah", 5871, 68, "pokebalik"]
li10[3] = "nic takoveho"
print(li10)

# 12
li11 = ["stromovk", 5, 257, "nenene"]
if 257 in li11:
    print("je tam prvek")
else:
    print("neni tam...")

# 13
li12 = ["hel p", "posli pomoc", 158, 112, "sranda.."]
tli12 = li12[2]
print(tli12)