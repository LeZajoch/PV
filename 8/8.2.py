import re

class Zbozi:
    def __init__(self, nazev, cena):
        """
        Nastavi cenu a nazev zbozi
        :param nazev: str Nazev jen znaky anglicke abecedy 2-50
        :param cena: float 0 az 1mio, kladne cislo
        """
        if type(nazev) is not str or not re.match(r"[a-zA-Z]{2,50}", nazev):
            raise Exception('Nazev musi byt 2-50 znaku')
        if (type(cena) is not float and type(cena) is not int) or cena < 0:
            raise Exception('Nazev musi byt 2-50 znaku')
        self._nazev = nazev
        self._cena = cena

    def get_cena(self):
        """
        Vrati cenu
        :return: int
        """
        return self._cena

class ZlevneneZbozi(Zbozi):
    def __init__(self, nazev, cena, sleva):
        Zbozi.__init__(self, nazev, cena)
        if not (0.0 <= sleva <= 0.5):
            raise ValueError("Sleva musí být v rozmezí 0.0 až 0.5")
        self._sleva = sleva

    def get_cena(self):
        """
        Vrati cenu po sleve
        :return: int
        """
        return self._cena * (1 - self._sleva)

        return self._cena

    def __repr__(self):
        return (f"ZlevneneZbozi(nazev='{self._nazev}', cena={self._cena}, "
                f"sleva={self._sleva}, cena_po_sleve={self.get_cena()})")

# Test the implementation
z1 = ZlevneneZbozi("Televize", 10000, 0.25)
print(z1)  # Prints the discounted object

print(z1.get_cena())  # Prints the discounted price