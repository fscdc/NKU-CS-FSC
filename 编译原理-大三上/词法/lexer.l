%option noyywrap
%option nounput
%option noinput
%option yylineno
%top{
    #include <stdarg.h>
    #include "common.h"
    #include <iomanip>
    #include <fstream>
    #include <vector>
    using namespace std;
}
%{
    extern dump_type_t dump_type;


    inline void dump_tokens(const char* format, ...){
        va_list args;
        va_start(args, format);
        if (dump_type == TOKENS)
            vfprintf(yyout, format, args);
        va_end(args);
    }

    /* Your code here,if desired (lab3). */
    int column = 1;


    class SymbolTableEntry{
    public:
        string name = "";
        int tag = -1;
        bool used = false;
    };
    int curr_tag = 0;
    int temptag=0;

    int tagusestate[1000] = {0};

    const int max_num_of_entries = 1000;
    int count_entry = 0;
    SymbolTableEntry table[max_num_of_entries];


    int find_empty(){
        for(int i=0;i<max_num_of_entries;i++){
            if(!table[i].used){
                return i;
            }
        }
        return -1;
    }

%}


/* definitions section */
/*  Your code here (lab3). */
/*十进制*/
DECIMAL ([1-9][0-9]*|0)
/*八进制*/
OCT (0([1-7][0-7]*|0))
/*十六进制*/
HEX (0[xX]([1-9A-Fa-f][0-9A-Fa-f]*|0))
/*标识符*/
ID [[:alpha:]_][[:alpha:][:digit:]_]*
/*行结束*/
EOL (\r\n|\n|\r)
/*制表符，空格*/
WHITE [\t ]
/*浮点数*/
FLO (([1-9][0-9]*|0).[0-9][0-9]*)



%x BLOCKCOMMENT
COMLINE \/\/[^\n]*
commentbegin "/*"
commentelement .|\n
commentend "*/"


%%
    /* rules section */
"int" {
    dump_tokens("INT\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=3;
}

"float" {
    dump_tokens("FLOAT\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=5;
}

"void" {
    dump_tokens("VOID\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=4;
}

"if" {
    dump_tokens("IF\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=2;
}

"else" {
    dump_tokens("ELSE\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=4;
}

"return" {
    dump_tokens("RETURN\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=6;
}

"const" {
    dump_tokens("CONST\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=5;
}

"while" {
    dump_tokens("WHILE\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=5;
}

"break" {
    dump_tokens("BREAK\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=5;
}

"continue" {
    dump_tokens("CONTINUE\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=8;
}

"=" {
    dump_tokens("ASSIGN\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"==" {
    dump_tokens("EQUAL\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=2;
}

"!=" {
    dump_tokens("NOTEQUAL\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=2;
}

"<" {
    dump_tokens("LESS\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"<=" {
    dump_tokens("LESSEQUAL\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=2;
}

">" {
    dump_tokens("MORE\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

">=" {
    dump_tokens("MOREEQUAL\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=2;
}

"+" {
    dump_tokens("ADD\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"-" {
    dump_tokens("SUB\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"*" {
    dump_tokens("MUL\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"/" {
    dump_tokens("DIV\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"%" {
    dump_tokens("MOD\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"&&" {
    dump_tokens("AND\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=2;
}

"||" {
    dump_tokens("OR\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column+=2;
}

"!" {
    dump_tokens("NOT\t\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

";" {
    dump_tokens("SEMICOLON\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"," {
    dump_tokens("COMMA\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"(" {
    dump_tokens("LPAREN\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

")" {
    dump_tokens("RPAREN\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"{" {
    dump_tokens("LBRACE\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
    temptag=curr_tag;
    for(int i=1;i<=1000;i++){
        if(tagusestate[i]==0){
            curr_tag=i;
            tagusestate[i]=1;
            break;
        }
    }

}

"}" {
    dump_tokens("RBRACE\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
    curr_tag=temptag;
}

"[" {
    dump_tokens("LBRACKET\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

"]" {
    dump_tokens("RBRACKET\t\t\t%-20s\tline:%d\tcol:%d\n", yytext,yylineno,column);
    column++;
}

{DECIMAL} {
    int decimal;
    decimal = atoi(yytext);
    int len = strlen(yytext);
    dump_tokens("DECIMAL\t\t\t%-20s\tline:%d\tcol:%d\t%d\n", yytext,yylineno,column,decimal);
    column+=len;
}
{OCT} {
    int octal = strtol(yytext, NULL, 8);
    int len = strlen(yytext);
    dump_tokens("OCT\t\t\t\t%-20s\tline:%d\tcol:%d\t%d\n", yytext,yylineno,column,octal);
    column+=len;
}   
{HEX} {
    int hex = strtol(yytext, NULL, 16);
    int len = strlen(yytext);
    dump_tokens("HEX\t\t\t\t%-20s\tline:%d\tcol:%d\t%d\n", yytext,yylineno,column,hex);
    column+=len;
}
{FLO} {
    float flo = stof(yytext);
    int len = strlen(yytext);
    dump_tokens("FLO\t\t\t\t%-20s\tline:%d\tcol:%d\t%f\n", yytext,yylineno,column,flo);
    column+=len;
}  

{ID} {
    int len = strlen(yytext);

    string id_s = yytext;

    int target_index = 0;
    bool get = false;
    for(int i=max_num_of_entries-1;i>=0;i--){
        if(table[i].used){
            if(table[i].name == id_s && table[i].tag == curr_tag){
                target_index = i;
                get = true;
                break;
            }
        }
    }
    if(get==false){
        int index = find_empty();
        target_index = index;
        table[index].name = id_s;
        table[index].tag = curr_tag;
        table[index].used = true;
    }
    dump_tokens("ID\t\t\t\t%-20s\tline:%d\tcol:%d\t%p\n", yytext,yylineno,column,&table[target_index]);
    column+=len;
}

{EOL} {
    column++;
    column = 1;
}

{WHITE} {
    column++;
}

{COMLINE} {}

{commentbegin} {
    BEGIN BLOCKCOMMENT;   
}
<BLOCKCOMMENT>{commentelement} {}
<BLOCKCOMMENT>{commentend} {
    BEGIN INITIAL;
}

    /*  Your code here (lab3). */
%%
/* user code section */
