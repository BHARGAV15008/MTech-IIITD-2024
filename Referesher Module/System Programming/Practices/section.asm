section .data
    a dd 10
    b dd 5
    result dd 0

section .text
global _start

sum:
    mov eax, [a]
    mov ebx, [b]
    add eax, bax
    mov [result], eax
    ret

_start
    call sum

    ;exit
    mov eax, 60
    xor rdi, rdi
    syscall

