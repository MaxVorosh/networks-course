import sys
import socket
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QPoint, QThread, pyqtSignal


class SocketThread(QThread):
    result_ready = pyqtSignal((int, int, int, int))

    def __init__(self, addr, port):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((addr, port))

    def run(self):
        while True:
            resp, addr = self.socket.recvfrom(1024)
            from_x, from_y, to_x, to_y = resp.decode('utf-8').split(' ')
            self.result_ready.emit(int(from_x), int(from_y), int(to_x), int(to_y))


class Server(QWidget):
    def __init__(self, addr, port):
        super().__init__()
        self.setWindowTitle('Server')
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.brushSize = 2
        self.brushColor = Qt.black
        self.socketThread = SocketThread(addr, port)
        self.socketThread.result_ready.connect(self.paint)
        self.socketThread.start()

    def paint(self, from_x, from_y, to_x, to_y):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(QPoint(from_x, from_y), QPoint(to_x, to_y))

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())


if len(sys.argv) != 3:
    print("Provide address and port")
    sys.exit(1)
app = QApplication([])
s = Server(sys.argv[1], int(sys.argv[2]))
s.show()
sys.exit(app.exec())