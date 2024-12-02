import unittest
import linked_list

class TestLinkedList(unittest.TestCase):
    def setUp(self):
        # Vytvoříme prázdný seznam pro každý test
        self.ll = linked_list.LinkedList()

    def test_add(self):
        # Přidání jednoho prvku a ověření velikosti seznamu
        self.ll.add(5)
        self.assertEqual(self.ll.get_size(), 1)

        # Přidání více prvků
        self.ll.add(8)
        self.assertEqual(self.ll.get_size(), 2)
        self.ll.add(12)
        self.assertEqual(self.ll.get_size(), 3)

    def test_remove(self):
        # Přidáme nějaké prvky
        self.ll.add(5)
        self.ll.add(8)
        self.ll.add(12)

        # Ověření odstranění prvku
        self.assertTrue(self.ll.remove(8))  # Mělo by to být úspěšné
        self.assertEqual(self.ll.get_size(), 2)

        # Pokusíme se odstranit prvek, který tam není
        self.assertFalse(self.ll.remove(100))  # Mělo by to být neúspěšné

        # Ověření odstranění hlavy seznamu (12)
        self.assertTrue(self.ll.remove(12))
        self.assertEqual(self.ll.get_size(), 1)

    def test_find(self):
        # Přidáme nějaké prvky
        self.ll.add(5)
        self.ll.add(8)
        self.ll.add(12)

        # Ověření vyhledávání prvků
        self.assertEqual(self.ll.find(5), 5)  # Mělo by vrátit 5
        self.assertEqual(self.ll.find(8), 8)  # Mělo by vrátit 8
        self.assertIsNone(self.ll.find(100))  # Neexistující prvek by měl vrátit None

    def test_size(self):
        # Přidáme prvky a zkontrolujeme velikost
        self.ll.add(5)
        self.ll.add(8)
        self.assertEqual(self.ll.get_size(), 2)

        # Odstraníme prvek a zkontrolujeme opět velikost
        self.ll.remove(8)
        self.assertEqual(self.ll.get_size(), 1)

        # Přidáme další prvek
        self.ll.add(12)
        self.assertEqual(self.ll.get_size(), 2)

        # Odstraníme poslední prvek
        self.ll.remove(5)
        self.assertEqual(self.ll.get_size(), 1)


if __name__ == "__main__":
    unittest.main()