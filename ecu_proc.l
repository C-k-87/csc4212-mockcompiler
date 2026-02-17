%{
#include "ecu_proc.tab.h"
%}

%%

[0-9]+      { yylval.ival = atoi(yytext); return NUMBER; }
[ \t\n]     ;

"rpm"       {return RPM;}
"throttle"  {return THROTTLE;}
"load"      {return LOAD;}

"end"       { return END; }

"="         { return ASSIGN; }
";"         {return SEMICOLON;}

.           { return yytext[0]; }

%%

int yywrap(){ return 1; }