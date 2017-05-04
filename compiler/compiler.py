from ast.core import NodeVisitor, ExplicitConstant

class Compiler(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def compile(self):
        head = self.parser.parse()
        return self.visit(head)

    def visit_IfStatement(self, node):
        endiflabel = "__endif" + str(id(node))
        endelselabel = "__endelse" + str(id(node))

        code += self.visit(self.expression)
        code += "pop eax\n"
        code += "jz "+label
        code+= self.visit(self.body)
        code+= self.visit()
        code += endiflabel + "\n"

        if(self.elsebody != None)
            code +=
            code += self.visit(self.elsebody)
            code += endelselabel +"\n"
        return code

    def visit_FunctionCall(self, node):
        code = ""
        esp_count = 0
        for parameter in node.parameters[::-1]:
            if isinstance(parameter, ExplicitConstant) and parameter.type == 'INTEGER':
                    code += "push %i ;    func parameter\n" % parameter.value
                    esp_count += 4

            else:
                raise Exception("Don't know what to do!")
        code += "call %s\n" %("_"+node.callee_name)
        code += "add esp, %i\n" %esp_count
        return code


    def visit_NoOperation(self, node):
        return ""

    def visit_ScopeBlock(self, node):
        # later scoping will be handled here as well
        code = ""
        for statement in node.statements:
            code += self.visit(statement)
        return code

    def visit_FunctionDefinition(self, node):
        code = "_%s: \n" % node.name
        code += self.visit(node.body)
        code += "ret"
        return code

    def visit_Return(self,node):
        return "ret\n"

    def visit_Program(self, node):
        # remove extern printf when the Symbol Resource Table Arrives
        code = """"global _main
extern _printf
section .text\n"""
        for func in node.functions:
            code += self.visit(func)
        return code
