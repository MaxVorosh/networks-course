from PyQt5.QtWidgets import *
from ftplib import FTP
import sys
import io
import pathlib


class ConnectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.padding = 10
        self.w = 330
        self.errorRoomH = 20
        self.h = 90
        self.allH = self.errorRoomH + self.h + 2 * self.padding

        self.move(800, 400)
        self.setFixedSize(self.w, self.allH)
        self.setWindowTitle('ftp client')

        self.editH = (self.h - 3 * self.padding) // 2
        self.editW = (self.w - 3 * self.padding) // 2

        self.userEdit = QTextEdit('', self)
        self.userEdit.setGeometry(self.padding, self.padding, self.editW, self.editH)
        self.userEdit.setPlaceholderText('Enter users name')

        self.serverEdit = QTextEdit('', self)
        self.serverEdit.setGeometry(2 * self.padding + self.editW, self.padding, self.editW, self.editH)
        self.serverEdit.setPlaceholderText('Enter server address')

        self.passwordEdit = QTextEdit('', self)
        self.passwordEdit.setGeometry(self.padding, 2 * self.padding + self.editH, self.editW, self.editH)
        self.passwordEdit.setPlaceholderText('Enter password')

        self.connect = QPushButton('Connect', self)
        self.connect.setGeometry(2 * self.padding + self.editW, 2 * self.padding + self.editH, self.editW, self.editH)
        self.connect.clicked.connect(self.makeConnection)

        self.error = QLabel('', self)
        self.error.setGeometry(self.padding, self.h + self.padding, self.w - 2 * self.padding, self.errorRoomH)

    def makeConnection(self):
        try:
            server = self.serverEdit.toPlainText()
            user = self.userEdit.toPlainText()
            pswd = self.passwordEdit.toPlainText()
            self.ftp = FTP(server)
            self.ftp.login(user, pswd)
            self.worker = Worker(self.ftp)
            self.worker.show()
            self.close()
        except Exception as e:
            self.error.setText(str(e))


class Worker(QWidget):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.files = []
        self.initUI()

    def initUI(self):
        self.padding = 10
        self.w = 500
        self.h = 500
        self.buttonH = 150
        self.errorH = 20
        self.allH = self.h + 3 * self.padding + self.buttonH + self.errorH

        self.move(800, 200)
        self.setFixedSize(self.w, self.allH)
        self.setWindowTitle('ftp client')

        filesNames = self.getFilesList()
        self.filesLbl = QTextEdit('', self)
        self.filesLbl.setPlainText(filesNames)
        self.filesLbl.setReadOnly(True)
        self.showerW = self.w - 2 * self.padding
        self.showerH = self.h - 2 * self.padding
        self.filesLbl.setGeometry(self.padding, self.padding, self.showerW, self.showerH)

        self.btnH = (self.buttonH - 2 * self.padding) // 2
        self.btnW = (self.w - 5 * self.padding) // 4

        self.create = QPushButton('Create', self)
        self.create.setGeometry(self.padding, self.padding + self.h, self.btnW, self.btnH)
        self.create.clicked.connect(self.createFile)

        self.retreive = QPushButton('Retreive', self)
        self.retreive.setGeometry(2 * self.padding + self.btnW, self.padding + self.h, self.btnW, self.btnH)
        self.retreive.clicked.connect(self.retreiveFile)

        self.update = QPushButton('Update', self)
        self.update.setGeometry(3 * self.padding + 2 * self.btnW, self.padding + self.h, self.btnW, self.btnH)
        self.update.clicked.connect(self.updateFile)

        self.delete = QPushButton('Delete', self)
        self.delete.setGeometry(4 * self.padding + 3 * self.btnW, self.padding + self.h, self.btnW, self.btnH)
        self.delete.clicked.connect(self.deleteFile)

        self.disconnectBtn = QPushButton('Disconnect', self)
        self.disconnectBtn.setGeometry(3 * self.padding + 2 * self.btnW, self.h + 2 * self.padding + self.btnH,
                                       2 * self.btnW, self.btnH)
        self.disconnectBtn.clicked.connect(self.disconnect)

        self.filenameEdit = QTextEdit('', self)
        self.filenameEdit.setPlaceholderText('Enter filename')
        self.filenameEdit.setGeometry(self.padding, self.h + 2 * self.padding + self.btnH, 2 * self.btnW, self.btnH)

        self.errorLbl = QLabel('', self)
        self.errorLbl.setGeometry(self.padding, self.allH - self.errorH - self.padding, self.w - 2 * self.padding,
                                  self.errorH)

    def process_dirs(self, path, dirs):
        for dir in dirs:
            self.connection.cwd(dir)
            entities = []
            self.connection.retrlines('LIST', entities.append)
            Q = []
            for file in entities:
                filename = file.split()[-1]
                if file[0] == 'd':
                    Q.append(filename)
                else:
                    self.files.append(str(path / dir / filename))
            self.process_dirs(path / dir, Q)
            self.connection.cwd('./..')

    def read_file(self, filename):
        parts = filename.split('\\')
        filename = parts[-1]
        content = []
        for p in parts[:-1]:
            self.connection.cwd(p)
        self.connection.retrlines(f'RETR {filename}', content.append)
        for _ in parts[:-1]:
            self.connection.cwd('./..')
        return '\n'.join(content)


    def getFilesList(self):
        self.files = []
        self.process_dirs(pathlib.Path('.'), ['.'])
        return '\n'.join(self.files)

    def check(self, filename):
        return '..' not in filename and pathlib.Path(filename).stem != ''

    def createFile(self):
        self.errorLbl.setText('')
        filename = self.filenameEdit.toPlainText()
        if not self.check(filename):
            self.error('Bad file name')
            return
        self.ew = FileWindow('', filename, self.connection, True)
        self.ew.show()
        self.close()

    def retreiveFile(self):
        self.errorLbl.setText('')
        filename = self.filenameEdit.toPlainText()
        if not self.check(filename):
            self.error('Bad file name')
            return
        if filename not in self.files:
            self.error('Not such file')
            return
        content = self.read_file(filename)
        self.sw = FileWindow(content, filename, self.connection, False)
        self.sw.show()
        self.close()

    def updateFile(self):
        self.errorLbl.setText('')
        filename = self.filenameEdit.toPlainText()
        if not self.check(filename):
            self.error('Bad file name')
            return
        if filename not in self.files:
            self.error('Not such file')
            return
        content = self.read_file(filename)
        self.ew = FileWindow(content, filename, self.connection, True)
        self.ew.show()
        self.close()

    def deleteFile(self):
        self.errorLbl.setText('')
        filename = self.filenameEdit.toPlainText()
        if not self.check(filename):
            self.error('Bad file name')
            return
        if filename not in self.files:
            self.error('Not such file')
            return
        parts = filename.split('\\')
        filename = parts[-1]
        for p in parts[:-1]:
            self.connection.cwd(p)
        self.connection.delete(filename)
        for _ in parts[:-1]:
            self.connection.cwd('./..')

        text = self.getFilesList()  # Maybe there is another update other than deleting
        self.filesLbl.setPlainText(text)

    def disconnect(self):
        self.connector = ConnectWindow()
        self.connector.show()
        self.connection.close()
        self.close()

    def error(self, msg):
        self.errorLbl.setText(msg)


class FileWindow(QWidget):
    def __init__(self, initialText, filename, connection, edible):
        super().__init__()
        self.text = initialText
        self.filename = filename
        self.connection = connection
        self.edible = edible
        self.initUI()

    def initUI(self):
        self.w = 500
        self.h = 500
        self.lblH = 20
        self.padding = 10
        self.lblW = (self.w - 4 * self.padding) // 3
        self.editH = self.h - self.lblH - 3 * self.padding

        self.move(800, 400)
        self.setFixedSize(self.w, self.h)
        self.setWindowTitle('ftp client')

        self.lbl = QLabel(f'File: {self.filename}', self)
        self.lbl.setGeometry(self.padding, self.padding, self.lblW, self.lblH)

        self.saveButton = QPushButton('Save', self)
        self.saveButton.setGeometry(2 * self.padding + self.lblW, self.padding, self.lblW, self.lblH)
        self.saveButton.clicked.connect(self.save)

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.setGeometry(3 * self.padding + 2 * self.lblW, self.padding, self.lblW, self.lblH)
        self.exitButton.clicked.connect(self.exit)

        self.editSpace = QTextEdit(self.text, self)
        self.editSpace.setPlaceholderText('Edit file here')
        self.editSpace.setGeometry(self.padding, self.lblH + 2 * self.padding, self.w - 2 * self.padding, self.editH)
        self.editSpace.setReadOnly(not self.edible)

    def save(self):
        parts = self.filename.split('\\')
        filename = parts[-1]
        for p in parts[:-1]:
            self.connection.cwd(p)

        file = io.BytesIO()
        file_wrapper = io.TextIOWrapper(file, encoding='utf-8')
        file_wrapper.write(self.editSpace.toPlainText())
        file_wrapper.seek(0)
        self.connection.storbinary(f'STOR {filename}', file)
        for _ in parts[:-1]:
            self.connection.cwd('./..')
        self.exit()

    def exit(self):
        self.worker = Worker(self.connection)
        self.worker.show()
        self.close()


app = QApplication(sys.argv)
cw = ConnectWindow()
cw.show()
sys.exit(app.exec())
