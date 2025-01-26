import unittest
from alfa1.chat_app.app.config_manager import ConfigManager

class TestConfig(unittest.TestCase):
    def test_load_config(self):
        cm = ConfigManager()
        cm.load_config("config.yaml")
        self.assertIsNotNone(cm.get("server.host"))

if __name__ == '__main__':
    unittest.main()
