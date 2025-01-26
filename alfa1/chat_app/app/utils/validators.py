from ..config_manager import ConfigManager

class MessageValidator:
    """
    Validates chat messages according to config rules.
    """

    def __init__(self):
        config = ConfigManager()
        self.max_length = config.get("chat.max_message_length", 200)
        self.allowed_chars = config.get("chat.allowed_characters", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?@#")

    def validate(self, message: str) -> bool:
        if not isinstance(message, str):
            return False
        if len(message) > self.max_length:
            return False
        for char in message:
            if char not in self.allowed_chars:
                return False
        return True
