import socket
import random
import threading
from control import check_sum, get_sum, K


def gen_ack_msg(num, message):
    message = [num] + list(message)
    s = get_sum(message)
    header = [s // 256, s % 256]
    header += message
    return header


f = open("example.txt", "rb")
content = list(f.read())
f.close()
block_size = 8
N = K // 8

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9050
serverSocket.bind(('localhost', port))
clientsLock = threading.Lock()
aliveClients = {}
running = True
data = []
last_num = -1
cnt = 0
while running:
    message, client_address = serverSocket.recvfrom(1024)
    if random.random() < 0.3:
        continue
    message = list(message)
    if len(message) < N + 3:
        continue
    s = message[0] * 256 + message[1]
    if not check_sum(message[N:], s):
        continue
    num = message[N]
    if num != last_num:
        if cnt < len(content) and last_num != -1:
            cnt = min(cnt + block_size, len(content))
        data += message[N + 2:]
        last_num = num
    to_send = []
    if cnt < len(content):
        to_send = content[cnt: cnt + block_size]
    running = message[N + 1] == 0
    ack_msg = gen_ack_msg(num, to_send)
    print(f"Ack {num} {cnt}/{len(content)}")
    if random.random() < 0.3:
        continue
    serverSocket.sendto(bytearray(ack_msg), client_address)

while True:
    message, client_address = serverSocket.recvfrom(1024)
    if len(message) == 1 and message[0] == 0:
        break
    ack_msg = gen_ack_msg(last_num, [])
    serverSocket.sendto(bytearray(ack_msg), client_address)
serverSocket.close()

rec = open("received.png", "wb")
rec.write(bytearray(data))
rec.close()
