import socket
import sys


if len(sys.argv) != 2:
    print("Wrong amount of arguments")

port = 8000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('localhost', port))
clientSocket.send(bytes(sys.argv[1], 'utf-8'))
response_content = clientSocket.recv(1024).decode('utf-8')
clientSocket.close()
print(response_content)
