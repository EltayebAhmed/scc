# Grammar

This file is contains all the currently implemented grammar.

%tokens LPAREN RPAREN OPENCURLY CLOSECURLY SEMICOLON COMA EOF
%tokens VOID
%tokens RETURN
%tokens INTEGER ID


type_spec: VOID

program : (funcdef)* EOF

funcdef : type_spec ID LPAREN RPAREN OPENCURLY compoundstatement CLOSECURLY

compoundstatement: statement_list

statement_list: statement (SEMICOLON statement)*

statement : (funccall
            | RETURN
            | empty)



funccall : ID LPAREN ((expression (COMA expression)+) | empty) RPAREN

expression: INTEGER | funcall
