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


if len(sys.argv) != 4:
    print("Provide number of hops and host name")
    sys.exit(1)

max_hops = int(sys.argv[1])
tries = int(sys.argv[2])
host_name = sys.argv[3]
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
clientSocket.settimeout(1)
host = socket.gethostbyname(host_name)
time = 0
for hop in range(max_hops):
    clientSocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, hop + 1)
    results = []
    addr = ""
    for i in range(tries):
        try:
            startTime = datetime.datetime.now()
            clientSocket.sendto(form_packet(1, str(startTime)), (host, i + 1))
            resp, addr = clientSocket.recvfrom(1024)
            addr = addr[0]
            time = datetime.datetime.now()
            header = resp[20:28]
            type, code = header[0], header[1]
            if code != 11 and code != 0:
                results.append('*')
                continue
            diff = time - startTime
            rtt = diff.microseconds / 1000
            results.append(str(rtt))
        except Exception as e:
            # print(e)
            results.append('*')
    result_addr = addr
    try: result_addr = socket.gethostbyaddr(addr)[0]
    except: pass
    print(hop, ' '.join(results), result_addr)
    if addr == host_name:
        break
clientSocket.close()
