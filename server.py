import socket
from threading import Thread
from views import index
import os


class IpTcpServer:
    def __init__(self, ip: str, port: int):
        self._serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serv_socket.bind((ip, port))
        self._URLS = {
            '/': index,
            '/test': index,
        }
        self.dd = ""
        self.RES_PATH = 'resources/'
        
    def run(self):
        self._serv_listen()
            
    def _serv_listen(self):
        self._serv_socket.listen()
        while True:
            client, addr = self._serv_socket.accept()
            self._client_thread(client)
            
    def _create_response(self, request):
        request = request.decode('utf-8')
        method, url, file_path = self._get_request_string(request)
        header, code = self._create_headers(method, url)
        body = self._create_body(code, url)
        if file_path:
            file = self.render_file(file_path)
            return file
        else:
            return (header + body).encode()
    
    def render_file(self, file_path):
        # response = None
        with open(file_path, 'rb') as file:
            response = file.read()
        
        header = 'HTTP/1.1 200 OK\n'
 
        if(file_path.endswith(".jpg")):
            mimetype = 'image/jpg'
        elif(file_path.endswith(".css")):
            mimetype = 'text/css'
        else:
            mimetype = 'text/html'
        
        header += 'Content-Type: '+str(mimetype)+'\n\n'
        
        final_response = header.encode('utf-8')
        final_response += response
        
        return final_response
            
    def open_data(self):
        f = open('text.txt', 'r')
        a = f.read()
        self.dd = a
        f.close()
            
    def _get_request_string(self, request):
        parsed = request.split(' ')
        method = parsed[0]
        url = parsed[1]        
        
        file_path = self._find_file(url)
        return (method, url, file_path)
    
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
            return self._URLS[url]()
        
    def output_request_url(self, request):
        # request_url = request.splitlines()
        # print(request.decode('utf-8'))
        pass
            
    def _client_thread(self, client):
        while True:
            request = client.recv(4048)
            response = self._create_response(request)
            client.send(response)
            client.close()
            break
        self.output_request_url(request)
        
    def _find_file(self, path):
        myfile = path.lstrip('/')
        return myfile
        
        # path_elem = url.lstrip('/').split('/')
        # isFile = str(path_elem[-1]).find('.')
        
        # file_path = None
        # if isFile != -1:
        #     file_path = self.RES_PATH
        #     for i in path_elem[:-1]:
        #         file_path += i + '/'
            
        #     for root, dirs, files in os.walk(file_path):
        #         if 'phoo.jpg' in files:
        #             print('good')