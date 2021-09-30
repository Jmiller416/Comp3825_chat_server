import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 1234
sock.connect(('localhost', port))

def send_message():
    while True:
        message = input()
        if message == '.exit':
                sock.close()
        else:
            sock.send(bytes(input(""), 'utf-8'))
             
client_thread = threading.Thread(target = send_message)
client_thread.daemon = True
client_thread.start()

def update_peers(peer_data):
    peers = str(peer_data).split(",")[:-1]     

while True:
    data = sock.recv(1024)
    if not data:
        break
    if data[0:1] == b'\x11':
        update_peers(data[1:])
    else:
        print(str(data))
