import pathlib
import socket
import sys


if len(sys.argv) != 4:
    print("Wrong number of arguments")
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])
clientSocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
clientSocket.connect((host, port))
requestContent = sys.argv[3]
clientSocket.send(bytes(requestContent, 'utf-8'))
responseContent = clientSocket.recv(1024).decode('utf-8')
print(responseContent)
