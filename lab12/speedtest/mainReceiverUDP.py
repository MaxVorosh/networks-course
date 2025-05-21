from PyQt5.QtWidgets import QApplication
from UDP_Receiver import ReceiverUDP
import sys

app = QApplication(sys.argv)
rf = ReceiverUDP()
rf.show()
sys.exit(app.exec())
