        .globl _main
        .p2align 2
_main:
        adr x0, msg
        bl _puts
        mov x0, #42
        b _exit

msg:
        .asciz  "Hello ASM!"
