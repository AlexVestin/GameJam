


import socket

HOST = '130.236.181.73'  # The server's hostname or IP address
PORT = 65431        # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
recv_count = 0
while 1:
    msg = ""
    try:
        msg = s.recv(12)
    except:
        pass
    
    if msg:
        print(msg.encode("UTF-8"))
        print(recv_count)
        recv_count += 1