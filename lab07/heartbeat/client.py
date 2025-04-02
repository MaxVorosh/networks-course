import time
import socket
import sys
import random

if len(sys.argv) != 3:
    print("Add number of messages and max time gap between them")
    sys.exit(1)

msgs = int(sys.argv[1])
gap = float(sys.argv[2])
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverPort = 9050
for i in range(msgs):
    message = f"{i} {time.time()}"
    clientSocket.sendto(bytes(message, 'utf-8'), ('localhost', serverPort))
    time.sleep(random.random() * gap)

clientSocket.close()