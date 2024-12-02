class ZvysitelnaUrovenInterface:

    def zvysitUroven(self):
        raise NotImplemented()


class Bojovnik:
    def __init__(self, sila):
        if type(sila) is not int or sila < 0 or sila > 3:
            raise Exception("Sila bojovnika neni dostatecne dlouhe")

        self.sila = sila

class Mag:
    def __init__(self, bilaMagie, cernaMagie):
        if type(bilaMagie) is not bool:
            raise Exception("Bila magie musi byt True/False")
        if type(cernaMagie) is not bool:
            raise Exception("Cerna magie musi byt True/False")

        self.cernaMagie = cernaMagie
        self.bilaMagie = bilaMagie

bobik = Bojovnik(1)
bobik.zvysitUroven()
print(bobik.sila)

martina = Mag(True, False)
martina.zvysitUroven()
print(martina.cernaMagie)