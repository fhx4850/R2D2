import socket
import threading
import asyncio


class IpTcpServer:
    def __init__(self, ip: str, port: int):
        self._serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serv_socket.bind((ip, port))
        self._URLS = {
            '/': 'index',
            '/test': 'test',
        }
        
    def run(self):
        self._serv_listen()
            
    def _serv_listen(self):
        self._serv_socket.listen()
        while True:
            client, addr = self._serv_socket.accept()
            self._client_thread(client)
            # t1 = threading.Thread(target=self._client_thread, args=(client,))
            # t1.start()
            # t1.join()

            # asyncio.run(self._client_thread(client))
            # asyncio.ensure_future(display_date(2, loop))
            
    def _create_response(self, request):
        request = request.decode('utf-8')
        method, url = self._get_url(request)
        header, code = self._create_headers(method, url)
        body = self._create_body(code, url)
        f = open('text.txt', 'r')
        a = f.read()
        f.close()
        body += a
        return (header + body).encode()
            
    def _get_url(self, request):
        parsed = request.split(' ')
        method = parsed[0]
        url = parsed[1]
        return (method, url)
    
    def _create_headers(self, method, url):
        if not method == 'GET':
            return ('HTTP/1.1 405 Method not allowed\n\n', 405)
        
        if not url in self._URLS:
            return ('HTTP/1.1 404 Not found\n\n', 404)
        
        return ('HTTP/1.1 200 OK\n\n', 200)
        
    def _create_body(self, code, url):
        if code == 404:
            return '<h1>404</h1><p>Not found</p>'
        elif code == 405:
            return '<h1>405</h1><p>Method not allowed</p>'
        else:
            return self._URLS[url]
        
    def output_request_url(self, request):
        request_url = request.splitlines()
        print(request_url[0])
            
    def _client_thread(self, client):
        while True:
            request = client.recv(4048)
            response = self._create_response(request)
            client.send(response)
            client.close()
            break