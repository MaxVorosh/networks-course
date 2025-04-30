import socket
import sys


if len(sys.argv) != 2:
    print("Wrong number of arguments")
    sys.exit()

serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
port = int(sys.argv[1])
serverSocket.bind(('', port))
serverSocket.listen(10)
while True:
    connectionSocket, addr = serverSocket.accept()
    content = connectionSocket.recv(1024).decode('utf-8')
    response = content.upper()
    connectionSocket.send(bytes(response, 'utf-8'))