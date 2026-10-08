"""NEW P14 wrapper over unchanged accepted finite SCI evaluator; no native proof.
No P14 transition is implemented here. Executes the retained SCI methods.
"""
from pathlib import Path
import json
from tools.assertions import load
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
base=load('p14_accepted_source_primitives',ROOT/'dependencies/domain_source_vm.py')
M=json.loads((HERE/'manifest.json').read_text())
AST=base.parse((HERE/'src/module996.sc').read_text())
CLASS=next(n for n in AST if n[:2]==['class','P14State'])
PROPS=next(n[1:] for n in CLASS[2:] if n[0]=='properties')
DEFAULTS=dict(zip(PROPS[::2],PROPS[1::2]));METHODS={n[1][0]:n for n in CLASS[2:] if n[0]=='method'}
CONSTANTS={n[1]:n[2] for n in AST if n[0]=='define'};LOCALS=next(n[1:] for n in AST if n[0]=='local')
SIGNATURES={name:(m[1][1:].index('&tmp') if '&tmp' in m[1] else len(m[1])-1) for name,m in METHODS.items()}
class VM(base.VM):
 def __init__(self):
  self.p=DEFAULTS.copy();self.methods=METHODS;self.constants=CONSTANTS
  self.arrays={a[0]:[0]*a[1] for a in LOCALS};self.call('p14Init')
 def call(self,name,*args):
  if any(type(x) is not int or not -32768<=x<=32767 for x in args):raise ValueError('SCI argument')
  if name not in SIGNATURES or len(args)!=SIGNATURES[name]:raise ValueError('Unknown method or arity')
  return super().call(name,*args)
 def persistent(self):return {k:self.p[k] for k in M['persisted_properties']}
def restore_words(words):
 from codec import decode_words
 decode_words(words);v=VM();v.p.update(zip(M['persisted_properties'],words))
 if not v.call('p14AfterRestore'):raise ValueError('Invalid SCI restore')
 return v
