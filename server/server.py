from SimpleWebSocketServ import SimpleWebSocketServer, WebSocket
import socket

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65431        # Port to listen on (non-privileged ports are > 1023)

conn = None
s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

connected_to_server = False
sent_count = 0
clients = []
class SimpleServer(WebSocket):
    initialized = False
    name = ""

    def handleMessage(self):
        global connected_to_server
        global sent_count
        if not self.initialized:
            self.name = self.data
            self.initialized = True

        # self.messages.append(self.data)
        if connected_to_server:
            try:
                conn.sendall(self.data)
                sent_count += 1
            except:
                connected_to_server = False
                print("Disconnected")
        # update(self.data)


    def handleConnected(self):
       print(self.address, 'connected')
       clients.append(self)

    def handleClose(self):
       clients.remove(self)
       print(self.address, 'closed')
       for client in clients:
          client.sendMessage(self.address[0] + u' - disconnected')


server = SimpleWebSocketServer('0.0.0.0', 8000, SimpleServer)
ping_cnt = 0
while True:
    msg = None
    if not connected_to_server:
        print("waiting for connections")
        s.listen(1)
        connected_to_server = True
        conn, addr = s.accept()
        print(addr, "connected")
    else:
        if ping_cnt % 12 == 0:
            try:
                conn.sendall("ping||||||||")
            except:
                connected_to_server = False
                print("Disconnected")
    server.serveonce()
    ping_cnt += 1
