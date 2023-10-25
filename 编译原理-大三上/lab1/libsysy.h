#ifndef __SYLIB_H_
#define __SYLIB_H_

#include<stdio.h>
#include<stdarg.h>
#include<sys/time.h>
/* Input & output functions */
int getint(),getch(),getarray(int a[]);
void putint(int a),putch(int a),putarray(int n,int a[]);
#endif
