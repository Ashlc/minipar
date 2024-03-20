import socket
import threading

class Server:
    def __init__(self, host):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (host, 9999)
        self.server_socket.bind(self.addr)
        self.server_socket.listen()
        self.connected_clients = []
        self.procedure = None

    def start(self):
        print("[SERVER] Waiting for connections...")
        while True:
            client_socket, client_addr = self.server_socket.accept()
            print(f"[SERVER] Connected to {client_addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
            self.connected_clients.append((client_socket, client_thread))

    def handle_client(self, client_socket):
        connected = True
        while connected:
            data = client_socket.recv(1024)
            if not data:
                connected = False
                break
            message = data.decode()
            print(f"[SERVER] Received message: {message}")
            if message == "exit":
                connected = False
            elif self.procedure == "calculadora":
                result = self.calculate(message)
                client_socket.send(str(result).encode("ascii"))
            else:
                client_socket.send("Invalid command".encode("ascii"))
        client_socket.close()

    def set_procedure(self, procedure):
        if procedure == "calculadora":
            self.procedure = procedure
            self.broadcast("Awaiting expression...")
        else:
            self.broadcast("Invalid procedure")

    def broadcast(self, message):
        for client_socket, _ in self.connected_clients:
            client_socket.send(message.encode("ascii"))

    def calculate(self, expression):
        try:
            result = eval(expression)
            return result
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    server = Server("127.0.0.1")
    server.start()
