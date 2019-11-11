import socket
import threading


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        try:
            self.sock.listen()
            print(f'listening on {self.host}:{self.port}')
        except Exception as e:
            print(e)
            return -1
        while True:
            client, address = self.sock.accept()
            print('accepted connection from {}:{}'.format(*address))
            client.settimeout(60)
            threading.Thread(target=self.listenToClient,
                             args=(client, address)).start()

    def listenToClient(self, client, address):
        while True:
            try:
                data = client.recv(1024)
                if data:
                    # Set the response to echo back the recieved data
                    print('got {} from {}:{}'.format(data, *address))
                    client.send(data)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                print('closing connection to {}:{}'.format(*address))
                return False


if __name__ == "__main__":
    ThreadedServer('', 8080).listen()
