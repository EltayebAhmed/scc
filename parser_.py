from tokens import *

def do_something(*args):
    print(args)
    print('\n')
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
            node = do_something(VOID)
            self.eat(VOID.type)
        else:
            node =None
            self.error()
        return node

    def program(self):
        program = []
        while self.current_token.type != EOF:
            program.append(self.funcdef())
        return do_something(program)

    def funcdef(self):
        ret_type = self.type_spec()
        name = self.current_token
        self.eat(ID)
        self.eat(LPAREN)
        self.eat(RPAREN)
        self.eat(OPENCURLY)
        body = self.compound_statement()
        self.eat(CLOSE_CURLY)
        return do_something(ret_type, name, body)

    def compound_statement(self):
        return do_something(self.statement_list())

    def statement_list(self):
        """statement_list: statement (SEMICOLON statement)*"""
        nodes = []
        nodes.append(self.statement())
        while self.current_token.type == SEMICOLON:
            self.eat(SEMICOLON)
            nodes.append(self.statement())
        return do_something(nodes)

    def statement(self):
        """statement : (funccall
            | RETURN
            | empty)"""
        if self.current_token in (RETURN,):
            node = RETURN
            self.eat(RETURN.type)
        elif self.current_token.type == ID:
            node = self.funccall()
        else:
            # Empty statement
            node = 'EMPTY STATEMENT'
        return do_something(node)

    def funccall(self):
        """funccall : ID LPAREN ((expression (COMA expression)+) | empty) RPAREN"""
        name = self.current_token
        parameters = []
        self.eat(ID)
        self.eat(LPAREN)
        while self.current_token.type != RPAREN:
            parameters.append(self.expression())
        self.eat(RPAREN)
        return do_something(name, parameters)

    def expression(self):
        """expression: INTEGER | funcall"""
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
            return do_something(token.value)
        else:
            return do_something(self.funccall())

    def parse(self):
        """"
        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node
