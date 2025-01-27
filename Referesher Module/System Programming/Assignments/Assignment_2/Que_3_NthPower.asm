section .data
  exponent dd 5
  base dd 5
  result dq 0
  
section .text
  global _start
  
_start:
  ; Load value here
  mov eax, 1
  mov ebx, [base]
  mov ecx, [exponent]
  
  ; Power finds here
loop:
  mul ebx
  dec ecx
  jnz loop
  
  mov [result], eax
  
  ;Exit condition
  mov eax, 60
  xor rdi, rdi
  syscall