#include<stdio.h>
#include"libsysy.h"
/* Input & output functions */
int getint(){int t; scanf("%d",&t); return t; }
int getch(){char c; scanf("%c",&c); return (int)c; }
int getarray(int a[]){
    int n;
    scanf("%d",&n);
    for(int i=0;i<n;i++)scanf("%d",&a[i]);
    return n;
}
void putint(int a){ printf("%d",a);}
void putch(int a){ printf("%c",a); }
void putarray(int n,int a[]){
    printf("%d:",n);
    for(int i=0;i<n;i++)printf(" %d",a[i]);
    printf("\n");
}


