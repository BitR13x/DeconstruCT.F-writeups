# https://www.codeconvert.ai/c++-to-python-converter
class charArray:
    def __init__(self):
        self.cArr = None
        self.length = 0

def decode(aObj):
    disp = aObj.length
    decoded_string = ""
    while disp > 0:
        printChar = ord(aObj.cArr[aObj.length - disp])
        if (printChar >= 65) and (printChar <= 90): # uppercase
            if printChar - disp < 65:
                printChar = printChar - 64 - disp + 90
                #? printChar = ((printChar + disp) % 90) + 64
                print(chr(printChar), end='')
                decoded_string += chr(printChar)
                
            else:
                printChar -= disp
                #? printChar += disp
                print(chr(printChar), end='')
                decoded_string += chr(printChar)

        elif (printChar >= 97) and (printChar <= 122): # lowercase
            if printChar - disp < 97:
                printChar = printChar - 96 - disp + 122
                #? printChar = ((printChar + disp) % 122) + 96
                print(chr(printChar), end='')
                decoded_string += chr(printChar)

            else:
                printChar -= disp
                #? printChar += disp
                print(chr(printChar), end='')
                decoded_string += chr(printChar)

        else:
            print(chr(printChar), end='')
            decoded_string += chr(printChar)

        disp -= 1
    print('')
    return decoded_string



cArr = "esb{ikjebf_axbqm_wjl_gy_pg}"
aObj = charArray()
aObj.cArr = cArr
aObj.length = len(cArr)

reponse = decode(aObj)
print(reponse)
