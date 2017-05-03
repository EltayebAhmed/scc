from parser_ import Parser
from lexer import Lexer
from compiler.compiler import Compiler
code = """
void main(){
    printf(12,15);
    {};;
    printf(133,134,13335);
    return;
}
"""

lex = Lexer(text=code)
parser = Parser(lexer=lex)
comp = Compiler(parser=parser)

print(comp.compile())