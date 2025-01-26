# chat_app/app/server.py

from flask import Flask
from flask_sock import Sock
from multiprocessing import Process, Queue
from alfa1.chat_app.app.config_manager import ConfigManager
from alfa1.chat_app.app.utils.logger import LoggerFactory
from alfa1.chat_app.app.chat.manager import ChatManager
from alfa1.chat_app.app.chat.handlers.message_handler import MessageHandler
from alfa1.chat_app.app.utils.validators import MessageValidator
from alfa1.chat_app.app.web.routes import web_bp
import json
from alfa1.chat_app.app import message_process
from alfa1.chat_app.app import logger_process

class ChatServer:
    """
    Main Chat Server Application using multiprocessing for message handling and logging.
    """

    def __init__(self, config_path="config.yaml"):
        self.config_manager = ConfigManager()
        self.config_manager.load_config(config_path)

        # Setup logging queue
        self.log_queue = Queue()
        self.logger = LoggerFactory.setup_logger(self.log_queue, name="server")

        # Start logger process
        self.logger_proc = Process(target=logger_process.logger_process_main, args=(config_path,), daemon=True)
        self.logger_proc.start()

        self.app = Flask(__name__)
        self.app.register_blueprint(web_bp)

        self.sock = Sock(self.app)

        # Setup message queue for inter-process communication
        self.message_queue = Queue()
        self.broadcast_queue = Queue()

        # Start message processing process
        self.message_proc = Process(target=message_process.message_process_main, args=(
            self.message_queue, self.broadcast_queue, self.log_queue, config_path
        ), daemon=True)
        self.message_proc.start()

        # Initialize ChatManager with broadcast_queue
        self.chat_manager = ChatManager(
            logger=self.logger,
            message_queue=self.message_queue,
            broadcast_queue=self.broadcast_queue
        )

        self.validator = MessageValidator()
        self.message_handler = MessageHandler(
            validator=self.validator,
            logger=self.logger,
            manager=self.chat_manager
        )

        @self.sock.route('/ws')
        def websocket_route(ws):
            return self.handle_websocket(ws)

    def handle_websocket(self, ws):
        """
        Handles WebSocket connections.
        """
        # Register the connection
        self.chat_manager.register_connection(ws)

        try:
            while True:
                data = ws.receive()
                if data is None:
                    break  # Client disconnected
                # Handle incoming messages (assume JSON)
                try:
                    message_data = json.loads(data)
                    response = self.handle_incoming_message(message_data)
                    if response.get("error"):
                        ws.send(json.dumps({"type": "error", "error": response["error"]}))
                except Exception as ex:
                    self.logger.error(f"Error processing message: {ex}")
                    ws.send(json.dumps({"type": "error", "error": "Invalid message format."}))
        except Exception as e:
            self.logger.warning(f"WebSocket disconnected with error: {e}")
        finally:
            # Unregister the connection
            self.chat_manager.unregister_connection(ws)

    def handle_incoming_message(self, message_data: dict) -> dict:
        msg_type = message_data.get("type", "message")
        if msg_type == "message":
            return self.message_handler.handle_message(message_data)
        else:
            self.logger.warning("Unknown message type received.")
            return {"error": "Unknown message type."}

    def run(self):
        host = self.config_manager.get("server.host", "127.0.0.1")
        port = self.config_manager.get("server.port", 5000)
        debug = self.config_manager.get("server.debug", False)
        self.logger.info(f"Starting server at {host}:{port}")

        self.app.run(host=host, port=port, debug=debug)

    def shutdown(self):
        """
        Shuts down all processes gracefully.
        """
        self.logger.info("Shutting down server...")
        self.message_proc.terminate()
        self.logger_proc.terminate()
        self.message_proc.join()
        self.logger_proc.join()
        self.logger.info("Server shut down successfully.")
