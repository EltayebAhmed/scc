from lexer import Lexer
from parser_ import Parser
from compiler.compiler import Compiler
import os
from tests.conf_parser import build_chain
import subprocess
import time

def run_code(text):
    """text should be a valid c program, code runner will compile and run the program and return its output

    run code will throw any exceptions thrown by the compilation attempt if it fails
    The code will receive no input for the run and should output to std.out"""
    lex = Lexer(text)
    pars = Parser(lex)
    comp = Compiler(pars)
    asm_code = comp.compile()
    directory_path =  os.path.dirname(os.path.realpath(__file__))
    os.chdir(directory_path)
    asm_file_name = 'temp_asm_file'
    asm_file = open(asm_file_name +"asm", 'w')
    asm_file.write(asm_code)
    asm_file.close()

    for tool in build_chain:
        tool = tool.replace("sample", 'temp_asm_file')
        tool = tool.split()
        p = subprocess.Popen(tool)
        out, err = p.communicate()
        time.sleep(.5)
    return out

code = """
    void main(){
        printf ("hello world %d",3);
    }
"""

print(run_code(code))
