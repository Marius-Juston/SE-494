import socket

import numpy as np

from configuration import Config

config = Config()

localIP = config.SENSOR_IP

localPort = config.SENSOR_PORT

bufferSize = config.BUFFER_SIZE

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))
UDPServerSocket.listen()
conn, addr = UDPServerSocket.accept()

print("UDP server up and listening")

# Listen for incoming datagrams

num_datapoints = 10
num_columns = 3

with conn:
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

        msgFromServer = ",".join(map(str, np.round(np.random.random(num_columns * num_datapoints), 2)))

        bytesToSend = str.encode(msgFromServer + " " * (config.BUFFER_SIZE - len(msgFromServer)))
        print(bytesToSend)

        # UDPServerSocket.sendto(bytesToSend, (localIP, localPort))
        conn.sendall(bytesToSend)
        
