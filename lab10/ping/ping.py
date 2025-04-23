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
time = 0
min_rtt = 1000
max_rtt = 0
lost = 0
sum_rtt = 0
for i in range(tries):
    try:
        clientSocket.sendto(form_packet(1, str(datetime.datetime.now())), (host, i + 1))
        resp, addr = clientSocket.recvfrom(1024)
        time = datetime.datetime.now()
        header = resp[20:28]
        data = resp[28:]
        resp_time = datetime.datetime.strptime(data.decode('utf-8'), "%Y-%m-%d %H:%M:%S.%f")
        diff = time - resp_time
        rtt = diff.microseconds / 1000
        min_rtt = min(min_rtt, rtt)
        max_rtt = max(max_rtt, rtt)
        sum_rtt += rtt
        print("ping")
    except Exception as e:
        lost += 1
        print(e)
    print(f"Min rtt: {min_rtt}ms")
    print(f"Max rtt: {max_rtt}ms")
    print(f"Avg rtt: {sum_rtt / (i + 1)}ms")
    print(f"Lost: {lost / (i + 1) * 100}%")
clientSocket.close()
