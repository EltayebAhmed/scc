from ast.visualizer import Visualizer
from parser_ import Parser
from lexer import Lexer
from compiler.compiler import Compiler
code = """
void main(){


    switch(1){
    case 1:
        break;
    case 2:
        print(2);
    default:
        break;
    }


    return;
}
"""

lex = Lexer(text=code)
lex2 = Lexer(text=code)
parser = Parser(lexer=lex)
parser2 = Parser(lexer=lex2)
comp = Compiler(parser=parser)
viz = Visualizer(parser=parser2)


print(comp.compile())
viz.visualize()


