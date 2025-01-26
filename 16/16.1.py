import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 65532
server_socket.bind((host, port))

server_socket.listen(1)
print("Čekám na připojení klienta...")

client_socket, client_address = server_socket.accept()
print(f"Klient připojen: {client_address}")

client_socket.send(b"HELLO\n")




client_socket.close()
server_socket.close()
