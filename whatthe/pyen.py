# https://www.codeconvert.ai/c++-to-python-converter
class charArray:
    def __init__(self):
        self.cArr = None
        self.length = 0

def encode(aObj):
    disp = aObj.length
    encoded_string = ""
    while disp > 0:
        printChar = ord(aObj.cArr[aObj.length - disp])
        if (printChar >= 65) and (printChar <= 90): # lowercase
            if printChar + disp > 90:
                printChar = ((printChar + disp) % 90) + 64
                print(chr(printChar), end='')
                encoded_string += chr(printChar)
                
            else:
                printChar += disp
                print(chr(printChar), end='')
                encoded_string += chr(printChar)

        elif (printChar >= 97) and (printChar <= 122): # uppercase
            if printChar + disp > 122:
                printChar = ((printChar + disp) % 122) + 96
                print(chr(printChar), end='')
                encoded_string += chr(printChar)

            else:
                printChar += disp
                print(chr(printChar), end='')
                encoded_string += chr(printChar)

        else:
            print(chr(printChar), end='')
            encoded_string += chr(printChar)

        disp -= 1
    print('')
    return encoded_string



cArr = "Input_from_python_code"
aObj = charArray()
aObj.cArr = cArr
aObj.length = len(cArr)

reponse = encode(aObj)
print(reponse)
