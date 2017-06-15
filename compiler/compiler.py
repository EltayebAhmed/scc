from ast.core import NodeVisitor, ExplicitConstant, WhileStatement, SwitchStatement
from tokens import *
from compiler.symtable_ import *

comparison_funnctions = {
    "big": """
        bigger:
            mov ebx,[esp+4]
            mov eax,[esp+8]
            cmp eax, ebx
            jg bigger_true
            jle bigger_false
            bigger_done:ret


        bigger_true:
            mov eax, 1
            jmp bigger_done
        bigger_false:
            mov eax, 0
            jmp bigger_done
        """,
    "less":"""
        less:
            mov ebx,[esp+4]
            mov eax,[esp+8]
            cmp eax, ebx
            jl less_true
            jge less_false
            less_done:ret


            less_true:
                mov eax, 1
                jmp less_done
            less_false:
                mov eax, 0
                jmp less_done
    """,
    "bigeq":"""
        bigeq:
            mov ebx,[esp+4]
            mov eax,[esp+8]
            cmp eax, ebx
            jge bigeq_true
            jl bigeq_false
            bigeq_done:ret


            bigeq_true:
                mov eax, 1
                jmp bigeq_done
            bigeq_false:
                mov eax, 0
                jmp bigeq_done
    """,
    "lesseq":"""
            lesseq:
                mov ebx,[esp+4]
                mov eax,[esp+8]
                cmp eax, ebx
                jle lesseq_true
                jg lesseq_false
                lesseq_done:ret


                lesseq_true:
                    mov eax, 1
                    jmp lesseq_done
                lesseq_false:
                    mov eax, 0
                    jmp lesseq_done
        """,
    "eq":"""
        eq:
            mov ebx,[esp+4]
            mov eax,[esp+8]
            cmp eax, ebx
            je eq_true
            jne eq_false
            eq_done:ret


            eq_true:
                mov eax, 1
                jmp eq_done
            eq_false:
                mov eax, 0
                jmp eq_done
    """,


    "noteq":"""
        noteq:
            mov ebx,[esp+4]
            mov eax,[esp+8]
            cmp eax, ebx
            jne noteq_true
            je noteq_false
            noteq_done:ret


           noteq_true:
               mov eax, 1
               jmp eq_done
           noteq_false:
               mov eax, 0
               jmp noteq_done
    """
}
#Todo implement Statement that encloses expression and makes sure no unused expression leaves something in the stack


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
        self._symboltable = None
        self.stack_pos = 0  # This will become an object later
        self.scope_stack = ScopeStack()
        self.loop_switch_stack = LoopSwitchStack()
        self.strings = []

    def compile(self):
        head = self.parser.parse()
        symbol_builder = SymbolTableBuilder()
        symbol_builder.visit(head)
        self._symboltable = symbol_builder.getSymbolTable()
        return self.visit(head)

    def visit_IfStatement(self, node):
        endiflabel = "__endif" + str(id(node))
        endelselabel = "__endelse" + str(id(node))
        code = ""
        code += self.visit(node.expression)
        code += "pop eax\n"
        code += "cmp eax,0\n"
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
        code += "add esp, %i\n" % (old_stack_pos - self.stack_pos)
        self.stack_pos = old_stack_pos
        return code

    def visit_NoOperation(self, node):
        return ""

    def visit_ScopeBlock(self, node):
        # later scoping will be handled here as well
        self.scope_stack.current_scope().incrementRelativeEnd(4)
        start_relative_to_prev = self.scope_stack.current_scope().end_relative_to_start
        nodeScopeObject = ScopeObject(node, start_relative_to_prev)
        self.scope_stack.enter_scope(nodeScopeObject)
        code = ""
        code += "push ebp\n"
        code += "mov ebp,esp\n"
        self.stack_pos -= 4
        for statement in node.statements:
            code += self.visit(statement)
        code += "mov esp,ebp\n"
        code += "pop ebp\n"
        self.stack_pos += 4
        self.scope_stack.exit_scope(nodeScopeObject)
        self.scope_stack.current_scope().incrementRelativeEnd(-4)
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
        code += self.visit(node.body)
        self.stack_pos += 4

        return code

    def visit_BinOp(self, node):
        code = ""
        code += self.visit(node.left)
        code += self.visit(node.right)
        code += "pop ebx\n"
        code += "pop eax\n"
        if node.op.type == PLUS:
            code+=  "add eax, ebx\n"
            code += "push eax\n"
        elif node.op.type == MINUS:
            code += "sub eax, ebx\n"
            code += "push eax\n"
        elif node.op.type == MUL:
            code += "mul ebx\n"
            code += "push eax\n"
        elif node.op.type == INT_DIV:
            code += "xor edx, edx\n"
            code += "div ebx\n"
            code += "push eax\n"
        elif node.op.type == BIG:
            code += "push eax\npush ebx\n"
            code += "call bigger\n"
            code += "add esp,8\n"
            code += "push eax\n"
        elif node.op.type == LESS:
            code += "push eax\npush ebx\n"
            code += "call less\n"
            code += "add esp,8\n"
            code += "push eax\n"
        elif node.op.type == BIGEQ:
            code += "push eax\npush ebx\n"
            code += "call bigeq\n"
            code += "add esp,8\n"
            code += "push eax\n"
        elif node.op.type == LESSEQ:
            code += "push eax\npush ebx\n"
            code += "call lesseq\n"
            code += "add esp,8\n"
            code += "push eax\n"
        elif node.op.type == EQ:
            code += "push eax\npush ebx\n"
            code += "call eq\n"
            code += "add esp,8\n"
            code += "push eax\n"
        elif node.op.type == NOTEQ:
            code += "push eax\npush ebx\n"
            code += "call noteq\n"
            code += "add esp,8\n"
            code += "push eax\n"
        self.stack_pos += 4
        return code

    def visit_UnaryOp(self, node):
        code = ""
        op = node.op.type
        if op == PLUS:
            code += self.visit(node.expression)

        elif op == MINUS:
            code += self.visit(node.expression)
            code += "pop eax\nmov ebx, -1\n Mul ebx\npush eax\n"

        return code

    def visit_Return(self, node):
        code = "pop ebp\nret\n"
        self.stack_pos += 4

        return code

    def visit_Program(self, node):
        # remove extern printf when the Symbol Resource Table Arrives
        header = "global _main\nextern _printf\n"
        definitions_body = ""
        for func in node.functions:
            definitions_body += self.visit(func)

        data_section = "section .data\n"
        for string in self.strings:
            data_section  += string+ "\n"
        code = header + data_section + "section .text\n" + definitions_body

        for item in comparison_funnctions.values():
            code+=item

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

    def visit_CaseStatement(self, node):
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

    def visit_ConstantString(self, node):
        code = ""
        code += node.name + ' : db "' + node.string + '",0'
        assert ('\n' not in node.string)  # we do not support escapc chars yet </3
        self.strings.append(code)
        self.stack_pos-=4
        return "push %s\n" % node.name

    def visit_BreakStatement(self, node):
        top_item = self.loop_switch_stack.get_top_loop_switch()
        if isinstance(top_item, WhileStatement):
            code = "jmp __while_label_end" + str(id(top_item)) + ":\n"
        elif isinstance(top_item, SwitchStatement):
            code = "jmp " + "end_switch_" + str(id(top_item)) + "\n"
        else:
            raise Exception("Invalid syntax")
        return code


    def visit_VariableDeclaration(self, node):
        code = ""
        code += "sub esp,4\n"  # to be edited when floats arrive
        self.scope_stack.current_scope().incrementRelativeEnd(4)
        self.stack_pos -= 4
        return code


    def visit_VariableAssignment(self, node):
        code = ""
        code += self.visit(node.value)
        code += "pop eax\n"
        self.stack_pos += 4
        sym = Symbol(node.name)
        key = None
        for scope in reversed(list(self.scope_stack.getScopes())):
            key = SymbolTableKey(sym, scope)
            if self._symboltable.iskey_available(key) and self._symboltable.get_d_type(key) != FUNCSYMBOL:
                break
        if key is None:
            raise SemanticError("Use of undeclared variable whithin scope.")
        offset = self._symboltable.get_offset(key)
        currentScope = self.scope_stack.current_scope()

        offset -= currentScope.get_start_relative_to_scope(key.scope, self.scope_stack)
        if offset > 0:
            code += "mov [ebp-" + str(offset) + "],eax\n"  # review offset sign
        elif offset < 0:
            code += "mov [ebp+" + str(abs(offset)) + "],eax\n"
        return code


    def visit_Variable(self, node):
        code = ""
        sym = Symbol(node.name)
        key = None
        for scope in reversed(list(self.scope_stack.getScopes())):
            key = SymbolTableKey(sym, scope)
            if self._symboltable.iskey_available(key) and self._symboltable.get_d_type(key) != FUNCSYMBOL:
                break
        if key is None:
            raise SemanticError("Use of undeclared variable whithin scope.")
        offset = self._symboltable.get_offset(key)
        currentScope = self.scope_stack.current_scope()
        # if scope is current scope the get_start_relative_to_scope method should return 0
        offset -= currentScope.get_start_relative_to_scope(key.scope, self.scope_stack)
        if offset > 0:
            code += "push dword [ebp-" + str(offset) + "]\n" #review offset sign
        elif offset < 0:
            code += "push dword [ebp+" + str(abs(offset)) + "]\n"
        else: #offset = 0
            code += "push dword [ebp]\n"
        self.stack_pos -= 4
        return code

    def visit_ExpressionPopper(self , node):
        old_stack_pos = self.stack_pos
        code = ""+self.visit(node.expression)

        code += "add esp, %i\n" % (old_stack_pos - self.stack_pos)
        self.stack_pos = old_stack_pos
        return code

