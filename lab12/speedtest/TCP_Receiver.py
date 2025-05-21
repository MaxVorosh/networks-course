from BaseReceiverForm import BaseReceiverForm
import socket


class ReceiverTCP(BaseReceiverForm):
    def __init__(self):
        super().__init__()
        self.working = False
        self.setWindowTitle('TCP receiver')

    def makeSocket(self, addr, port):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.settimeout(1)
        serverSocket.bind((addr, port))
        serverSocket.listen(10)
        return serverSocket

    def getBody(self):
        connectionSocket, addr = self.serverSocket.accept()
        body = connectionSocket.recv(1024)
        connectionSocket.close()
        return body
