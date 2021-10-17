import socket
import threading
import configparser

connections = []
users = {}


def get_config() -> tuple[str, int]:
    config = configparser.ConfigParser()
    config.read('config.ini')
    port = 1234

    if 'server' in config:
        if 'port' in config['server']:
            port = int(config['server']['port'])

    server = ''
    return server, port


def send_to_peers(message: str, addr: any, connection: socket.socket):
    for conn in connections:
        if conn != connection:
            formatted_message = ("%s> %s" % (users[addr[0]], message))

            try:
                conn.send(formatted_message.encode('utf-8'))

            except Exception as e:
                print(e)
                terminate_connection(conn, addr)


def handler(conn, addr):
    while True:
        try:
            data = conn.recv(1024)

            if data:
                user_message = data.decode('utf-8')
                send_to_peers(user_message, addr, conn)
            else:
                terminate_connection(conn, addr)
                break

        except Exception as e:
            print(e)
            terminate_connection(conn, None)
            break


def terminate_connection(conn: socket.socket, addr: any):
    if conn in connections:
        conn.close()
        connections.remove(conn)

        if addr:
            del users[addr[0]]


def create_server():
    server, port = get_config()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.bind((server, port))
        sock.listen(4)

        print("Server ready to connect at %s:%d" % (server, port))

        while True:
            conn, addr = sock.accept()
            conn.send("%IDENTIFY".encode('utf-8'))
            username = conn.recv(1024).decode('utf-8')

            users[addr[0]] = username
            connections.append(conn)
            print("New user connected: %s" % username)
            threading.Thread(target=handler, args=[conn, addr]).start()

    except Exception as e:
        print(e)
    finally:
        if len(connections) > 0:
            for conn in connections:
                terminate_connection(conn, addr)

        sock.close()


if __name__ == "__main__":
    create_server()
