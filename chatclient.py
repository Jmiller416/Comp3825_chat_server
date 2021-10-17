import socket
import threading
import configparser
import shortuuid

PROMPT = '(you)> '


def get_config() -> tuple[str, int, str]:
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

        return host, port, username
    else:
        exit(2)


def create_client():
    # Create the socket instance for use later
    sock = socket.socket()

    try:
        # Fetch the host and port from the get_config function
        host, port, username = get_config()

        sock.connect((host, port))

        # Create a thread for processing messages
        threading.Thread(target=receive_messages, args=[sock, username]).start()

        while True:
            next_message = input(PROMPT)

            if next_message == 'quit' or next_message == 'exit':
                break

            sock.send(next_message.encode())

        # Close the socket when we're done
        sock.close()

    except Exception as e:
        print(e)
        sock.close()


def receive_messages(conn: socket.socket, username: str):
    while True:
        try:
            last_data = conn.recv(1024)

            if last_data:
                last_message = last_data.decode('utf-8')
                if last_message == '%IDENTIFY':
                    conn.send(username.encode('utf-8'))
                else:
                    print('\r' + last_message + '\n' + PROMPT, end='')
            else:
                conn.close()
                break

        except Exception as err:
            print(err)
            conn.close()
            break


if __name__ == '__main__':
    create_client()
