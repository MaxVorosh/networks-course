import os
import socket


def get_response(content):
    try:
        return os.popen(content).read()
    except Exception:
        return "Error in executing command"


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8000
serverSocket.bind(('localhost', port))
serverSocket.listen(1)
while True:
    connectionSocket, addr = serverSocket.accept()
    content = connectionSocket.recv(1024).decode('utf-8')
    print(f"New command {content}")
    response_content = get_response(content)
    connectionSocket.send(bytes(response_content, 'utf-8'))
    connectionSocket.close()
