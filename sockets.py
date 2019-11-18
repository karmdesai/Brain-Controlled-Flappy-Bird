import socket

# set the IP address and port
udpIP = "192.168.0.17"
udpPort = 8000

sendUdpIp = "192.168.0.17"
sendPort = 9000

# define socket, specify the use of internet and UDP
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket
mySocket.bind((udpIP, udpPort))

while True:
    # print the data received from the server
    data, address = mySocket.recvfrom(1024)
    dataPoint = str(data)
    
    if ('blink' in dataPoint):
        blinkData = str(dataPoint)[-2]

        if (int(blinkData) == 1):
            print(blinkData)
            sendSocket.sendto(b'1', (sendUdpIp, sendPort))

        else:
            sendSocket.sendto(b'0', (sendUdpIp, sendPort))