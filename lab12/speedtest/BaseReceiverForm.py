from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEvent
from threading import Thread
import datetime
from abc import abstractmethod


class UpdateEvent(QEvent):
    EventType = QEvent.User + 1

    def __init__(self, seconds, bytes, realBytes):
        super().__init__(UpdateEvent.EventType)
        self.seconds = seconds
        self.bytes = bytes
        self.realBytes = realBytes


class BaseReceiverForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.working = False

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
        self.btnY = 5 * self.stepY + 4 * self.lblSizeY
        h = 6 * self.stepY + 4 * self.lblSizeY + self.btnSizeY

        self.setFixedSize(w, h)
        self.move(200, 200)

        lblTexts = ['IP address', 'Port', 'Speed', 'Number of bytes received']
        self.labels = []
        self.edits = []
        for i in range(len(lblTexts)):
            self.labels.append(QLabel(self))
            y = self.lblY + i * (self.stepY + self.lblSizeY)
            self.labels[-1].setGeometry(self.lblX, y, self.lblSizeX, self.lblSizeY)
            self.labels[-1].setText(lblTexts[i])
            self.edits.append(QTextEdit(self))
            self.edits[-1].setGeometry(self.editX, y, self.editSizeX, self.editSizeY)
            if i >= 2:
                self.edits[-1].setReadOnly(True)
        self.btn = QPushButton(self)
        self.btn.setGeometry(self.btnX, self.btnY, self.btnSizeX, self.btnSizeY)
        self.btn.setText('Start')
        self.btn.clicked.connect(self.startServer)

    def startServer(self):
        if self.working:
            return
        try:
            addr, port = self.edits[0].toPlainText(), int(self.edits[1].toPlainText())
            self.serverSocket = self.makeSocket(addr, port)
            self.socketThread = Thread(target=self.processSocket)
            self.socketThread.start()
        except Exception as e:
            print(e)

    @abstractmethod
    def makeSocket(self, addr, port):
        pass

    def processSocket(self):
        self.working = True
        microseconds = 0
        nBytes = 0
        while self.working:
            time = datetime.datetime.now()
            try:
                body = self.getBody()
            except:
                continue
            if len(body) > 3 and body[:3] == bytes("END", "utf-8"):
                realBytes, dateStr, timeStr = body[3:].decode("utf-8").split()
                sentTime = datetime.datetime.strptime(dateStr + ' ' + timeStr, "%Y-%m-%d %H:%M:%S.%f")
                microseconds += (time - sentTime).microseconds
                QApplication.postEvent(self, UpdateEvent(microseconds, nBytes, int(realBytes)))
                microseconds = 0
                nBytes = 0
            else:
                nBytes += len(list(body))
        self.working = False

    @abstractmethod
    def getBody(self):
        pass

    def printStat(self, microseconds, bytes, sentBytes):
        speed = 0
        if microseconds > 0:
            speed = bytes * 1000 / microseconds
        self.edits[-2].setText(f"{speed} B/s")
        self.edits[-1].setText(f"{bytes}/{sentBytes}")

    def exit(self):
        if self.working:
            self.working = False
            self.socketThread.join()
        self.serverSocket.close()
        self.close()

    def event(self, event):
        if event.type() == UpdateEvent.EventType:
            self.printStat(event.seconds, event.bytes, event.realBytes)
            return True
        return super().event(event)

    def closeEvent(self, event):
        self.exit()
