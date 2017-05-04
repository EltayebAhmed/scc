# Grammar

This file is contains all the currently implemented grammar.

%tokens LPAREN RPAREN OPENCURLY CLOSECURLY SEMICOLON COMA EQUALS EOF
%tokens VOID INT
%tokens RETURN
%tokens INTEGER ID


ret_type: VOID

program : (funcdef)* EOF

funcdef : type_spec ID LPAREN RPAREN scope_block

scope_block: OPENCURLY (statement)* CLOSECURLY

statement : (funccall SEMICOLON)
            | (RETURN SEMICOLON)
            | scope_block
            | (var_assignment SEMICOLON)
            | (var_decl SEMICOLON)
            | SEMICOLON



funccall : ID LPAREN ((expression (COMA expression)*) | empty) RPAREN

expression: INTEGER | funccall | var | var_assignment

var : ID

var_decl: var_type var_identifier_decl (COMA var_identifier_decl)*

var_identifier_decl: (var | var_assigment)

var_assignemnt: var EQUALS expression

var_type: INT