from lexer import Lexer
from parser_ import Parser
from compiler.compiler import Compiler
import os
from tests.conf_parser import build_chain
import subprocess
import time

def wait_file(file_name,file_dir ,timeout_in_seconds):
    """Wait for file to show up in the given directory If the timeout is reached without the file showing up an
     exception is raised"""
    start_time = time.time()
    while time.time() - start_time < timeout_in_seconds:
        if file_name in os.listdir(file_dir):
            return
    raise IOError("file (%s) did not appear within %s seconds"  % (file_name, timeout_in_seconds))


def run_code(text):
    """text should be a valid c program, code runner will compile and run the program and return its output

    run code will throw any exceptions thrown by the compilation attempt if it fails
    The code will receive no input for the run and should output to std.out"""
    lex = Lexer(text)
    pars = Parser(lex)
    comp = Compiler(pars)
    asm_code = comp.compile()
    directory_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(directory_path)
    asm_file_name = 'test' + '.asm'
    asm_file = open(asm_file_name, 'w')
    asm_file.write(asm_code)
    asm_file.close()
    wait_file(asm_file_name , directory_path, 1)
    for command, output_file in build_chain:

        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if output_file:
            wait_file(output_file,directory_path, 1)
    out = out.decode("utf-8")
    return out

code = """
    void main(){
        printf ("hello world %d",3);
    }
"""

run_code(code)