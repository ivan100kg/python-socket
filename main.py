import socket
from views import *

URLS = {
    '/': index,
    '/blog': blog,
}


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return method, url


def generate_headers(method, url):
    if method != 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405
    if url not in URLS:
        return 'HTTP/1.1 404 Not found\n\n', 404
    return 'HTTP/1.1 200 OK\n\n', 200


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)
    return (headers + body).encode('utf-8')


def main():
    listening_address = ('localhost', 5800)  # IP, port
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP, IPv4
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse addr True
    server_sock.bind(listening_address)
    server_sock.listen()

    # get messages from client and send response back
    while True:
        client_sock, client_address = server_sock.accept()
        request = client_sock.recv(1024)  # receive buffer in bytes
        response = generate_response(request.decode('utf-8'))
        client_sock.sendall(response)
        client_sock.close()


if __name__ == '__main__':
    main()
