import os
import sys
import json
import subprocess
import time


def load_config():
    """
    Load the configuration from a JSON file located in the same directory as this script.
    If the configuration file does not exist, a default configuration is created.

    Returns:
        dict: The configuration dictionary containing backend and frontend settings.
    """
    # Determine the path to the config.json file.
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    # If the config file does not exist, create it with default settings.
    if not os.path.exists(config_path):
        default_config = {
            "backend": {"host": "127.0.0.1", "port": 5000},
            "frontend": {"host": "localhost", "port": 8000}
        }
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)
        print(f"Created default config file at {config_path}")
        return default_config

    # Load the existing configuration.
    with open(config_path, "r") as f:
        config = json.load(f)
    return config


# Get the absolute path to the website directory.
website_dir = os.path.abspath(os.path.dirname(__file__))
print(f"Website directory: {website_dir}")

# Load configuration for backend and frontend servers.
config = load_config()
backend_host = config["backend"]["host"]
backend_port = config["backend"]["port"]
frontend_host = config["frontend"]["host"]
frontend_port = config["frontend"]["port"]


def run_backend():
    """
    Start the backend server using Flask.

    Returns:
        subprocess.Popen: The process object for the backend server.
    """
    print(f"Starting backend server on {backend_host}:{backend_port}...")
    # Start the Flask backend server with specified host and port.
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "flask", "run", "--host", backend_host, "--port", str(backend_port)],
        cwd=website_dir,
        env={**os.environ, "FLASK_APP": "backend.views.app"}
    )
    return backend_process


def run_frontend():
    """
    Start the frontend server using Python's built-in HTTP server.

    Returns:
        subprocess.Popen: The process object for the frontend server.
    """
    # Define the path to the frontend directory.
    frontend_dir = os.path.join(website_dir, "frontend")
    print(f"Frontend directory: {frontend_dir}")

    print(f"Starting frontend server on {frontend_host}:{frontend_port}...")
    # Start the HTTP server on the specified port.
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(frontend_port)],
        cwd=frontend_dir
    )
    return frontend_process


def main():
    """
    Main function to start both backend and frontend servers.
    The servers will keep running until a KeyboardInterrupt (Ctrl+C) is received.
    """
    # Launch the backend server.
    backend_process = run_backend()
    # Allow some time for the backend to start up.
    time.sleep(2)
    # Launch the frontend server.
    frontend_process = run_frontend()

    print("\nServers are running!")
    print(f"Backend server: http://{backend_host}:{backend_port}")
    print(f"Frontend server: http://{frontend_host}:{frontend_port}")
    print("\nPress Ctrl+C to stop both servers\n")

    try:
        # Keep the main thread alive.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C.
        print("\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()


if __name__ == "__main__":
    main()
