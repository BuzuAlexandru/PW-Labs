import socket
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse


def send_request(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(f'GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n'.encode())
    response = b''
    data = 1
    while data:
        data = sock.recv(1024)
        response += data
    sock.close()
    return BeautifulSoup(response.decode(), 'html.parser').body.get_text()


def get_page(url):
    print(send_request(url))
    ...


def google_search(url):
    ...


def main():
    if len(sys.argv) == 1 or sys.argv[1] == "-h":
        print(
            '''
go2web -u <URL>         # make an HTTP request to the specified URL and print the response
go2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results
go2web -h               # show this help
            '''
        )
        sys.exit(0)

    if sys.argv[1] == "-u":
        if len(sys.argv) != 3:
            print("Command 'go2web -u <URL>' expects a single URL containing to space characters")
            sys.exit(1)
        url = sys.argv[2]
        get_page(url)

    elif sys.argv[1] == "-s":
        if len(sys.argv) == 2:
            print("Command 'go2web -s <search-term>' expects at least a single search term")
            sys.exit(1)
        search_term = tuple(sys.argv[2:])
        print(search_term)
        google_search(search_term)

    else:
        print("Invalid argument. Use -h for a list of commands.")


if __name__ == "__main__":
    main()
