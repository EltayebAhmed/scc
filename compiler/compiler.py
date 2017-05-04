from ast.core import NodeVisitor, ExplicitConstant
from tokens import INT

class Compiler(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.stack_pos = 0  # This will become an object later

    def compile(self):
        head = self.parser.parse()
        return self.visit(head)

    def visit_FunctionCall(self, node):
        code = ""
        old_stack_pos = self.stack_pos
        for parameter in node.parameters[::-1]:
            code += self.visit(parameter)

        code += "call %s\n" %("_"+node.callee_name)
        code += "add esp, %i\n" % (self.stack_pos - old_stack_pos)
        self.stack_pos = old_stack_pos
        return code


    def visit_NoOperation(self, node):
        return ""

    def visit_ScopeBlock(self, node):
        # later scoping will be handled here as well
        code = ""
        for statement in node.statements:
            code += self.visit(statement)
        return code

    def visit_MultiNode(self, node):
        code = ""
        for sub_node in node.nodes:
            code+= self.visit(sub_node)
        return code

    def visit_FunctionDefinition(self, node):
        # TODO!!!! function declarations should have a jump to right after the body to
        # handle nested functions correctly
        code = "_%s: \n" % node.name
        code += """push ebp
mov ebp, esp\n"""
        code += self.visit(node.body)
        code += "pop ebp\nret\n"
        return code

    def visit_Return(self,node):
        return "pop ebp\nret\n"

    def visit_Program(self, node):
        # remove extern printf when the Symbol Resource Table Arrives
        code = """"global _main
extern _printf
section .text\n"""
        for func in node.functions:
            code += self.visit(func)
        return code

    def visit_ExplicitConstant(self, node):
        if node.type == INT:
            self.stack_pos += 4
            return "push %i\n" % (node.value)
