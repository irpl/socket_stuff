import socket
import select

HEADER_LENGTH = 10

IP = ""
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]

clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving


def receive_message(client_socket):
    print("4 - ENTERED receive_message()")
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        print(f"5 - RECEIVED MESSAGE: {message_header}")
        if not len(message_header):
            print("6b- CONNECTION CLOSED")
            return False

        return {'data': client_socket.recv()}

    except Exception as e:
        print(e)
        print("9 - SOMETHING IN THE TRY FAILED")
        return False


while True:
    print("1 - BEGUN")
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        print("2 - CONNECTED")
        if notified_socket == server_socket:
            print("3 - IF")
            client_socket, client_address = server_socket.accept()
            print('Accepted new connection from {}:{}'.format(*client_address))

            user = receive_message(client_socket)
            print("6 - BEFORE USER")
            if user is False:
                print("6c- CONNECTION TO {}:{} WAS DROPPED".format(*client_address))
                continue
            print("7 - AFTER USER")
            sockets_list.append(client_socket)

            clients[client_socket] = user

        else:
            message = receive_message(notified_socket)

            if message is False:
                print('Closed connection from: {}'.format(
                    clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            # f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            print(f'Received message from {user.decode("utf-8")}')

            for client_socket in clients:

                # But don't send it to sender
                if client_socket != notified_socket:
                    client_socket.send(user)

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
