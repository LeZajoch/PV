import multiprocessing
from .chat.models import ChatMessage
from .config_manager import ConfigManager
from .utils.logger import LoggerFactory

def message_process_main(message_queue: multiprocessing.Queue, broadcast_queue: multiprocessing.Queue, log_queue: multiprocessing.Queue, config_path="config.yaml"):
    """
    Main function for the message processing.
    """
    config = ConfigManager()
    config.load_config(config_path)
    logger = LoggerFactory.setup_logger(log_queue, name="message_process")

    while True:
        try:
            message_data = message_queue.get()
            if message_data == "SHUTDOWN":
                logger.info("Shutting down message processing.")
                break

            username = message_data.get("username", "Anonymous")
            content = message_data.get("content", "")
            chat_message = ChatMessage(username, content)
            message_dict = chat_message.to_dict()
            data = {"type": "message", "data": message_dict}

            # Place the processed message into the broadcast_queue
            broadcast_queue.put(data)
            logger.info(f"Processed message from {username} and queued for broadcast.")
        except Exception as e:
            logger.error(f"Error in message processing: {e}")
