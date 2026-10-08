#!/usr/bin/env python3
"""Bounded source, build, equivalence and sealed-checkpoint entrypoints."""
from pathlib import Path
import sys,json,hashlib,subprocess,zipfile
sys.dont_write_bytecode=True
from derive import H,F,sha,dump,require,derive

ROOT_INPUTS=['build.py','derive.py','audit.py','run.py','README.md','DEPENDENCY-INVENTORY.json','EXTRACTION-INVENTORY.json','INPUT-MANIFEST.json','selectors.json']
GROUPS=[('first','tests/check_milestone.py'),('matrix','tests/paint_matrix.py'),('supplement','tests/branch_supplement.py'),('order','tests/state_order.py'),('preparation','tests/preparation_matrix.py')]

def sources():
 paths=[p for d in ['src','tools','tests','toolchain','references'] for p in (H/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
 paths += [H/n for n in ROOT_INPUTS]
 return {str(p.relative_to(H)):sha(p) for p in sorted(paths)}
def source_identity():return hashlib.sha256(json.dumps(sources(),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def outputs():
 paths=[p for p in (H/'build/coherent').rglob('*') if p.is_file() and p.suffix!='.sco']
 return {str(p.relative_to(H)):sha(p) for p in sorted(paths)}
def coverage():
 c=json.loads((H/'evidence/matrix-coverage.json').read_text());p=json.loads((H/'evidence/preparation-coverage.json').read_text());s=json.loads((H/'evidence/supplement-coverage.json').read_text());summary=[]
 for v in c[:2]:
  require(len(p)==4,'Preparation coverage incomplete');extra={tuple(x) for x in p[v['variant']]['branches']};sup={(x['module'],x['method']):x for x in s[v['variant']]['emitted']};rows=[]
  for m in v['emitted']:
   if v['variant']==1 and m['module']!=991:continue
   miss2=sup[m['module'],m['method']]['uncovered_branch_edges'];missing=[x for x in m['uncovered_branch_edges'] if x in miss2 and (m['module'],m['method'],x['pc'],x['taken']) not in extra]
   require(not missing,'Reachable branch coverage missing',m['method'],missing)
   rows.append({'method':m['method'],'conditional_edges':m['branch_edges'],'uncovered_conditional_edges':missing})
  summary.append({'variant':v['variant'],'methods':rows,'conditional_edges':sum(r['conditional_edges'] for r in rows),'covered':sum(r['conditional_edges'] for r in rows)})
 require(all(v['conditional_edges']==376 for v in summary),'Expected finite branch set changed')
 result={'status':'PASS_ALL_MOVED_CONDITIONAL_EDGES','programs':summary,'input_receipts':{n:sha(H/'evidence'/n) for n in ['matrix-coverage.json','preparation-coverage.json','supplement-coverage.json']},'scope':'All conditional outgoing edges of the fourteen original/moved emitted paint methods; does not claim all possible state combinations or native execution','native_acceptance':False}
 dump(H/'evidence/combined-coverage.json',result);return result

def finalize():
 from audit import audit
 audit();derive(True);coverage()
 required={'first-equivalence.json':'PASS_FIRST_EMITTED_EQUIVALENCE','matrix-complete.json':'PASS_FOUR_WAY','branch-supplement.json':'PASS_FOUR_WAY','state-order-progress.json':'PASS_FOUR_WAY_ORDER_READER_MENU_RESTORE','preparation-progress.json':'PASS_FOUR_WAY_ACTUAL_PREPARATION','cold-reproducibility.json':'PASS_COLD_BYTE_REPRODUCTION'}
 for n,status in required.items():require(json.loads((H/'evidence'/n).read_text())['status']==status,'Incomplete receipt',n)
 dump(H/'SOURCE-MANIFEST.json',sources());dump(H/'OUTPUT-MANIFEST.json',outputs())
 receipt={'status':'PASS_NON_NATIVE_SCENERENDERER_EXTRACTION','source_identity_sha256':source_identity(),'source_manifest_sha256':sha(H/'SOURCE-MANIFEST.json'),'output_manifest_sha256':sha(H/'OUTPUT-MANIFEST.json'),'evidence':{n:sha(H/'evidence'/n) for n in [*required,'static-audit.json','draw-chain-rebinding.json','combined-coverage.json']},'class':{'script':991,'species':13,'export':0},'main_bytes':54642,'main_headroom':10893,'bytes_recovered':10146,'new_selector_names':0,'native_acceptance':False,'live_game_changed':False,'future_rebase':'Preserve separately accepted current P08 ACK/kernel storage/E03 source; apply extraction transform only, never replace989 with ancestor.'}
 dump(H/'VERIFICATION.json',receipt);dump(H/'CURRENT-GATE.json',receipt);print(receipt['status']);return receipt

def check():
 derive(True);require(sources()==json.loads((H/'SOURCE-MANIFEST.json').read_text()),'Source manifest drift');require(outputs()==json.loads((H/'OUTPUT-MANIFEST.json').read_text()),'Output manifest drift')
 gate=json.loads((H/'VERIFICATION.json').read_text());require(gate['status']=='PASS_NON_NATIVE_SCENERENDERER_EXTRACTION' and gate['source_identity_sha256']==source_identity(),'Unbound gate')
 for n,digest in gate['evidence'].items():require(sha(H/'evidence'/n)==digest,'Evidence changed',n)
 for n,key in [('SOURCE-MANIFEST.json','source_manifest_sha256'),('OUTPUT-MANIFEST.json','output_manifest_sha256')]:require(sha(H/n)==gate[key],'Manifest changed',n)
 print('PASS_BOUND_CHECKPOINT');return gate

def reproduce():
 before=sources();dump(H/'VERIFICATION.json',{'status':'REBUILDING','native_acceptance':False})
 subprocess.run([sys.executable,'-B',str(H/'build.py')],check=True)
 receipts=[]
 for name,script in GROUPS:
  before_group=sources();output_before=outputs()
  with (H/f'evidence/reproduce-{name}.log').open('w') as log:subprocess.run([sys.executable,'-B',str(H/script)],stdout=log,stderr=subprocess.STDOUT,check=True)
  require(sources()==before_group and outputs()==output_before,'Inputs changed during group',name)
  receipts.append({'group':name,'status':'PASS','source_identity_sha256':source_identity(),'log_sha256':sha(H/f'evidence/reproduce-{name}.log')});dump(H/'evidence/reproduction-groups.json',receipts)
 require(sources()==before,'Reproduction source drift');finalize()

def package():
 check();paths=[p for p in H.rglob('*') if p.is_file() and not {'delivery','library-helper','__pycache__'}.intersection(p.relative_to(H).parts) and p.name!='PACKAGE-MANIFEST.json']
 # Historical attempts remain sealed evidence. No hidden caches or recursive archives.
 manifest={str(p.relative_to(H)):sha(p) for p in sorted(paths)};dump(H/'PACKAGE-MANIFEST.json',manifest);paths.append(H/'PACKAGE-MANIFEST.json')
 out=H/'delivery/CaKoOD-SceneRenderer991-Compile-Equivalence-Milestone-20261007.zip'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(paths):
   n=str(p.relative_to(H));i=zipfile.ZipInfo('scene991-extraction-r1/'+n,(2026,10,7,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=(0o100755 if n.endswith('/scicompile') else 0o100644)<<16;z.writestr(i,p.read_bytes())
 print(str(out),out.stat().st_size,sha(out));return out
if __name__=='__main__':
 require(not sys.flags.optimize,'Optimized Python forbidden')
 command=sys.argv[1] if len(sys.argv)>1 else 'check'
 if command=='finalize':finalize()
 elif command=='check':check()
 elif command=='reproduce':reproduce()
 elif command=='package':package()
 elif command=='coverage':coverage()
 else:raise SystemExit('Use check, reproduce, coverage, finalize, package')
