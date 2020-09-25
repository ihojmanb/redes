import socket

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
			response = (
			'HTTP/1.1 200 OK \r\n',
			'\r\n',
	
			}
			return data




class HTTPServer(TCPServer):
	def handle_request(self, data):
			return "Request received!"


if __name__ == '__main__':
	server = HTTPServer()
	server.start()
