"""Execute actual script995 methods using the existing fail-closed SCI parser.

Arithmetic is signed 16-bit here; this remains source conformance, not bytecode
execution or stock ScummVM acceptance. No model transition is reimplemented.
"""
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('p13_parser_primitives', HERE.parent/'p02-domain-adapter/tests/source_vm.py')
primitives = importlib.util.module_from_spec(spec)
spec.loader.exec_module(primitives)
parse, Array, Literal = primitives.parse, primitives.Array, primitives.Literal
AST = parse((HERE/'src/module995.sc').read_text())
CLASS = next(x for x in AST if x[:2] == ['class', 'P13State'])
PROPS = next(x[1:] for x in CLASS[2:] if x[0] == 'properties')
DEFAULTS = dict(zip(PROPS[::2], PROPS[1::2]))
METHODS = {x[1][0]:x for x in CLASS[2:] if x[0] == 'method'}
CONSTANTS = {x[1]:x[2] for x in AST if x[0] == 'define'}
LOCALS = next(x[1:] for x in AST if x[0] == 'local')
primitives.CONSTANTS = CONSTANTS
primitives.METHODS = METHODS
primitives.validate_forms(METHODS)


class VM(primitives.VM):
    def __init__(self):
        self.p = DEFAULTS.copy()
        self.arrays = {x[0]:[0]*x[1] for x in LOCALS}
        self.events, self.output = [], []
        self.call('p13Init')

    def ev(self, node, env):
        if (isinstance(node, list) and not isinstance(node, Array) and node
                and node[0] in {'++', '--'}):
            # Wrap before the assignment, including locals and array cells.
            return self.ev(['=',node[1],['+' if node[0]=='++' else '-',node[1],1]],env)
        result = super().ev(node, env)
        if (isinstance(node, list) and not isinstance(node, Array) and node
                and node[0] in {'+', '-', '*', '/', 'mod', '&', '|'}):
            return ((result + 32768) & 65535) - 32768
        # The pinned SCI port preserves the deciding and/or operand, including
        # serial limbs and object references. Only explicit not normalizes it.
        return result

    def persistent(self):
        names = json.loads((HERE/'manifest.json').read_text())['persisted_properties']
        return {name:self.p[name] for name in names}


def validate_program(methods=METHODS):
    """Reject unknown symbols, methods, arities, operators and array shapes."""
    primitives.validate_forms(methods)
    arrays={x[0]:x[1] for x in LOCALS}
    signatures={}
    for name,method in methods.items():
        signature=method[1][1:]
        signatures[name]=signature.index('&tmp') if '&tmp' in signature else len(signature)
    def visit(node,known,lvalue=False):
        if type(node) is int:
            if lvalue or not -32768 <= node <= 32767:raise ValueError('invalid word/lvalue')
            return
        if type(node) is str:
            if node not in known or (lvalue and node in CONSTANTS):raise ValueError(('unknown/constant value',node))
            return
        if isinstance(node,Array):
            if len(node)!=2 or node[0] not in arrays:raise ValueError('unknown array')
            visit(node[1],known)
            return
        if type(node) is not list or not node:raise ValueError('invalid source node')
        op,*args=node
        if lvalue:raise ValueError('expression assignment')
        if op=='self':
            if not args or type(args[0]) is not str or not args[0].endswith(':'):raise ValueError('method selector required')
            name=args[0][:-1]
            if name not in signatures or len(args)-1!=signatures[name]:raise ValueError(('method arity',name))
            for value in args[1:]:visit(value,known)
        elif op=='switch':
            if not args:raise ValueError('switch arity')
            visit(args[0],known)
            for branch in args[1:]:
                if not branch:raise ValueError('empty switch branch')
                if branch[0]!='else':visit(branch[0],known)
                for item in branch[1:]:visit(item,known)
        elif op=='if':
            if len(args)<2 or args.count('else')>1:raise ValueError('if arity')
            for value in args:
                if value!='else':visit(value,known)
        elif op=='for':
            if len(args)<4 or type(args[0]) is not list or type(args[2]) is not list:raise ValueError('for arity')
            for value in args[0]+[args[1]]+args[2]+args[3:]:visit(value,known)
        else:
            bounds={'=':(2,2),'++':(1,1),'--':(1,1),'return':(0,1),'not':(1,1),
                    'and':(1,999),'or':(1,999),'+':(2,999),'-':(2,2),'*':(2,2),'/':(2,2),
                    'mod':(2,2),'==':(2,2),'!=':(2,2),'<':(2,2),'>':(2,2),'<=':(2,2),'>=':(2,2),'&':(2,2),'|':(2,2)}
            if op not in bounds or not bounds[op][0]<=len(args)<=bounds[op][1]:raise ValueError(('operator arity',op))
            for i,value in enumerate(args):visit(value,known,lvalue=op in ('=','++','--') and i==0)
    for name,method in methods.items():
        known=set(DEFAULTS)|set(CONSTANTS)|set(method[1][1:])
        known.discard('&tmp')
        for node in method[2:]:visit(node,known)
    return signatures

SIGNATURES=validate_program()
_original_call=VM.call

def checked_call(self,name,*args):
    if any(type(x) is not int or not -32768 <= x <= 32767 for x in args):
        raise ValueError('SCI arguments must be signed integer words')
    if name not in SIGNATURES or len(args)!=SIGNATURES[name]:raise ValueError('unknown method or arity')
    return _original_call(self,name,*args)
VM.call=checked_call

def restore_words(words):
    """Strict test transport envelope; native RestoreGame restores the same words."""
    names=json.loads((HERE/'manifest.json').read_text())['persisted_properties']
    if type(words) is not list or len(words)!=len(names) or any(type(x) is not int or not 0<=x<=32767 for x in words):
        raise ValueError('invalid saved word vector')
    vm=VM();vm.p.update(zip(names,words))
    if not vm.call('p13AfterRestore'):raise ValueError('invalid restored branch')
    return vm
