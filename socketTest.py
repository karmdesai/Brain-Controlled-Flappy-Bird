import math
import struct

global NTP_epoch
from calendar import timegm
NTP_epoch = timegm((1900,1,1,0,0,0)) # NTP time started in 1 Jan 1900
del timegm

global NTP_units_per_second
NTP_units_per_second = 0x100000000 # about 232 picoseconds

def _readString(data):
    """Reads the next (null-terminated) block of data.
    """
    length   = data.find(b'\0')
    nextData = int(math.ceil((length+1) / 4.0) * 4)
    readstring = (data[0:length].decode('latin-1'), data[nextData:])
    return readstring

def _readBlob(data):
    """Reads the next (numbered) block of data
    """

    length   = struct.unpack(">i", data[0:4])[0]
    nextData = int(math.ceil((length) / 4.0) * 4) + 4
    return (data[4:length+4], data[nextData:])

def _readInt(data):
    """Tries to interpret the next 4 bytes of the data
    as a 32-bit integer. """

    if(len(data)<4):
        print("Error: too few bytes for int", data, len(data))
        rest = data
        integer = 0
    else:
        integer = struct.unpack(">i", data[0:4])[0]
        rest    = data[4:]

    return (integer, rest)

def _readLong(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit signed integer.
     """

    high, low = struct.unpack(">ll", data[0:8])
    big = (int(high) << 32) + low
    rest = data[8:]
    return (big, rest)

def _readTimeTag(data):
    """Tries to interpret the next 8 bytes of the data
    as a TimeTag.
     """
    high, low = struct.unpack(">LL", data[0:8])
    if (high == 0) and (low <= 1):
        time = 0.0
    else:
        time = int(NTP_epoch + high) + float(low / NTP_units_per_second)
    rest = data[8:]
    return (time, rest)

def _readFloat(data):
    """Tries to interpret the next 4 bytes of the data
    as a 32-bit float.
    """

    if(len(data)<4):
        print("Error: too few bytes for float", data, len(data))
        rest = data
        float = 0
    else:
        float = struct.unpack(">f", data[0:4])[0]
        rest  = data[4:]

    return (float, rest)

def _readDouble(data):
    """Tries to interpret the next 8 bytes of the data
    as a 64-bit float.
    """

    if(len(data)<8):
        print("Error: too few bytes for double", data, len(data))
        rest = data
        float = 0
    else:
        float = struct.unpack(">d", data[0:8])[0]
        rest  = data[8:]

    return (float, rest)

def decodeOSC(data):
    """Converts a binary OSC message to a Python list.
    """
    table = {"i":_readInt, "f":_readFloat, "s":_readString, "b":_readBlob,
            "d":_readDouble, "t":_readTimeTag}
    decoded = []
    address,  rest = _readString(data)
    if address.startswith(","):
        typetags = address
        address = ""
    else:
        typetags = ""

    if address == "#bundle":
        time, rest = _readTimeTag(rest)
        decoded.append(address)
        decoded.append(time)
        while len(rest)>0:
            length, rest = _readInt(rest)
            decoded.append(decodeOSC(rest[:length]))
            rest = rest[length:]

    elif len(rest)>0:
        if not len(typetags):
            typetags, rest = _readString(rest)
        decoded.append(address)
        decoded.append(typetags)
        if typetags.startswith(","):
            for tag in typetags[1:]:
                value, rest = table[tag](rest)
                decoded.append(value)
        else:
            print('Could Not Decode The Byte!')

    return decoded

# import the required libraries
import threading
import socket
import time

# set the IP address and port
udpIP = "192.168.0.17"
udpPort = 8000

# define socket, specify the use of internet and UDP
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind the socket
mySocket.bind((udpIP, udpPort))

def eegWave():

    averageList = []
    finalAverage = 0
    blinkCount = 0

    while True:
        # print the data received from the server
        data, address = mySocket.recvfrom(1024)
        dataPoint = str(data)

        if ('blink' in dataPoint):
            lastNumber = int(dataPoint[-2])

            if (lastNumber == 1):
                blinkCount += 1
                print('Blink Number: ', blinkCount)
         
eegWave()