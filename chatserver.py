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

    sock.bind(('', port))
    sock.listen(2)
    print("Server ready to connect on port %d" % port)


def handler(con, addr):
    while True:
        data = con.recv(1024)
        for connection in connections:
            connection.send(data)
            if not data:
                print(str(addr[0]) + ':' + str(addr[1]), "disconnected")
                connections.remove(con)
                peers.remove(addr[0])
                con.close()
                send_peers()
                break


# this is not functional needs to be fixed
def send_peers():
    p = ''
    for peer in peers:
        p = p + peer + ","
    for connection in connections:
        connection.send(b'\x11' + bytes(p, "utf-8"))

setup_server()

while True:
    con, addr = sock.accept()
    client_thread = threading.Thread(target=handler, args=(con, addr))
    client_thread.daemon = True
    client_thread.start()
    connections.append(con)
    peers.append(addr[0])
    print(str(addr[0]) + ':' + str(addr[1]), "connected")
    send_peers()
