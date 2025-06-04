import socket
import threading
import json
import os

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        print("Nueva conexión:", clientAddress)
        super().__init__()
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        

    def run(self):
        try:
            data = self.csocket.recv(4096)
            mensaje = json.loads(data.decode('utf-8'))
            print(f"[{self.clientAddress}] -> {mensaje['algoritmo']} "
                  f"tardó {mensaje['tiempo']:.4f}s "
                  f"para {mensaje['cantidad_datos']} registros.")
            # Guardar en recibidos.json
            if os.path.exists("recibidos.json"):
                with open("recibidos.json", "r") as f:
                    recibidos = json.load(f)
            else:
                recibidos = []
            recibidos.append(mensaje)
            with open("recibidos.json", "w") as f:
                json.dump(recibidos, f, indent=4)
        except Exception as e:
            print("Error al procesar datos del cliente:", e)
        finally:
            self.csocket.close()

LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Servidor iniciado. Esperando conexiones...")

while True:
    server.listen(3)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()



