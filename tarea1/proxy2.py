import socket
import sys

class Proxy():
    def __init__(self, host='localhost', port=1818, server_port=1819):
        self.host = host
        self.port = port
        self.server_port = server_port

    def start(self):
        # UDP SOCKET as server to listen to proxy1
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server.bind((self.host, self.port))
        print('Proxy2 connected at {}'.format(udp_server.getsockname()))
        # TCP SOCKET as client to connect with server_echo4
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((self.host, self.server_port))
        while True:
            # UDP SOCKET receives Proxy1 request
            clientData, proxy1Address = udp_server.recvfrom(1024)
            # print('Proxy2 recieved data from {}'.format(proxy1Address))
            # send Proxy1 request to Server with TCP
            tcp_client.send(clientData)
            # receive server Response
            serverData = tcp_client.recv(1024)
            # print('data from server: {}'.format(serverData.decode()))
            # send server response back to Proxy1 via UDP
            udp_server.sendto(serverData, proxy1Address)
        udp_server.close()
        tcp_client.close()

if __name__ == '__main__':
    proxy2 = Proxy()
    proxy2.start()
