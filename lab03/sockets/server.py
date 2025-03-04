import socket
import sys
import pathlib
import _thread
import threading
from collections import deque


def connection():
    global requests_queue, queue_lock, queue_cond
    while True:
        queue_lock.acquire()
        while len(requests_queue) == 0:
            queue_cond.wait()
        connectionSocket, addr = requests_queue.popleft()
        queue_lock.release()
        content = connectionSocket.recv(1024).decode('utf-8')
        filename = find_filename(content)
        if filename.exists() and filename.is_file():
            file = open(filename, 'rb')
            file_bytes = file.read()
            file.close()
            response = form_correct_http(file_bytes, str(filename).split('.')[-1])
        else:
            response = form_bad_http()
        connectionSocket.send(response)
        connectionSocket.close()


def find_filename(http_text):
    first_line = http_text.split('\n')[0]
    return pathlib.Path(first_line.split()[1][1:])


def form_bad_http():
    content = "HTTP/1.1 404 Not Found\r\n"
    return bytes(content, 'utf-8')


def form_correct_http(content, extencion):
    contentByExtencion = {'png': 'image/apng', 'txt': 'text/plain', 'html': 'text/html'}
    if extencion not in contentByExtencion:
        return form_correct_http(content, 'txt')
    header = "HTTP/1.1 200 OK\r\n" + \
             f"Content-Type: {contentByExtencion[extencion]}\r\n" + \
             f"Content-Length: {len(content)}\r\n" + \
             "Connection: close\r\n" + \
             "\r\n"
    return bytes(header, 'utf-8') + content


if len(sys.argv) != 3:
    print("Wrong number of arguments")
    sys.exit()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1])
max_threads = int(sys.argv[2])
serverSocket.bind(('', port))
serverSocket.listen(1)
working_threads = 0
requests_queue = deque([])
print(f'Server started on')
queue_lock = threading.Lock()
queue_cond = threading.Condition(queue_lock)
while True:
    connectionSocket, addr = serverSocket.accept()
    queue_lock.acquire()
    requests_queue.append((connectionSocket, addr))
    queue_cond.notify_all()
    queue_lock.release()
    if working_threads < max_threads:
        working_threads += 1
        _thread.start_new_thread(connection, ())
