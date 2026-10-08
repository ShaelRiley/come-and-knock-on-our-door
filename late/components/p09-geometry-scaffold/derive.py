#!/usr/bin/env python3
"""Measured, guarded append onto the accepted inactive P09 source universe."""
from pathlib import Path
import json,hashlib,sys,re
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;F=H/'frozen/foundation'
sys.path.insert(0,str(H/'tools'))
from source_tools import methods,tokens
from source_derivation import merge,append_locals,insert,replace,balanced
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def require(v,s):
 if not v:raise RuntimeError(s)
def array(source,name):
 m=re.search(r'\['+name+r' (\d+)\] = \[([^]]*)\]',source);require(m is not None,'Missing '+name)
 values=list(map(int,m[2].split()));require(len(values)==int(m[1]),'Array extent '+name);return values
def verify_inputs():
 require(not sys.flags.optimize,'Optimized Python forbidden')
 pins=json.loads((H/'INPUT-SEAL.json').read_text())
 actual={str(p.relative_to(H)) for d in ('frozen','toolchain') for p in (H/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 actual.add('references/FOUNDATION-INDEPENDENT-REVIEW.md')
 require(actual==set(pins),'Frozen membership changed')
 for name,digest in pins.items():require(sha(H/name)==digest,'Frozen input changed '+name)
def derive(check=False):
 verify_inputs();contract=json.loads((H/'GEOMETRY-CONTRACT.json').read_text())
 output={p.name:p.read_text() for p in (F/'src').glob('*.sc')}
 rows=[ [c['id'],*c['rect'],*c['approach'],c['default']] for c in contract['controls']]
 for tag in contract['tag_shapes']:rows.append([396,*tag['rect'],tag['thread'][0],tag['thread'][1],1])
 require(len(rows)==10 and all(len(r)==8 for r in rows),'Bounded geometry dimensions')
 values=sum(rows,[]);require(len(values)==80,'80 geometry words')
 geo='(method (h9Geo row field)\n (if (or (< row 0) (>= row 10) (< field 0) (>= field 8)) (return -1))\n (return [h9G (+ (* row 8) field)]))'
 labels='(method (h9Label obj) (switch obj\n'+''.join(f' ({n} (return {json.dumps(s)}))\n' for n,s in contract['labels'].items())+') (return "CONSERVATORY"))'
 added=methods(geo+'\n'+labels+'\n'+(H/'templates/ui990.sc.in').read_text())
 require(set(added)=={'h9Geo','h9Label','h9UI'},'Selector plan drift')
 before=methods(output['module990.sc']);domain=append_locals(output['module990.sc'],'[h9G 80] = ['+' '.join(map(str,values))+']')
 output['module990.sc']=merge(domain,added)
 require(all(methods(output['module990.sc'])[n]==v for n,v in before.items()),'Accepted P09 method drift')
 main=output['main.sc'];mm=methods(main);hooks={}
 for method in ('uiHostItemLabel','uiHostShortLabel'):
  hooks[method]=insert(mm[method],'(if (and p09 (p09 h9Active:) (>= arg1 395) (<= arg1 398)) (return (p09 h9Label: arg1)))')
 for method,field in [('uiHostDefaultVerb',7),('approachX',5),('approachY',6)]:
  hooks[method]=insert(mm[method],f'(if (and p09 (p09 h9Active:) (>= arg1 395) (<= arg1 398)) (return (p09 h9Geo: (if (== arg1 398) 6 else (if (== arg1 397) 5 else 0)) {field})))')
 hooks['uiHostWorldControls']=replace(mm['uiHostWorldControls'],'(return 1)','(if p09 (p09 h9UI: 0)) (return 1)')
 anchor='''            pushi 7
            pushi 302
            push0
            push0
            push0
            push0
            pushi -1
            push0
            callk DrawCel, 14
            pushi 7
            pushi 224'''
 replacement='''            pushi 7
            pushi 302
            push0
            push0
            push0
            push0
            pushi -1
            push0
            callk DrawCel, 14
            pToa p09
            bnt L_p09_geometry_tags_done
            pushi 3166
            push1
            push1
            send 6
            L_p09_geometry_tags_done: pushi 7
            pushi 224'''
 hooks['drawP03Conservatory']=replace(mm['drawP03Conservatory'],anchor,replacement)
 output['main.sc']=merge(main,hooks)
 selectors=json.loads((F/'selectors.json').read_text());allocation={'h9Geo':3164,'h9Label':3165,'h9UI':3166}
 require(not set(allocation)&set(selectors) and not set(allocation.values())&set(selectors.values()),'Selector collision')
 selectors.update(allocation)
 for name,text in output.items():
  balanced(text);path=H/'src'/name
  if check:require(path.is_file() and path.read_text()==text,'Derived source drift '+name)
  else:path.write_text(text)
 require({p.name for p in (H/'src').glob('*.sc')}==set(output),'Unexpected script')
 if check:require(json.loads((H/'selectors.json').read_text())==selectors,'Selector drift')
 else:
  dump(H/'selectors.json',selectors);dump(H/'HOST-ALLOCATION.json',allocation)
  dump(H/'INTEGRATION-DELTA.json',{'base':'accepted inactive P09 foundation','changed_main_methods':list(hooks),'new990_methods':list(added),'new990_locals':{'h9G':80},'main_new_properties':[],'new_saved_viewpoint_state':False,'h9Active':'unchanged constantfalse','h9Dispatch':'unchanged closed395–399 refusal','future_rebase':'Apply after foundation deltas to separately accepted P08 E03 source; never replace its989 or storage/readiness code.'})
 return output,selectors
if __name__=='__main__':derive('--check' in sys.argv);print('PASS_GUARDED_GEOMETRY_DERIVATION')
