# this files contains the Token definition and token types

from cookbook import Enum
INTEGER, PLUS, MINUS, MUL, INT_DIV, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'INT_DIV', 'EOF'
)

class TokenType(Enum):
    pass


class Token:
    def __init__(self, type_, value):
        assert (isinstance(type_, TokenType))
        self.type = type_
        self.value = value

    def __str__(self):
        return "<Token, %s: %s>" % (self.type.name, self.value)

    __repr__ = __str__


#

LPAREN = TokenType("LPARAN(")
RPAREN = TokenType("RPARAN)")
OPENCURLY = TokenType("OPENCURLY{")
CLOSE_CURLY = TokenType("CLOSECURLY}")
SEMICOLON = TokenType("SEMICOLON;")
COMA = TokenType("COMA,")
DOUBLE_QUOTE = TokenType("D_QUOTE")
CHAR = TokenType("CHAR")
EQUALS = TokenType("EQUALS")
ESCAPED_CHAR = TokenType("ESCAPED_CHAR")
PLUS = TokenType("PLUS+")
MINUS = TokenType("MINUS-")
MUL= TokenType("MUL*")
INT_DIV= TokenType("INT_DIV//")
EOF = TokenType("EOF")
COLON = TokenType("COLON")
BIG = TokenType("BIG>")
LESS = TokenType("LESS<")
BIGEQ = TokenType("BIGEQ>=")
LESSEQ = TokenType("LESSEQ<=")
EQ = TokenType("EQ==")
NOTEQ = TokenType("NOTEQ!=")
STRING = TokenType("STRING")

__WHILE = TokenType("WHILE")
WHILE = Token(__WHILE, "WHILE")

__SWITCH = TokenType("SWITCH")
SWITCH = Token(__SWITCH, "SWITCH")

__CASE = TokenType("CASE")
CASE = Token(__CASE, "CASE")

__DEFAULT = TokenType("DEFAULT")
DEFAULT = Token(__DEFAULT, "DEFAULT")

__FOR = TokenType("FOR")
FOR = Token(__FOR, "FOR")



ID = TokenType("ID")
INTEGER = TokenType("INTEGER")

__BREAK = TokenType("BREAK")
BREAK = Token(__BREAK, __BREAK)

__VOID = TokenType("VOID")  # Keywords will have single token instances, the token type will not be used
VOID = Token(__VOID, 'VOID')

__RETURN = TokenType("RETURN")
RETURN = Token(__RETURN, "RETURN")

__IF = TokenType("IF")
IF = Token(__IF, "IF")

__ELSE = TokenType("ELSE")
ELSE = Token(__ELSE, "ELSE")

__BREAK = TokenType("BREAK")
BREAK = Token(__BREAK, "BREAK")

ID = TokenType("ID")

__INT = TokenType("INT")
INT = Token(__INT, "INT")

INTEGER = TokenType("INTEGER")

KEYWORDS = {'void': VOID,
            'return': RETURN,
            'if': IF,
            'else': ELSE,
            'int': INT,
            'while': WHILE,
            'break': BREAK,
            'for': FOR,
            'switch': SWITCH,
            'case': CASE,
            'default': DEFAULT
            }
