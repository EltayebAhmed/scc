from tokens import INT
from collections import namedtuple
from ast.core import ScopeBlock, NodeVisitor
from cookbook import Enum

class Symbol:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return (type(other) == type(self)) and (other.name == self.name)


class SymbolType(Enum):
    pass


VARSYMBOL = SymbolType('VarSym')
FUNCSYMBOL = SymbolType('FuncSym')


class EmptyStackException(Exception):
    pass


class StackTracker:
    def __init__(self):
        self._pos = 0   #  location of top of stack relative to ebp
        self._items = []
        self._sizes = {INT: 4}

    def get_stack_pos(self):
        return self._pos

    def push(self, type_):
        if type_ == INT:
            self._items.append(INT)
            self._pos -= self._items[INT]

    def pop(self):
        if self.is_empty():
            raise EmptyStackException('Cannot pop empty stack!')
        self._pos += self._sizes[self._items[-1]]
        return self._items.pop()

    def top_dtype(self):
        if self.is_empty():
            raise EmptyStackException('Empty Stack, nothing on top!')

    def is_empty(self):
        return bool(self._items)

GLOBAL = ScopeBlock([])


class ScopeStack:
    def __init__(self):
        self._scopes = [GLOBAL]

    def enter_scope(self, scope):
        assert (isinstance(scope, ScopeBlock))
        self._scopes.append(scope)

    def exit_scope(self, scope):
        # 'eat' scope
        assert (scope._scopes[-1]== scope)
        self._scopes.pop()

    def is_active(self, scope):
        """Return true if 'scope' is active"""
        assert (isinstance(scope, ScopeBlock))
        return scope in self._scopes

SymbolTableEntry = namedtuple('SymbolTableEntry', ('symbol', 'type', 'scope' ))


class SymbolTable:
    def __init__(self):
        self._entries = {} # (entry: position in stack)

    def entries(self):
        return iter(self._entries.keys())

    def add_entry(self,entry, position):
        assert isinstance(position, int)
        assert (isinstance(entry, SymbolTableEntry))
        self._entries[entry] = position

    def get_position(self, entry):
        if entry not in self._entries.keys():
            raise Exception('Invalid Entry')
        return self._entries[entry]

    def get_entry_by_symbol(self, symbol):
        # we will iterate in reverse to get the nearest scoped shadow
        for entry in self._entries[::-1]:
            if entry.symbol == symbol:
                return entry
        return None

class SemanticError(Exception):
    pass

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self._scope_stack = ScopeStack()
        self._symtable = SymbolTable()

    def visit_Program(self, node):
        for function in node.functions:
            self.visit(function)

    def visit_FunctionDefinition(self, node):
        self.visit(node.body)

    def visit_MultiNode(self, node):
        for node in node.nodes:
            self.visit(node)

    def visit_ScopeBlock(self, node):
        self._scope_stack.enter_scope(node)
        for statement in node.statements:
            self.visit(statement)
        self._scope_stack.exit_scope(node)

    def visit_NoOperation(self, node):
        pass

    def visit_FunctionCall(self, node):
        sym = Symbol(node.callee_name)
        entry = self._symtable.get_entry_by_symbol(sym)
        if entry is None:
            print("Waring assuming <%s> is an external function", sep="  ")
            print("Warning! this is still implemented!")
        elif entry.type != FUNCSYMBOL:
            raise SemanticError('Cannot call non function %s'%(sym.name))
        else:
            pass
            # do nothing function call is correct!

    def visit_ExplicitConstant(self, node):
        pass

    def visit_Return(self, node):
        pass


