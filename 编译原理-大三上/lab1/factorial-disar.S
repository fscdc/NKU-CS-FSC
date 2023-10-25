
factorial:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <_init>:
    1000:	f3 0f 1e fa          	endbr64 
    1004:	48 83 ec 08          	sub    $0x8,%rsp
    1008:	48 8b 05 d9 2f 00 00 	mov    0x2fd9(%rip),%rax        # 3fe8 <__gmon_start__@Base>
    100f:	48 85 c0             	test   %rax,%rax
    1012:	74 02                	je     1016 <_init+0x16>
    1014:	ff d0                	call   *%rax
    1016:	48 83 c4 08          	add    $0x8,%rsp
    101a:	c3                   	ret    

Disassembly of section .plt:

0000000000001020 <printf@plt-0x10>:
    1020:	ff 35 92 2f 00 00    	push   0x2f92(%rip)        # 3fb8 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	ff 25 94 2f 00 00    	jmp    *0x2f94(%rip)        # 3fc0 <_GLOBAL_OFFSET_TABLE_+0x10>
    102c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000000001030 <printf@plt>:
    1030:	ff 25 92 2f 00 00    	jmp    *0x2f92(%rip)        # 3fc8 <printf@GLIBC_2.2.5>
    1036:	68 00 00 00 00       	push   $0x0
    103b:	e9 e0 ff ff ff       	jmp    1020 <_init+0x20>

0000000000001040 <__isoc99_scanf@plt>:
    1040:	ff 25 8a 2f 00 00    	jmp    *0x2f8a(%rip)        # 3fd0 <__isoc99_scanf@GLIBC_2.7>
    1046:	68 01 00 00 00       	push   $0x1
    104b:	e9 d0 ff ff ff       	jmp    1020 <_init+0x20>

Disassembly of section .plt.got:

0000000000001050 <__cxa_finalize@plt>:
    1050:	ff 25 a2 2f 00 00    	jmp    *0x2fa2(%rip)        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    1056:	66 90                	xchg   %ax,%ax

Disassembly of section .text:

0000000000001060 <_start>:
    1060:	f3 0f 1e fa          	endbr64 
    1064:	31 ed                	xor    %ebp,%ebp
    1066:	49 89 d1             	mov    %rdx,%r9
    1069:	5e                   	pop    %rsi
    106a:	48 89 e2             	mov    %rsp,%rdx
    106d:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
    1071:	50                   	push   %rax
    1072:	54                   	push   %rsp
    1073:	45 31 c0             	xor    %r8d,%r8d
    1076:	31 c9                	xor    %ecx,%ecx
    1078:	48 8d 3d d1 00 00 00 	lea    0xd1(%rip),%rdi        # 1150 <main>
    107f:	ff 15 53 2f 00 00    	call   *0x2f53(%rip)        # 3fd8 <__libc_start_main@GLIBC_2.34>
    1085:	f4                   	hlt    
    1086:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
    108d:	00 00 00 

0000000000001090 <deregister_tm_clones>:
    1090:	48 8d 3d 79 2f 00 00 	lea    0x2f79(%rip),%rdi        # 4010 <__TMC_END__>
    1097:	48 8d 05 72 2f 00 00 	lea    0x2f72(%rip),%rax        # 4010 <__TMC_END__>
    109e:	48 39 f8             	cmp    %rdi,%rax
    10a1:	74 15                	je     10b8 <deregister_tm_clones+0x28>
    10a3:	48 8b 05 36 2f 00 00 	mov    0x2f36(%rip),%rax        # 3fe0 <_ITM_deregisterTMCloneTable@Base>
    10aa:	48 85 c0             	test   %rax,%rax
    10ad:	74 09                	je     10b8 <deregister_tm_clones+0x28>
    10af:	ff e0                	jmp    *%rax
    10b1:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
    10b8:	c3                   	ret    
    10b9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000000000010c0 <register_tm_clones>:
    10c0:	48 8d 3d 49 2f 00 00 	lea    0x2f49(%rip),%rdi        # 4010 <__TMC_END__>
    10c7:	48 8d 35 42 2f 00 00 	lea    0x2f42(%rip),%rsi        # 4010 <__TMC_END__>
    10ce:	48 29 fe             	sub    %rdi,%rsi
    10d1:	48 89 f0             	mov    %rsi,%rax
    10d4:	48 c1 ee 3f          	shr    $0x3f,%rsi
    10d8:	48 c1 f8 03          	sar    $0x3,%rax
    10dc:	48 01 c6             	add    %rax,%rsi
    10df:	48 d1 fe             	sar    %rsi
    10e2:	74 14                	je     10f8 <register_tm_clones+0x38>
    10e4:	48 8b 05 05 2f 00 00 	mov    0x2f05(%rip),%rax        # 3ff0 <_ITM_registerTMCloneTable@Base>
    10eb:	48 85 c0             	test   %rax,%rax
    10ee:	74 08                	je     10f8 <register_tm_clones+0x38>
    10f0:	ff e0                	jmp    *%rax
    10f2:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
    10f8:	c3                   	ret    
    10f9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000001100 <__do_global_dtors_aux>:
    1100:	f3 0f 1e fa          	endbr64 
    1104:	80 3d 05 2f 00 00 00 	cmpb   $0x0,0x2f05(%rip)        # 4010 <__TMC_END__>
    110b:	75 2b                	jne    1138 <__do_global_dtors_aux+0x38>
    110d:	55                   	push   %rbp
    110e:	48 83 3d e2 2e 00 00 	cmpq   $0x0,0x2ee2(%rip)        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    1115:	00 
    1116:	48 89 e5             	mov    %rsp,%rbp
    1119:	74 0c                	je     1127 <__do_global_dtors_aux+0x27>
    111b:	48 8b 3d e6 2e 00 00 	mov    0x2ee6(%rip),%rdi        # 4008 <__dso_handle>
    1122:	e8 29 ff ff ff       	call   1050 <__cxa_finalize@plt>
    1127:	e8 64 ff ff ff       	call   1090 <deregister_tm_clones>
    112c:	c6 05 dd 2e 00 00 01 	movb   $0x1,0x2edd(%rip)        # 4010 <__TMC_END__>
    1133:	5d                   	pop    %rbp
    1134:	c3                   	ret    
    1135:	0f 1f 00             	nopl   (%rax)
    1138:	c3                   	ret    
    1139:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000001140 <frame_dummy>:
    1140:	f3 0f 1e fa          	endbr64 
    1144:	e9 77 ff ff ff       	jmp    10c0 <register_tm_clones>
    1149:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000001150 <main>:
    1150:	55                   	push   %rbp
    1151:	48 89 e5             	mov    %rsp,%rbp
    1154:	48 83 ec 20          	sub    $0x20,%rsp
    1158:	c7 45 ec 00 00 00 00 	movl   $0x0,-0x14(%rbp)
    115f:	c7 45 f0 e8 03 00 00 	movl   $0x3e8,-0x10(%rbp)
    1166:	8b 75 f0             	mov    -0x10(%rbp),%esi
    1169:	48 bf 04 20 00 00 00 	movabs $0x2004,%rdi
    1170:	00 00 00 
    1173:	b0 00                	mov    $0x0,%al
    1175:	e8 b6 fe ff ff       	call   1030 <printf@plt>
    117a:	48 bf 08 20 00 00 00 	movabs $0x2008,%rdi
    1181:	00 00 00 
    1184:	48 8d 75 f4          	lea    -0xc(%rbp),%rsi
    1188:	b0 00                	mov    $0x0,%al
    118a:	e8 b1 fe ff ff       	call   1040 <__isoc99_scanf@plt>
    118f:	c7 45 fc 02 00 00 00 	movl   $0x2,-0x4(%rbp)
    1196:	c7 45 f8 01 00 00 00 	movl   $0x1,-0x8(%rbp)
    119d:	8b 45 fc             	mov    -0x4(%rbp),%eax
    11a0:	3b 45 f4             	cmp    -0xc(%rbp),%eax
    11a3:	7f 15                	jg     11ba <main+0x6a>
    11a5:	8b 45 f8             	mov    -0x8(%rbp),%eax
    11a8:	0f af 45 fc          	imul   -0x4(%rbp),%eax
    11ac:	89 45 f8             	mov    %eax,-0x8(%rbp)
    11af:	8b 45 fc             	mov    -0x4(%rbp),%eax
    11b2:	83 c0 01             	add    $0x1,%eax
    11b5:	89 45 fc             	mov    %eax,-0x4(%rbp)
    11b8:	eb e3                	jmp    119d <main+0x4d>
    11ba:	8b 75 f8             	mov    -0x8(%rbp),%esi
    11bd:	48 bf 04 20 00 00 00 	movabs $0x2004,%rdi
    11c4:	00 00 00 
    11c7:	b0 00                	mov    $0x0,%al
    11c9:	e8 62 fe ff ff       	call   1030 <printf@plt>
    11ce:	31 c0                	xor    %eax,%eax
    11d0:	48 83 c4 20          	add    $0x20,%rsp
    11d4:	5d                   	pop    %rbp
    11d5:	c3                   	ret    

Disassembly of section .fini:

00000000000011d8 <_fini>:
    11d8:	f3 0f 1e fa          	endbr64 
    11dc:	48 83 ec 08          	sub    $0x8,%rsp
    11e0:	48 83 c4 08          	add    $0x8,%rsp
    11e4:	c3                   	ret    
