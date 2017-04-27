import wave
import struct
import sys

binDict = {
    ' ': '00000', 'a': '00001', 'b': '00010', 'c': '00011', 'd': '00100', 'e': '00101',
    'f': '00110', 'g': '00111', 'h': '01000', 'i': '01001', 'j': '01010', 'k': '01011',
    'l': '01100', 'm': '01101', 'n': '01110', 'o': '01111', 'p': '10000', 'q': '10001',
    'r': '10010', 's': '10011', 't': '10100', 'u': '10101', 'v': '10110', 'w': '10111',
    'x': '11000', 'y': '11001', 'z': '11010'
}

def stringToBin(s):
    toReturn = ""
    for c in s:
        b = binDict[c]
        toReturn += b
    return toReturn

def writeToSong(noise_output, leftInput, rightInput):
    left_packed_value = struct.pack('h', leftInput)
    right_packed_value = struct.pack('h', rightInput)
    noise_output.writeframes(left_packed_value)
    noise_output.writeframes(right_packed_value)

def encodeSong(message):
    noise_output = wave.open('inputSong.wav', 'w')
    noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
    song = wave.open("outputSong.wav", 'r')
    messagePointer = 0
    messageLength = len(message)
    for i in range(song.getnframes()):
        data = song.readframes(1)
        values = struct.unpack('<hh', data)
        print values
        if i%22050 == 0 and messagePointer != messageLength:
            writeToSong(noise_output, values[0], values[1])
            data = song.readframes(1)
            data = song.readframes(1)
            i += 2
            newvalues = struct.unpack('<hh', data)
            leftValue = (newvalues[0] + values[0])/2
            rightValue = (newvalues[1] + values[1])/2
            dig = message[messagePointer]
            if dig == '1':
                leftValue += 1
            messagePointer += 1
            try:
                dig = message[messagePointer]
                if dig == '1':
                    rightValue += 1
                messagePointer += 1
            except:
                pass
            writeToSong(noise_output, leftValue, rightValue)
            writeToSong(noise_output, newvalues[0], newvalues[1])
        else:
            writeToSong(noise_output, values[0], values[1])

    noise_output.close()

def main():
    message = stringToBin(raw_input("Enter secret message: ") + "   ")
    encodeSong(message)

main()
