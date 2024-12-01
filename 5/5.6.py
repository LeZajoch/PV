# Definice třídy pro uzel (Node)
class Node:
    def __init__(self, data):
        self.data = data  # Hodnota uzlu
        self.next = None  # Ukazatel na další uzel (vpravo)
        self.prev = None  # Ukazatel na předchozí uzel (vlevo)

# Definice třídy pro frontu s obousměrným spojovým seznamem
class Queue:
    def __init__(self):
        self.head = None  # Hlava fronty (začátek)
        self.tail = None  # Konec fronty
        self.size = 0     # Počet prvků ve frontě

    # Metoda pro přidání prvku na konec fronty
    def add(self, data):
        new_node = Node(data)  # Vytvoří nový uzel s daty
        if self.tail is None:  # Pokud je fronta prázdná
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node  # Konec ukazuje na nový uzel
            new_node.prev = self.tail  # Nový uzel ukazuje zpět na starý konec
            self.tail = new_node  # Nový uzel je teď konec
        self.size += 1  # Zvýšíme velikost fronty

    # Metoda pro odebrání prvku ze začátku fronty
    def pop(self):
        if self.head is None:  # Pokud je fronta prázdná
            raise IndexError("Fronta je prázdná, nelze odebrat prvek.")
        data = self.head.data  # Získáme data z hlavy
        self.head = self.head.next  # Posuneme hlavu na další prvek
        if self.head is None:  # Pokud byl ve frontě jen jeden prvek
            self.tail = None  # Nyní je fronta prázdná
        else:
            self.head.prev = None  # Nová hlava nemá předchůdce
        self.size -= 1  # Snížíme velikost fronty
        return data  # Vrátíme data z odebraného prvku

    # Metoda pro získání počtu prvků ve frontě
    def count(self):
        return self.size  # Vrací aktuální počet prvků

    # Metoda pro vyprázdnění celé fronty
    def clear(self):
        self.head = None  # Vyprázdníme frontu
        self.tail = None
        self.size = 0     # Velikost nastavíme na 0

    # Metoda pro odebrání všech prvků a jejich vrácení jako seznam
    def popAll(self):
        elements = []  # Seznam pro uložení všech prvků
        while self.head is not None:  # Procházíme frontu, dokud není prázdná
            elements.append(self.pop())  # Odebereme a přidáme prvek do seznamu
        return elements  # Vrátíme seznam všech prvků

# Testování fronty
queue = Queue()
queue.add(10)
queue.add(20)
queue.add(30)
queue.add(40)
queue.add(50)

# Získání a odebrání prvního prvku
print("Odebrán prvek:", queue.pop())  # Odebere a vrátí první prvek (10)

# Zobrazení počtu prvků ve frontě
print("Počet prvků ve frontě:", queue.count())  # Vrací počet zbývajících prvků (4)

# Vypsání a odebrání všech prvků
print("Všechny prvky z fronty:", queue.popAll())  # Vrací všechny prvky a vyprázdní frontu

# Zobrazení počtu prvků po vyprázdnění fronty
print("Počet prvků po vyprázdnění:", queue.count())  # Vrací 0
