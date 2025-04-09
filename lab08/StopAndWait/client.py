import sys
import socket
from control import get_sum, check_sum, K


def modify_message(msg, num, end):
    msg = list(map(int, ''.join(list(map(lambda x: bin(x)[2:].rjust(8, '0'), msg)))))
    msg = [num, int(end)] + msg
    s = get_sum(msg)
    add_data = list(map(int, bin(s)[2:].rjust(K, '0')))
    return add_data + msg


if len(sys.argv) != 2:
    print("Set timeout")
    sys.exit(1)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
f = open("example.png", "rb")
message = list(f.read())
f.close()
serverPort = 9050
timeout = int(sys.argv[1])
block_size = (1024 - K - 2) // 8
num = 0
block_index = 0

while block_index < len(message):
    print(f"{block_index}/{len(message)}")
    msg = modify_message(message[block_index: block_index + block_size], num, block_index + block_size >= len(message))
    clientSocket.sendto(bytearray(msg), ('localhost', serverPort))
    clientSocket.settimeout(timeout)
    try:
        while True:
            resp, serverAddress = clientSocket.recvfrom(2048)
            resp = list(resp)
            if len(resp) < K + 1:
                continue
            s = int(''.join(map(str, resp[:K])), 2)
            if not check_sum(resp[K:], s):
                continue
            n = resp[K]
            if n != num:
                continue
            num ^= 1
            block_index += block_size
            break
    except:
        continue
clientSocket.close()