from tokens import *
from ast.core import *


def do_something(*args):
    print(args)
    print('\n')
    raise  Exception('I shouldnt be called')
    return args


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def type_spec(self):
        if self.current_token == VOID:
            type_ = VOID
            self.eat(VOID.type)
        else:
            type_ = None
            self.error()
        return type_

    def program(self):
        func_list = []
        while self.current_token.type != EOF:
            func_list.append(self.funcdef())
        return Program(func_list)

    def funcdef(self):
        ret_type = self.type_spec()
        name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)
        self.eat(RPAREN)
        self.eat(OPENCURLY)
        body = self.compound_statement()
        self.eat(CLOSE_CURLY)
        return FunctionDefinition(ret_type, name, body)

    def compound_statement(self):
        return self.statement_list()

    def statement_list(self):
        """statement_list: statement ( (SEMICOLON statement)* SEMICOLON) [0-1]"""
        statements = []
        statements.append(self.statement())
        while self.current_token.type == SEMICOLON:
            self.eat(SEMICOLON)
            statements.append(self.statement())
        return MultiStatement(statements)

    def statement(self):
        """statement : (funccall
            | RETURN
            | empty)"""
        statement = None
        if self.current_token in (RETURN,):
            self.eat(RETURN.type)
            return Return()

        elif self.current_token.type == ID:
            statement = self.funccall()
        else:
            # Empty statement
            statement = NoOperation()
        return statement

    def funccall(self):
        """funccall : ID LPAREN ((expression (COMA expression)+) | empty) RPAREN"""
        name = self.current_token.value
        parameters = []
        self.eat(ID)
        self.eat(LPAREN)
        while self.current_token.type != RPAREN:
            parameters.append(self.expression())
            while self.current_token.type == COMA:
                self.eat(COMA)
                parameters.append(self.expression())
        self.eat(RPAREN)
        return FunctionCall(name, parameters)

    def expression(self):
        """expression: INTEGER | funcall"""
        # At some point it might be a good idea to create an expression ASTNode and
        # wrap all nodes instatiated her by it
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
            return ExplicitConstant(token.value, 'INTEGER') # remove string
        else:
            return self.funccall()

    def parse(self):
        """"
        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node
