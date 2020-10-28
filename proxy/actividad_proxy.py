import socket
import http.client
import os
import json

class TCPServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        with open('data.json') as json_file:
            self.json_data = json.load(json_file)

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at ", s.getsockname())

        while True:
            connection_socket, address = s.accept()
            print("Connected by ", address)
            connection_socket.close()

    def handle_request(self, data):
        return "Request received!"

class HTTPServer(TCPServer):
    headers = {
        'Server': 'YamirServer',
    }
    status_codes = http.client.responses

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at ", s.getsockname())

        while True:
            connection_socket, address = s.accept()
            print("Connected by ", address)
            request = connection_socket.recv(2048)
            print('Request: ')
            print(request)
            mod_request = self.modify_request(request)
            print('Modified Request: ')
            print(mod_request)
            webserver, port = self.get_web_server_info(mod_request)
            url = self.get_url(request)
            print('url: ', url)
            try:
                # create a socket to connect to the web server
                if(self.isForbiddenUrl(url)):
                    print('Forbiden url!')
                    forbidden_response = self.handleForbiddenUrl(url)
                    connection_socket.send(bytes(forbidden_response, 'utf-8'))

                else:
                    ws = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ws.settimeout(60)
                    ws.connect((webserver, port))
                    ws.sendall(mod_request)
                    while True:
                        # receive dataprintout from web server
                        data = ws.recv(2048)
                        data = self.replaceForbiddenWords(data)
                        if(len(data) > 0):
                            # send to browser
                            connection_socket.send(data)
                        else:
                            break
                    ws.close()
                    connection_socket.close()
            except socket.error as error_msg:
                print(error_msg)
                if ws:
                    ws.close()
                if connection_socket:
                    connection_socket.close()
            connection_socket.close()

    def replaceForbiddenWords(self, data):
        new_data = data.decode()
        list_of_dict_of_words = self.json_data['forbidden_words']
        # TODO: entender que chucha es una comprehension
        dict_of_words = {k: v for dic in list_of_dict_of_words for k, v in dic.items()}
        words_to_replace = list(dict_of_words.keys())
        new_words = list(dict_of_words.values())
        for i,_ in enumerate(words_to_replace):
            new_data = new_data.replace(words_to_replace[i], new_words[i])
            print(new_data)

        print('replaced words in data: ', new_data)
        return bytes(new_data, 'utf-8')

    def handleForbiddenUrl(self, url):
        response_line = self.response_line(status_code=403)
        response_headers = self.response_headers()
        blank_line ="\r\n"
        response_body = "<h1>el Proxy no telo permite</h1>"
        return "%s%s%s%s" % (
            response_line,
            response_headers,
            blank_line,
            response_body
        )

    def isForbiddenUrl(self, url):
        forbidden_urls = self.get_forbidden_urls(self.json_data)
        if(url in forbidden_urls):
            return True
        else:
            return False
    def get_forbidden_urls(self, data):
        return data['blocked']

    def modify_request(self, request):
        user_email = self.json_data['user']
        extra_headers = {'X-ElQuePregunta': user_email}
        response_headers = self.response_headers(extra_headers)
        blank_line = "\r\n"
        #deleting last \r\n, adding extra headers and last blank line
        request = request.decode()[:-2] + response_headers + blank_line
        request = bytes(request, 'utf-8')
        return request

    def get_url(self, request):
        # parse the first line
        first_line = request.decode().split('\n')[0]
        # get url
        url = first_line.split(' ')[1]
        return url
    def get_web_server_info(self, request):
        # parse the first line
        first_line = request.decode().split('\n')[0]
        # get url
        url = first_line.split(' ')[1]
        http_pos = url.find("://") # find pos of ://
        if (http_pos==-1):
            temp = url
        else:
            temp = url[(http_pos+3):] # get the rest of url
        port_pos = temp.find(":") # find the port pos (if any)
        # find end of web server
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if (port_pos==-1 or webserver_pos < port_pos):
            # default port
            port = 80
            webserver = temp[:webserver_pos]

        else: # specific port
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        return webserver, port

    def response_line(self, status_code):
        reason = self.status_codes[status_code]
        return "HTTP/1.1 %s %s\r\n" % (status_code, reason)

    def response_headers(self, extra_headers=None):
        headers_copy = self.headers.copy()

        if(extra_headers):
            headers_copy.update(extra_headers)

        self.headers = headers_copy
        headers=""
        for h in self.headers:
            headers += "%s: %s\r\n" % (h, self.headers[h])
        return headers

if __name__ == '__main__':
    server = HTTPServer()
    server.start()
