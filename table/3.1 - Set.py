# 1
se = {"aa", "ca", "b"}
print(se)

# 2
se1 = {1, 5, 9, 3, 8, 10, 25, 20}
print(se1)

# 3 - nejde

# 4
se2 = {1,1,1,2,2,3,"aa","aa"}
print(se2)

# 5
se3 = {1,2,5,3,471,None,"aa",None,"bbas"}
print(se3)

# 6
#se4 = {1,5,3,6,{2,5,6,"aaaa"},32,"aq"}
#print(se4)

# 7
se5 = {1,6,8,2,"asdd","bababq"}
print("pred", se5)
se5.add(255)
se5.remove("asdd")
print("po", se5)

# 8
se6 = {5,9,8,6,4,"asdaplq",6,9}
poc = len(se6)
print(poc)

# 9
se7 = {5,6,9,654465,"laokq"}
se7.add("ahojjjda")
print(se7)

# 10
se8 = {"kolotocky", 157, "masloslovnitvar", "masivitia", 8594}
se8.remove(157)
print(se8)

# 11
se9 = {"jedna", 22, 65, "pocetkol", 2}
se9.remove(65)
se9.add("makovec")
print(se9)

# 12
se10 = {"mak", "jamajka", 1578, 32, "orangutan"}
if "mak" in se10:
    print("prvek tam je")
else:
    print("neni tam, zase..")

# 13 - nejde