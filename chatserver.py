import socket
import threading
import configparser

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
peers = []

def setup_server():
    config = configparser.ConfigParser()
    config.read('config.ini')
    port = 1234

    if 'server' in config:
        if 'port' in config['server']:
            port = int(config['server']['port'])

    server = ''
    address = (server, port)

    sock.bind(address)
    sock.listen(2)
    print("Server ready to connect at %s:%d" % (server, port))


def handler(conn, addr):
    connected = True

    while connected:
        message = conn.recv(1024)
        send_peers(message)

    conn.close()


def send_peers(msg):
    for connection in connections:
        connection.send(msg)

setup_server()

while True:
    con, addr = sock.accept()

    con.send("%IDENTIFY".encode('utf-8'))

    client_id = con.recv(1024).decode('utf-8')

    connections.append(con)
    peers.append(client_id)

    send_peers(f"{client_id} has joined the chat!".encode('utf-8'))
    con.send('Connection successful!'.encode('utf-8'))

    client_thread = threading.Thread(target=handler, args=(con, addr))
    client_thread.daemon = True
    client_thread.start()

