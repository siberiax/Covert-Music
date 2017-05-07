import wave
import struct

#
# Dictionary of ascii letters to binary
#
binDict = {
    ' ': '00000', 'a': '00001', 'b': '00010', 'c': '00011', 'd': '00100', 'e': '00101',
    'f': '00110', 'g': '00111', 'h': '01000', 'i': '01001', 'j': '01010', 'k': '01011',
    'l': '01100', 'm': '01101', 'n': '01110', 'o': '01111', 'p': '10000', 'q': '10001',
    'r': '10010', 's': '10011', 't': '10100', 'u': '10101', 'v': '10110', 'w': '10111',
    'x': '11000', 'y': '11001', 'z': '11010'
}

#
# This simple function will turn an ascii string into into it's
# Binary equivalent
#
def stringToBin(s):
    toReturn = ""
    for c in s:
        b = binDict[c]
        toReturn += b
    return toReturn

#
# This is a helper function to write values to the output song file
#
def writeToSong(noise_output, leftInput, rightInput):
    left_packed_value = struct.pack('h', leftInput)
    right_packed_value = struct.pack('h', rightInput)
    noise_output.writeframes(left_packed_value)
    noise_output.writeframes(right_packed_value)

#
# This function will encoder the message it take in into the song
#
def encodeSong(message):

    # open the song files
    noise_output = wave.open('output.wav', 'w')
    noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
    song = wave.open("input.wav", 'r')
    messagePointer = 0
    messageLength = len(message)
    print song.getnframes()

    # loop through the frames of the song
    for i in range(song.getnframes()):
        data = song.readframes(1)
        values = struct.unpack('<hh', data)
        print values

        # write values to the song if we are on one of the 22050th frames
        if i%22050 == 0 and messagePointer != messageLength:
            writeToSong(noise_output, values[0], values[1])
            data = song.readframes(1)
            data = song.readframes(1)
            i += 2

            # get the values of the frame 2 away and take the average
            newvalues = struct.unpack('<hh', data)
            leftValue = (newvalues[0] + values[0])/2
            rightValue = (newvalues[1] + values[1])/2
            dig = message[messagePointer]

            # increment value by one if we are writing a one
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

    # close the song file
    noise_output.close()

#
# This main function prompts the user for a message and then calles the
# encoder
#
def main():
    message = stringToBin(raw_input("Enter secret message: ") + "   ")
    encodeSong(message)

if __name__ == "__main__":
    main()
