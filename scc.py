from parser_ import Parser
from lexer import Lexer

code = """
void main(){
    printf(11);
    return;
}
"""

lex = Lexer(text=code)
parser = Parser(lexer=lex)

parser.parse()