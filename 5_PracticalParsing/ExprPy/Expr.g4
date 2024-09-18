grammar Expr;

expr   : expr '+' term | term;
term   : term '*' factor | factor;
factor : '(' expr ')' | NUMBER;

NUMBER : [0-9]+;
WS     : [ \t\r\n]+ -> skip;
