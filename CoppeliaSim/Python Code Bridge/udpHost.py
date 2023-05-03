# This python script listens on UDP port 3333
# for messages from the ESP32 board and prints them
import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error as msg:
    print('Failed to create socket. Error Code : ' + str(msg.errno) + ' Message ' + msg.strerror)
    sys.exit()

try:
    s.bind(('', 3333))
except socket.error as msg:
    print('Bind failed. Error: ' + str(msg.errno) + ': ' + msg.strerror)
    sys.exit()

print('Server listening')

while True:
    d = s.recvfrom(1024)
    data = d[0]

    if not data:
        break

    print(data.decode().strip())

s.close()
