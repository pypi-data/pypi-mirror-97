import logging
import socket

from .constants import \
    SOCKET_SERVER, \
    SOCKET_MAX_CONNECTIONS

logging.getLogger().setLevel(logging.INFO)


class SocketServer:
    def __init__(self, is_parallel: bool = False):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_parallel = is_parallel
        self.connect()

    def connect(self):
        logging.info('Connecting to %s', SOCKET_SERVER)
        # Set socket reuse timeout to 0
        if self.is_parallel:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(SOCKET_SERVER)
        self.socket.listen(SOCKET_MAX_CONNECTIONS)
        logging.info('Listening...')

    def accept(self):
        return self.socket.accept()

    def sendall(self, buffer: bytes):
        return self.socket.sendall(buffer)

    def close(self):
        return self.socket.close()
