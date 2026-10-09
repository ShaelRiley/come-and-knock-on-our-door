#!/usr/bin/env python3
"""Portable bounded source/asset checks. One fresh process per independent case."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time,traceback
sys.dont_write_bytecode=True
S=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',choices=['pins','preservation','opening','credits']);p.add_argument('--output',type=Path,default=S/'build/static-checks');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
if not a.case:
 summary={'status':'RUNNING','scope':'BOUNDED_STATIC_NOT_NATIVE','cases':[]}
 for case in ['pins','preservation','opening','credits']:
  started=time.monotonic()
  with (a.output/f'{case}.log').open('w') as f:
   try:r=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--case',case,'--output',str(a.output)],stdout=f,stderr=subprocess.STDOUT,timeout=90);code=r.returncode
   except subprocess.TimeoutExpired:code=124
  q=a.output/f'{case}.json';detail=json.loads(q.read_text()) if q.exists() else {}
  row={'case':case,'exit_code':code,'wall_seconds':time.monotonic()-started,'status':detail.get('status','NO_RECEIPT'),'max_rss_kib':detail.get('max_rss_kib'),'receipt_sha256':sha(q) if q.exists() else None};summary['cases'].append(row);print(json.dumps(row),flush=True)
  if code:summary['status']='FAIL';break
 else:summary['status']='PASS_BOUNDED_STATIC_NOT_NATIVE'
 (a.output/'SUITE.json').write_text(json.dumps(summary,indent=2)+'\n');raise SystemExit(summary['status'].startswith('FAIL'))
report={'case':a.case,'status':'RUNNING','native_acceptance':False};start=time.monotonic()
try:
 if a.case=='pins':
  profile=json.loads((S/'BUILD-PROFILE.json').read_text())
  for name,pin in profile['protected_inputs'].items():assert sha(S/name)==pin,name
  inventory=json.loads((S/'RESOURCE-INVENTORY.json').read_text());assert len(inventory)==len({(x['type'],x['number']) for x in inventory})
  assert {x['extracted_path'] for x in inventory if (x['type'],x['number']) not in {(6,996),(6,997)}}=={p.name for p in (S/'assets/resources').iterdir()}
  for row in inventory:
   if (row['type'],row['number']) in {(6,996),(6,997)}:continue # generated and identity-checked by the compiler build
   q=S/'assets/resources'/row['extracted_path'];assert q.stat().st_size==row['size'] and sha(q)==row['sha256'],q.name
  audio=json.loads((S/'AUDIO-INVENTORY.json').read_text());assert audio['file_count']==len(audio['files'])==profile['audio_files'];assert set(audio['files'])=={p.name for p in (S/'assets/audio').iterdir()}
  for name,row in audio['files'].items():
   q=S/'assets/audio'/name;assert q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],name
  report.update(resources=len(inventory),audio_files=len(audio['files']),protected=len(profile['protected_inputs']))
 elif a.case=='preservation':
  sys.path.insert(0,str(S/'tools'));from source_tools import methods
  pins=json.loads((S/'CORE-PRESERVATION.json').read_text());count=0
  for filename,entries in pins['unchanged_methods'].items():
   current=methods((S/'src'/filename).read_text())
   for name,pin in entries.items():assert hashlib.sha256(current[name].encode()).hexdigest()==pin,(filename,name);count+=1
  selectors=json.loads((S/'selectors.json').read_text())
  for name,value in pins['preserved_selectors'].items():assert selectors[name]==value,(name,value)
  report.update(unchanged_core_methods=count,preserved_selectors=len(pins['preserved_selectors']))
 elif a.case=='opening':
  art=json.loads((S/'OPENING-ASSET-MANIFEST.json').read_text());assert not art.get('fixture_category');assert art['performed_pose_count']==64;assert set(art['views'])==set(range(245,253))
  sys.path.insert(0,str(S/'tools'));from inspect_opening_view import decode_view
  hashes=[]
  for view in range(245,253):
   loops=decode_view((S/'assets/resources'/f'{view}.view.bin').read_bytes());assert len(loops[0])==8 and len(loops[1])==len(loops[2])==1
   cells=[hashlib.sha256(c['pixels']).hexdigest() for c in loops[0]];assert len(set(cells))==8,view;hashes+=cells
  assert len(set(hashes))==64
  src=(S/'src/module970.sc').read_text();assert 'TIMING TEST' not in src and 'STATIC REFERENCE' not in src and 'AUDIO_TIMING_ONLY' not in src
  assert 'DrawCel 301' not in src
  report.update(views=8,distinct_action_cels=64)
 elif a.case=='credits':
  credits=json.loads((S/'P14-CREDIT-URLS.json').read_text());text=(S/'assets/resources/215.text.bin').read_bytes()
  for name in ['Ned Still','Quinn Keyes','Roxy Bellows','Perry Quibble','Kit Glitch','Bea Bunch','Ada Branch','Mira Aside']:assert name.encode() in text,name
  assert credits['mandatory_cards']==26 and credits['total_cards']==26+credits['asset_cards']
  masks=credits['masks'];assert all(0<=x<=32767 for x in masks[:2]) and 0<=masks[2]<=7;assert sum(x.bit_count() for x in masks)==credits['asset_cards']
  src=(S/'src/module996.sc').read_text()
  for i,value in enumerate(masks):assert f'(define H14_CREDIT_MASK{i} {value})' in src
  assert 'Blender Foundation / LeeZH' in src and 'opengameart.org/content/applause' in src
  report.update(writers=8,credit_cards=credits['total_cards'],supplementary_credit='Applause / Blender Foundation / LeeZH / CC BY3.0')
 report['status']='PASS_STATIC_NOT_NATIVE'
except BaseException as e:
 report.update(status='FAIL',error=repr(e),traceback=traceback.format_exc());raise
finally:
 try:
  import resource
  report['max_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 except ImportError:report['max_rss_kib']=None
 report['wall_seconds']=time.monotonic()-start;(a.output/f'{a.case}.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
