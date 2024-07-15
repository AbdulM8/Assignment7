# CSCI 355 Internet Web Technologies
# Summer 2024
# Abdul Mutallif
# Assignment 2 - Socket Program
# ACK - I worked with the class
# Website Used:
import socket
# [1] Define a function get_host_info() to determine your computer’s IP address.
# See https://www.geeksforgeeks.org/python-program-find-ip-address/
def get_host_info():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return ip_addr, hostname
# [2] Define a function binary_address() to convert your IP Address from “dotted decimal notation” to a 32-bit binary string.
# First, split the dotted decimal notation into four numbers, then find the binary equivalent of each and concatenate them back together. Be sure to remove the "0b" prefix of the binary numbers and to pad each component to 8 binary digits. When you are done, your binary address should be exactly 32  characters long.
# See https://www.geeksforgeeks.org/python-program-to-covert-decimal-to-binary-number/
# and https://stackoverflow.com/questions/3528146/convert-decimal-to-binary-in-python
def get_binary_address(ip_addr):
    binary = "".join([bin(int(octet))[2:].zfill(8) for octet in ip_addr.split('.')])
    return binary

# [3] Write a function to determine if the address is Class A, B, C, D or E by examining the first few bits of the 32-bit string.
# See https://en.wikipedia.org/wiki/Classful_network
def get_class(binary_address):
    result = "?"
    if binary_address[:1] == "0":
        result = "A"
    elif binary_address[:2] == "10":
        result = "B"
    elif binary_address[:3] == "110":
        result = "C"
    elif binary_address[:4] == "1110":
        result = "D"
    elif binary_address[:5] == "1111":
        result = "E"
    return result

# [4] Define a function port_type(port) to determine the type of port number. The options are:
# 0-1023: Well-Known
# 1024-49151: Registered
# 49152-65535: Dynamic/Private
# See https://en.wikipedia.org/wiki/Port_(computer_networking)
def get_port_type(port):
    result = "?"
    if 0 <= port <= 1023:
        result = "Well-Known"
    elif 1024 <= port <= 49151:
        result = "Registered"
    elif 49152 <= port <= 65535:
        result = "Dynamic/Private"
    return result


# [5] Write a function to connect to the Google server
# https: // www.geeksforgeeks.org / socket - programming - python /
# An example script to connect to Google using socket programming in Python
import socket  # for socket
import sys
def connect_to_server(hostname, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))
    try:
        host_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        # this means could not resolve the host
        print("there was an error resolving the host")
        sys.exit()
    # connecting to the server
    s.connect((host_ip, port))
    print("the socket has successfully connected to ", hostname, "on ip", host_ip, "on port", port)

#[7] Write a programs Assignment2Client.py that will talk to that server
def connect_to_serverv2(hostname, ip_addr, port):
    s = socket.socket()
    if not ip_addr:
        try:
            ip_addr = socket.gethostbyname(hostname)
        except socket.gaierror:
            # this means could not resolve the host
            print("there was an error resolving the host", hostname)
            sys.exit()
    s.connect((ip_addr, port))
    print("The socket has successfully connected to hostname",hostname, "to ip", ip_addr, "on port", port)
    print("Message recevied:", s.recv(1024).decode())
    s.close()
def main():
    ip_addr, hostname = get_host_info()
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + ip_addr)
    binary = get_binary_address(ip_addr)
    print("binary", binary, len(binary))
    cls = get_class(binary)
    print("class", cls)
    print("port", 80, "port type", get_port_type(80))
    connect_to_server("www.google.com", 80)
    connect_to_serverv2("djxmmx.net", None, 17)
    connect_to_serverv2("time-a-g.nist.gov", None, 13)
    connect_to_serverv2("abduls machine", "127.0.0.1", 12345)

if __name__ == '__main__':
    main()
