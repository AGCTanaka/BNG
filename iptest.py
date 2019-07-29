import socket
host = socket.gethostname()
print(host)
ip = socket.gethostbyname(host)
print(ip)
