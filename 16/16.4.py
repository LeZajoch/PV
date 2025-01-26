import socket
import random
from datetime import datetime
import threading
import state


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.clients = []
        self.shutdown_votes = {}
        self.state = None  # Stav pro Ohmův zákon je výchoze None (mimo stavový režim)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server běží na {self.host}:{self.port}")
        while self.running:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Připojen klient: {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        client_socket.send("Vítejte na serveru! Napište 'help' pro dostupné příkazy.\r\n".encode('utf-8'))
        buffer = ""
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                buffer += data
                while '\r\n' in buffer:
                    command, buffer = buffer.split('\r\n', 1)
                    command = command.strip()
                    print(f"Přijatý příkaz: {command}")

                    # Pokud je stav Ohmova zákona aktivní, zpracovává se stavovým modelem
                    if self.state:
                        response = self.state.handle_input(self, client_socket, command)
                        if response:
                            client_socket.send((response + "\r\n").encode('utf-8'))
                        # Stavový režim končí, pokud klient zadá příkaz "EXITCALCULATE"
                        if command.upper() == "EXITCALCULATE":
                            self.state = None
                            client_socket.send("Opouštíte režim výpočtu Ohmova zákona.\r\n".encode('utf-8'))
                        continue

                    # Zpracování standardních příkazů
                    response = self.process_command(command, client_socket)
                    if response:
                        client_socket.send((response + "\r\n").encode('utf-8'))
            except ConnectionResetError:
                break

        self.clients.remove(client_socket)
        client_socket.close()

    def process_command(self, command, client_socket):
        commands = {
            "help": self.show_help,
            "cit": self.send_quote,
            "dat": self.send_date,
            "cli": self.show_client_count,
            "bro": self.broadcast_message,
            "ss": self.request_shutdown,
            "ex": self.disconnect_client,
            "calculateohm": self.start_ohm_calculation,  # Nový příkaz pro Ohmův zákon
        }
        func = commands.get(command.split()[0].lower(), self.unknown_command)
        return func(client_socket, command)

    def start_ohm_calculation(self, client_socket, command):
        self.state = state.StateKnowNothing()  # Přepnutí na výchozí stav pro Ohmův zákon
        return "Zahajujete výpočet Ohmova zákona. Zadejte hodnoty U, R nebo I."

    def show_help(self, client_socket, command):
        help_message = (
            "Dostupné příkazy:\r\n"
            "cit - vypíše citát\r\n"
            "dat - vrátí aktuální datum\r\n"
            "cli - zobrazí počet aktuálně připojených klientů\r\n"
            "bro [zpráva] - pošle zprávu všem připojeným klientům\r\n"
            "ss - zahájí hlasování o vypnutí serveru\r\n"
            "ex - odpojí vás ze serveru\r\n"
            "calculateohm - zahájí výpočet Ohmova zákona (U, R, I)\r\n"
        )
        return help_message

    def send_quote(self, client_socket, command):
        quotes = [
            "Nejlepší čas zasadit strom byl před 20 lety. Druhý nejlepší čas je teď.",
            "Buď změnou, kterou chceš vidět ve světě.",
            "Nikdy se nevzdávej. Velké věci potřebují čas.",
        ]
        return random.choice(quotes)

    def send_date(self, client_socket, command):
        return f"Dnešní datum je: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def show_client_count(self, client_socket, command):
        return f"Aktuálně připojených klientů: {len(self.clients)}"

    def broadcast_message(self, client_socket, command):
        message = command[len("bro "):].strip()
        if not message:
            return "Zpráva je prázdná. Použijte: bro [zpráva]"

        for client in self.clients:
            if client != client_socket:  # Neposílat zprávu odesilateli
                try:
                    client.send(f"BROADCAST: {message}\r\n".encode('utf-8'))
                except:
                    pass  # Ignorujeme chyby při posílání

        return "Broadcast zpráva byla odeslána."

    def request_shutdown(self, client_socket, command):
        if client_socket in self.shutdown_votes:
            return "Již jste hlasoval pro vypnutí serveru."

        self.shutdown_votes[client_socket] = None
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send("Příkaz 'shutdown-server' byl odeslán. Souhlasíte s vypnutím serveru? (yes/no)\r\n".encode('utf-8'))
                except:
                    pass

        return "Hlasování o vypnutí serveru zahájeno. Čeká se na odpovědi všech klientů."

    def disconnect_client(self, client_socket, command):
        client_socket.send("Byli jste odpojeni.\r\n".encode('utf-8'))
        self.clients.remove(client_socket)
        client_socket.close()
        return None

    def unknown_command(self, client_socket, command):
        return "Neznámý příkaz. Napište 'help' pro seznam dostupných příkazů."


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 65532
    server = Server(host, port)
    server.start()
