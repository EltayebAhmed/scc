# this files contains the Token definition and token types



from cookbook import Enum


class TokenType(Enum):
    pass

SEMI = TokenType("SEMICOLON;")
EOF = TokenType("EOF")
OPENCURLY = TokenType("OPENCURLY{")
CLOSE_CURLY = TokenType("CLOSECURLY}")
RPAREN = TokenType("RPARAN)")
LPAREN = TokenType("LPARAN(")
QUOTE = TokenType('"')

ID = TokenType("ID"),
__VOID = TokenType("VOID")  # Keywords will have single token instances, the token type will not be used
__RETURN = TokenType("RETURN")



class Token:
    def __init__(self, type, value):
        self._type = type
        self._value = value

    def __str__(self):
        return "<Token, %s: %s>" %(type.__name__, self._value)

KEYWORDS  = { 'void': Token(__VOID, 'VOID'),
              'return': Token(__RETURN, 'return')
              }