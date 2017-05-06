# Grammar

This file is contains all the currently implemented grammar.

%tokens LPAREN RPAREN OPENCURLY CLOSECURLY SEMICOLON COMA EOF WHILE BREAK SWITCH CASE COLON DEFAULT
%tokens VOID
%tokens RETURN
%tokens INTEGER STRING ID PLUS MINUS MUL DIV


*tokens IF ELSE WHILE BREAK

ret_type: VOID

program : (funcdef)* EOF

funcdef : type_spec ID LPAREN RPAREN scope_block

scope_block: OPENCURLY (statement)* CLOSECURLY

statement : expression SEMICOLON
            | (RETURN SEMICOLON)
            | scope_block
            | SEMICOLON
            | ifstatement
            | while_statement
            | (BREAK SEMICOLON)
            | for_statement
            | switch_statement

while_statement : WHILE LPAREN expression RPAREN statement

for_statement : FOR LPAREN expression (COMA expression)* SEMICOLON expression SEMICOLON expression (COMA expression)*
RPAREN statement

switch_statement : SWITCH LPAREN expression RPAREN OPENCURLY case_statement* (DEFAULT COLON statement*)? CLOSECURLY

case_statement : CASE expression COLON statement*

ifstatement: IF LPAREN expression RPAREN statement (ELSE statement)?


funccall : ID LPAREN ((expression (COMA expression)*) | empty) RPAREN
expression   : term ((PLUS | MINUS) term)*
term   : factor ((MUL | DIV) factor)*
factor :(PLUS|MINUS)factor | INTEGER |  string | funccall | (LPAREN expression RPAREN)
string : DOUBLE_QUOTE (CHAR | ESCAPED_CHAR)* DOUBLE_QUOTE

