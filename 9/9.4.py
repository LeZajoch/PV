def generatorSudychCisel(od, do):
    i = od
    while(i < do):
        while i%2 == 0:
            yield i
            i=i+1
        i=i+1

for x in generatorSudychCisel(1,50):
    print(x)