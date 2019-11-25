import socket

# create a class for our socket
class newSocket:

    # initialize the class
    def __init__(self, udpIP, udpPort):
        # create a new socket
        self.udpIP = udpIP
        self.udpPort = udpPort
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # bind it (with the IP and port as parameters)
        self.mySocket.bind((udpIP, udpPort))

    def eegWave(self):
        while True:
            # print the data received from the server
            data, address = self.mySocket.recvfrom(1024)
            # convert the data into a string
            dataPoint = str(data)   

            # if 'blink' is in dataPoint
            if ('blink' in dataPoint):
                # get the last number (second last character)
                lastNumber = int(dataPoint[-2])

                # if the last number is 1, then a blink occurred
                if (lastNumber == 1):
                    return 1

                else:
                    # break out of the loop and return 0
                    break
        return 0