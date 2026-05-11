.globl _main
_main:
  adr x0, msg
  bl _puts
  b _exit

msg:
  .asciz  "Hello ASM!"
