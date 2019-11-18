# import the required libraries
import threading
import socket
import time

def getDecDigit(certainDigit):
    # list of digits / characters
    characters = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

    for item in range(len(characters)):
        # if the passed argument is equal to the item, return it
        if certainDigit.lower() == characters[item]:
            return (item)

def hexToDec(hexNum):
    decNum = 0
    power = 0

    # -1 step size (go from right to left)
    for character in range(len(hexNum), 0, -1):
        try:
            decNum = decNum + 16 ** power * getDecDigit(hexNum[character - 1])
            power += 1

        except:
            return None

    return(int(decNum))

def eegWave():
    # set the IP address and port
    udpIP = "192.168.0.17"
    udpPort = 7000

    # define socket, specify the use of internet and UDP
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind the socket
    mySocket.bind((udpIP, udpPort))

    stocker = []
    counter = 0

    while True:
        # print the data received from the server
        data, address = mySocket.recvfrom(1024)
        dataPoint = str(data)

        if ('alpha_absolute' in dataPoint):
            # split on the comma
            cleanData = dataPoint.split(',')
            # the string before the comma isn't required
            cleanData = cleanData[1]
            # split on the 'x'
            cleanData = cleanData.split('x')
            # the 'ffff\\' (at the 0th index) isn't required
            cleanData = cleanData[1:]

            outData = []

            # convert each item to decimal and add it to outData
            for item in cleanData:
                # ignore the last character
                outData += [hexToDec(item[:-1])]

            finalData = []

            # if the item is an integer and greater than 0, add it to finalData
            for item in outData:
                if (isinstance(item, int)) and (item > 0):
                    finalData += [item]

            if len(finalData) == 0:
                continue

            stocker += [sum(finalData) / len(finalData)]
            counter += 1

            if counter == 2:
                s = sum(stocker) / len(stocker)
                if s == (sum(finalData) / len(finalData)):
                    print('True')

                else:
                    print('False')

outPut = eegWave()