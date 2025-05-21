from BaseReceiverForm import BaseReceiverForm
import socket


class ReceiverUDP(BaseReceiverForm):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UDP receiver')

    def makeSocket(self, addr, port):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.settimeout(1)
        serverSocket.bind((addr, port))
        return serverSocket

    def getBody(self):
        body, addr = self.serverSocket.recvfrom(1024)
        return body

