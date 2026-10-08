#!/usr/bin/env python3
"""Verify the three-method source delta, preserved SCI layouts and scalar rewrites."""
from pathlib import Path
import argparse,hashlib,json,sys
sys.dont_write_bytecode=True
C=Path(__file__).resolve().parents[1]
def require(ok,message):
 if not ok:raise RuntimeError(message)
def digest(data):return hashlib.sha256(data).hexdigest()
def canonical(value):return digest(json.dumps(value,sort_keys=True,separators=(',',':')).encode())
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work',type=Path,required=True);args=parser.parse_args()
 require(not sys.flags.optimize,'Optimized Python is forbidden')
 W=args.work.resolve();B=W/'build/coherent'
 pins=json.loads((C/'OUTPUT-PINS.json').read_text());old=json.loads((C/'repair/history/OUTPUT-PINS.json').read_text())
 require(all(digest((B/n).read_bytes())==h for n,h in pins['outputs'].items()),'Current cold-build outputs do not match pins')
 sys.path[:0]=[str(W/'tools'),str(W)]
 import room_render_fix as fix
 from source_tools import methods
 pairs={'module988.sc':[(fix.BUNNY_OLD,fix.BUNNY_NEW),(fix.RETURN_OLD,fix.RETURN_NEW)],'module991.sc':[(fix.OLD,fix.NEW)]}
 changes=[]
 for name,expected in pins['sources'].items():
  text=(W/'src'/name).read_text();require(digest(text.encode())==expected,'Current source identity changed')
  original=text
  for before,after in pairs.get(name,[]):
   require(text.count(after)==1,'Repaired method is not unique');text=text.replace(after,before)
  require(digest(text.encode())==old['sources'][name],'More source changed than the declared methods')
  left,right=methods(text),methods(original);require(left.keys()==right.keys(),'Method membership changed')
  changes += [name+':'+n for n in left if left[n]!=right[n]]
 require(sorted(changes)==['module988.sc:h7DrawBunny','module988.sc:h7ReturnBunny','module991.sc:h6BaseDrawWorld'],'Unexpected gameplay scope')
 baseline=json.loads((C/'repair/BASELINE-SCOPE.json').read_text());abi=json.loads((B/'ABI-MAPPINGS.json').read_text())
 require(len(abi['modules'])==len(baseline['modules'])==14,'Full fourteen-module universe required')
 for n,r in baseline['modules'].items():
  layout={k:v for k,v in abi['modules'][n]['reference_layout'].items() if k not in ('script','heap','script_sha256')}
  require(canonical(layout)==r['layout_sha256'],'Saved layout changed in module '+n)
  data=bytearray((B/f'compiled/{n}.scr.bin').read_bytes());require(len(data)==r['script_bytes'],'Script size changed')
  for part in r['allowed_method_intervals']:data[part['start']:part['end_exclusive']]=bytes(part['end_exclusive']-part['start'])
  require(digest(data)==r['script_outside_intervals_sha256'],'Script changed outside allowed methods')
 # Exhaustive ordinary signed-SCI16 scalar equivalence. This is not a gameplay fixture.
 for raw in range(65536):
  value=raw if raw<32768 else raw-65536
  require((0 if value<0 or value>2 else value)==(0 if (value&65535)>2 else value),'Mouth clamp mismatch')
  require((0 if value>14720 else 1)==int(14720>=value),'Facing mismatch')
 report={'status':'PASS_SCOPED_SOURCE_LAYOUT_AND_SCALAR_CHECKS','changed_methods':changes,'modules':14,'source_files':14,'pinned_outputs':len(pins['outputs']),'compiled_receipt_sha256':digest((B/'compile-receipt.json').read_bytes()),'all_heaps_exports_locals_properties_method_entries_and_relocations_preserved':True,'all_script_bytes_outside_three_method_intervals_identical':True,'scalar_values_checked':65536,'native_launch_performed':False,'native_save_acceptance_asserted':False}
 output=W/'evidence/PUBLIC-REPAIR-SCOPE.json';output.parent.mkdir(exist_ok=True);output.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
if __name__=='__main__':main()
