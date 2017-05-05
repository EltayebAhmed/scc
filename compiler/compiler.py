from ast.core import NodeVisitor, ExplicitConstant, WhileStatement, SwitchStatement
from tokens import INT


class LoopSwitchStack:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        assert (isinstance(item, WhileStatement) or isinstance(item, SwitchStatement))
        self._items.append(item)

    def exit_item(self, item):
        # 'eat' scope
        assert (self._items[-1] == item)
        self._items.pop()

    def get_top_loop_switch(self):
        if len(self._items) == 0:
            raise Exception("None valid syntax")
        else:
            return self._items[-1]


class Compiler(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.stack_pos = 0  # This will become an object later
        self.loop_switch_stack = LoopSwitchStack()

    def compile(self):
        head = self.parser.parse()
        return self.visit(head)

    def visit_IfStatement(self, node):
        endiflabel = "__endif" + str(id(node))
        endelselabel = "__endelse" + str(id(node))
        code = ""
        code += self.visit(node.expression)
        code += "pop eax\n"
        code += "cmp eax,0\n";
        code += "jz " + endiflabel + "\n"
        self.stack_pos += 4
        code += self.visit(node.body)

        if (node.elsebody is not None):
            code += "jmp " + endelselabel + "\n"

        code += endiflabel + ":\n"

        if (node.elsebody is not None):
            code += self.visit(node.elsebody)
            code += endelselabel + ":\n"
        return code

    def visit_FunctionCall(self, node):
        code = ""
        old_stack_pos = self.stack_pos
        for parameter in node.parameters[::-1]:
            code += self.visit(parameter)

        code += "call %s\n" % ("_" + node.callee_name)
        code += "add esp, %i\n" % (old_stack_pos-self.stack_pos)
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
            code += self.visit(sub_node)
        return code

    def visit_FunctionDefinition(self, node):
        # TODO!!!! function declarations should have a jump to right after the body to
        # handle nested functions correctly
        code = "_%s: \n" % node.name
        code += """push ebp
mov ebp, esp\n"""
        self.stack_pos -= 4

        code += self.visit(node.body)
        code += "pop ebp\nret\n"
        self.stack_pos += 4

        return code

    def visit_Return(self, node):
        code = "pop ebp\nret\n"
        self.stack_pos += 4

        return code

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
            self.stack_pos -= 4
            return "push %i\n" % (node.value)

    def visit_WhileStatement(self, node):
        self.loop_switch_stack.add_item(node)
        start_label = '__while_label_start' + str(id(node))
        end_label = '__while_label_end' + str(id(node))

        code = start_label + ':\n'
        code += self.visit(node.expression)
        code += "pop eax\ncmp eax,0\n"
        code += "jz " + end_label + '\n'
        self.stack_pos += 4
        code += self.visit(node.block)
        code += "\njmp " + start_label + '\n'
        code += end_label + ":\n"
        self.loop_switch_stack.exit_item(node)
        return code

    def visit_CaseStatement(self,node):
        code = ""
        end_case_label = "end_case_" + str(id(node))
        code += self.visit(node.switch_expr)
        code += self.visit(node.expression)
        code += "pop eax\n"
        code += "cmp eax,[esp]\n"
        code += "add esp,4\n"
        code += "jne " + end_case_label + "\n"
        self.stack_pos += 8
        code += self.visit(node.statements)
        code += end_case_label + ":\n"
        return code

    def visit_SwitchStatement(self, node):
        self.loop_switch_stack.add_item(node)
        code = ""
        end_switch_label = "end_switch_" + str(id(node))
        code += self.visit(node.cases)
        if node.default is not None:
            code += self.visit(node.default)

        code += end_switch_label + ":\n"

        self.loop_switch_stack.exit_item(node)

        return code

    def visit_BreakStatement(self, node):
        top_item = self.loop_switch_stack.get_top_loop_switch()
        if isinstance(top_item, WhileStatement):
            code = "jmp __while_label_end" + str(id(top_item)) + ":\n"
        elif isinstance(top_item, SwitchStatement):
            code = "jmp " + "end_switch_" + str(id(top_item)) + "\n"
        else:
            raise Exception("Invalid syntax")
        return code
