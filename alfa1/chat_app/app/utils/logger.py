# app/utils/logger.py
import logging
import multiprocessing
import sys
from multiprocessing import Queue
from logging.handlers import QueueHandler, QueueListener

from ..config_manager import ConfigManager

class LoggerFactory:
    """
    Factory for creating a configured logger instance that sends logs to a multiprocessing queue.
    """

    @staticmethod
    def setup_logger(queue: Queue, name="chat_app"):
        config = ConfigManager()
        log_level_str = config.get("logging.level", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        log_file = config.get("logging.file", None)

        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.handlers = []

        # Use QueueHandler to send logs to the queue
        qh = QueueHandler(queue)
        qh.setLevel(log_level)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
        qh.setFormatter(formatter)
        logger.addHandler(qh)

        return logger

def configure_listener(queue: Queue, config_path="config.yaml"):
    """
    Configures the logging listener which runs in a separate process.
    """
    config = ConfigManager()
    config.load_config(config_path)
    log_level_str = config.get("logging.level", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    log_file = config.get("logging.file", None)

    handlers = []
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')

    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        handlers.append(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    handlers.append(ch)

    listener = QueueListener(queue, *handlers)
    listener.start()
    return listener
