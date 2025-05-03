import sys
import socket
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QImage
from PyQt5.QtCore import Qt


class Client(QWidget):
    def __init__(self, addr, port):
        super().__init__()
        self.setWindowTitle('Client')
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.point = None
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = addr
        self.port = port

    def mousePressEvent(self, event):
        self.point = event.pos()
        self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.point, event.pos())
            self.send(self.point, event.pos())
            self.point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.point = None

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def send(self, pointFrom, pointTo):
        content = f"{pointFrom.x()} {pointFrom.y()} {pointTo.x()} {pointTo.y()}"
        self.socket.sendto(bytes(content, 'utf-8'), (self.addr, self.port))


if len(sys.argv) != 3:
    print("Provide address and port")
    sys.exit(1)
app = QApplication([])
s = Client(sys.argv[1], int(sys.argv[2]))
s.show()
sys.exit(app.exec())