# 1
di = {
  "a": "aa",
  "b": 125,
  "c": "aloq"
}
print(di)

# 2
di1 = {
  1: 5,
  4: 2,
  6: 10,
  5: 7
}
print(di1)

# 3
di2 = {
  "bla": "2blab",
  "haf": 5,
  "hahha": "hasd"
}
bla = di2["bla"]
print(bla)
# 4
di3 = {
  "aa": 10,
  "ac": 20,
  "ab": 20
}
print(di3)

# 5
di4 = {
  "ne": None,
  None: "ano"
}
print(di4)
# 6
di5 = {
  "ne":{
    "aa": 252,
    "bb": "aq"
  },
  "ano":{
    "aa": 2555,
    "ne": 20
  }
}
print(di5)

# 7
di6 = {
  "aasa": 20,
  "iqwql": 200
}
print(di6)
di6["abs"] = "aaa"
print(di6)

# 8
di7 = {
  "awokado": "holub",
  "masloslovi": 1568,
  "lala": 777
}
poc = len(di7)
print(poc)

# 9
di8 = {
  "kawasakiii": "modrochodec",
  "pomerancowski": 197
}
di8["polechtatit"] = "anakonda"
print(di8)
# 10
di9 = {
  "jednaa": "dropink",
  "vadnact": "maslosem",
  "doping": 199
}
del di9["jednaa"]
kon = di9.pop("vadnact")
print(di9)

# 11
di10 = {
  "acko": 32,
  "becko": 44,
  "mast": 3
}
di10["acko"] = 22
print(di10)

# 12
di11 = {
  "mrakkoslov": "oliej",
  "muskato": 267,
  "lalala": 111
}
if "lalala" in di11:
  print("je tu!")
else:
  print("neni tu..")

# 13
di12 = {
  1: "jedna",
  "dva": 2,
  "tri?": "ano umis pocitat"
}
tdi12 = di12["tri?"]
print(tdi12)