import unittest
from alfa1.chat_app.app.chat.handlers.message_handler import MessageHandler
from alfa1.chat_app.app.utils.validators import MessageValidator
from alfa1.chat_app.app.utils.logger import LoggerFactory

class FakeManager:
    def __init__(self):
        self.broadcasted = []

    def broadcast_message(self, msg):
        self.broadcasted.append(msg)

class TestMessageHandler(unittest.TestCase):
    def setUp(self):
        self.logger = LoggerFactory.create_logger("test")
        self.validator = MessageValidator()
        self.fake_manager = FakeManager()
        self.handler = MessageHandler(validator=self.validator, logger=self.logger, manager=self.fake_manager)

    def test_handle_valid_message(self):
        response = self.handler.handle_message({"username": "User1", "content": "Hello"})
        self.assertIn("success", response)
        self.assertTrue(response["success"])
        self.assertEqual(response["message"]["content"], "Hello")

    def test_handle_invalid_message(self):
        # Message with invalid character (e.g. §)
        response = self.handler.handle_message({"username": "User2", "content": "Hello§"})
        self.assertIn("error", response)

if __name__ == '__main__':
    unittest.main()
