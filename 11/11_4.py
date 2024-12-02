import unittest
from bottle import Bottle

class TestBottle(unittest.TestCase):
    def setUp(self):
        self.bottle = Bottle(max_capacity=5, current_capacity=2)

    def test_initialization(self):
        self.assertEqual(self.bottle.max_capacity, 5)
        self.assertEqual(self.bottle.current_capacity, 2)

    def test_fill_liters(self):
        self.bottle.open()
        self.bottle.fill_liters(2)
        self.assertEqual(self.bottle.current_capacity, 4)

    def test_fill_over_capacity(self):
        self.bottle.open()
        self.bottle.fill_liters(10)  # Překročí kapacitu
        self.assertEqual(self.bottle.current_capacity, 2)

    def test_close_and_open(self):
        self.bottle.close()
        self.assertTrue(self.bottle.cap)
        self.bottle.open()
        self.assertFalse(self.bottle.cap)

if __name__ == "__main__":
    unittest.main()