class ChatMessage:
    """
    Model representing a chat message.
    """

    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    def to_dict(self):
        return {"username": self.username, "content": self.content}
