# Grammar

This file is contains all the currently implemented grammar.

%tokens LPAREN RPAREN OPENCURLY CLOSECURLY SEMICOLON COMA EOF WHILE
%tokens VOID
%tokens RETURN
%tokens INTEGER ID PLUS MINUS MUL DIV


ret_type: VOID

program : (funcdef)* EOF

funcdef : type_spec ID LPAREN RPAREN scope_block

scope_block: OPENCURLY (statement)* CLOSECURLY

statement : (funccall SEMICOLON)
            | (RETURN SEMICOLON)
            | scope_block
            | SEMICOLON
            | while_statement

while_statement : WHILE LPAREN expression RPAREN statement




funccall : ID LPAREN ((expression (COMA expression)*) | empty) RPAREN
expression   : term ((PLUS | MINUS) term)*
term   : factor ((MUL | DIV) factor)*
factor :(PLUS|MINUS)factor | INTEGER | funccall | LPAREN expression RPAREN
