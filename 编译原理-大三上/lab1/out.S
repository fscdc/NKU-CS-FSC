	.text
	.file	"llvm-link"
	.globl	getarea                         # -- Begin function getarea
	.p2align	4, 0x90
	.type	getarea,@function
getarea:                                # @getarea
	.cfi_startproc
# %bb.0:                                # %entry
	movq	pi@GOTPCREL(%rip), %rax
	mulss	%xmm0, %xmm0
	mulss	(%rax), %xmm0
	retq
.Lfunc_end0:
	.size	getarea, .Lfunc_end0-getarea
	.cfi_endproc
                                        # -- End function
	.section	.rodata.cst4,"aM",@progbits,4
	.p2align	2                               # -- Begin function main
.LCPI1_0:
	.long	0x40000000                      # float 2
.LCPI1_1:
	.long	0x42c80000                      # float 100
.LCPI1_2:
	.long	0x43160000                      # float 150
	.text
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	subq	$56, %rsp
	.cfi_def_cfa_offset 64
	movl	$10, 4(%rsp)
	callq	getint
	movl	%eax, 12(%rsp)
	cvtsi2ss	%eax, %xmm0
	divss	.LCPI1_0(%rip), %xmm0
	movss	%xmm0, 8(%rsp)
	movl	$10, 32(%rsp)
	movl	$5, 16(%rsp)
	callq	getarea@PLT
	movss	%xmm0, (%rsp)
	movss	.LCPI1_1(%rip), %xmm0           # xmm0 = mem[0],zero,zero,zero
	movss	.LCPI1_2(%rip), %xmm1           # xmm1 = mem[0],zero,zero,zero
	.p2align	4, 0x90
.LBB1_1:                                # %loop
                                        # =>This Inner Loop Header: Depth=1
	cmpl	$0, 4(%rsp)
	jle	.LBB1_4
# %bb.2:                                # %loop_body
                                        #   in Loop: Header=BB1_1 Depth=1
	xorps	%xmm2, %xmm2
	cvtsi2ssl	32(%rsp), %xmm2
	addss	(%rsp), %xmm2
	movss	%xmm2, (%rsp)
	ucomiss	%xmm0, %xmm2
	jbe	.LBB1_1
# %bb.3:                                # %loop_body
                                        #   in Loop: Header=BB1_1 Depth=1
	ucomiss	%xmm2, %xmm1
	jbe	.LBB1_1
.LBB1_4:                                # %loop_end
	cvttss2si	(%rsp), %edi
	movq	a@GOTPCREL(%rip), %rax
	addl	16(%rsp), %edi
	addl	(%rax), %edi
	callq	putint
	xorl	%eax, %eax
	addq	$56, %rsp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc
                                        # -- End function
	.globl	getint                          # -- Begin function getint
	.p2align	4, 0x90
	.type	getint,@function
getint:                                 # @getint
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movabsq	$.L.str, %rdi
	leaq	-4(%rbp), %rsi
	movb	$0, %al
	callq	__isoc99_scanf@PLT
	movl	-4(%rbp), %eax
	addq	$16, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end2:
	.size	getint, .Lfunc_end2-getint
	.cfi_endproc
                                        # -- End function
	.globl	getch                           # -- Begin function getch
	.p2align	4, 0x90
	.type	getch,@function
getch:                                  # @getch
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movabsq	$.L.str.1, %rdi
	leaq	-1(%rbp), %rsi
	movb	$0, %al
	callq	__isoc99_scanf@PLT
	movsbl	-1(%rbp), %eax
	addq	$16, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end3:
	.size	getch, .Lfunc_end3-getch
	.cfi_endproc
                                        # -- End function
	.globl	getarray                        # -- Begin function getarray
	.p2align	4, 0x90
	.type	getarray,@function
getarray:                               # @getarray
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -16(%rbp)
	movabsq	$.L.str, %rdi
	leaq	-8(%rbp), %rsi
	movb	$0, %al
	callq	__isoc99_scanf@PLT
	movl	$0, -4(%rbp)
.LBB4_1:                                # =>This Inner Loop Header: Depth=1
	movl	-4(%rbp), %eax
	cmpl	-8(%rbp), %eax
	jge	.LBB4_4
# %bb.2:                                #   in Loop: Header=BB4_1 Depth=1
	movq	-16(%rbp), %rsi
	movslq	-4(%rbp), %rax
	shlq	$2, %rax
	addq	%rax, %rsi
	movabsq	$.L.str, %rdi
	movb	$0, %al
	callq	__isoc99_scanf@PLT
# %bb.3:                                #   in Loop: Header=BB4_1 Depth=1
	movl	-4(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -4(%rbp)
	jmp	.LBB4_1
.LBB4_4:
	movl	-8(%rbp), %eax
	addq	$16, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end4:
	.size	getarray, .Lfunc_end4-getarray
	.cfi_endproc
                                        # -- End function
	.globl	putint                          # -- Begin function putint
	.p2align	4, 0x90
	.type	putint,@function
putint:                                 # @putint
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movl	%edi, -4(%rbp)
	movl	-4(%rbp), %esi
	movabsq	$.L.str, %rdi
	movb	$0, %al
	callq	printf@PLT
	addq	$16, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end5:
	.size	putint, .Lfunc_end5-putint
	.cfi_endproc
                                        # -- End function
	.globl	putch                           # -- Begin function putch
	.p2align	4, 0x90
	.type	putch,@function
putch:                                  # @putch
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movl	%edi, -4(%rbp)
	movl	-4(%rbp), %esi
	movabsq	$.L.str.1, %rdi
	movb	$0, %al
	callq	printf@PLT
	addq	$16, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end6:
	.size	putch, .Lfunc_end6-putch
	.cfi_endproc
                                        # -- End function
	.globl	putarray                        # -- Begin function putarray
	.p2align	4, 0x90
	.type	putarray,@function
putarray:                               # @putarray
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movl	%edi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movl	-8(%rbp), %esi
	movabsq	$.L.str.2, %rdi
	movb	$0, %al
	callq	printf@PLT
	movl	$0, -4(%rbp)
.LBB7_1:                                # =>This Inner Loop Header: Depth=1
	movl	-4(%rbp), %eax
	cmpl	-8(%rbp), %eax
	jge	.LBB7_4
# %bb.2:                                #   in Loop: Header=BB7_1 Depth=1
	movq	-16(%rbp), %rax
	movslq	-4(%rbp), %rcx
	movl	(%rax,%rcx,4), %esi
	movabsq	$.L.str.3, %rdi
	movb	$0, %al
	callq	printf@PLT
# %bb.3:                                #   in Loop: Header=BB7_1 Depth=1
	movl	-4(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -4(%rbp)
	jmp	.LBB7_1
.LBB7_4:
	movabsq	$.L.str.4, %rdi
	movb	$0, %al
	callq	printf@PLT
	addq	$16, %rsp
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end7:
	.size	putarray, .Lfunc_end7-putarray
	.cfi_endproc
                                        # -- End function
	.type	a,@object                       # @a
	.data
	.globl	a
	.p2align	2
a:
	.long	5                               # 0x5
	.size	a, 4

	.type	pi,@object                      # @pi
	.section	.rodata,"a",@progbits
	.globl	pi
	.p2align	2
pi:
	.long	0x40490fda                      # float 3.1415925
	.size	pi, 4

	.type	.L.str,@object                  # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"%d"
	.size	.L.str, 3

	.type	.L.str.1,@object                # @.str.1
.L.str.1:
	.asciz	"%c"
	.size	.L.str.1, 3

	.type	.L.str.2,@object                # @.str.2
.L.str.2:
	.asciz	"%d:"
	.size	.L.str.2, 4

	.type	.L.str.3,@object                # @.str.3
.L.str.3:
	.asciz	" %d"
	.size	.L.str.3, 4

	.type	.L.str.4,@object                # @.str.4
.L.str.4:
	.asciz	"\n"
	.size	.L.str.4, 2

	.ident	"Ubuntu clang version 14.0.0-1ubuntu1.1"
	.section	".note.GNU-stack","",@progbits
