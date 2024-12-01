class ZamceneDvereException(Exception):
    pass

class Dvere:
    def __init__(self,zamceno):
        self.zamceno = zamceno

    def otevrit(self):
        if self.zamceno:
            raise ZamceneDvereException("dvere jsou zamcene")
        else:
            print("dvere jsou otevrene muzes projit")



d = Dvere(zamceno=True)
prosel = False
try:
    d.otevrit()
    print("Prosel jsem")
    prosel = True
except ZamceneDvereException as e:
    print("Dvere jsou zamcene, nemuzes je otevrit")
finally:
    if prosel:
        print("Prosel jsem")
    else:
        print("neprosel")