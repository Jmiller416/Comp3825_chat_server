import socket
import threading
import configparser
import shortuuid
import os

from typing import Tuple

from gui import GUI


class ChatClient:
    def __init__(self):
        self.connected = False
        self.identifier = shortuuid.uuid()
        self.sock = socket.socket()
        self.username = self.identifier
        self.gui = GUI(self.send_message, self.start_chatting)

    def receive_messages(self):
        self.connected = True

        while self.connected:
            try:
                last_data = self.sock.recv(1024)

                if last_data:
                    last_message = last_data.decode('utf-8')
                    if last_message == '%IDENTIFY':
                        self.sock.send(self.username.encode('utf-8'))
                    else:
                        self.gui.message_received(last_message)
                else:
                    os.close(self.sock.fileno())
                    break

            except Exception as err:
                print(err)
                break

    def send_message(self, next_message):
        while True:
            if next_message == '.quit' or next_message == '.exit':
                self.sock.send("has disconnected".encode('utf-8'))
                self.connected = False
            else:
                self.sock.send(next_message.encode())

            break

    def get_config(self) -> Tuple[str, int]:
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'client' in config:
            host = '0.0.0.0'
            port = 1234

            if 'host' in config['client']:
                host = config['client']['host']

            if 'port' in config['client']:
                port = int(config['client']['port'])

            return host, port
        else:
            exit(2)

    def start_chatting(self, username):
        try:
            # Fetch the host and port from the get_config function
            host, port = self.get_config()

            self.username = username
            self.sock.connect((host, port))

            # Create a thread for processing messages
            threading.Thread(target=self.receive_messages).start()

        except Exception as e:
            print(e)
            self.sock.close()


if __name__ == '__main__':
    chat_client = ChatClient()
