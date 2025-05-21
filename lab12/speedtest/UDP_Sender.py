from BaseSenderForm import BaseSenderForm
import socket


class SenderUDP(BaseSenderForm):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UDP sender')

    def makeSocket(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendMessage(self, msg):
        host, port = self.edits[0].toPlainText(), int(self.edits[1].toPlainText())
        self.clientSocket.sendto(msg, (host, port))