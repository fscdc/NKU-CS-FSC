.arch armv8-a

.comm n, 4

.text
.align 2

.section .rodata
.align 2
str:
    .ascii "%d \00"
str1:
    .ascii "\n\00"
str2:
    .ascii "%d\00"

.text
.align 2

.global sqrt_int
.syntax unified
.fpu vfpv3-d16
sqrt_int:
    push {lr}
    vmov s15, r1
    vcvt.f64.s32 d7, s15
    vmov.f64 d0, d7
    bl sqrt
    vcvt.s32.f64 s15, d0
    vmov r2, s15
    pop {pc}

.global isPrime
.syntax unified
.fpu vfpv3-d16

@ r1是n，r3是i，r2是sqrt(n)的结果

isPrime: 
    push {r4, r5, lr}
    cmp r1, #2
    beq true
    blt false
    bl sqrt_int
    mov r3, #2
L2:
    cmp r3, r2
    bgt true
    sdiv r4, r1, r3
    mul r5, r3, r4
    sub r4, r1, r5
    cmp r4, #0
    beq false
    add r3, r3, #1
    b L2

false:
    mov r0, #0
    b ret
true:
    mov r0, #1
ret:
    pop {r4, r5, pc}

.global main
.syntax unified
.fpu vfpv3-d16
main:
    push {r4, r5, fp, lr}
    ldr r0, _bridge+8
    ldr r1, _bridge+12
    bl __isoc99_scanf
    ldr r3, _bridge+12
    ldr r5, [r3]
    mov r4, #1
L1:
    mov r1, r4
    bl isPrime
    cmp r0, #1
    bne not
    ldr r0, _bridge
    mov r1, r4
    bl printf
not:
    add r4, r4, #1
    cmp r4, r5
    ble L1
    ldr r0, _bridge+4
    bl printf
    mov r0, #0
    pop {r4, r5, fp, pc}

_bridge:
    .word str
    .word str1
    .word str2
    .word n

.section .note.GNU-stack,"",%progbits
