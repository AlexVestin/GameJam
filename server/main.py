from server import SimpleServer
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import time

server = SimpleWebSocketServer('0.0.0.0', 8000, SimpleServer)

start_time = time.time()
while True:
    server.serveonce()
