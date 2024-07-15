# CSCI 355 Internet Web Technologies
# Summer 2024
# Abdul Mutallif
# Assignment 3 - Socket Program

import socket
import threading
import time

# [3] Define these constants used for the 3-way handshake:
SYN = 'SYN'
ACK = 'ACK'
ACKSYN = 'ACK+SYN'
FIN = 'FIN'
ACKFIN = 'ACK+FIN'


# [4] Define a function to handle resending the file after a certain amount of elapsed time:
def send_again_check(c, addr, has_received, msg):
    old_time = time.time()
    while not has_received[0]:
        if time.time() - old_time >= 10:
            c.send(msg.encode())
            print(str(addr) + ' Sending again : ' + msg)
            break


#[5] Define a function to handle each client connection
def each_connection(c, addr):
    print(str(addr) + ' Connected')
    is_finishing = False
    has_received = [False]
    while True:
        msg_recv = c.recv(2048).decode()
        has_received[0] = True
        if msg_recv == SYN:
            print(str(addr) + ' Received : ' + msg_recv)
            msg_send = ACKSYN
            c.send(msg_send.encode())
            print(str(addr) + ' Sending : ' + msg_send)
        elif msg_recv.startswith(ACK) and not is_finishing:
            print(str(addr) + ' Received : ' + msg_recv)
            file_name = msg_recv[3:]
            if len(file_name) > 0:
                f = open(file_name, 'r')
                file_content = f.read()
                f.close()
                print(str(addr) + ' File contents read')
                c.send(file_content.encode())
                print(str(addr) + ' Sending : ' + file_content)
                has_received[0] = False
                threading.Thread(target=send_again_check, args=(c, addr, has_received, file_content,)).start()
        elif msg_recv == FIN:
            print(str(addr) + ' Received : ' + msg_recv)
            msg_send = ACKFIN
            c.send(msg_send.encode())
            print(str(addr) + ' Sending : ' + msg_send)
            is_finishing = True
        elif msg_recv == ACK and is_finishing:
            break
        else:
            break
    c.close()
    print(str(addr) + ' Connection closed')


# [6] Create a function main to manage the overall server activity
def main():
    s = socket.socket()
    print("Socket successfully created")
    port = 12345
    s.bind(('', port))
    print("socket binded to %s" % (port))
    s.listen(5)
    print("socket is listening")
    while True:
        c, addr = s.accept()
        threading.Thread(target=each_connection, args=(c, addr,)).start()
    s.close()


if __name__ == '__main__':
    main()
