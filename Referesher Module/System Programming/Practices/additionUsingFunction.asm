section .data
	num1  dd 10        ; num1 = 10
	num2  dd 15        ; num2 = 15
	result dd 0        ; result = 0 (initialize 0)

section .text
	global _start

addition:             ; Addition function
	; load variable value into the registers
	mov eax, [num1]
	mov ecx, [num2]

	add eax, ecx        ; Add ecx to eax and store result stored in eax
	ret                 ; Return from the function

_start:
	call addition        ; Call the addition function
	mov [result], eax   ; Store the result from eax into result

	; exit program code
	mov eax, 60   
	xor edi, edi 
	syscall 