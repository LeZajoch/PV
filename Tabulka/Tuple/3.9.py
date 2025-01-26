test_tuple = (1, 2, 3)
print("test_tuple ID")
print(id(test_tuple))
test_tuple2 = (1, "a", 2)
test_tuple3 = test_tuple + test_tuple2
print("test_tuple3 ID")
print(id(test_tuple3))