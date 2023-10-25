#include <stdio.h>
#define MIN 0.001
#define MAX 1000

//FSC的编译原理第一次实验-阶乘代码

int main(){
    int k=MIN+MAX;//添加代码，验证宏定义在预处理阶段的进程 
    printf("%d\n",k);
    int i, n, f;
    scanf("%d", &n);
    i = 2;
    f = 1;
    while(i <= n){
        f = f * i;
        i = i + 1;
    }
    if (0 == 1){//死代码
        printf("fool");
    }
    printf("%d\n", f);
    return 0;
}
