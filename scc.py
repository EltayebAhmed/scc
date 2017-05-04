from ast.visualizer import Visualizer
from parser_ import Parser
from lexer import Lexer
from compiler.compiler import Compiler
code = """
void main(){

    if(1){
    print(2);
    }else if(2){
    print(3);
    while(1){
        break;
    }
    }
    printf(12,15);

    while(1){
        break;

    }
    return;
}
"""

lex = Lexer(text=code)
parser = Parser(lexer=lex)
comp = Compiler(parser=parser)
viz = Visualizer(parser=parser)



print(comp.compile())
viz.visualize()


