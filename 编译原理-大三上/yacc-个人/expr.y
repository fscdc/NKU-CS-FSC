%{
#include<stdio.h>
#include<stdlib.h>
#include <ctype.h>  //导入isdigit()函数

#ifndef YYSTYPE
// 用于确定$$的变量类型，由于返回的是简单表达式计算结果，因此定义为double类型，除法就会产生小数
#define YYSTYPE double 
#endif
int yylex();//词法分析
extern int yyparse();// yyparse不断调用yylex函数来得到token的类型
FILE* yyin;//文件指针指向输入文件
void yyerror(const char* s);//错误处理函数
%}


//给每个符号定义一个单词类别
%token ADD MINUS
%token MULT DIV LPT RPT 
%token NUMBER
//优先级定义
%left ADD MINUS
%left MULT DIV
%right UMINUS // 取负，这个优先级最高

// 声明语法规则定义部分
%%

// 处理输入的一行以分号结束的简单表达式
lines :    lines expr ';' { printf("%f\n", $2); } 
      |    lines ';'
      |
      ;

expr  :    expr ADD expr  { $$ = $1 + $3; } // $$代表产生式左部的属性值，$n 为产生式右部第n个token的属性值
      |    expr MINUS expr  { $$ = $1 - $3; }
      |    expr MULT expr  { $$ = $1 * $3; }
      |    expr DIV expr  { $$ = $1 / $3; }
      |    LPT expr RPT   { $$ = $2; }
      |    MINUS expr %prec UMINUS  { $$ =-$2; }  // %prec 提升优先级
      |    NUMBER { $$ = $1; }
      ;
%%


// yylex函数：实现词法分析功能
int yylex()
{
    int t;
    while (1) {
        t = getchar();//从标准输入读取一个字符
        if (t==' ' || t=='\t' || t=='\n'){
            ;// 什么都不做直接继续读取下一个字符就实现了要求
        }
        else if (isdigit(t)) {//这个地方由于这里是求数值即可，所以直接将原来的数字×10，然后加上新数字的数值即可，会自动去掉前面的无意义的0。
            yylval = 0;
            while (isdigit(t)) {
                yylval = yylval * 10 + t - '0';//将获得的数值传给yylval，这是存储词法分析器返回的词法单元的值，
            //当词法分析器识别出一个token，它会将该标记的值存储在 yylval 中。解析器会从
            // yylval 中读取这些值，以便在语法分析过程中获取标记的语义信息。
                t = getchar();
            }
            // 将读取的字符放回输入流
            ungetc(t, stdin);
            return NUMBER;//返回number类型，代表是数字
        }
        else if(t=='+') {
            return ADD;  
        }
        else if(t=='-'){
            return MINUS;
        }
        else if(t=='*'){
            return MULT;
        }
        else if(t=='/'){
            return DIV;
        }
        else if(t=='('){
            return LPT;
        }
        else if(t==')'){
            return RPT;
        }
        else {
            if(t!=';'){
            printf("存在无效符号：%c\n", t);//这里我添加了一个非法符号检测功能，可以检测出你输入表达式的第一个非法符号，提升了程序的用户便利度
            }
            return t;
        }
    }
}

int main(void)
{
    yyin = stdin;
    //feof函数检查是否到输入文件结尾
    do{
        yyparse();//调用yyparse函数对完整输入进行一次解析
    } while(!feof(yyin));
    return 0;
}

// 报错函数被yyparse()调用，以便在遇到错误时汇报错误
void yyerror(const char* s){
    fprintf(stderr, "解析错误在: %s\n", s);
    exit(1);
}