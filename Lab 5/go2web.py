import socket
from bs4 import BeautifulSoup


def send_request(host, link):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 80
    sock.connect((host, port))
    sock.send(f'GET {link} HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n'.encode())
    response = sock.recv(4096)
    sock.close()
    return BeautifulSoup(response.decode(), 'html.parser')


print(send_request('example.com', '/'))
