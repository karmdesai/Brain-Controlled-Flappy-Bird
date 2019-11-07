# import the required libraries
import socket

# set the IP address and port
udpIP = "192.168.0.17"
udpPort = 7000

# define socket, specify the use of internet and UDP
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket
mySocket.bind((udpIP, udpPort))
    
while True:
    # print the data received from the server
    print(mySocket.recvfrom(1024))