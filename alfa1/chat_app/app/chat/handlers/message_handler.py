from .base_handler import BaseHandler

class MessageHandler(BaseHandler):
    """
    Handles normal chat messages by placing them into the message_queue.
    """

    def __init__(self, validator, logger, manager):
        self.validator = validator
        self.logger = logger
        self.manager = manager

    def handle_message(self, message_data: dict) -> dict:
        username = message_data.get("username", "Anonymous")
        content = message_data.get("content", "")
        if not self.validator.validate(content):
            self.logger.warning("Invalid message content received.")
            return {"error": "Invalid message content."}

        # Place the message into the message_queue for processing
        self.manager.message_queue.put(message_data)
        self.logger.info(f"Received message from {username} and queued for processing.")
        return {"success": True}
