import socket
import random
import threading
import sys
from control import check_sum, get_sum, K


def to_bytes(arr):
    res = []
    for i in range(0, len(arr), 8):
        res.append(int(''.join(list(map(str, arr[i: i + 8]))), 2))
    return bytearray(res)


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
last_num = -1
while running:
    message, client_address = serverSocket.recvfrom(1024)
    if random.random() < 0.3:
        continue
    if len(message) < K + 3:
        continue
    message = list(message)
    s = int(''.join(map(str, message[:K])), 2)
    if not check_sum(message[K:], s):
        continue
    num = message[K]
    if num != last_num:
        data += list(message[K + 2:])
        last_num = num
    running = message[K + 1] == 0
    ack_msg = gen_ack_msg(num)
    print(f"Ack {num}")
    if random.random() < 0.3:
        continue
    serverSocket.sendto(bytearray(ack_msg), client_address)

while True:
    message, client_address = serverSocket.recvfrom(1024)
    if len(message) == 1 and message[0] == 0:
        break
    ack_msg = gen_ack_msg(last_num)
    serverSocket.sendto(bytearray(ack_msg), client_address)
serverSocket.close()

rec = open("received.png", "wb")
rec.write(to_bytes(data))
rec.close()
