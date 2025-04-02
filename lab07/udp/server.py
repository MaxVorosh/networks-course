import socket
import random
import time

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9050
serverSocket.bind(('localhost', port))
while True:
    message, client_address = serverSocket.recvfrom(1024)
    modifiedMessage = message.upper()
    time.sleep(random.random() / 10)  # To check correct time measurement
    if random.random() > 0.2:
        serverSocket.sendto(modifiedMessage, client_address)