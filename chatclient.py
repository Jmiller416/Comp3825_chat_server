import socket
import threading
import configparser

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_server(host, port):
    sock.connect((host, port))

def configure_and_connect():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'client' in config:
        host = '0.0.0.0'
        port = 1234

        if 'host' in config['client']:
            host = config['client']['host']

        if 'port' in config['client']:
            port = int(config['client']['port'])

        print("Connecting to host %s:%d" % (host, port))
        connect_server(host, port)
    else:
        exit(2)

def send_message():
    while True:
        message = input()
        if message == '.exit':
            sock.close()
        else:
            sock.send(bytes(input(""), 'utf-8'))




def update_peers(peer_data):
    peers = str(peer_data).split(",")[:-1]

def receive(self):
    while True:
        try:
            last_message = sock.recv(1024).decode('utf-8')

            if last_message == '%IDENTIFY':
                sock.send(self.name.encode('utf-8'))
            else:
                print(last_message + "\r\n")
        except:
            print("An error occured!")
            sock.close()
            break


def setup():
    configure_and_connect()
    client_thread = threading.Thread(target=receive)
    client_thread.daemon = True
    client_thread.start()


setup()