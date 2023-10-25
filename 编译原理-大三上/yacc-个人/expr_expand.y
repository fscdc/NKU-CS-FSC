%{
#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>//导入isdigit()函数
#include<string.h>
#ifndef YYSTYPE
#define YYSTYPE double//这里是求值所以类型是double
#endif
int yylex();//词法分析
extern int yyparse();// yyparse不断调用yylex函数来得到token的类型
FILE* yyin;//文件指针指向输入文件
void yyerror(const char* s);//错误处理函数

struct symbol//定义符号表结构
{
    char* name;//标识符名
    double value;//对应的值
};
static struct symbol sym[99];//符号表最多存99个
int count_id = 0;
%}

//TODO:给每个符号定义一个单词类别，多了一个 = 的类别
%token ADD MINUS
%token MULT DIV LPT RPT 
%token NUMBER ID
%token ASSIGN
//确定优先级,与前两个文件相同
%left ADD MINUS
%left MULT DIV
%right UMINUS         

// 声明语法规则定义部分
%%


lines   :       lines expr ';' {
                    printf("%f\n", $2);
                }
        |       lines decl ';' {//这里我额外添加了一个赋值的功能，如果识别成声明则会赋值语句，例如a=1+3;可以被识别成赋值，可以看下面的decl的规则
                    printf("标识符成功赋值为%f\n", $2);
                }
        |       lines ';'
        |
        ;

expr    :       expr ADD expr   {
                    $$ = $1 + $3;
                }
        |       expr MINUS expr   {
                    $$ = $1 - $3;
                }
        |       expr MULT expr  { 
                    $$ = $1 * $3;
                }
        |       expr DIV expr   {
                    $$ = $1 / $3;
                }
        |       LPT expr RPT    { $$=$2; }
        |       MINUS expr %prec UMINUS   {$$=-$2;}    
        |       NUMBER  {$$=$1;}
        |       ID {
                    int index = $1;
                    $$=sym[index].value;
        }
        ;
//定义声明的语法规则,将标识符和对应的值存到符号表中,index是符号表的下标
decl    :       ID ASSIGN expr     {
                    int index = $1;
                    sym[index].value = $3;
                    $$=$3;
                }
        ;



%%

// programs section

int yylex()
{
    int t;
    while(1){
        t=getchar();//从标准输入读取一个字符
        if(t==' '||t=='\t'||t=='\n'){
            ;//什么都不做直接继续读取下一个字符就实现了要求
        }else if(isdigit(t)){//这部分与expr.y的处理相同
            yylval = t - '0';
            while (isdigit(t = getchar())) {
                yylval = yylval*10+t-'0';
            }
            ungetc(t, stdin); // 将读取的字符放回输入流
            return NUMBER;//返回 `NUMBER` 标识符，表示识别出一个数字词法单元。
        }else if((t>='a'&& t<='z')||(t>='A'&&t<='Z')||(t=='_')){//检测到标识符，以大小写字母或者下划线开头
            char* name = (char*)malloc(100 * sizeof(char));//开辟空间
            int i;
            for(i=0; (t>='a'&& t<='z')||(t>='A'&&t<='Z')||(t=='_')||isdigit(t); i++)//后面跟上大小写字母或者数字或者下划线
            {
                name[i] = t;//存储标识符名字
                t = getchar();
            }
            ungetc(t, stdin); // 将读取的字符放回输入流
            name[i] = '\0';//加入结束符
            if(count_id == 0)//如果符号表为空,创建一个新条目并把标识符存入
            {
                sym[count_id].name = (char*)malloc(100 * sizeof(char));//开辟空间
                strcpy(sym[count_id].name,name);
                yylval = count_id;
                count_id++;
                return ID;
            }
            for(int i=0;i<count_id;i++)//它循环遍历符号表，查找匹配的标识符。如果找到匹配项，它将索引赋值给 `yylval` 并返回。
            {
                struct symbol curr_id = sym[i];
                if(strcmp(curr_id.name, name) == 0)
                {
                    yylval = i;
                    break;
                }
                if(i+1 == count_id)//如果到达符号表的末尾也没有找到匹配项，它创建一个新条目，并将 count_id 递增。
                {
                    sym[count_id].name = (char*)malloc(100 * sizeof(char));
                    strcpy(sym[count_id].name,name);
                    yylval = count_id;
                    count_id++;
                }
            }
            return ID;
        }
        else if(t=='+'){
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
        }else if(t=='='){
            return ASSIGN;
        }
        else{
            if(t!=';'){
            printf("存在无效符号：%c\n", t);//这里我添加了一个非法符号检测功能，可以检测出你输入表达式的第一个非法符号，提升了程序的用户便利度
            }
            return t;
        }
    }
}
//这部分与前两个y程序相同
int main(void)
{
    yyin=stdin;
    do{
        yyparse();
    }while(!feof(yyin));
    return 0;
}
void yyerror(const char* s){
    fprintf(stderr,"编译错误在: %s\n",s);
    exit(1);
}