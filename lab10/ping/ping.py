import datetime
import socket
import struct
import sys


def form_packet(id, raw_data):
    data = bytes(raw_data, "utf-8")
    header = struct.pack('bbHHh', 8, 0, 0, id, 1)
    checksum = get_checksum(header + data)
    header = struct.pack('bbHHh', 8, 0, socket.htons(checksum), id, 1)
    return header + data


def get_checksum(data):
    sum = 0
    for i in range(0, len(data) - len(data) % 2, 2):
        sum += data[i + 1] * 256 + data[i]
        sum &= 0xffffffff
    if len(data) % 2 != 0:
        sum += data[-1]
        sum &= 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

# def get_checksum(source_string):
#     sum = 0
#     count_to = (len(source_string) // 2) * 2
#     count = 0
#     while count < count_to:
#         this_val = source_string[count + 1]*256+source_string[count]
#         sum = sum + this_val
#         sum = sum & 0xffffffff
#         count = count + 2
#     if count_to < len(source_string):
#         sum = sum + source_string[len(source_string) - 1]
#         sum = sum & 0xffffffff
#     sum = (sum >> 16) + (sum & 0xffff)
#     sum = sum + (sum >> 16)
#     answer = ~sum
#     answer = answer & 0xffff
#     answer = answer >> 8 | (answer << 8 & 0xff00)
#     return answer


if len(sys.argv) != 3:
    print("Provide number of requests and host name")
    sys.exit(1)

tries = int(sys.argv[1])
host_name = sys.argv[2]
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
clientSocket.settimeout(1)
host = socket.gethostbyname(host_name)
print(host)
time = 0
for i in range(tries):
    try:
        clientSocket.sendto(form_packet(1, str(datetime.datetime.now().time())), (host, i + 1))
        resp, addr = clientSocket.recvfrom(1024)
        time = datetime.datetime.now().time()
        header = resp[20:28]
        data = resp[28:]
        resp_time = datetime.datetime.strptime(data.decode('utf-8'), "%H:%M:%S.%f").time()
        # print(time, resp_time)
        print("ping")
    except Exception as e:
        print(e)
clientSocket.close()
