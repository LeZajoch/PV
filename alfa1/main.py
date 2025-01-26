# main.py

from alfa1.chat_app.app.server import ChatServer
import multiprocessing
import sys
import os

def main():
    # Optional: Print sys.path for debugging
    print("Current sys.path:", sys.path)

    # Initialize and run the ChatServer
    server = ChatServer(config_path="chat_app/config.yaml")  # Adjust path if necessary
    try:
        server.run()
    except KeyboardInterrupt:
        print("Shutting down...")
        server.shutdown()

if __name__ == "__main__":
    # Set multiprocessing start method
    multiprocessing.set_start_method('spawn')
    main()
