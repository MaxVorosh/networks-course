import sys
import socket
from control import get_sum, check_sum, K


def modify_message(msg, num, end):
    msg = [num, int(end)] + msg
    s = get_sum(msg)
    add_data = [s // 256, s % 256]
    return add_data + msg


if len(sys.argv) != 2:
    print("Set timeout")
    sys.exit(1)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
f = open("example.png", "rb")
message = list(f.read())
f.close()
serverPort = 9050
timeout = float(sys.argv[1])
N = K // 8
block_size = 1024 - N - 2
num = 0
block_index = 0
data = []

while block_index < len(message):
    print(f"{block_index}/{len(message)}")
    msg = modify_message(message[block_index: block_index + block_size], num, block_index + block_size >= len(message))
    clientSocket.sendto(bytearray(msg), ('localhost', serverPort))
    clientSocket.settimeout(timeout)
    try:
        while True:
            resp, serverAddress = clientSocket.recvfrom(2048)
            resp = list(resp)
            if len(resp) < N + 1:
                print("Format error")
                continue
            s = resp[0] * 256 + resp[1]
            if not check_sum(resp[N:], s):
                print("Wrong sum")
                continue
            n = resp[N]
            if n != num:
                print("Wrong ack number")
                continue
            num ^= 1
            block_index += block_size
            data += resp[N + 1:]
            break
    except:
        print("Timeout")

clientSocket.sendto(bytearray([0]), ('localhost', serverPort))
clientSocket.close()

f = open("received.txt", "wb")
f.write(bytearray(data))
f.close()
