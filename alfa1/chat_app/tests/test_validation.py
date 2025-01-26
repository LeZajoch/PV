import unittest
from alfa1.chat_app.app.utils.validators import MessageValidator

class TestValidation(unittest.TestCase):
    def setUp(self):
        self.validator = MessageValidator()

    def test_valid_message(self):
        self.assertTrue(self.validator.validate("Hello world!"))

    def test_long_message(self):
        msg = "a" * 1000
        self.assertFalse(self.validator.validate(msg))

    def test_invalid_chars(self):
        self.assertFalse(self.validator.validate("Hello ♥"))

if __name__ == '__main__':
    unittest.main()
