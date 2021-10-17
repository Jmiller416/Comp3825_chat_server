import socket
import threading
import configparser
import shortuuid
import os
PROMPT = '(you)> '
CONNECTED = False


def get_config() -> tuple[str, int, str]:
    global PROMPT

    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'client' in config:
        host = '0.0.0.0'
        port = 1234
        username = shortuuid.uuid()

        if 'host' in config['client']:
            host = config['client']['host']

        if 'port' in config['client']:
            port = int(config['client']['port'])

        if 'username' in config['client']:
            username = config['client']['username']

        PROMPT = ("%s (you)> " % username)
        return host, port, username
    else:
        exit(2)


def create_client():
    global CONNECTED

    # Create the socket instance for use later
    sock = socket.socket()

    try:
        # Fetch the host and port from the get_config function
        host, port, username = get_config()

        sock.connect((host, port))

        # Create a thread for processing messages
        threading.Thread(target=receive_messages, args=[sock, username]).start()

        while CONNECTED:
            next_message = input(PROMPT)

            if next_message == '.quit' or next_message == '.exit':
                sock.send("has disconnected".encode('utf-8'))
                CONNECTED = False
                break

            sock.send(next_message.encode())

        # Close the socket when we're done
        os.close(sock.fileno())

    except Exception as err:
        print(err)
        os.close(sock.fileno())


def receive_messages(conn: socket.socket, username: str):
    global CONNECTED

    CONNECTED = True

    while CONNECTED:
        try:
            last_data = conn.recv(1024)

            if last_data:
                last_message = last_data.decode('utf-8')
                if last_message == '%IDENTIFY':
                    conn.send(username.encode('utf-8'))
                else:
                    print('\r' + last_message + '\n' + PROMPT, end='')
            else:
                os.close(conn.fileno())
                break

        except Exception as err:
            print(err)
            break


if __name__ == '__main__':
    create_client()
