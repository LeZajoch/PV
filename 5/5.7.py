# Definice třídy pro uzel (Node)
class Node:
    def __init__(self, data):
        self.data = data  # Hodnota uzlu
        self.next = None  # Ukazatel na další uzel (vpravo)

# Definice třídy pro zásobník
class Stack:
    def __init__(self):
        self.top = None  # Ukazatel na vrchol zásobníku
        self.size = 0    # Počet prvků v zásobníku

    # Metoda pro vložení nového prvku na vrchol zásobníku
    def add(self, data):
        new_node = Node(data)  # Vytvoření nového uzlu
        new_node.next = self.top  # Nový uzel ukazuje na současný vrchol
        self.top = new_node  # Nový uzel se stane vrcholem zásobníku
        self.size += 1  # Zvýšíme počet prvků v zásobníku

    # Metoda pro odebrání prvku z vrcholu zásobníku
    def pop(self):
        if self.top is None:
            raise IndexError("Zásobník je prázdný, nelze odebrat prvek.")
        data = self.top.data  # Získání dat z vrcholu zásobníku
        self.top = self.top.next  # Posun vrcholu na další uzel
        self.size -= 1  # Snížíme počet prvků v zásobníku
        return data  # Vrátíme data z odebraného prvku

    # Metoda pro získání počtu prvků v zásobníku
    def count(self):
        return self.size  # Vrátí počet prvků v zásobníku

    # Metoda pro vyprázdnění celého zásobníku
    def clear(self):
        self.top = None  # Nastavíme vrchol zásobníku na None
        self.size = 0    # Počet prvků vynulujeme

    # Metoda pro vrácení všech prvků v zásobníku a jeho vyprázdnění
    def popAll(self):
        elements = []  # Seznam pro uložení všech prvků
        while self.top is not None:  # Procházíme zásobníkem, dokud není prázdný
            elements.append(self.pop())  # Odebereme prvek a přidáme ho do seznamu
        return elements  # Vrátíme seznam všech prvků

# Testování zásobníku
stack = Stack()
stack.add(10)
stack.add(20)
stack.add(30)
stack.add(40)
stack.add(50)

# Odebrání prvního prvku z vrcholu zásobníku
print("Odebrán prvek:", stack.pop())  # Odebere a vrátí prvek z vrcholu (50)

# Zobrazení počtu prvků v zásobníku
print("Počet prvků v zásobníku:", stack.count())  # Počet prvků po odebrání (4)

# Vypsání a odebrání všech prvků ze zásobníku
print("Všechny prvky v zásobníku:", stack.popAll())  # Vrátí všechny prvky a vyprázdní zásobník

# Zobrazení počtu prvků po vyprázdnění zásobníku
print("Počet prvků po vyprázdnění:", stack.count())  # Počet prvků po vyprázdnění (0)

# Pokus o odebrání prvku z prázdného zásobníku (vyvolá chybu)
try:
    stack.pop()
except IndexError as e:
    print(e)  # Očekávaná chyba: "Zásobník je prázdný, nelze odebrat prvek."
