from ast import visualizer
from ast.visualizer import Visualizer
from parser_ import Parser
from lexer import Lexer
from compiler.compiler import Compiler
code = """
void main(){
    printf(12,15);
    {};{{{}{}}};
    printf(133,134,13335);
    return;
}
"""
code = """void main(){
    int x = 5;
    printf(x);
    return;
}
"""

lex = Lexer(text=code)
parser = Parser(lexer=lex)
comp = Compiler(parser=parser)
viz = Visualizer(parser=parser)


viz.visualize()