import socket
import sys


def portscan(target, port):
    global ports
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    try:
        s.connect((target, port))
        ports.append(port)
    except:
        pass
    s.close()


if len(sys.argv) != 4:
    print("Provide ip address, and range of ports")
    sys.exit(1)

ports = []
addr = sys.argv[1]
port_from = int(sys.argv[2])
port_to = int(sys.argv[3])
for port in range(port_from, port_to + 1):
    portscan(addr, port)
print('Available ports:', *ports)
