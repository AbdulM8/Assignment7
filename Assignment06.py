# CSCI 355 Internet Web Technologies
# Summer 2024
# Abdul Mutallif
# Assignment 6 -  Network Addressing and Forwarding
# Worked with class
# Sources: Listed in the functions/code

from subprocess import check_output


# [1] Write a function execute_command(cmd) to execute a windows shell command ("cmd").
# See https://stackoverflow.com/questions/14894993/running-windows-shell-commands-with-python
def exec_cmd(cmd):
    return check_output(cmd, shell=True)


# [2] Define a function get_routing_table by using the function from the previous step to run "route print" and then parsing the output into a table (2-D list).
def get_routing_table(routing_data):
    s = routing_data.decode()
    s = s[s.find("Destination"): s.find("Persistent Routes") - 1].replace("=", "").strip()
    lines = s.split('\n')
    # print(lines)
    headers = [get(lines[0], 0, 17), get(lines[0], 18, 35), get(lines[0], 36, 49), get(lines[0], 50, 60),
               get(lines[0], 61, 70)]
    print(headers)
    data = [[get(x, 0, 17), get(x, 18, 35), get(x, 36, 50), get(x, 51, 68), int(get(x, 69, 80))] for x in lines[1:]]
    for row in data:
        print(row)
    return headers, data


def get(s, i, j):
    return s[i:j + 1].strip()


# [3] Prompt the user to enter an IPv4 address in dotted-decimal notation. If the IP address is 0 or empty, this is our cue to quit. Otherwise proceed to next step
def get_ip():
    ip = input("Enter IP Address in dotted-decimal notation: ") or "123.123.123.123"
    return ip


# [4] Define a function validate_address() to validate the address in two ways:
# Call your own function to check that the entered IP address is valid, that is, it consists of four decimal numbers, each between 0 and 255, and separated by dots (periods).
# Call code from socket package to validate it. See https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python

def validate_address(ip, verbose=False):
    octets = ip.split(".")
    if len(octets) != 4:
        if verbose:
            print("Does not have four octets: ", ip)
        return False
    for octet in octets:
        if not octet.isnumeric():
            if verbose:
                print("Does not have numeric octets: ", ip)
            return False
        if int(octet) < 0 or int(octet) > 255:
            if verbose:
                print("Octet is out of 0-255: ", ip)
            return False
        return True


# [5] Define a function get_binary_address() to  find the binary equivalent of an IP address in dotted decimal notation and use it on the inputted IP address.
def get_binary_address(ip_addr):
    binary = "".join([bin(int(octet))[2:].zfill(8) for octet in ip_addr.split('.')])
    return binary


# [6] Define a function bitwise_and() to do the “bitwise-AND” of two bit-strings. You may either do it by iterating over the characters of the bit-strings, or use binary arithmetic. (See https://wiki.python.org/moin/BitwiseOperators)
def bitwise_and(bits1, bits2):
    res = ""
    n = max(len(bits1), len(bits2))
    for i in range(n):
        res += "1" if bits1[i] == "1" and bits2[i] == "1" else "0"
    return res


# [7] Define  a function get_classful_address_type() to dmetermine its class A thru E. If it is class D or E, tell the user that D is for multicast or E is reserved, and return to step [2]. You can determine the class either directly from the dotted decimal notation or from the leading bits of the binary equivalent. (See https://en.wikipedia.org/wiki/Classful_network#Classful_addressing_definition)
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


def find_prefix_match(binary_and):
    binary_and += "0"
    return binary_and.find("0")


# [8] Define a function get_next_hop() to loop through the rows of the routing table from step [2] and determine the “Next Hop” for the user-inputted address. To determine which row is determinant, use the following algorithm:
# Do a bitwise-AND of the network mask with the destination IP address and see if you have a match with “Network Destination”, the first column. Mathematically, this can be expressed at N = D & M where D is the Destination IP address, M is the (network) Mask, and N is the (destination) Network.
# Use the Metric column to decide between multiple matches (lowest value of Metric gets priority)
# If you have multiple matches and the Metric column is the same for all, then use the “Longest Prefix Match” to decide between ties, that is the one with more non-zero bits in the Mask.

def get_next_hop(table, dest_ip):
    dest_ip_bin = get_binary_address(dest_ip)
    best_row = None
    best_prefix = -1
    for row in table:
        table_dest = row[0]
        if validate_address(table_dest):
            table_dest_bin = get_binary_address(table_dest)
            binary_and = bitwise_and(dest_ip_bin, table_dest_bin)
            prefix = find_prefix_match(binary_and)
            if (prefix > best_prefix) or (prefix == best_prefix and row[4] < best_row[4]):
                best_prefix = prefix
                best_row = row
    return best_row, best_prefix


def process_ip(ip, table):
    print()
    print(f"IP: {ip}")
    ip_status = validate_address(ip, verbose=True)
    print(f"IP Status is: {ip_status}")
    if ip_status:
        ip_binary = get_binary_address(ip)
        best_row, best_prefix = get_next_hop(table, ip)
        print(f"Binary is: {ip_binary}")
        print(f"Best Row is: {best_row}")
        print(f"Best Prefix is: {best_prefix}")


def main():
    routing_data = exec_cmd("route print")
    headers, data = get_routing_table(routing_data)

    ips_to_test = ["abc.def.ghi.jkl", "111-111-111-111", "613.613.613.613", "123.123.123", "225.225.225.225",
                   "241.242.243.244", "127.0.0.1", "52.3.73.91", "216.239.63.255"]

    for ip in ips_to_test:
        process_ip(ip, data)


if __name__ == '__main__':
    main()
