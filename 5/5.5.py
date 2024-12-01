# Definice třídy pro uzel (Node)
class Node:
    def __init__(self, data):
        self.data = data  # Hodnota uzlu
        self.next = None  # Ukazatel na další uzel (vpravo)
        self.prev = None  # Ukazatel na předchozí uzel (vlevo)

# Definice třídy pro obousměrný spojový seznam (Doubly Linked List)
class DoublyLinkedList:
    def __init__(self):
        self.head = None  # Počáteční uzel (hlava)
        self.tail = None  # Konečný uzel (ocas)

    # Funkce pro přidání nového uzlu na konec seznamu
    def append(self, data):
        new_node = Node(data)  # Vytvoří nový uzel s daty
        if self.head is None:  # Pokud je seznam prázdný
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node  # Současný konec ukáže na nový uzel
            new_node.prev = self.tail  # Nový uzel ukáže zpět na předchozí uzel
            self.tail = new_node  # Nový uzel se stane novým koncem

    def add_to_start(self, data):
        new_node = Node(data)  # Vytvoří nový uzel s daty
        if self.head is None:  # Pokud je seznam prázdný
            self.head = new_node # Nový uzel se stane hlavou
            self.tail = new_node  # Nový uzel se stane i ocasem
        else:
            new_node.next = self.head  # Nový uzel ukazuje na současnou hlavu
            self.head.prev = new_node  # Současná hlava ukazuje zpět na nový uzel
            self.head = new_node  # Nový uzel se stane novou hlavou seznamu

    # Funkce pro vypsání prvků od prvního k poslednímu
    def display_forward(self):
        current = self.head
        if current is None:
            print("Seznam je prázdný.")
        else:
            print("Od prvního k poslednímu:")
            while current:
                print(current.data)
                current = current.next  # Přejdeme na další uzel

    # Funkce pro vypsání prvků od posledního k prvnímu
    def display_backward(self):
        current = self.tail
        if current is None:
            print("Seznam je prázdný.")
        else:
            print("Zpětně od posledního k prvnímu:")
            while current:
                print(current.data)
                current = current.prev  # Přejdeme na předchozí uzel

# Vytvoření obousměrného spojového seznamu a naplnění minimálně 5 prvky
doubly_linked_list = DoublyLinkedList()
doubly_linked_list.append(10)
doubly_linked_list.append(20)
doubly_linked_list.append(30)
doubly_linked_list.append(40)
doubly_linked_list.append(50)

# Vypsání všech prvků od prvního k poslednímu
doubly_linked_list.display_forward()

# Vypsání všech prvků zpětně od posledního k prvnímu
doubly_linked_list.display_backward()
