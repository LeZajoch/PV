import socket
import sys

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Připojeno k serveru na {self.host}:{self.port}")
        except ConnectionRefusedError:
            print("Nepodařilo se připojit k serveru. Ujistěte se, že server běží.")
            sys.exit(1)

    def send_command(self, command):
        try:
            self.client_socket.sendall((command + "\r\n").encode("utf-8"))
            response = self.client_socket.recv(1024).decode("utf-8")
            return response
        except (socket.error, KeyboardInterrupt):
            print("Spojení bylo přerušeno.")
            self.disconnect()
            sys.exit(1)

    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
            print("Odpojeno od serveru.")

    def run(self):
        print("Napište 'ex' pro ukončení programu.")
        welcome_message = self.client_socket.recv(1024).decode("utf-8")
        print(f"SERVER> {welcome_message.strip()}")
        while True:
            try:
                command = input("CLIENT> ").strip()
                if not command:
                    print()
                    continue
                if command.lower() == "ex":
                    self.disconnect()
                    break
                response = self.send_command(command)
                print(f"SERVER> {response}")
            except KeyboardInterrupt:
                print("\nOdpojování od serveru...")
                self.disconnect()
                break

if __name__ == "__main__":
    # Zadejte IP a port serveru
    host = input("Zadejte IP serveru (výchozí: 127.0.0.1): ").strip() or "127.0.0.1"
    port = input("Zadejte port serveru (výchozí: 65532): ").strip()
    port = int(port) if port else 65532

    client = Client(host, port)
    client.connect()
    client.run()
