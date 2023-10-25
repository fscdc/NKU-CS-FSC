.PHONY: test-prime, test-fibo ,clean-prime,clean-fibo
test-prime:
	arm-linux-gnueabihf-gcc prime.s -o prime.out -lm
	qemu-arm -L /usr/arm-linux-gnueabihf ./prime.out
test-fibo:
	arm-linux-gnueabihf-gcc fibo.s -o fibo.out 
	qemu-arm -L /usr/arm-linux-gnueabihf ./fibo.out
clean-prime:
	rm -fr prime.out
clean-fibo:
	rm -fr fibo.out