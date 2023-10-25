#include<stdio.h>
#include <sys/time.h>

int main()
{  

    int n ;
    int a[1000];
    const int count = 1000;
    scanf("%d", &n);

    struct timeval start, end;
    long int time_taken;
    
    for(int i=0;i<n;i++)
    {
        a[i] = i+1;
    }

    // 获取计时开始时间
    gettimeofday(&start, NULL);

    int sum = 0;
    for(int it = 0;it<count;it++)
    {
        sum = 0;
        for(int i=0;i<n;i++)
        {
            sum+=a[i];
        }
    }
    printf("%d",sum);

    // 获取计时结束时间
    gettimeofday(&end, NULL);

    // 计算时间差
    time_taken = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_usec - start.tv_usec);

    // 输出计时结果
    printf("Time taken: %ld microseconds\n", time_taken);
    return 0;
}