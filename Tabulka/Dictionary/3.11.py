di = {
  "acko": 32,
  "becko": 44,
  "mast": 3
}
di["acko"] = 22
print(di)
di.update({'c': 3, 'd': 4})
print(di)
di.setdefault('e', 5)
print(di)