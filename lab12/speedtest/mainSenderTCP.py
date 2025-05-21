from PyQt5.QtWidgets import QApplication
from TCP_Sender import SenderTCP
import sys

app = QApplication(sys.argv)
sf = SenderTCP()
sf.show()
sys.exit(app.exec())
