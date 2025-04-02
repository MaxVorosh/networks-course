import time
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
baseMessage = "ping"
serverPort = 9050
minTime = 1
maxTime = 0
loss = 0
for i in range(1, 11):
    message = f"{i} {baseMessage}"
    clientSocket.sendto(bytes(message, 'utf-8'), ('localhost', serverPort))
    clientSocket.settimeout(1)
    startTime = time.time()
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        endTime = time.time()
        curTime = endTime - startTime
        minTime = min(minTime, curTime)
        maxTime = max(maxTime, curTime)
        print(f"Ping {i} {curTime}")
    except:
        loss += 1
        print(f"Ping {i} Request time out")
    print("-------------")
    print(f"Min time = {minTime}")
    print(f"Max time = {maxTime}")
    print(f"{loss / i * 100}% packets lost")
    print("-------------")
    print()

clientSocket.close()