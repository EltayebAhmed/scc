# Grammar

This file is contains all the currently implemented grammar.

%tokens LPAREN RPAREN OPENCURLY CLOSECURLY SEMICOLON COMA EOF
%tokens VOID
%tokens RETURN
%tokens INTEGER ID


*tokens IF ELSE BREAK

ret_type: VOID

program : (funcdef)* EOF

funcdef : type_spec ID LPAREN RPAREN scope_block

scope_block: OPENCURLY (statement)* CLOSECURLY

statement : (funccall SEMICOLON)
            | (RETURN SEMICOLON)
            | scope_block
            | SEMICOLON
            | ifstatement



funccall : ID LPAREN ((expression (COMA expression)*) | empty) RPAREN

expression: INTEGER | funccall

ifstatement: IF LPAREN expression RPAREN statement (ELSE statement)?
