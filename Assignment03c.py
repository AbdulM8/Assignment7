# CSCI 355 Internet Web Technologies
# Summer 2024
# Abdul Mutallif
# Assignment 3 - Socket Program

import socket
import threading
import time

SYN = 'SYN'
ACK = 'ACK'
ACKSYN = 'ACK+SYN'
FIN = 'FIN'
ACKFIN = 'ACK+FIN'


# [7] On the client side, create and execute a function get_from_server(server_addr, server_port, file_name, client_path) that connects to the server, creates a connection using "3-way handshake", request the file, receives the file and writes it out locally in the client_apth (distinct from server_path), and then closes the connection using  a "3-way handshake"
def get_from_server(server_addr, server_port, file_name, client_path):
    s = socket.socket()
    s.connect((server_addr, server_port))
    print('Connected')
    msg_SYN = SYN
    s.send(msg_SYN.encode())
    print('Sending : ' + msg_SYN)
    msg_recv = s.recv(2048).decode()
    print('Received : ' + msg_recv)
    if msg_recv != ACKSYN:
        print(ACKSYN + ' not received. Received ' + msg_recv)
        s.close()
        return
    s.send((ACK + file_name).encode())
    print('Sending : ' + ACK + file_name)
    msg_recv = s.recv(2048).decode()
    print('Received : ' + msg_recv)
    f = open(client_path + file_name, 'w')
    f.write(msg_recv)
    f.close()
    print('Write to file : ' + msg_recv)
    s.send(FIN.encode())
    print('Sending : ' + FIN)
    msg_recv = s.recv(2048).decode()
    print('Received : ' + msg_recv)
    if msg_recv == ACKFIN:
        s.close()


def main():
    get_from_server('127.0.0.1', 12345, 'File1.txt', '')
    # ip_addr, hostname = get_host_info()
    # print("Your Computer Name is:" + hostname)
    # print("Your Computer IP Address is:" + ip_addr)
    # binary = get_binary_address(ip_addr)
    # print("binary", binary, len(binary))
    # cls = get_class(binary)
    # print("class", cls)
    # print("port", 80, "port type", get_port_type(80))
    # connect_to_server("www.google.com", 80)
    # connect_to_serverv2("djxmmx.net", None, 17)
    # connect_to_serverv2("time-a-g.nist.gov", None, 13)
    # connect_to_serverv2("abduls machine", "127.0.0.1", 12345)


if __name__ == '__main__':
    main()
