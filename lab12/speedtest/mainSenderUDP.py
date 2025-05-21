from PyQt5.QtWidgets import QApplication
from UDP_Sender import SenderUDP
import sys

app = QApplication(sys.argv)
sf = SenderUDP()
sf.show()
sys.exit(app.exec())
