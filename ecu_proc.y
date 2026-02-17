%{
    
#include <stdio.h>
#include <stdlib.h>    

#include  "ecu_proc.tab.h"

extern int yyparse();
extern void yy_scan_string(const char *str);

int yylex();

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
    }

int rpm = 1700;         // Idle RPM is 1700. Rev range 0-4000
int throttle = 0;       // Throttle position 0-100
int load = 0;           // Engine load percentage 0-100

double ecu_output = 0;  // ECU output 0 - 1.0

double cal_ecu_output() {
    ecu_output = ((throttle + load)/2)*(1-(rpm/4000.0))/100.0;
    printf("ECU Output: %.5f\n", ecu_output);
    return ecu_output;
}

double get_ecu_data(char *input) {
    yy_scan_string(input);
    yyparse();
    return ecu_output;
}

%}

%union {
    int ival;
}

%type <ival> expr assign

%token <ival> NUMBER
%token RPM LOAD THROTTLE
%token PLUS MUL ASSIGN SEMICOLON END

%left PLUS
%left MUL


%%
mainloop:
    mainloop program
    | program
    ;

program:
    statements END SEMICOLON
        { cal_ecu_output(); }
    ;

statements:
    statements statement
    | statement
    ;

statement:
    assign
    ;

assign:
    RPM ASSIGN expr SEMICOLON
        { rpm = $3; }
    | LOAD ASSIGN expr SEMICOLON
        { load = $3; }
    | THROTTLE ASSIGN expr SEMICOLON
        { throttle = $3; }
    ;

expr:
    expr PLUS expr 
        { $$ = $1 + $3; }
    | expr MUL expr
        { $$ = $1 * $3; }
    | NUMBER
        { $$ = $1; }
    ;

%%

/* int main() {
    printf("ECU is active\n");
    yyparse();
    return 0;
} */