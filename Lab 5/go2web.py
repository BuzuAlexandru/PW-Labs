import socket
from bs4 import BeautifulSoup, NavigableString
import sys
from urllib.parse import urlparse

user_agent = '\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'


def send_request(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    if parsed_url.path:
        path = parsed_url.path
    else:
        path = "/"
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(f'GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection: close{user_agent}\r\n\r\n'.encode())
    response = b''
    data = 1
    while data:
        data = sock.recv(1024)
        response += data
    sock.close()

    headers = response.split(b"\r\n\r\n")[0].decode().splitlines()

    for header in headers:
        if header.lower().startswith("location"):
            redirect_url = header.split(": ")[1]
            break

    for header in headers:
        if header.lower().startswith("content-type"):
            ctype = header.split(": ")[1]
            break
    # print(response.decode())
    return response.decode()


def get_page(url):
    res = send_request(url)
    soup = BeautifulSoup(res, 'html.parser')
    contents = soup.get_text(separator='\n\n', strip=True).strip()
    print(contents)


def google_search(search_terms):
    query = ""
    for term in search_terms:
        query += term + '+'
    url = "https://www.google.com/search?q=" + query[:-1]
    res = send_request(url)
    print(res)
    soup = BeautifulSoup(res, 'html.parser')
    print("\n Top 10 search results: \n")
    for i, result in enumerate(soup.find_all('a')[16:26], start=1):
        print(f"{i}. {result.text} - {result['href']}")


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
        google_search(search_term)

    else:
        print("Invalid argument. Use -h for a list of commands.")


if __name__ == "__main__":
    main()
