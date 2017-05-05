# Grammar

This file is contains all the currently implemented grammar.

%tokens LPAREN RPAREN OPENCURLY CLOSECURLY SEMICOLON COMA EOF WHILE
%tokens VOID
%tokens RETURN
%tokens INTEGER ID PLUS MINUS MUL DIV


*tokens IF ELSE WHILE BREAK

ret_type: VOID

program : (funcdef)* EOF

funcdef : type_spec ID LPAREN RPAREN scope_block

scope_block: OPENCURLY (statement)* CLOSECURLY

statement : (funccall SEMICOLON)
            | (RETURN SEMICOLON)
            | scope_block
            | SEMICOLON
            | ifstatement
            | while_statement
            | (BREAK SEMICOLON)

while_statement : WHILE LPAREN expression RPAREN statement


ifstatement: IF LPAREN expression RPAREN statement (ELSE statement)?


funccall : ID LPAREN ((expression (COMA expression)*) | empty) RPAREN
expression   : term ((PLUS | MINUS) term)*
term   : factor ((MUL | DIV) factor)*
factor :(PLUS|MINUS)factor | INTEGER | funccall | LPAREN expression RPAREN
