# this files contains the Token definition and token types

from cookbook import Enum


class TokenType(Enum):
    pass

class Token:
    def __init__(self, type_, value):
        assert (isinstance(type_,TokenType))
        self.type = type_
        self.value = value

    def __str__(self):
        return "<Token, %s: %s>" %(self.type.name, self.value)

    __repr__ = __str__

LPAREN = TokenType("LPARAN(")
RPAREN = TokenType("RPARAN)")
OPENCURLY = TokenType("OPENCURLY{")
CLOSE_CURLY = TokenType("CLOSECURLY}")
SEMICOLON = TokenType("SEMICOLON;")
COMA = TokenType("COMA,")
EQUALS = TokenType("EQAULS=")
EOF = TokenType("EOF")

ID = TokenType("ID")
INTEGER = TokenType("INTEGER")

__VOID = TokenType("VOID")  # Keywords will have single token instances, the token type will not be used
VOID = Token(__VOID, 'VOID')

__RETURN = TokenType("RETURN")
RETURN = Token(__RETURN, "RETURN")

__INT = TokenType("INT")
INT = Token(__INT, "INT")



KEYWORDS  = {'void': VOID,
              'return': RETURN,
              'int': INT}