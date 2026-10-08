"""Compile-only token aliases for new P14 selectors; pre-P14 ABI untouched.
Canonical authored source stays exact. SCI vocab997 strings have 16-bit offsets.
"""
import re,json,hashlib
from source_tools import tokens
def apply(output,selectors):
 names=sorted(n for n in selectors if n.startswith('p14'))
 aliases={n:'fX'+format(i,'x') for i,n in enumerate(names)}
 assert not(set(aliases.values())&set(selectors)), 'alias collision'
 def change(src):
  for t in reversed(list(tokens(src))):
   raw=t.group()
   if raw.startswith(chr(34)):continue
   changed=re.sub(r'\b[a-zA-Z_][a-zA-Z_0-9]*\b',lambda m:aliases.get(m[0],m[0]),raw)
   if changed!=raw:src=src[:t.start()]+changed+src[t.end():]
  return src
 compiled={f:change(s) for f,s in output.items()}
 mapped={aliases.get(n,n):v for n,v in selectors.items()}
 assert len(mapped)==len(selectors)
 # Alias names only. IDs remain identical; all legacy names remain byte-exact.
 for n,v in selectors.items():assert mapped[aliases.get(n,n)]==v
 return compiled,mapped,aliases
