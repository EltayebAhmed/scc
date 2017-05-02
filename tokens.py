# this files contains the Token definition and token types

from cookbook import Enum


class TokenType(Enum):
    pass

class Token:
    def __init__(self, _type, value):
        assert (isinstance(_type,TokenType))
        self._type = type
        self._value = value

    def __str__(self):
        return "<Token, %s: %s>" %(type.__name__, self._value)

LPAREN = TokenType("LPARAN(")
RPAREN = TokenType("RPARAN)")
OPENCURLY = TokenType("OPENCURLY{")
CLOSE_CURLY = TokenType("CLOSECURLY}")
SEMICOLON = TokenType("SEMICOLON;")
COMA = TokenType("COMA,")
EOF = TokenType("EOF")

__VOID = TokenType("VOID")  # Keywords will have single token instances, the token type will not be used
VOID = Token(__VOID, 'VOID')

__RETURN = TokenType("RETURN")
RETURN = Token(__RETURN, "RETURN")

ID = TokenType("ID"),

INTEGER = TokenType("INTEGER")


KEYWORDS  = {'void': VOID,
              'return': RETURN
              }