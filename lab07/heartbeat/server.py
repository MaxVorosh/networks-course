import socket
import random
import time
import threading
import sys


def delete_client(addr):
    clientsLock.acquire()
    aliveClients[addr].timer.cancel()
    aliveClients.pop(addr)
    print(f"Client {addr} is now dead")
    clientsLock.release()


class ClientInfo:
    def __init__(self, package, curTime, timeout, address):
        self.package = package
        self.lastTime = curTime
        self.timeout = timeout
        self.address = address
        self.createTimer()

    def createTimer(self):
        self.timer = threading.Timer(self.timeout, delete_client, [self.address])
        self.timer.start()

    def reloadTimer(self):
        self.timer.cancel()
        self.createTimer()

    def update(self, package, curTime):
        packDiff = package - self.package
        timeDiff = curTime - self.lastTime
        self.package = package
        self.lastTime = curTime
        self.reloadTimer()
        return packDiff, timeDiff


if len(sys.argv) != 2:
    print("Provide timeout")
    sys.exit(1)

timeout = int(sys.argv[1])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9050
serverSocket.bind(('localhost', port))
clientsLock = threading.Lock()
aliveClients = {}
while True:
    message, client_address = serverSocket.recvfrom(1024)
    time.sleep(random.random() / 10)  # To check correct time measurement
    if random.random() < 0.2:
        continue
    n, curTime = message.decode('utf-8').split()
    n = int(n)
    curTime = float(curTime)
    clientsLock.acquire()
    if client_address in aliveClients:
        packDiff, timeDiff = aliveClients[client_address].update(n, curTime)
        print(f"Message from {client_address} after {timeDiff}s. Lost {packDiff - 1} packages")
    else:
        aliveClients[client_address] = ClientInfo(n, curTime, timeout, client_address)
        print(f"New client {client_address}")

    clientsLock.release()