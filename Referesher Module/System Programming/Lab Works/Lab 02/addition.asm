section .data
	num1 dd 12                 ; assign 12 to num1 variable
	num2 dd 13                 ; assign 13 to num2 variable
	result dq 200		   ; assign 8bit address to the result
section .text           ; Section for code
global _start

_start:
	mov ecx, [num1]       	   ; load the value from memory location num1 to ecx
	mov edx, [num2]       	   ; load the value from memory location num2 to edx
	add ecx, edx       	   ; Add the value of edx and ecx and result stored into the ecx
	
	mov [result], ecx     	   ; move result to location present in result variable form the ecx;
	
	mov eax, 60		   ; for system call, exit
	xor edi, edi
	syscall
