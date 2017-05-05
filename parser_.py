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

    def factor(self):
        """factor :(PLUS|MINUS)factor | INTEGER | funccall | LPAREN expression RPAREN"""
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return ExplicitConstant(token.value,INT)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expression()
            self.eat(RPAREN)
            return node
        else:
            return self.funccall()

    def term(self):
        """term : factor ((MUL | INT_DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, INT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == INT_DIV:
                self.eat(INT_DIV)
            node = BinOp(left=node, op=token, right=self.factor())

        return node


    def expression(self):
        """expr   : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

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
            | ifstatement
            | while_statement
            | (BREAK SEMICOLON)
            | for_statement
            | switch_statement"""

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
        elif self.current_token == SWITCH:
            statement = self.switch_statement()

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

    def switch_statement(self):
        """
        switch_statement :
         SWITCH LPAREN expression RPAREN
          OPENCURLY
           case_statement*
           (DEFAULT COLON statement*)?
          CLOSECURLY

        """

        self.eat(SWITCH.type)
        self.eat(LPAREN)
        expression = self.expression()
        self.eat(RPAREN)
        self.eat(OPENCURLY)
        cases = []
        while self.current_token == CASE:
            case = self.case_statement(expression)
            cases.append(case)

        cases_node = MultiNode(cases, "Cases")
        if self.current_token == DEFAULT:
            default_statements = []
            self.eat(DEFAULT.type)
            self.eat(COLON)

            while self.current_token.type != CLOSE_CURLY:
                default_statements.append(self.statement())

            default_node = MultiNode(default_statements, "default")
            switch_node = SwitchStatement(expression, cases_node, default_node)

        else:
            switch_node = SwitchStatement(expression, cases_node)

        self.eat(CLOSE_CURLY)
        return switch_node

    def case_statement(self, switch_expr):
        """case_statement : CASE expression COLON statement*"""
        self.eat(CASE.type)

        case_expr = self.expression()
        self.eat(COLON)
        case_statements = []

        while self.current_token != CASE and self.current_token != DEFAULT and self.current_token != CLOSE_CURLY:
            case_statements.append(self.statement())

        case_statements_node = MultiNode(case_statements, "statement")
        case = CaseStatement(switch_expr, case_expr, case_statements_node)
        return case



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
