from tokens import *
from ast.core import *


def do_something(*args):
    print(args)
    print('\n')
    raise Exception('I shouldnt be called')
    return args

type_specifiers = (INT,)
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


    def statement(self):
        """statement : (funccall SEMICOLON)
            | (RETURN SEMICOLON)
            | scope_block
            | (var_assignment SEMICOLON)
            | (var_decl SEMICOLON)
            | SEMICOLON
            | while_statement
            | ifstatement"""

        if self.current_token.type == ID and self.peek_token().type == LPAREN:
            statement = self.funccall()
            self.eat(SEMICOLON)

        elif self.current_token in (RETURN,):
            self.eat(RETURN.type)
            statement = Return()
            self.eat(SEMICOLON)

        elif self.current_token.type == OPENCURLY:
            statement = self.scope_block()

        elif self.current_token in type_specifiers:
            statement = self.var_decl()
            self.eat(SEMICOLON)

        elif self.current_token.type == ID and self.peek_token().type == EQUALS:
            statement = self.var_assignment()
            self.eat(SEMICOLON)

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
        """expression: INTEGER | funccall | var assignment"""
        # At some point it might be a good idea to create an expression ASTNode and
        # wrap all nodes instatiated her by it
        token = self.current_token
        expr = None
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
            expr = ExplicitConstant(token.value, INT)
        elif self.current_token.type == ID:
            if self.peek_token().type == LPAREN :
                expr = self.funccall()
            elif self.peek_token().type == EQUALS:
                expr = self.var_assignment()
            else:
                expr = self.var()
        if expr is None:
            self.error()
        return expr

    def var(self):
        """var : ID"""
        name = self.current_token.value
        self.eat(ID)
        return Variable(name)

    def var_decl(self):
        """var_decl: var_type var_identifier_decl (COMA var_identifier_decl)*"""
        d_type = self.var_type()
        identifier_decls = [self.var_identifier_decl()]
        while self.current_token.type == COMA:
            self.eat(COMA)
            identifier_decls.append(self.var_identifier_decl())

        # this will produce a list of statements each statement is either a single decl
        # or a single assignment and pack them into a MultiNode
        nodes = []
        for decl in identifier_decls:
            if isinstance(decl,VariableAssignment):
                # variable declaration with initialization
                declaration = VariableDeclaration(decl.name, d_type)
                nodes.append(declaration) # add the declaration
                nodes.append(decl)        # add the assignment

            elif isinstance(decl, Variable):
                declaration = VariableDeclaration(decl.name, d_type)
                nodes.append(declaration)
            else:
                raise Exception("Invalid declaration")

        return MultiNode(nodes)

    def var_identifier_decl(self):
        """var_identifier_decl: (var | var_assigment)"""
        if self.lexer.peek_token().type == EQUALS:
            return self.var_assignment()
        else:
            return self.var()

    def var_assignment(self):
        """var_assignemnt: var EQUALS expression"""
        var_name = self.var().name
        self.eat(EQUALS)
        value = self.expression()
        return VariableAssignment(var_name, value)

    def var_type(self):
        """var_type: INT"""
        d_type = self.current_token
        if d_type in type_specifiers:
            self.eat(d_type.type)  # This is not great but is necessary
        else:
            self.error()
        return d_type

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
