
factorial.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <main>:
   0:	55                   	push   %rbp
   1:	48 89 e5             	mov    %rsp,%rbp
   4:	48 83 ec 20          	sub    $0x20,%rsp
   8:	c7 45 ec 00 00 00 00 	movl   $0x0,-0x14(%rbp)
   f:	c7 45 f0 e8 03 00 00 	movl   $0x3e8,-0x10(%rbp)
  16:	8b 75 f0             	mov    -0x10(%rbp),%esi
  19:	48 bf 00 00 00 00 00 	movabs $0x0,%rdi
  20:	00 00 00 
  23:	b0 00                	mov    $0x0,%al
  25:	e8 00 00 00 00       	call   2a <main+0x2a>
  2a:	48 bf 00 00 00 00 00 	movabs $0x0,%rdi
  31:	00 00 00 
  34:	48 8d 75 f4          	lea    -0xc(%rbp),%rsi
  38:	b0 00                	mov    $0x0,%al
  3a:	e8 00 00 00 00       	call   3f <main+0x3f>
  3f:	c7 45 fc 02 00 00 00 	movl   $0x2,-0x4(%rbp)
  46:	c7 45 f8 01 00 00 00 	movl   $0x1,-0x8(%rbp)
  4d:	8b 45 fc             	mov    -0x4(%rbp),%eax
  50:	3b 45 f4             	cmp    -0xc(%rbp),%eax
  53:	7f 15                	jg     6a <main+0x6a>
  55:	8b 45 f8             	mov    -0x8(%rbp),%eax
  58:	0f af 45 fc          	imul   -0x4(%rbp),%eax
  5c:	89 45 f8             	mov    %eax,-0x8(%rbp)
  5f:	8b 45 fc             	mov    -0x4(%rbp),%eax
  62:	83 c0 01             	add    $0x1,%eax
  65:	89 45 fc             	mov    %eax,-0x4(%rbp)
  68:	eb e3                	jmp    4d <main+0x4d>
  6a:	8b 75 f8             	mov    -0x8(%rbp),%esi
  6d:	48 bf 00 00 00 00 00 	movabs $0x0,%rdi
  74:	00 00 00 
  77:	b0 00                	mov    $0x0,%al
  79:	e8 00 00 00 00       	call   7e <main+0x7e>
  7e:	31 c0                	xor    %eax,%eax
  80:	48 83 c4 20          	add    $0x20,%rsp
  84:	5d                   	pop    %rbp
  85:	c3                   	ret    
