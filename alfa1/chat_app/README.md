# Web Chat Application

## Overview

This project implements a simple real-time web chat application using Python, Flask, and WebSockets (Flask-Sock). Users can connect to the web interface, enter a username, and start exchanging messages in real-time. The server broadcasts messages to all connected clients.


## Features

- **Real-time messaging** using WebSockets
- **Configurable** via `config.yaml` without modifying source code
- **OOP Design** with classes for configuration, message handling, and server management
- **Validation and Logging**: Messages are validated, invalid input is handled gracefully, and logs are recorded
- **Testing**: Includes unit tests for configuration, message handling, validation, and basic server checks
- **Error Handling**: Handles common errors and logs them
- **Scalable**: Supports multiple connected clients simultaneously

## Usage

1. **Install Dependencies**
   ```bash
   pip install flask pyyaml flask-sock

2. **Run the Server**
   ```bash
   python -m app.server

3. **Send Messages**
    - Open the Chat UI Go to http://127.0.0.1:5000 in your browser.
    - Enter a username and message, and click Send.
    - Open the same URL in another browser/tab to see messages in real-time.

## Testing
**To run tests**
   ```bash
   cd tests
   python -m unittest discover
