section .data
    num1 dq 10
    num2 dq 20
    result dq 0
    msg db 'Result: ', 0   
    msg_len equ $ - msg     

section .bss
    num_str resb 20        

section .text
    global _start

_start:
    call SumNum

    mov rdi, num_str       
    mov rax, [result]      
    call int_to_string     

    mov rax, 1            
    mov rdi, 1            
    mov rsi, msg          
    mov rdx, msg_len      
    syscall

    mov rax, 1            
    mov rdi, 1            
    mov rsi, num_str      
    mov rdx, rbx          
    syscall

    mov rax, 60           
    xor rdi, rdi          
    syscall

SumNum:
    push rbp
    mov rax, [num1]       
    mov rbx, [num2]       
    add rax, rbx         
    mov [result], rax    
    pop rbp
    ret

; Converts integer in rax to a string in rdi
int_to_string:
    mov rbx, 10           
    mov rcx, num_str + 19 
    mov byte [rcx], 0     
reverse_loop:
    dec rcx               
    xor rdx, rdx          
    div rbx               
    add dl, '0'           
    mov [rcx], dl         
    test rax, rax         
    jnz reverse_loop      
    mov rbx, num_str + 19 - rcx; Calculate length of the string
    ret
