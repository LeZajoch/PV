# Definice třídy pro uzel (Node)
class Node:
    def __init__(self, data):
        self.data = data  # Hodnota, kterou uzel obsahuje
        self.next = None  # Ukazatel na další uzel, výchozí hodnota None

# Definice třídy pro jednosměrný spojový seznam
class LinkedList:
    def __init__(self):
        self.head = None  # Počáteční uzel seznamu je None (prázdný)

    # Funkce pro přidání nového uzlu na konec seznamu
    def append(self, data):
        new_node = Node(data)  # Vytvoří nový uzel s daty
        if self.head is None:
            self.head = new_node  # Pokud je seznam prázdný, nový uzel se stane hlavou
        else:
            current = self.head
            while current.next:  # Procházíme seznamem až na konec
                current = current.next
            current.next = new_node  # Připojíme nový uzel na konec seznamu
    def add_to_start(self,data):
        new_node = Node(data)  # Vytvoří nový uzel s daty
        if self.head is None:
            self.head = new_node  # Pokud je seznam prázdný, nový uzel se stane hlavou
        else:
            new_node.next = self.head  # Nový uzel ukazuje na současnou hlavu
            self.head = new_node  # Nový uzel se stane novou hlavou seznamu
    # Funkce pro vypsání všech prvků seznamu
    def display(self):
        current = self.head
        if current is None:
            print("Seznam je prázdný.")  # Pokud je seznam prázdný
        else:
            while current:
                print(current.data)  # Vypíše data aktuálního uzlu
                current = current.next  # Přesun na další uzel

# Vytvoření spojového seznamu a naplnění minimálně 5 prvky
linked_list = LinkedList()
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)
linked_list.append(40)
linked_list.append(50)
linked_list.add_to_start(9)

# Vypsání všech prvků seznamu
linked_list.display()


