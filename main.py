import socket
from select import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5001))
server_socket.listen()

to_monitor = []
clients = []


def accept_connection(server_socket):
    client_socket, adr = server_socket.accept()
    to_monitor.append(client_socket)
    if client_socket not in clients:
        clients.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(1024)
    if request:
        response = request.decode('utf-8')
        # client_socket.send(response.encode())

        for client in clients:
            if client is client_socket:
                continue
            client.send(response.encode())

    else:
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, ready_to_write, errors = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


# def run_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     server_socket.bind(('localhost', 9002))

#     server_socket.listen()

#     while True:
#         client_socket , address = server_socket.accept()

#         while True:
#             request = client_socket.recv(1024)

#             if not request:
#                 break
#             else:
#                 a = request.decode('utf-8')
#                 response = '{}'.format(a).encode()
#                 client_socket.sendall(response)

#     client_socket.close()

to_monitor.append(server_socket)
event_loop()
