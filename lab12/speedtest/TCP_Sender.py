from BaseSenderForm import BaseSenderForm
import socket


class SenderTCP(BaseSenderForm):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TCP sender')

    def makeSocket(self):
        pass

    def sendMessage(self, msg):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = self.edits[0].toPlainText(), int(self.edits[1].toPlainText())
        self.clientSocket.connect((host, port))
        self.clientSocket.send(msg)
        self.clientSocket.close()