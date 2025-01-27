section .data
    result dq 0

section .text
    global _start

_start:
    mov rdi, 10           ; n = 10

    mov rax, 0            ; a = 0
    mov rbx, 1            ; b = 1

    cmp rdi, 0
    je .done
    cmp rdi, 1
    je .set_bx

    sub rdi, 1

.loop:
    add rax, rbx
    xchg rax, rbx
    dec rdi
    jnz .loop

.done:
    mov [result], rbx

    mov rax, 60
    xor rdi, rdi
    syscall
