#from ast import visualizer
#from ast.visualizer import Visualizer
from parser_ import Parser
from lexer import Lexer
from compiler.compiler import Compiler
code = """
void main(){
    printf(3 + 12*5);
}
"""

lex = Lexer(text=code)
parser = Parser(lexer=lex)
comp = Compiler(parser=parser)
#viz = Visualizer(parser=parser)


print(comp.compile())