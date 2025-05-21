from PyQt5.QtWidgets import QApplication
from TCP_Receiver import ReceiverTCP
import sys

app = QApplication(sys.argv)
rf = ReceiverTCP()
rf.show()
sys.exit(app.exec())
