%{
/*********************************************
**********************************************/
#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>//导入isdigit()函数
#include<string.h>
//条件编译指令，确保YYSTYPE没被定义，没有定义则被定义成‘char*’类型，因为返回的是字符串
//其中 YYSTYPE 用于确定 $$ 变量类型
#ifndef YYSTYPE
#define YYSTYPE char*
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
//优先级定义，单目运算负号最高的优先级
%left ADD MINUS
%left MULT DIV
%right UMINUS         
//声明语法规则定义部分
%%

// 处理输入的一行以分号结束的简单表达式
lines   :       lines expr ';' {
                    printf("%s\n", $2);
                }
        |       lines ';'
        |
        ;
//TODO:完善表达式的规则
expr    :       expr ADD expr   {
                    int len = strlen($1) + strlen($3) + 2;//+2 是为了包括最后的加号和字符串的终止字符 \0
                    $$ = (char*)malloc(len * sizeof(char));//这里我选择了使用精确分配内存，而不是直接预设一个较大的空间，这样可以更节省空间
                    strcpy($$, $1);//把第一个expr放入结果
                    strcat($$, $3); //把第二个expr追加到结果中
                    strcat($$, "+ ");//把加号追加进去，这地方后面加了一个空格，可以更清晰表达后缀表达式
                }
        |       expr MINUS expr   {
                    int len = strlen($1) + strlen($3) + 2;
                    $$ = (char*)malloc(len * sizeof(char));
                    strcpy($$, $1);
                    strcat($$, $3); 
                    strcat($$, "- ");
                }
        |       expr MULT expr  { 
                    int len = strlen($1) + strlen($3) + 2;
                    $$ = (char*)malloc(len * sizeof(char));
                    strcpy($$, $1);
                    strcat($$, $3); 
                    strcat($$, "* ");
                }
        |       expr DIV expr   {
                    int len = strlen($1) + strlen($3) + 2;
                    $$ = (char*)malloc(len * sizeof(char));
                    strcpy($$, $1);
                    strcat($$, $3); 
                    strcat($$, "/ ");
                }
        |       LPT expr RPT    { $$=$2; }
        |       MINUS expr %prec UMINUS   {// %prec 提升优先级
                    int len = strlen($2) + 2;
                    $$ = (char*)malloc(len * sizeof(char));
                    strcpy($$,"-");//这里没有加上空格，是为了在后缀表达式中可以体现减号和单目运算符-的不同
                    strcat($$,$2);
                }  //处理单目运算符 - 
        |       NUMBER  {//处理数字就是直接赋值
                    $$= (char*)malloc(strlen($1));
                    strcpy($$,$1);}
        ;

%%


// yylex函数：实现词法分析功能
int yylex()
{
    int t;
    while(1){
        t=getchar();//从标准输入读取一个字符
        if(t==' '||t=='\t'||t=='\n'){
            ;//什么都不做直接继续读取下一个字符就实现了要求
        }else if(isdigit(t)){
            //解析多位数字返回数字类型
            char* num = (char*)malloc(100 * sizeof(char));//预设一个较大的空间，因为不知道这个数字有多长，100肯定够用了
            num[0] = t;
            int i=1;
            while (isdigit(t = getchar())) {//循环将是数字的所有字符都存到num指向的字符数组中
                num[i] = t;
                i++;
            }
            ungetc(t, stdin); // 将读取的字符放回输入流
            num[i+1] = '\0';//结尾加个结束符
            //这部分我进行了一个简单的小扩展,就是把开头是0但是后面有非零的多位数字前面的无意义的0去掉,例如0990经过程序后会变成990，由于这里是字符串，所以这种情况需要我单独进行处理
            int start_idx = 0;
            while (num[start_idx] == '0' && num[start_idx + 1] != '\0') {//寻找前面有多少个无意义的0的个数(也可以代表位置)
                start_idx++;
            }
            for(int j = 0; start_idx + j < i; j++) {//将整体前移覆盖掉无意义0的部分
                num[j] = num[start_idx + j];
            }
            num[i - start_idx] = ' ';//结尾添加一个空格
            num[i - start_idx+1] = '\0';//再加一个结束符
            yylval = num;//将获得的数字传给yylval，这是存储词法分析器返回的词法单元的值，
            //当词法分析器识别出一个token，它会将该标记的值存储在 yylval 中。解析器会从
            // yylval 中读取这些值，以便在语法分析过程中获取标记的语义信息。
            return NUMBER;//返回number类型，代表是数字
        //识别其他符号
        }else if(t=='+'){
            return ADD;
        }else if(t=='-'){
            return MINUS;
        }
        else if(t=='*'){
            return MULT;
        }else if(t=='/'){
            return DIV;
        }else if(t=='('){
            return LPT;
        }else if(t==')'){
            return RPT;
        }
        else{
            if(t!=';'){
            printf("存在无效符号：%c\n", t);//这里我添加了一个非法符号检测功能，可以检测出你输入表达式的第一个非法符号，提升了程序的用户便利度
            }
            return t;
        }
    }
}

int main(void)
{
    yyin=stdin;
    do{
        yyparse();//调用yyparse函数对完整输入进行一次解析
    }while(!feof(yyin));//feof函数检查是否到输入文件结尾
    return 0;
}
//错误处理函数
void yyerror(const char* s){
    fprintf(stderr,"解析错误在: %s\n",s);
    exit(1);
}