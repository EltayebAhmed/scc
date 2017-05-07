code1 = """
        void main(){
        int x = 0;
        while (x-10){
            printf("%d  ",x);
            x = x + 1;
        }
    }

"""
code2 = """
    void main(){
        int x = 0;
        while (x-10){
            int prev = 0;
            int cur = 1;
            int temp, counter = 0;
            while(counter - x){
                temp = cur;
                cur = prev + cur;
                prev = temp;
                counter = counter + 1;
            }
            printf("%d  ", cur);
            x = x +1;
        }
    }
"""

from tests.system_tests.code_runner import  run_code
from lexer import Lexer
from parser_ import Parser
from compiler.compiler import Compiler
from ast.visualizer import Visualizer
l = Lexer(code1)
p = Parser(l)
c = Compiler(p)
print("="*10)
print (c.compile())
print("="*10)

l = Lexer(code1)
p = Parser(l)
v = Visualizer(p)

v.visualize()



print(run_code(code2))
v.visualize()