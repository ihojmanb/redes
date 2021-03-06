import socket
import http.client
import os

class TCPServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at ", s.getsockname())

        while True:
            connection_socket, address = s.accept()
            print("Connected by ", address)
            data = connection_socket.recv(2048)
            
            response = self.handle_request(data)

            connection_socket.sendall(bytes (response,'utf-8'))
            connection_socket.close()

    def handle_request(self, data):
        return "Request received!"





class HTTPServer(TCPServer):
    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html'
    }
    status_codes = http.client.responses

    def handle_request(self, data):
        request = HTTPRequest(data)
        try:
            handler = getattr(self, 'handle_{}'.format(request.method))
        except AttributeError:
            handler = self.HTTP_501_handler(request)
        response = handler(request)


        return response


    def HTTP_501_handler(self, request):
        response_line = self.response_line(status_code=501)
        response_headers = self.response_headers()
        blank_line ="\r\n"
        response_body = "<h1>501 Not Implemented</h1>"
        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )
    def handle_OPTIONS(self, request):
        response_line = self.response_line(status_code=200)
        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers= self.response_headers(extra_headers)
        blank_line= "\r\n"
        return "%s%s%s%s" % (
                response_line,
                response_headers,
                blank_line,
            )

    def handle_GET(self, request):
        filename = request.uri.strip('/') #remove the slash from URI
        extra_headers = {'X-ElQuePregunta': 'ihojmanb@gmail.com'}
        if os.path.exists(filename):
            response_line = self.response_line(status_code=200)
            response_headers = self.response_headers()

            with open(filename) as f:
                response_body = f.read()
        else:
            response_line = self.response_line(status_code=404)
            response_headers = self.response_headers()
            response_body = "<h1>404 Not Found</h1>"

        blank_line = "\r\n"

        return "%s%s%s%s" % (
                response_line,
                response_headers,
                blank_line,
                response_body
            )

    def response_line(self, status_code):
        reason = self.status_codes[status_code]
        return "HTTP/1.1 %s %s\r\n" % (status_code, reason)

    def response_headers(self, extra_headers=None):
        headers_copy = self.headers.copy()

        if(extra_headers):
            headers_copy.update(extra_headers)

        print(headers_copy)
        headers=""
        for h in self.headers:
            headers += "%s: %s\r\n" % (h, self.headers[h])
        return headers

class HTTPRequest:
        def __init__(self, data):
            self.method = None
            self.uri = None
            self.http_version = "1.1"
            self.headers = {} # a dictionary of headers
            self.parse(data)
		# call self.parse method to parse the request data
        def parse(self, data):
            lines = data.decode().split('\r\n')
            request_line = lines[0]
            self.parse_request_line(request_line)

        def parse_request_line(self, request_line):
            words = request_line.split(' ')
            self.method = words[0]
            self.uri = words[1]

            if len(words) > 2:
                self.http_version = words[2]

if __name__ == '__main__':
    server = HTTPServer()
    server.start()
