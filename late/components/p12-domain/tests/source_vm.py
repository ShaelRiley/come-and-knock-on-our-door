"""New construction wrapper over the unchanged accepted SCI source evaluator.

Literal supporting P12 source_vm is preserved under historical/supporting.
No transition or expression behavior is implemented in this wrapper.
"""
import json
from harness import H, SourceDomain, source_base
M=json.loads((H/'manifest.json').read_text())
_BASE=SourceDomain()
DEFAULTS=_BASE.p.copy()
METHODS=_BASE.methods
SIGNATURES={name:(method[1][1:].index('&tmp') if '&tmp' in method[1] else len(method[1])-1) for name,method in METHODS.items()}

def validate_call(name,args):
    if any(type(x) is not int or not -32768<=x<=32767 for x in args):
        raise ValueError('SCI arguments must be signed integer words')
    if name not in SIGNATURES or len(args)!=SIGNATURES[name]:
        raise ValueError('Unknown method or arity')

class VM(SourceDomain):
    def call(self,name,*args):
        validate_call(name,args)
        return super().call(name,*args)
    def persistent(self):
        return {name:self.p[name] for name in M['persisted_properties']}

def restore_words(words):
    from codec import decode_words
    decode_words(words)
    vm=VM();vm.p.update(zip(M['persisted_properties'],words))
    if not vm.call('p12AfterRestore'):raise ValueError('Invalid restored branch')
    return vm
