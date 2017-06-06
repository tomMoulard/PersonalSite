# -*- coding: utf-8 -*-
"""
Created on Mon Jun 5 13:00:00 2017

@author: tm

The goal is to do the same as "iperf" but by using large files

Usage:
    - server : "python3 customIperf.py -s"
    - client : "python3 customIperf.py -c <server IP @> <file>"
"""

usage = """
Usage:
    - server : "python3 customIperf.py -s"
    - client : "python3 customIperf.py -c <server IP @> <file>"
"""

# Connection Stuff
import socket
import sys

# For file management
import os

# Miscellaneous
# import threading

def get_constants(prefix):
    """
    Create a dictionary mapping socket module constants to their names.
    """
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )


def isServer():
    """
    This manages the server part
    will save by default the file in the current folder with the same name
    as the one sent.
    """
    port      = 10000
    families  = get_constants("AF_")
    types     = get_constants("SOCK_")
    protocols = get_constants("IPPROTO_")
    sock      = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = ("localhost", port)
    try:
        sock.bind(server_address)
    except Exception as e:
        print(e)
    sock.listen(1)
    print("------------------------------------------------------------")
    print("Server Listening on port {}".format(port))
    print("Family {} Type: {} Protocol: {}".\
        format(families[sock.family], types[sock.type], protocols[sock.proto]))
    print("------------------------------------------------------------")
    while True:
        # Wait for connection
        connection, client_address = sock.accept()
        try:
            print("Client connected: {}".format(client_address))
            lenFileName = int(connection.recv(512).\
                decode(encoding="utf-8", errors="strict"))
            fileName    = str(connection.recv(lenFileName).\
                decode(encoding="utf-8", errors="strict"))
            # Receive the data in small chunks and retransmit it
            f = open(fileName, "w+b")
            while True:
                data = connection.recv(64)
                # print("received \"{}\"".format([data]))
                f.write(data)
                if not data:
                    f.close()
                    print("EOF from {} for the file \"{}\"".\
                        format(client_address, fileName))
                    break
        finally:
            # Clean up the connection
            connection.close()
            print("Client disconnected")

def isClient(serverIP, fileName):
    """
    This manages the client part
    serverIP should be like : (ipAdress, port)
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (serverIP[0],  int(serverIP[1]))
    print("connecting to {}:{}".format(serverIP[0], serverIP[1]))
    while sock.connect_ex(server_address):
        pass
    print("Connection established")
    try:
        # sending fileName:
        # first the len
        sock.sendall("{:>512}".format(str(len(fileName))).\
            encode(encoding="utf-8", errors="strict"))
        # and then the name
        sock.sendall("{}".format(fileName).\
            encode(encoding="utf-8", errors="strict"))
        # crushing data
        file    = open(fileName, "r+b")
        lines   = file.read()
        file.close()
        # Send data
        print("Sending file")
        # sock.sendall(fileName)
        sock.sendall(lines)
        print("File sent")
    finally:
        print("Closing Connection")
        sock.close()


def main():
    if "-s" in sys.argv:
        isServer()
    elif "-c" in sys.argv:
        args = sys.argv[2]
        ip   = ""
        port = ""
        pos  = 0
        ll   = len(args)
        while pos < ll and args[pos] != ":":
            ip  += args[pos]
            pos += 1
        pos += 1
        while pos < ll:
            port += args[pos]
            pos  += 1
        isClient((ip, port), sys.argv[3])
    else:
        print(usage)
        return 1

if __name__ == "__main__":
    main()