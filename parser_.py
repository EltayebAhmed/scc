from tokens import *
from ast.core import *


def do_something(*args):
    print(args)
    print('\n')
    raise Exception('I shouldnt be called')
    return args


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def peek_token(self):
        return self.lexer.peek_token()

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

    def ret_type(self):
        """VOID"""
        if self.current_token == VOID:
            type_ = VOID
            self.eat(VOID.type)
        else:
            type_ = None
            self.error()
        return type_

    def program(self):
        """program: (funcdef) * EOF"""
        func_list = []
        while self.current_token.type != EOF:
            func_list.append(self.funcdef())
        return Program(func_list)

    def funcdef(self):
        """funcdef : type_spec ID LPAREN RPAREN scope_block"""
        ret_type = self.ret_type()
        name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)
        self.eat(RPAREN)
        body = self.scope_block()
        return FunctionDefinition(ret_type, name, body)

    def scope_block(self):
        """scope_block: OPENCURLY (statement)* CLOSECURLY"""
        statements = []
        self.eat(OPENCURLY)
        while self.current_token.type != CLOSE_CURLY:
            statements.append(self.statement())
        self.eat(CLOSE_CURLY)
        return ScopeBlock(statements)

    def while_statement(self):
        """while_statement : WHILE LPAREN expression RPAREN statement"""
        self.eat(WHILE.type)
        self.eat(LPAREN)
        expression = self.expression()
        self.eat(RPAREN)
        block = self.scope_block()
        return WhileStatement(expression, block)

    def for_statement(self):
        """for_statement : FOR LPAREN expression (COMA expression)* SEMICOLON expression SEMICOLON expression (COMA expression)*
RPAREN statement"""
        self.eat(FOR.type)
        self.eat(LPAREN)
        initializer = self.expression()
        initializers = [initializer]

        while self.current_token == COMA:
            self.eat(COMA)
            initializers.append(self.expression())

        self.eat(SEMICOLON)
        condition = self.expression()

        self.eat(SEMICOLON)
        increment = self.expression()
        increments = [increment]
        while self.current_token == COMA:
            self.eat(COMA)
            increments.append(self.expression())

        self.eat(RPAREN)

        initializers_nodes = MultiNode(initializers, "initializers")

        statement = self.statement()

        increments_node = MultiNode(increments, "increments")
        mul_node = MultiNode([statement, increments_node], "body")

        _while = WhileStatement(condition, mul_node)

        result = MultiNode([initializers_nodes, _while], "For loop")

        return result

    def statement(self):
        """statement : (funccall SEMICOLON)
            | (RETURN SEMICOLON)
            | scope_block
            | SEMICOLON
            | while_statement
            | ifstatement"""

        if self.current_token.type == ID:
            statement = self.funccall()
            self.eat(SEMICOLON)

        elif self.current_token in (RETURN,):
            self.eat(RETURN.type)
            statement = Return()
            self.eat(SEMICOLON)

        elif self.current_token.type == OPENCURLY:
            statement = self.scope_block()
        elif self.current_token.type == SEMICOLON:
            # Empty statement
            statement = NoOperation()
            self.eat(SEMICOLON)

        elif self.current_token == IF:
            statement = self.ifstatement()

        elif self.current_token == WHILE:
            statement = self.while_statement()
        elif self.current_token == BREAK:
            statement = self.break_statement()
        elif self.current_token == FOR:
            statement = self.for_statement()

        else:
            self.error()

        return statement

    def funccall(self):
        """funccall : ID LPAREN ((expression (COMA expression)*) | empty) RPAREN"""
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

    def ifstatement(self):
        """ifstatement: IF LPAREN expression RPAREN statement (ELSE statement)?"""
        self.eat(IF.type)
        self.eat(LPAREN)
        expression = self.expression()
        self.eat(RPAREN)
        body = self.statement()
        if (self.current_token == ELSE):
            self.eat(ELSE.type)
            elsebody = self.statement()
            return IfStatement(expression, body, elsebody)
        return IfStatement(expression, body)

    def expression(self):
        """expression: INTEGER | funcall"""
        # At some point it might be a good idea to create an expression ASTNode and
        # wrap all nodes instatiated her by it
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)

            return ExplicitConstant(token.value, INT)  # remove string
        else:
            return self.funccall()

    def parse(self):
        """"
        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node

    def break_statement(self):
        self.eat(BREAK.type)
        self.eat(SEMICOLON)
        return BreakStatement()
