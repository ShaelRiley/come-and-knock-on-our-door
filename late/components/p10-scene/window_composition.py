"""Composition proof fixture: accepted P08 primitive over P09 tables, then P10.

No widening of the primitive's P08 document bounds or new presentation API.
The resulting fixture does not contain the separate full-source host gate.
"""
from pathlib import Path
import sys,importlib.util
H=Path(__file__).resolve().parent;W=H/'inputs/window-primitive'
sys.path.insert(0,str(H/'tools'));sys.path.insert(0,str(W/'tools'))
from source_tools import methods
from source_derivation import merge,append_locals
import extend_dialogue as ext

def predecessor():
    spec=importlib.util.spec_from_file_location('frozen_window_hooks',W/'window_hooks.py')
    wh=importlib.util.module_from_spec(spec);spec.loader.exec_module(wh)
    old=(W/'inputs/window-basis/module982.sc').read_text()
    window=wh.window_hooks({'module982.sc':old})['module982.sc']
    oldm,newm=methods(old),methods(window)
    hooks={n:s for n,s in newm.items() if oldm.get(n)!=s}
    assert set(hooks)=={'sdOpenWindow','sdWindowValue','sdOpen','sdLoad','sdTurn','sdControlAction','sdBuildControls','sdDraw','sdClose','sdAfterRestore'}
    p09=(H/'inputs/src/module982.sc').read_text()
    # Carry precisely the already accepted P09 load additions into the window body.
    body=hooks['sdLoad'];assert body.count('(>= index (* 1138 8))')==1
    body=body.replace('(>= index (* 1138 8))','(>= index (* 1191 8))')
    for prop,last,new in [('sdResource',208,210),('sdAudioModule',918,921)]:
        # P09 appends after the existing final condition, whose value need not be largest.
        import re
        matches=list(re.finditer(r'\(and(?:\s+\(!= '+prop+r' \d+\))+\)',body));assert len(matches)==1
        allow=matches[0].group();assert str(new) not in allow
        body=body.replace(allow,allow[:-1]+f' (!= {prop} {new}))')
    hooks['sdLoad']=body
    combined=merge(append_locals(p09,'[sdWindowBounds 2]'),hooks)
    assert all(ext.read_array(combined,n)==ext.read_array(p09,n) for n in ext.ARRAYS)
    return combined

def generate():
    before=predecessor();after,contract=ext.apply_source(before)
    path=H/'generated/window-src';path.mkdir(exist_ok=True)
    for p in (H/'generated/src').glob('*.sc'):(path/p.name).write_bytes(p.read_bytes())
    (path/'module982.sc').write_text(after)
    (H/'generated/window-predecessor.sc').write_text(before)
    return before,after

if __name__=='__main__':generate()
