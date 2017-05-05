from tokens import INT
from collections import namedtuple
from ast.core import ScopeBlock, NodeVisitor
from cookbook import Enum
from collections import  OrderedDict

class Symbol:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name) + 1232344324

    def __eq__(self, other):
        return other.name == self.name


class SymbolType(Enum):
    pass


VARSYMBOL = SymbolType('VarSym')
FUNCSYMBOL = SymbolType('FuncSym')


class EmptyStackException(Exception):
    pass

#This class should keep track of variable types in the stack, it will be needed when considering datatypes other than int.
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

class OutOfScopeAccessException(Exception):
    pass

class ScopeObject:
    def __init__(self,ScopeBlockNode,start_relative_to_prev):
        self.ScopeBlockNode = ScopeBlockNode
        self.start_relative_to_prev =  start_relative_to_prev
        self.end_relative_to_start = 0
    def incrementRelativeEnd(self,num):
        self.end_relative_to_start += num

    #Todo scope_object might not be active, take care for this problem later
    def get_start_relative_to_scope(self,scope_object,scope_stack):
        start_relative_to_scope_start = 0
        count_on = False
        multiple = 1
        if scope_stack.is_active(scope_object) and scope_stack.is_active(self):
            for temp in scope_stack:
                if(temp == self):
                    if (count_on == False):
                        count_on = True
                    else:
                        count_on = False
                if(temp == scope_object):
                    if(count_on == False):
                        count_on = True
                        multiple = -1
                    else:
                        count_on = False
                if(count_on == True):
                    start_relative_to_scope_start +=  scope_stack.curren_scope().end_relative_to_start+4 #The +4 is because every scope block has ebp pushed
        start_relative_to_scope_start *= multiple
        return start_relative_to_scope_start

GlobalScopeBlock = ScopeBlock([])
GlobalScopeObject = ScopeObject(GlobalScopeBlock,0)

class ScopeStack:
    def __init__(self):
        self._scopes = [GlobalScopeObject]

    def enter_scope(self, scope):
        assert (isinstance(scope, ScopeObject))
        self._scopes.append(scope)

    def exit_scope(self, scope):
        # 'eat' scope
        assert (scope!= GlobalScopeObject)
        assert (self._scopes[-1]== scope)
        self._scopes.pop()

    def is_active(self, scope):
        """Return true if 'scope' is active"""
        assert (isinstance(scope, ScopeObject))
        return scope in self._scopes

    def current_scope(self):
        assert (self._scopes)
        return self._scopes[-1]


SymbolTableEntry = namedtuple('SymbolTableEntry', ('symbol', 'type', 'scope'))


class SymbolTable:
    def __init__(self):
        self._entries = OrderedDict() # (entry: position of variable relative to scope)


    def entries(self):
        return iter(self._entries.keys())

    def add_entry(self,entry, offest):
        assert isinstance(offest, int)
        assert (isinstance(entry, SymbolTableEntry))
        self._entries[entry] = offest

    def get_offset(self, entry):
        if entry not in self._entries.keys():
            raise Exception('Invalid Entry')
        offset = self._entries[entry]
        return offset

    def get_entry_by_symbol(self, symbol):
        # we will iterate in reverse to get the nearest scoped shadow
        for entry in list(self._entries.keys())[::-1]:
            if entry.symbol == symbol:
                return entry
        return None


class SemanticError(Exception):
    pass

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self._scope_stack = ScopeStack()
        self._symtable = SymbolTable()

    def getSymbolTable(self):
        return self._symtable
    def visit_Program(self, node):
        for function in node.functions:
            self.visit(function)

    def visit_FunctionDefinition(self, node):
        self.visit(node.body)

    def visit_MultiNode(self, node):
        for node in node.nodes:
            self.visit(node)

    def visit_ScopeBlock(self, node):
        start_relative_to_prev = self._scope_stack.current_scope().end_relative_to_start
        nodeScopeObject = ScopeObject(node, start_relative_to_prev)
        self._scope_stack.enter_scope(nodeScopeObject)
        for statement in node.statements:
            self.visit(statement)
        self._scope_stack.exit_scope(nodeScopeObject)

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

    def visit_VariableDeclaration(self, node):
        self._scope_stack.current_scope().incrementRelativeEnd(4)
        sym = Symbol(node.name)
        cur_scope = self._scope_stack.current_scope()
        offset = self._scope_stack.current_scope().end_relative_to_start
        entry = SymbolTableEntry(symbol=sym, type=node.type, scope=cur_scope)
        self._symtable.add_entry(entry, offset)

    def visit_VariableAssignment(self, node):
        pass

    def visit_Variable(self, node):
        sym = Symbol(node.name)
        entry = self._symtable.get_entry_by_symbol(sym)
        if entry is None:
            raise SemanticError("Use of undeclared variable")
        offset = self._symboltable.get_offset(entry)
        currentScope = self._scope_stack.current_scope()
        if entry.scope != currentScope:
            relativeincrement = currentScope.get_start_relative_to_scope(entry.scope, self._scope_stack)
            if relativeincrement == 0 and currentScope == entry.scope:
                raise  OutOfScopeAccessException("You are trying to access a variable that is not visible within current scope!")