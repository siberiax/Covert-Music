import wave
import struct
import sys

#
# Dictionary of binary to the ascii character respresentation
#
binDict = {
    '00000': ' ',
    '00001': 'a',
    '00010': 'b',
    '00011': 'c',
    '00100': 'd',
    '00101': 'e',
    '00110': 'f',
    '00111': 'g',
    '01000': 'h',
    '01001': 'i',
    '01010': 'j',
    '01011': 'k',
    '01100': 'l',
    '01101': 'm',
    '01110': 'n',
    '01111': 'o',
    '10000': 'p',
    '10001': 'q',
    '10010': 'r',
    '10011': 's',
    '10100': 't',
    '10101': 'u',
    '10110': 'v',
    '10111': 'w',
    '11000': 'x',
    '11001': 'y',
    '11010': 'z'
}

song = wave.open("output.wav", 'r')
print song.getnframes()

message = ""
term = 0
for i in range(song.getnframes()):

    # stop when there are 3 spaces (15 0s)
    if term >= 15:
        break
    data = song.readframes(1)
    values = struct.unpack('<hh', data)
    if i % 22050 == 0:
        data = song.readframes(1)
        checkValues = struct.unpack('<hh', data)
        data = song.readframes(1)
        i += 2
        newvalues = struct.unpack('<hh', data)
        lToPut = (newvalues[0] + values[0])/2
        rToPut = (newvalues[1] + values[1])/2
        if checkValues[0] == lToPut:
            message += '0'
            term += 1
        else:
            message += '1'
            term = 0
        if checkValues[1] == rToPut:
            message += '0'
            term += 1
        else:
            message += '1'
            term = 0

decodedMessage = ""
currString = ""
for c in message:
    if len(currString) == 5:
        decodedMessage += binDict[currString]
        currString = ""
    currString += c

print decodedMessage
