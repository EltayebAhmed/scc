from tokens import INT
from collections import namedtuple
from ast.core import ScopeBlock, NodeVisitor
from cookbook import Enum
from collections import  OrderedDict


class SemanticError(Exception):
    pass

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

class OutOfScopeAccessException(SemanticError):
    pass
#Todo add a type feature to ScopeObject to deffrentiate between function scope and other scopes, needed for offset calculation and return
class ScopeObject:
    def __init__(self, scope_block_node, start_relative_to_prev):
        self.scope_block_node = scope_block_node
        self.start_relative_to_prev =  start_relative_to_prev
        self.end_relative_to_start = 0

    def incrementRelativeEnd(self,num):
        self.end_relative_to_start += num

    def __hash__(self):
        return id(self.scope_block_node) + 1233

    def __eq__(self, other):
        return hash(other) == hash(self)

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
                    start_relative_to_scope_start +=  scope_stack.curren_scope().end_relative_to_start
        start_relative_to_scope_start *= multiple
        return start_relative_to_scope_start


GlobalScopeBlock = ScopeBlock([])
GlobalScopeObject = ScopeObject(GlobalScopeBlock,0)

class ScopeStack:
    def __init__(self):
        self._scopes = [GlobalScopeObject]

    def enter_scope(self, scope):
        assert (isinstance(scope, ScopeObject))
        #Todo add another four if Scope is a function scope
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

    def getScopes(self):
        scopes = self._scopes
        return  scopes

SymbolTableKey= namedtuple('SymbolTableEntry', ('symbol', 'scope'))


class SymbolTable:
    def __init__(self):
        self._offsets = OrderedDict()
        self._d_types = OrderedDict()

    def add_key(self,key, offset, d_type ):
        assert isinstance(key, SymbolTableKey)
        self._offsets[key] = offset
        self._d_types[key] = d_type

    def get_offset(self, key):
        if key not in self._offsets.keys():
            raise Exception('Invalid Entry')
        offset = self._offsets[key]
        return offset

    def get_offset_by_name_and_scope(self,name,scope):
        sym = Symbol(name)
        key = SymbolTableKey(name,scope)
        return  self.get_offset(key)


    def get_d_type(self, key):
        assert (key in self._d_types.keys())
        return self._d_types[key]

    def iskey_available(self,key):
        if key in self._offsets.keys():
            return True
        False


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

    def visit_IfStatement(self, node):
        self.visit(node.expression)
        self.visit(node.body)
        if node.elsebody is not None:
            self.visit(node.elsebody)

    def visit_ScopeBlock(self, node):
        self._scope_stack.current_scope().incrementRelativeEnd(4)
        start_relative_to_prev = self._scope_stack.current_scope().end_relative_to_start
        nodeScopeObject = ScopeObject(node, start_relative_to_prev)
        self._scope_stack.enter_scope(nodeScopeObject)
        for statement in node.statements:
            self.visit(statement)
        self._scope_stack.exit_scope(nodeScopeObject)
        self._scope_stack.current_scope().incrementRelativeEnd(-4)
    def visit_NoOperation(self, node):
        pass

    def visit_FunctionCall(self, node):
        sym = Symbol(node.callee_name)
        key = SymbolTableKey(sym, GlobalScopeObject)
        if not self._symtable.iskey_available(key):
            #print("Waring assuming <" + node.callee_name + "> is an external function ")
            #print("Warning! this is still implemented!")
            pass
        elif self._symtable.get_d_type(key) != FUNCSYMBOL:
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
        key = SymbolTableKey(symbol=sym, scope=cur_scope)
        self._symtable.add_key(key, offset,node.type)
    def visit_VariableAssignment(self, node):
        pass

    def visit_Variable(self, node):
        sym = Symbol(node.name)
        key = None
        for scope in reversed(list(self._scope_stack.getScopes())):
            key = SymbolTableKey(sym, scope)
            if self._symtable.iskey_available(key) and self._symtable.get_d_type(key) != FUNCSYMBOL:
                break
        if key is None:
            raise SemanticError("Use of undeclared variable whithin scope.")
        offset = self._symboltable.get_offset(key)
        currentScope = self._scope_stack.current_scope()
        if key.scope != currentScope:
            offset += currentScope.get_start_relative_to_scope(key.scope, self._scope_stack) #relative increment

    def visit_WhileStatement(self, node):
        self.visit(node.expression)
        self.visit(node.block)
        

    def visit_CaseStatement(self, node):

        self.visit(node.switch_expr)
        self.visit(node.expression)
        self.visit(node.statements)


    def visit_SwitchStatement(self, node):
        
        self.visit(node.cases)
        if node.default is not None:
            self.visit(node.default)

        

    def visit_ConstantString(self, node):
        pass
    def visit_BreakStatement(self, node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        

    def visit_UnaryOp(self, node):
        self.visit(node.expression)