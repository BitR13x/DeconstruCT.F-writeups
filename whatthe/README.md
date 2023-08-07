# CTF Writeup: WhatThe - Reversing Challenge

## Challenge Description

**Title:** WhatThe - Reversing Challenge
**Category:** Reversing
**Description:** In this reversing challenge, you are provided with an gzip file named "whatThe.py.gz". The objective is to reverse engineer the file and find the hidden flag. Can you figure out "whatThe" is going on?

## Challenge Files

- [whatThe.py.gz](https://traboda-arena-87.s3.amazonaws.com/files/attachments/whatThe_abbdc0d6-11ca-48c8-b3d9-e7f91b9e2986.py.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GUFVMV6HO3NYL6Z%2F20230806%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20230806T233802Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=06216fbb6980c3f1ffe6a6aac79bcd930c179c60bc48aa3b6a2814a920df29bc)

## Approach / Solution

To solve this reversing challenge, we will follow these steps:

1. **Unpacking:** Huge file in gzip.
2. **Initial Analysis:** Before diving into reversing, we'll start with some basic checks and information gathering about the executable.
3. **Writing recursive decoder:** To simplify the process.
4. **Analyzing Part 2:** Analyze the decoded code to understand its functionality.
5. **Identify the Flag:** Locate the code responsible for checking the flag and extract the hidden flag.
6. **C++ encryption:** We get C++ function which we need to format and inspect.
7. **Reversing the c++ encryption funtion:** In order to receive a flag we need to reverse the function.
8. **Grab the Flag**

## Step 1: Unpacking

```bash
gzip -d whatThe.py.gz
```

## Step 2: Initial Analysis

The file is so huge, there is lots of junk.

```bash
ls -al
```

```bash
.rw-r--r-- 1.1G kali  7 Aug 01:43 whatThe.py
```

Tried reading and noticed there were mostly a bunch of 3's, then I temporarily removed the 3's so I could easily read the file.

```
cat whatThe.py
sed 's/3333//g' whatThe.py > out
cat out
```

In the end, it's just python code with an array and a for loop for decoding the array.

```py
blob = ['','','', ...]
whySoEagerToSolve

for i in blob:
    print((bytearray.fromhex(i).decode()))
```

There is a bonus text which happens to throw an error upon execution. So I removed it and moved the file into my workspace.

```bash
sed 's/3333//g' whatThe.py > ~/workspace/whatThe.py
```

So I hoped straight forward and executed it and hoped for the best.

And I just kept getting the same output quite confused about what was happening.

## Step 3: Writing recursive decoder

But then I played with that thing and realised that it's just recursively encoded. So write a python program for it.

We need to execute the file and get the output, then repeat it until we get the final output.

```py
import os

def get_command_output(command):
    try:
        with os.popen(command) as stream:
            output = stream.read().strip()
            return output
    except Exception as e:
        print(f"Error executing the command: {e}")
        return None

command_to_run = "python whatThe.py"
output = get_command_output(command_to_run)

# keep repeating until "whySoEagetToSolve" in output
while "whySoEagerToSolve" in output:
    output = output.replace("whySoEagerToSolve", "")

    with open("whatThe.py", "w") as f:
        f.write(output)

    output = get_command_output(command_to_run)


# when done write in file "out_w" and print first line
with open("out_w", "w") as f:
    f.write(output)
print(output.split("\n")[0])
```

## Step 4: Analyzing Part 2

After decoding, we get "out_w", which is another python file. With another junk.

```py
def someSortOfEncryption(flag):

    # didnt't have time to make my cpp file a shared library. Now i cannot use

    # the encryption function from my cpp code :(

    blob = [1110, ...]

    # ok, i will have my cpp code here just for a while

    return "broken_function"

eval(''+eval('str(str)'..)) # and even more evals, str casting and all
```

And I said to myself, What the\* is that? But that's another story.

On the top we can see a broken function for the encryption and some hints about C++ code.

On the bottom we can see quite a weird python expression.

First I started at the bottom. I was so overthinking it and in the end, I just tried using `print()` to print the whole response of that expression and that worked like a charm, after so much pain.

And get this response:

```py
print('Passing the flag inside someSortOfEncryption will give esb{ikjebf_axbqm_wjl_gy_pg}')
```

## Step 5: Machine code

Not quite, its compressed data.

Now we just need to convert this `blob` into a file. After quick lookup on Google, it was quite easier than I expected.

```py
def machine_code_to_file():

    blob = [11111, 10001011, 1000, 0, 1001100, 10011011, ...]

    binary_data = bytes(int(str(blob[i]), 2) for i in range(0, len(blob)))

    temp_file_path = "temp_binary_file.bin"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(binary_data)


machine_code_to_file()
```

```bash
file temp_binary_file.bin
```

```bash
temp_binary_file.bin: gzip compressed data, last modified: Wed Jun 29 18:34:52 2022, max compression, original size modulo 2^32 940
```

We can see it's just gzip so quick decompression and we are ready to go.

```bash
mv temp_binary_file.bin temp.gz
gzip -d temp.gz
```

And we get C++ code.

## Step 6: C++ encryption

We finally got the c++ encryption function and also badly formatted. Now just format it and reverse it.

```c++

#include <iostream>
using namespace::std; class charArray { public: char* cArr; int length; };ostream& operator << (ostream& out, charArray aObj) { int disp = aObj.length; char printChar; while(disp > 0) { printChar = *(aObj.cArr + aObj.length - disp); if ((printChar >= 65) && (printChar <= 90)) { if (printChar+disp > 90) { printChar = ((printChar+disp) % 90) + 64; out << printChar; }else{ printChar += disp; out << printChar; }; } else if ((printChar >= 97) && (printChar <= 122)) { if (printChar+disp > 122) { printChar = ((printChar+disp) % 122) + 96; out << printChar; }else{ printChar += disp; out << printChar; }; } else { out << printChar; }; disp -= 1; }; out << "
"; return out; };int main() { char cArr[23] = "Input_from_python_code"; // personalNote: please add the exact amount of characters to make the string :)
charArray aObj; aObj.cArr = cArr; aObj.length = (sizeof(cArr) / sizeof(char)) - 1; cout << aObj; return 0; }

```

I used formatting tool for this. [Codebeutify](https://codebeautify.org/cpp-formatter-beautifier) and then just repaired the last few things.

```c++
#include <iostream>

using namespace::std;
class charArray {
    public: char * cArr;int length;
};

ostream & operator << (ostream & out, charArray aObj) {
    int disp = aObj.length;
    char printChar;
    while (disp > 0) {
        printChar = * (aObj.cArr + aObj.length - disp);
        if ((printChar >= 65) && (printChar <= 90)) {
            if (printChar + disp > 90) {
                printChar = ((printChar + disp) % 90) + 64;
                out << printChar;
            } else {
                printChar += disp;
                out << printChar;
            };
        } else if ((printChar >= 97) && (printChar <= 122)) {
            if (printChar + disp > 122) {
                printChar = ((printChar + disp) % 122) + 96;
                out << printChar;
            } else {
                printChar += disp;
                out << printChar;
            };
        } else {
            out << printChar;
        };
        disp -= 1;
    };
    out << "";
    return out;
};

int main() {
    char cArr[23] = "Input_from_python_code"; // personalNote: please add the exact amount of characters to make the string :)
    charArray aObj;
    aObj.cArr = cArr;
    aObj.length = (sizeof(cArr) / sizeof(char)) - 1;
    cout << aObj;
    return 0;
}
```

## Step 7: Reversing the c++ encryption funtion

After understanding the functionality of the function, we aim to reverse the function.

I overwrite this into python with [online tool](https://www.codeconvert.ai/c++-to-python-converter) and again made few changes to make it work.

```py
# pyen.py
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
            if printChar + disp > 90:
                printChar = ((printChar + disp) % 90) + 64
                print(chr(printChar), end='')
                decoded_string += chr(printChar)

            else:
                printChar += disp
                print(chr(printChar), end='')
                decoded_string += chr(printChar)

        elif (printChar >= 97) and (printChar <= 122): # lowercase
            if printChar + disp > 122:
                printChar = ((printChar + disp) % 122) + 96
                print(chr(printChar), end='')
                decoded_string += chr(printChar)

            else:
                printChar += disp
                print(chr(printChar), end='')
                decoded_string += chr(printChar)

        else:
            print(chr(printChar), end='')
            decoded_string += chr(printChar)

        disp -= 1
    print('')
    return decoded_string



cArr = "Input_from_python_code"
aObj = charArray()
aObj.cArr = cArr
aObj.length = len(cArr)

reponse = decode(aObj)
print(reponse)
```

After understanding the functionality of the function, we aim to reverse the function.Then I quite understand what the function is doing and keep reversing. Basically, we need to do everything in reverse and that's easier said than done.

These two lines are actually the main manipulation except the `printChar += disp`. We reverse this by subtracting the disp and padding number and adding the modulo. We can just add modulo, because the ascii ends at 255, meaning, the max number we can encounter is 255 and we are eliminating it with the if statement to be max `printChar - disp < 65`.

```py
# original
printChar = ((printChar + disp) % 90) + 64
printChar = ((printChar + disp) % 122) + 96

# reversed
printChar = printChar - 64 - disp + 90
printChar = printChar - 96 - disp + 122
```

The condition `if printChar - disp < 65:` is used to check if the resulting character after decoding falls below the range of uppercase letters ('A' to 'Z'). If the decoded character goes below 'A' (ASCII 65), the code wraps it back to the end of the uppercase range ('Z').

Next just change the plus to minus and we are done.

```py
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
```

In contrast, in the `decode` function, the code is shifting the character to a lower ASCII value (towards the beginning of the alphabet) by subtracting `disp` from the ASCII value of the character. If the new value goes below 'A' (ASCII 65), it wraps back to 'Z'.

## Step 8: Grab the Flag

Finally, the sweet reliave and good feeling.

## Flag

The flag for this reversing challenge will be in the format: `dsc{[a-zA-Z0-9_]+}`.

**result**: `dsc{lookin_kinda_mad_at_me}`

## Conclusion

In this CTF challenge "WhatThe - Reversing," we demonstrated how to reverse engineer a python file to find a hidden flag. Reversing challenges like these test our ability to analyze and understand the functionality, allowing us to think like a reverse engineer.

If you found this challenge interesting, consider exploring more CTFs and practicing different reversing techniques to enhance your reverse engineering skills.

Happy hacking!
