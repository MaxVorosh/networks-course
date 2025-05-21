import datetime
import random
from PyQt5.QtWidgets import *
from abc import abstractmethod


class BaseSenderForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.makeSocket()

    def initUI(self):
        w = 400
        self.lblX = 10
        self.editX = w // 2 + self.lblX
        self.lblSizeX = self.editSizeX = w // 2 - 2 * self.lblX
        self.lblY = 10
        self.stepY = 10
        self.lblSizeY = self.editSizeY = self.btnSizeY = 30
        self.btnSizeX = 80
        self.btnX = (w - self.btnSizeX) // 2
        self.btnY = 4 * self.stepY + 3 * self.lblSizeY
        h = 5 * self.stepY + 3 * self.lblSizeY + self.btnSizeY

        self.setFixedSize(w, h)
        self.move(200, 200)

        lblTexts = ['Receiver IP address', 'Receiver port', 'Number of bytes to send']
        self.labels = []
        self.edits = []
        for i in range(len(lblTexts)):
            self.labels.append(QLabel(self))
            y = self.lblY + i * (self.stepY + self.lblSizeY)
            self.labels[-1].setGeometry(self.lblX, y, self.lblSizeX, self.lblSizeY)
            self.labels[-1].setText(lblTexts[i])
            self.edits.append(QTextEdit(self))
            self.edits[-1].setGeometry(self.editX, y, self.editSizeX, self.editSizeY)
        self.btn = QPushButton(self)
        self.btn.setGeometry(self.btnX, self.btnY, self.btnSizeX, self.btnSizeY)
        self.btn.setText('Send')
        self.btn.clicked.connect(self.send)

    @abstractmethod
    def makeSocket(self):
        pass

    def send(self):
        time = datetime.datetime.now()
        bytesToSend = bytes([random.randint(0, 255) for _ in range(int(self.edits[-1].toPlainText()))])
        self.sendMessage(bytesToSend)
        self.sendMessage(bytes(f"END{len(bytesToSend)} {str(time)}", "utf-8"))

    @abstractmethod
    def sendMessage(self, msg):
        pass