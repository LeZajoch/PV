import os
import sys
import json
import subprocess
import time


def load_config():
    """Load configuration from config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    # Create default config if it doesn't exist
    if not os.path.exists(config_path):
        default_config = {
            "backend": {"host": "127.0.0.1", "port": 5000},
            "frontend": {"host": "localhost", "port": 8000}
        }
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)
        print(f"Created default config file at {config_path}")
        return default_config

    # Load existing config
    with open(config_path, "r") as f:
        config = json.load(f)
    return config


# Get the current directory (which is the website directory)
website_dir = os.path.abspath(os.path.dirname(__file__))
print(f"Website directory: {website_dir}")

# Load configuration
config = load_config()
backend_host = config["backend"]["host"]
backend_port = config["backend"]["port"]
frontend_host = config["frontend"]["host"]
frontend_port = config["frontend"]["port"]


# Function to run the backend server
def run_backend():

    print(f"Starting backend server on {backend_host}:{backend_port}...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "flask", "run", "--host", backend_host, "--port", str(backend_port)],
        cwd=website_dir,
        env={**os.environ, "FLASK_APP": "backend.views.app"}
    )
    return backend_process


# Function to run the frontend server
def run_frontend():
    frontend_dir = os.path.join(website_dir, "frontend")
    print(f"Frontend directory: {frontend_dir}")

    print(f"Starting frontend server on {frontend_host}:{frontend_port}...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(frontend_port)],
        cwd=frontend_dir
    )
    return frontend_process


def main():
    # Start both servers
    backend_process = run_backend()
    time.sleep(2)  # Give backend a moment to start
    frontend_process = run_frontend()

    print("\nServers are running!")
    print(f"Backend server: http://{backend_host}:{backend_port}")
    print(f"Frontend server: http://{frontend_host}:{frontend_port}")
    print("\nPress Ctrl+C to stop both servers\n")

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()


if __name__ == "__main__":
    main()
