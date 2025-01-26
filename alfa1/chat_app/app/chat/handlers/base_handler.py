from abc import ABC, abstractmethod

class BaseHandler(ABC):
    """
    Abstract base class for message handlers.
    """

    @abstractmethod
    def handle_message(self, message_data: dict) -> dict:
        pass
