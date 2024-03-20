import socket


class Client:
    def __init__(self, server_addr):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = server_addr
        self.socket.connect(self.server_addr)

    def send(self, message):
        print(f"[CLIENT] Sending message: {message}")
        self.socket.send(message.encode("ascii"))
        if message == "exit":
            self.close()

    def receive(self):
        data = self.socket.recv(1024)
        message = data.decode()
        print(f"[CLIENT] Received message: {message}")

    def close(self):
        self.socket.close()
