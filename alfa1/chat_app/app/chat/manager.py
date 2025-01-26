from flask_sock import Sock
import json
import multiprocessing
import threading
from ..utils.logger import LoggerFactory
from ..utils.validators import MessageValidator

class ChatManager:
    """
    Manages active WebSocket connections and communicates with the message processing.
    """

    def __init__(self, logger, message_queue: multiprocessing.Queue, broadcast_queue: multiprocessing.Queue):
        self.logger = logger
        self.message_queue = message_queue
        self.broadcast_queue = broadcast_queue
        self.active_connections = set()
        self.lock = threading.Lock()

        # Start a thread to listen to broadcast_queue
        self.listener_thread = threading.Thread(target=self.listen_to_broadcast, daemon=True)
        self.listener_thread.start()

    def register_connection(self, ws):
        with self.lock:
            self.active_connections.add(ws)
            self.logger.info(f"New connection registered: {ws}")

    def unregister_connection(self, ws):
        with self.lock:
            if ws in self.active_connections:
                self.active_connections.remove(ws)
                self.logger.info(f"Connection unregistered: {ws}")

    def send_message_to_all(self, data):
        """
        Sends a message to all active WebSocket connections.
        """
        with self.lock:
            for conn in self.active_connections.copy():
                try:
                    conn.send(json.dumps(data))
                except Exception as e:
                    self.logger.error(f"Error sending message to {conn}: {e}")
                    self.active_connections.remove(conn)

    def listen_to_broadcast(self):
        """
        Listens to the broadcast_queue and sends messages to all clients.
        """
        while True:
            try:
                data = self.broadcast_queue.get()
                if data == "SHUTDOWN":
                    self.logger.info("Shutting down broadcast listener.")
                    break
                self.send_message_to_all(data)
            except Exception as e:
                self.logger.error(f"Error in broadcast listener: {e}")
