.PHONY: expr,expr_final,expr_expand,expr_2asm, clean
expr:
	bison -d expr.y
	gcc -o expr.out expr.tab.c
	./expr.out

expr_final:
	bison -d expr_final.y
	gcc -o expr_final.out expr_final.tab.c
	./expr_final.out

expr_expand:
	bison -d expr_expand.y
	gcc -o expr_expand.out expr_expand.tab.c
	./expr_expand.out

expr_2asm:
	bison -d expr_2asm.y
	gcc -o expr_2asm.out expr_2asm.tab.c
	./expr_2asm.out	

test:
	arm-linux-gnueabihf-gcc test.s -o test.out
	qemu-arm -L /usr/arm-linux-gnueabihf ./test.out
clean:
	rm -fr *.out
