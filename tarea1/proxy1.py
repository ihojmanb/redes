import socket

class Proxy():
    def __init__(self, host='localhost', port=1818):
        self.host = host
        self.port = port

    def start(self):
        # TCP SOCKET for client_echo2
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(2)
        print('Proxy running at {}'.format(s.getsockname()))

        while True:
            #connecting to client_echo2
            conn, address = s.accept()
            print('Client at {} connected'.format(address))

            # create UDP SOCKET as client to communicate with proxy2
            udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while True:
                # receive data from client
                clientData = conn.recv(1024)
                if not clientData: break
                # print('Client at {} says: {} '.format(address, clientData.decode()))
                # send data to proxy2 via UDP
                udp_client.sendto(clientData, ('localhost', 1818))
                serverResponse, proxyAddres = udp_client.recvfrom(1048)
                # print(response)
                conn.send(serverResponse)
            udp_client.close()
            conn.close()
            print('Client at {} disconnected'.format(address))
        # s.close()

if __name__ == '__main__':
    proxy1 = Proxy()
    proxy1.start()
