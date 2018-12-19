'''
    Eric Ng
    Picture encoding

    Input:
        message - the message to encode into the picture
    Output:
        decryptedMessage - the message that was found within the picture
    processing:
        this program will encrypt a bmp image with a message and find that message afterwards
'''

from io import SEEK_CUR
from sys import exit

def main():
        #================================= Variables ==========================
        imgFile = open("image.bmp","rb+")
        fileSize = readInt(imgFile, 2)
        start = readInt(imgFile, 10)
        width = readInt(imgFile, 18)
        height = readInt(imgFile, 22)
        message = ""
        image = ""

        print("File size: " + str(fileSize) + " Starting: " + str(start) + " Width: " + str(width) + " Height: " + str(height))

        # ========================= Calculations ===========================================
        scanlineSize = width * 3
        if scanlineSize % 4 == 0:
            padding = 0
        else:
            padding = 4 - scanlineSize % 4

        print("Paddding: " + str(padding))

        # Make sure this is a valid image.
        if fileSize != (start + (scanlineSize + padding) * height):
            print("Not a 24-bit true color image file.")

        imgFile.seek(start)
        # ================================= Input ==========================
        message = input("Please enter a message: ") + "~"

        # ========================= Output ===========================================
        for i in range(len(message)):
            encodeImage(imgFile,message[i])

        print("Done encoding message into the image!")

        imgFile.close()
        # ================================= Input ==========================
        image = input("Please enter an image to be decoded: ")
        decodeImage(image)

"""
    This function will encode an image with a given message
    @:param - imgFile - the image file
    @:param - character - the character to encode into the first 8 bytes
    @:return none
"""
def encodeImage(imgFile,character) :
    # ================================= Variables ==========================
    # Read the pixel as individual bytes.
    theBytes = imgFile.read(8)
    binByteHolder = []
    byteOfChar = ""
    # ================================= Calculations ==========================
    #this turns the ascii value of the character  into binary  so we know what to turn the byte to
    byteOfChar = deciToBin(ord(character))
    #gets the binary for the numbers
    for i in range(len(list(theBytes))):
        binByteHolder.append(deciToBin(list(theBytes)[i]))
    #changes the 7th digit in order to encode the message
    for i in range(len(binByteHolder)):
        binByteHolder[i] = binByteHolder[i][:7] + byteOfChar[i]
    #turns the binary back into numbers so that they can be color values
    for i in range(len(binByteHolder)):
        binByteHolder[i] = binToAscii(binByteHolder[i])

    # Write the pixel.
    imgFile.seek(-8, SEEK_CUR) # Go back 8 bytes to the start of the pixel.
    imgFile.write(bytes(binByteHolder))

    #move to next 8 after the encoding finishes
    imgFile.seek(8,SEEK_CUR)
"""
    This function will get the information for the 24-bit true color image
    @:param - imgFile - the image
    @:param offset - the offset of the image
    @:return result - the imformation of the image
"""
def readInt(imgFile, offset) :
    # ================================= Variables ==========================
    # Move the file pointer to the given byte within the file.
    imgFile.seek(offset)
    # Read the 4 individual bytes and build an integer.
    theBytes = imgFile.read(4)
    result = 0
    base = 1
    # ================================= Calculations ==========================
    for i in range(4) :
        result = result + theBytes[i] * base
    base = base * 256
    # ================================= Return ==========================
    return result
"""
    this function converts a decimal number into a binary number
    @:param deci - the number to convert
    @:return binary - the binary form of the number
"""
def deciToBin(deci):
    # ================================= Variables ==========================
    binaryHolder = []
    binary = ""
    # ================================= Calculations ==========================
    while deci//2 != 0:
        binaryHolder.append(deci%2)
        deci = deci//2
    binaryHolder.append(deci % 2)
    for i in range(len(binaryHolder)-1,-1,-1):
        binary += str(binaryHolder[i])

    while len(binary) != 8:
        binary = "0" + binary
    # ================================= Return ==========================
    return binary

"""
    this function will convert the binary number into a ascii number
    @:param bin - the binary number
    @:return character - the value of the ascii character
"""
def binToAscii(bin):
    # ================================= Variables ==========================
    asciiCode = int(bin,2) #uses a base 2 and multiplies the binary
    character = asciiCode
    # ================================= Return ==========================
    return character

"""
    This function will decode the message within the image
    @:param image - the image
    @:return none it will print out the message
"""
def decodeImage(image):
    # ================================= Variables ==========================
    picture = open(image,"rb")
    fileSize = readInt(picture, 2)
    start = readInt(picture, 10)
    width = readInt(picture, 18)
    height = readInt(picture, 22)
    binByteHolder = []
    readCharacter = ""
    message = []
    decryptedMessage = ""

    # ================================= Calculations ==========================
    picture.seek(start)
    #while readCharacter != 127:

    theBytes = picture.read(8)

    #checks for the sentinel  value of ` which is 127
    while readCharacter != 126:
        # reset for next
        readCharacter = ""
        #gets the binary number of the bytes that were read in
        for i in range(len(list(theBytes))):
            binByteHolder.append(deciToBin(list(theBytes)[i]))
        #gets the 7th index of the read in bytes which is where the message is at (gets one character of the message)
        for i in range(1,len(binByteHolder)):
            readCharacter += binByteHolder[i][7]
        readCharacter = binToAscii(readCharacter)
        #creates a list of characters with the message inside
        message.append(readCharacter)
        # ================================= Reset ==========================
        #clears the bytes read in after one loop
        binByteHolder.clear()
        picture.seek(8,SEEK_CUR)
        theBytes = picture.read(8)

    #removes sentinel value
    message.pop()

    #decode the message
    for i in range(len(message)):
        decryptedMessage += chr(message[i])

    print("The encrypted message is: " + decryptedMessage)
main()

"""
    Sample run:
        File size: 168 Starting: 138 Width: 70 Height: 56
        Paddding: 2
        Not a 24-bit true color image file.
        Please enter a message: pile
        Done encoding message into the image!
        Please enter an image to be decoded: image.bmp
        The encrypted message is: pile
"""