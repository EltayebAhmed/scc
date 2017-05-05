from ast.visualizer import Visualizer
from parser_ import Parser
from lexer import Lexer
from compiler.compiler import Compiler
code = """
void main(){
    printf(3--3*4);


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
code = """
void main(){
    printf(3--3*4);
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


