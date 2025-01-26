di = {
  "jednaa": "dropink",
  "vadnact": "maslosem",
  "doping": 199,
    "a": 1,
    "b": 2,
}
del di["jednaa"]
kon = di.pop("vadnact")
print(di)
last_item = di.popitem()
print(di)
di.clear()
print(di)