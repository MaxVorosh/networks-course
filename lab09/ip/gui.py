import threading

from PyQt5.QtWidgets import *
import sys
import socket
from enum import Enum
from threading import Thread, Timer
from PyQt5.QtCore import QTimer


class Role(Enum):
    MASTER = 0
    WORKER = 1

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.running = False
        self.broadcast_address = '255.255.255.255'
        self.broadcast_port = 65535
        self.running = False
        self.initUI()

    def initUI(self):
        cell = 30

        self.setWindowTitle('Broadcast app')
        self.setFixedSize(11 * cell, 13 * cell)
        self.move(400, 100)

        self.portField = QTextEdit('', self)
        self.portField.setPlaceholderText('port')
        self.portField.setGeometry(3 * cell, cell, 2 * cell, cell)

        self.waitField = QTextEdit('', self)
        self.waitField.setPlaceholderText('wait')
        self.waitField.setGeometry(6 * cell, cell, 2 * cell, cell)

        self.start = QPushButton('start', self)
        self.start.setGeometry(3 * cell, 5 * cell // 2, 2 * cell, cell)
        self.start.clicked.connect(self.launch)

        self.closeBtn = QPushButton('close', self)
        self.closeBtn.setGeometry(6 * cell, 5 * cell // 2, 2 * cell, cell)
        self.closeBtn.clicked.connect(self.exit)

        self.copiesLabel = QLabel('', self)
        self.copiesLabel.setGeometry(3 * cell, 5 * cell, 5 * cell, cell)

        self.addresses = QTextEdit('', self)
        self.addresses.setGeometry(3 * cell, 6 * cell, 5 * cell, 6 * cell)
        self.addresses.setReadOnly(True)

    def updateLabels(self):
        self.addresses_lock.acquire()
        self.addresses.setPlainText('\n'.join(self.connectedAddresses.keys()))
        self.copiesLabel.setText(f'Copies launched: {len(self.connectedAddresses)}')
        self.addresses_lock.release()

    def launch(self):
        self.running = True
        self.port = int(self.portField.toPlainText())
        self.wait = int(self.waitField.toPlainText())
        self.portField.setReadOnly(True)
        self.waitField.setReadOnly(True)
        self.start.setEnabled(False)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(('localhost', self.port))

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.listener.settimeout(1)
        try:
            self.listener.bind(('localhost', self.broadcast_port))
            self.role = Role.MASTER
        except:
            self.s.sendto(bytes('NEW', 'utf-8'), (self.broadcast_address, self.broadcast_port))
            self.role = Role.WORKER

        if self.role == Role.MASTER:
            self.socket_thread = Thread(target=self.do_master_routing)
            self.addresses_lock = threading.Lock()
            self.updateTimer = QTimer()
            self.updateTimer.timeout.connect(self.updateLabels)
        else:
            self.socket_thread = Thread(target=self.do_worker_routing)
            self.addresses.setPlainText("Worker Node")

        self.socket_thread.start()
        if self.role == Role.MASTER:
            self.updateTimer.start(100)

    def do_worker_routing(self):
        def ping():
            self.s.sendto(bytes('CON', 'utf-8'), (self.broadcast_address, self.broadcast_port))
            self.timer = Timer(self.wait, ping, [])
            self.timer.start()

        self.timer = Timer(self.wait, ping, [])
        self.timer.start()

    def do_master_routing(self):
        def delete_address(addr):
            if addr in self.connectedAddresses:
                self.connectedAddresses.pop(addr)

        self.connectedAddresses = {f'127.0.0.1:{self.port}': None}
        while self.running:
            try:
                message, client_address = self.listener.recvfrom(1024)
                addr = f'{client_address[0]}:{client_address[1]}'
                message = message.decode('utf-8')
                self.addresses_lock.acquire()
                if message == 'NEW':
                    self.connectedAddresses[addr] = Timer(self.wait * 3, delete_address, [addr])
                    self.connectedAddresses[addr].start()
                elif message == 'EXT':
                    delete_address(addr)
                elif message == "CON":
                    if addr in self.connectedAddresses:
                        self.connectedAddresses[addr].cancel()
                    self.connectedAddresses[addr] = Timer(self.wait * 3, delete_address, [addr])
                    self.connectedAddresses[addr].start()
                self.addresses_lock.release()
            except TimeoutError:
                pass
            # print(self.port, message, client_address, self.role)

    def exit(self):
        if not self.running:
            return
        self.running = False
        self.socket_thread.join()
        if self.role == Role.WORKER:
            self.s.sendto(bytes('EXT', 'utf-8'), (self.broadcast_address, self.broadcast_port))
            self.timer.cancel()
        self.listener.close()
        self.s.close()
        self.close()

    def closeEvent(self, event):
        self.exit()


app = QApplication(sys.argv)
cw = AppWindow()
cw.show()
sys.exit(app.exec())
