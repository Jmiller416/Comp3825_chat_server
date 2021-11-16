import socket
import threading
import configparser
import signal
import sys
import ssl

from typing import Tuple


class ChatServer:
    def __init__(self):
        self.connections = []
        self.users = {}
        self.active = True

        self.stop_sock = threading.Event()
        self.host, self.port = self.get_config()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secureSock = ssl.wrap_socket(self.sock,
                                          server_side=True,
                                          certfile='./ssl/server.crt',
                                          keyfile='./ssl/server.key')

    def start(self):
        try:
            self.secureSock.bind((self.host, self.port))
            self.secureSock.listen(4)

            print("Server ready to connect at %s:%d" % (self.host, self.port))

            while True:
                connection, address = self.secureSock.accept()
                connection.send("%IDENTIFY".encode('utf-8'))
                username = connection.recv(1024).decode('utf-8')

                self.users[self.address_key(address)] = username
                self.connections.append(connection)
                self.broadcast_message("New user connected: %s" % username)

                print("New user connected: %s" % username)

                threading.Thread(target=self.handler, args=[connection, address, self.stop_sock]).start()

        except Exception as e:
            print(e)
        finally:
            if len(self.connections) > 0:
                for conn in self.connections:
                    self.terminate_connection(conn, address)

            self.secureSock.close()

    @staticmethod
    def get_config() -> Tuple[str, int]:
        config = configparser.ConfigParser()
        config.read('config.ini')
        port = 1234

        if 'server' in config:
            if 'port' in config['server']:
                port = int(config['server']['port'])

        server = ''
        return server, port

    def send_to_peers(self, message: str, address: any, connection: socket.socket):
        for conn in self.connections:
            if conn != connection:
                formatted_message = ("%s> %s" % (self.get_username(address), message))

                try:
                    conn.send(formatted_message.encode('utf-8'))

                except Exception as e:
                    print(e)
                    self.terminate_connection(conn, address)

    def handler(self, connection, address, stop_sock_event):
        while not stop_sock_event.is_set():
            try:
                data = connection.recv(1024)

                if data:
                    user_message = data.decode('utf-8')
                    self.send_to_peers(user_message, address, connection)
                else:
                    username = self.users[self.address_key(address)]
                    self.broadcast_message("%s has disconnected" % username)
                    print("%s has disconnected" % username)

                    self.terminate_connection(connection, address)
                    break

            except Exception as e:
                print(e)
                self.terminate_connection(connection, None)
                break

    def terminate_connection(self, connection: socket.socket, address: any):
        if connection in self.connections:
            connection.close()

            self.connections.remove(connection)

            if address:
                del self.users[address[0]]

    def broadcast_message(self, message: str):
        for conn in self.connections:
            conn.send(message.encode('utf-8'))

    def stop_server(self, signum, frame):
        for connection in self.connections:
            connection.close()
            self.connections.remove(connection)

        self.users = []
        self.active = False
        self.secureSock.close()
        self.sock.close()
        self.stop_sock.set()
        print("Bye!!")
        sys.exit(0)

    @staticmethod
    def address_key(address):
        return str(address[0]) + '-' + str(address[1])

    def get_username(self, address):
        return self.users[self.address_key(address)]


if __name__ == "__main__":
    server = ChatServer()

    signal.signal(signal.SIGINT, server.stop_server)
    server.start()
    signal.pause()
