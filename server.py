import socket
from threading import Thread
from views import index
from urls import url_path
from routing.url import UrlRouting
import settings

class IpTcpServer:
    def __init__(self, ip: str, port: int):
        self._serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serv_socket.bind((ip, port))
        UrlRouting(url_path)
        self._URLS = UrlRouting.URLS
        self.dd = ""
        
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
        file_path = None
        if url.find('.') != -1:
            path = settings.RESOURCEDIR + str(url).partition(settings.RESOURCEDIR)[2]
            file_path = self._find_file(path)            
        
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
        
    def output_request_log(self, request):
        request_url = request.decode('utf-8')
        print(str(request_url).splitlines()[0])
            
    def _client_thread(self, client):
        while True:
            request = client.recv(4048)
            response = self._create_response(request)
            client.send(response)
            client.close()
            break
        self.output_request_log(request)
        
    def _find_file(self, path):
        myfile = path.lstrip('/')
        return myfile