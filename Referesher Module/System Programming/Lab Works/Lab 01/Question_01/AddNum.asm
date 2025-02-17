section .data           ; Section for initialized data
a dd 15                 ; Define a 32-bit integer and initialize it to 1
b dd 35                 ; Define a 32-bit integer and initialize it to 4
sum dd 0			; Define initial value of sum is 0

section .text           ; Section for code
global _start           ; Make the _start label accessible from outside

_start:
    ; Load the values from memory into registers
    mov eax, [a]       ; Move the value at memory location 'a' into EAX
    mov ebx, [b]       ; Move the value at memory location 'b' into EBX

    ; Perform addition
    add eax, ebx       ; Add the value in EBX to EAX

    ; Store the result back to memory
    mov [sum], eax       ; Move the result in EAX back into memory location 'a'






