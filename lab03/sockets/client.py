import pathlib
import socket
import sys


def make_request(filename, host, port):
    request = f"GET /{filename} HTTP/1.1\r\n" + \
              f"Host: {host}:{port}\r\n"
    return request


if len(sys.argv) != 4:
    print("Wrong number of arguments")
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])
filename = sys.argv[3]
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))
requestContent = make_request(filename, host, port)
clientSocket.send(bytes(requestContent, 'utf-8'))
responseContent = clientSocket.recv(1024)
print(responseContent)
