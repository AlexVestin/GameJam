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
    id = ""

    def fill(self, s):
        l = len(s)
        s = self.id + s

        return s

    def handleMessage(self):
        global connected_to_server
        global sent_count
        if connected_to_server:
            if not self.initialized:
                self.name = self.data

                try:
                    conn.sendall(self.data)
                except:
                    connected_to_server = False
                    print("Disconnected")

                msg = ""
                try:
                    msg = conn.recv(2)
                except:
                    pass
                self.id = msg

                print("id:", self.id)
                self.initialized = True

        # self.messages.append(self.data)
            else:
                try:
                    conn.sendall(self.fill(self.data))
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
       conn.send(self.id + "CLOSED||||||||")


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
                conn.sendall("ping||||||||||||")
            except:
                connected_to_server = False
                print("Disconnected")
    server.serveonce()
    ping_cnt += 1
