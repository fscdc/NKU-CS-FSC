%{
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>//导入isdigit()函数
#include <string.h>
#define Mreg 8//存标识符的寄存器和最多用8个寄存器，这也是临时寄存器的数量，这里由于只是一个简单的实现，不考虑使用到过多的寄存器，实际上寄存器的分配是十分复杂的。
int yylex();
extern int yyparse(); // 该函数会一直调用 yylex，由 Bison 实现
FILE* yyin;
void yyerror(const char* s);



//这里需要记录标识符名字对应的寄存器
typedef struct VarNode {
    char* name;
    int reg;
    struct VarNode* next;//这里我后续打算用链表去链接，所以要定义一个next指针
} VarNode;

VarNode* symfirst = NULL; // 头指针

// 记录使用过的寄存器
int usereg[Mreg] = {0};
int expr_usereg[Mreg] = {0};


int search_reg(char* name);
int add_reg(char* name);
%}


%union {//使用 union 定义 yylval 的类型替代YYSTYPE，让yylval 可以是下面的任意一种类型
    int intv; // 这里将 double 改为了 int，因为识别的是整数，要显示在汇编代码里面
    // 使用结构体，同时具备两个属性值
    struct {
        char codechar[256]; // 现在它用来存储生成的汇编代码
        int reg;  // 表达式结果寄存器对应的编号
    } code;
}

// 给每个符号定义一个单词类别。
%token ADD MINUS
%token MUL DIV LPT RPT
//%token NUMBER
%token ASSIGN


%token <intv> NUMBER //识别到数字则返回给union中的intv里面去
%token <code> VAR //这意味着当词法分析器识别到一个标识符时，它将把生成的汇编代码存储在 yylval 结构体的 codechar 成员中，并将寄存器编号存储在 reg 成员中，以便语法分析器可以使用。
//在语法规则中，生成的语法树节点（或中间代码）的属性类型将为 code
%type <code> expr
%type <code> stmt
//定义优先级
%left ADD MINUS
%left MUL DIV
%right UMINUS

%%

//在这个部分我重新设计的产生式规则，stmt 替换原来的 expr，它除了表达式还包括赋值语句
lines   :       lines stmt ';' {
                    printf("    .text\n    .globl main\nmain:\n");
                    printf("%s", $2.codechar);
                    // 清空 expr_usereg
                    memset(expr_usereg, 0, sizeof(expr_usereg));
                }
        |       lines ';'
        |
        ;

stmt    :       VAR ASSIGN expr {
                    int reg = search_reg($1.codechar);
                    if (reg == -1) {//如果没找到，则给他分配一个寄存器
                        reg = add_reg($1.codechar);
                    }
                    // 设置属性
                    memset($1.codechar, 0, sizeof($1.codechar));
                    $1.reg = reg;
                    // 先计算 expr，再从结果寄存器中取出给 VAR 对应的寄存器
                    snprintf($$.codechar, 1000,"%sMOV R%d, R%d\n", $3.codechar, $1.reg, $3.reg);
                } 
        |       expr { $$ = $1; }
        ;

expr    :       VAR {
                    // 找未分配的寄存器
                    int reg = search_reg($1.codechar);
                    if (reg == -1) {
                        reg = add_reg($1.codechar);
                    }

                    // 直接设置
                    memset($$.codechar, 0, sizeof($$.codechar));
                    $$.reg = reg;
                }
        |       expr ADD expr   {
                    // 找未保存变量的寄存器
                    int i;
                    for (i = 0; i < Mreg; i++) {
                        if (!usereg[i] && !expr_usereg[i]) {
                            $$.reg = i;
                            break;
                        }
                    }

                    expr_usereg[i] = 1;

                    snprintf($$.codechar, 1000, "%s%sADD R%d, R%d, R%d\n", $1.codechar, $3.codechar, $$.reg, $1.reg, $3.reg);
                }
        |       expr MINUS expr {
                    // 找未保存变量的寄存器
                    int i;
                    for (i = 0; i < Mreg; i++) {
                        if (!usereg[i] && !expr_usereg[i]) {
                            $$.reg = i;
                            break;
                        }
                    }

                    expr_usereg[i] = 1;

                    snprintf($$.codechar, 1000, "%s%sSUB R%d, R%d, R%d\n", $1.codechar, $3.codechar, $$.reg, $1.reg, $3.reg);
                }
        |       expr MUL expr   {
                    // 找未保存变量的寄存器
                    int i;
                    for (i = 0; i < Mreg; i++) {
                        if (!usereg[i] && !expr_usereg[i]) {
                            $$.reg = i;
                            break;
                        }
                    }

                    expr_usereg[i] = 1;

                    snprintf($$.codechar, 1000, "%s%sMUL R%d, R%d, R%d\n", $1.codechar, $3.codechar, $$.reg, $1.reg, $3.reg);
                }
        |       expr DIV expr   {
                    // 找未保存变量的寄存器
                    int i;
                    for (i = 0; i < Mreg; i++) {
                        if (!usereg[i] && !expr_usereg[i]) {
                            $$.reg = i;
                            break;
                        }
                    }

                    expr_usereg[i] = 1;

                    snprintf($$.codechar, 1000, "%s%sDIV R%d, R%d, R%d\n", $1.codechar, $3.codechar, $$.reg, $1.reg, $3.reg);
                }
        |       LPT expr RPT { $$ = $2; }
        |       MINUS expr %prec UMINUS {
                    // 使用同一个寄存器
                    $$.reg = $2.reg;

                    // 对寄存器取反
                    snprintf($$.codechar, 1000, "%sNEG R%d\n", $2.codechar, $2.reg);

                }
        |       NUMBER          {
                    // 找未保存变量的寄存器
                    int i;
                    for (i = 0; i < Mreg; i++) {
                        if (!usereg[i] && !expr_usereg[i]) {
                            $$.reg = i;
                            break;
                        }
                    }

                    expr_usereg[i] = 1;

                    snprintf($$.codechar, 1000, "MOV R%d, #%d\n", $$.reg, $1);
                }
        ;

%%

// programs section

int search_reg(char* name) {//查找一个标识符
    VarNode* curr = symfirst;//头指针开始
    while (curr != NULL) {
        if (strcmp(curr->name, name) == 0) {
            return curr->reg;//找到了就返回其寄存器编号
        }
        curr = curr->next;
    }
    return -1; // -1代表未找到
}

int add_reg(char* name) {//给标识符分配一个寄存器
    int i;
    for (i = 0; i < Mreg; i++) {//查看i编号寄存器是否被使用
        if (!usereg[i] && !expr_usereg[i]) {
            break;
        }
    }
    if (i == Mreg) {//说明没找到可用寄存器
        perror("没有可用寄存器");
    }

    usereg[i] = 1;//标志一下使用i号寄存器


    // 新建节点，name: value
    VarNode* node = malloc(sizeof(VarNode));//创建新节点
    node->name = strdup(name);//赋值标识符名字进去
    node->reg = i;
    node->next = symfirst;//next字段指向头节点
    symfirst = node;//将新节点更新为新头节点

    return i; // 返回当前标识符对应的寄存器
}

int yylex()
{
    int t;
    while(1){
        t = getchar();
        if (t==' '||t=='\t'||t=='\n')
        {
            //do noting
        }
        else if (isdigit(t))
        {
            /* 解析多位数字返回数字类型
               其中yylval是属性值
            */
            yylval.intv = 0;
            while (isdigit(t))
            {
                // 这里减 '0' 是为了将字符转为数字
                yylval.intv = yylval.intv * 10 + t - '0';
                t = getchar();
            }
            ungetc(t, stdin);
            return NUMBER;
        }
        // 识别变量（标识符）
        else if (isalpha(t) || (t == '_') ) // 以字母或下划线打头
        {
            char varname[50];
            int i = 0;
            varname[i++] = t;
            while(isalnum(t = getchar()))
            {
                varname[i++] = t;
            }
            // 回退一个字符
            ungetc(t, stdin);
            varname[i] = '\0';

            strcpy(yylval.code.codechar, varname); // 记录变量名
            yylval.code.reg = -1; // 寄存器号初始化为-1
            return VAR;
        }
        // 识别等号
        else if (t == '=') {
            return ASSIGN;
        }
        else if (t == '+')
        {
            return ADD;
        }
        else if (t == '-')
        {
            return MINUS;
        }
        else if (t == '*')
        {
            return MUL;
        }
        else if (t == '/')
        {
            return DIV;
        }
        else if (t == '(')
        {
            return LPT;
        }
        else if (t == ')')
        {
            return RPT;
        }
        else
        {
            if(t!=';'){
            printf("存在无效符号：%c\n", t);//这里我添加了一个非法符号检测功能，可以检测出你输入表达式的第一个非法符号，提升了程序的用户便利度
            }
            return t;
        }
    }
}
//这部分和之前相同
int main(void)
{
    yyin = stdin;
    do{
        yyparse();
    }while (!feof(yyin));
    return 0;
}

void yyerror(const char* s){
    fprintf(stderr, "编译错误在: %s\n", s);
    exit(1);
}
