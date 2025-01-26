import multiprocessing
from .utils.logger import configure_listener
from .config_manager import ConfigManager

def logger_process_main(config_path="config.yaml"):
    """
    Main function for the logger process.
    """
    config = ConfigManager()
    config.load_config(config_path)
    log_queue = multiprocessing.Queue(-1)
    listener = configure_listener(log_queue, config_path)

    try:
        while True:
            # Keep the logger process alive
            listener.handle()
    except KeyboardInterrupt:
        listener.stop()

if __name__ == "__main__":
    logger_process_main()
