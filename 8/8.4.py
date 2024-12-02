from abc import ABC, abstractmethod

class VazitelneInterface(ABC):
    @abstractmethod
    def get_vaha_v_kg(self):
        pass

    @abstractmethod
    def get_cena_za_kg(self):
        pass

class KusoveInterface(ABC):
    @abstractmethod
    def get_pocet_kusu_v_baleni(self):
        pass

    @abstractmethod
    def get_cena_za_kus(self):
        pass

    @abstractmethod
    def get_cena_za_baleni(self):
        pass

class ZlevnitelneInterface(ABC):
    @abstractmethod
    def set_sleva(self):
        pass

    @abstractmethod
    def get_cena_po_sleve(self):
        pass