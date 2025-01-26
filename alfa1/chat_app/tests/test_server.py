import unittest
from alfa1.chat_app.app.server import ChatServer

class TestServer(unittest.TestCase):
    def test_config(self):
        server = ChatServer("config.yaml")
        self.assertIsNotNone(server.config_manager.get("server.host"))

if __name__ == '__main__':
    unittest.main()
