import socket
import random
import threading
import sys
from control import check_sum, get_sum, K


def gen_ack_msg(num):
    s = get_sum([num])
    header = list(map(int, bin(s)[2:].rjust(K, '0')))
    header.append(num)
    return header


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9050
serverSocket.bind(('localhost', port))
clientsLock = threading.Lock()
aliveClients = {}
running = True
data = []
while running:
    message, client_address = serverSocket.recvfrom(1024)
    if len(message) < K + 2:
        continue
    message = list(message)
    s = int(''.join(map(str, message[:K])), 2)
    if not check_sum(message[K:], s):
        continue
    num = message[K]
    running = message[K + 1] == 0
    data += list(message[K + 1:])
    ack_msg = gen_ack_msg(num)
    print(f"Ack {num}")
    serverSocket.sendto(bytearray(ack_msg), client_address)

rec = open("received.png", "wb")
rec.write(bytearray(data))
rec.close()
