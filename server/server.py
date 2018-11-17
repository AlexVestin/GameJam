from SimpleWebSocketServ import SimpleWebSocketServer, WebSocket
import socket

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65431        # Port to listen on (non-privileged ports are > 1023)

conn = None
s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(1)

print("waiting for connections")
conn, addr = s.accept()
print(addr, "connected")

def update(data):
    print(data)

clients = []
class SimpleServer(WebSocket):
    initialized = False
    name = ""

    def handleMessage(self):
        if not self.initialized:
            self.name = self.data
            self.initialized = True

        # self.messages.append(self.data)
        conn.sendall(self.data)
        # update(self.data)


    def handleConnected(self):
       print(self.address, 'connected')
       clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')
