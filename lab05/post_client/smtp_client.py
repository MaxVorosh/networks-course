import sys
import socket
from password import PASSWORD
import base64
import ssl


def check(smtp_socket, code):
    resp = smtp_socket.recv(1024).decode('utf-8')
    if resp[:3] != str(code):
        print(f'Expected code {code}, get {resp[:3]}')
        smtp_socket.close()
        sys.exit()


def send_and_check(smtp_socket, content, code, is_b64=False):
    if is_b64:
        content = base64.b64encode(bytes(content, 'utf-8')).decode('utf-8') + '\r\n'
    print(content)
    smtp_socket.send(bytes(content, 'utf-8'))
    check(smtp_socket, code)


if len(sys.argv) != 4:
    print("Wrong amount of arguments")
    sys.exit()

addr = sys.argv[1]
content = sys.argv[2]
type = sys.argv[3]
my_addr = 'ma.voroshilov2004@gmail.com'

if type not in ['html', 'text', 'image']:
    print('type should be html ot text')
    sys.exit()

content_type = 'text/plain'
if type == 'html':
    f = open(content)
    content = f.read()
    f.close()
    content_type = 'text/html'
if type == 'image':
    content_type = 'application/octet-stream'

raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname('smtp.gmail.com')
port = 587
raw_socket.connect((host, port))
check(raw_socket, 220)
send_and_check(raw_socket, f"HELO localhost\r\n", 250)
send_and_check(raw_socket, 'STARTTLS\r\n', 220)
smtp_socket = ssl.wrap_socket(raw_socket)
send_and_check(smtp_socket, "AUTH LOGIN\r\n", 334)
send_and_check(smtp_socket, f"{my_addr}", 334, True)
send_and_check(smtp_socket, f"{PASSWORD}", 235, True)
send_and_check(smtp_socket, f"MAIL FROM: <{my_addr}>\r\n", 250)
send_and_check(smtp_socket, f"RCPT TO: <{addr}>\r\n", 250)
send_and_check(smtp_socket, "DATA\r\n", 354)
msg = [f"From: {my_addr}", f"To: {addr}", "Subject: Socket example",
       f"Content-Type: {content_type}", content, ".", ""]
if type == 'image':
    f = open(content, 'rb')
    image_content = f.read()
    f.close()
    encrypted_content = base64.b64encode(image_content).decode('utf-8')
    msg = msg[:4] + [f"Content-Disposition: attachment; filename={content}", "Content-Transfer-Encoding: base64", f"{encrypted_content}"] + msg[-2:]
msg_string = '\r\n'.join(msg)
send_and_check(smtp_socket, msg_string, 250)
send_and_check(smtp_socket, "QUIT\r\n", 221)
smtp_socket.close()