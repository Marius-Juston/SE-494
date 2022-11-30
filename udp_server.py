import socket

import numpy as np

localIP = "127.0.0.1"

localPort = 20001

bufferSize = 1024

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

num_datapoints = 10
num_columns = 3

while (True):
    # bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    #
    # message = bytesAddressPair[0]
    #
    # address = bytesAddressPair[1]
    #
    # clientMsg = "Message from Client:{}".format(message)
    # clientIP = "Client IP Address:{}".format(address)
    #
    # print(clientMsg)
    # print(clientIP)

    # Sending a reply to client

    msgFromServer = ",".join(map(str, np.random.random(num_columns * num_datapoints)))

    bytesToSend = str.encode(msgFromServer)
    print(bytesToSend)

    UDPServerSocket.sendto(bytesToSend, ("127.0.0.1", localPort + 1))
