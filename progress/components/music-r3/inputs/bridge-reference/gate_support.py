#!/usr/bin/env python3
"""Fixed inventories and completed-receipt validation shared by R2 entrypoints."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
BASE_EVIDENCE=[
 'evidence/test-results.json','evidence/exhaustive-phase-sweep.json',
 'evidence/missed-aperture-sweep.json','evidence/render-results.json',
 'evidence/render.log','evidence/supplemental-render-results.json',
 'evidence/supplemental-render.log','evidence/build.py.log',
 'evidence/ready.py.log','evidence/tables.py.log','evidence/test.py.log',
 'evidence/guard-checks.json']
R2_GUARDS='evidence/guard-checks-r2.json'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text())
def require(ok,message):
    if not ok:raise RuntimeError(message)
def dump(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def inventory():return read(ROOT/'INVENTORY.json')
def files(folder):
    if not folder.exists():return set()
    result=set()
    for p in folder.rglob('*'):
        require(not p.is_symlink(),'Symlink forbidden in protected inventory: '+str(p))
        if p.is_file()and '__pycache__'not in p.parts:result.add(str(p.relative_to(ROOT)))
    return result

def source_files():
    result=set()
    for p in ROOT.iterdir():
        if p.name in ('generated','renders','evidence','delivery','__pycache__','SHA256SUMS'):continue
        require(not p.is_symlink(),'Symlink forbidden in source inventory: '+str(p))
        if p.is_file():result.add(p.name)
        elif p.is_dir():result.update(files(p))
    return result

def exact(actual,expected,label):
    require(bool(expected),label+' expected inventory is empty')
    require(actual==expected,label+' inventory mismatch; missing='+repr(sorted(expected-actual))+'; extra='+repr(sorted(actual-expected)))

def validate_data(source_only=False):
    spec=inventory();require(spec['schema']==2,'Unsupported inventory schema')
    exact(source_files(),set(spec['source_files']),'Source')
    exact(files(ROOT/'generated'),set(spec['generated_files']),'Generated')
    for name,pin in spec['generated_files'].items():require(sha(ROOT/name)==pin,'Generated hash mismatch: '+name)
    actual=files(ROOT/'renders');wanted=set(spec['render_files'])
    if actual or not source_only:exact(actual,wanted,'Render')
    for name in actual:require(sha(ROOT/name)==spec['render_files'][name],'Render hash mismatch: '+name)
    reports=[]
    for name,status in [('render-results.json','PASS_OFFLINE_COMPONENT_ONLY'),('supplemental-render-results.json','PASS_OFFLINE_SUPPLEMENT_ONLY')]:
        r=read(ROOT/'evidence'/name);require(r['status']==status,'Incomplete render receipt: '+name)
        require(r['renderer_sha256']==sha(ROOT/'render.py'),'Original renderer receipt stale')
        if 'supplemental_renderer_sha256'in r:require(r['supplemental_renderer_sha256']==sha(ROOT/'supplemental_render.py'),'Supplemental renderer receipt stale')
        for n,pin in r['input_native_sha256'].items():require(sha(ROOT/f'generated/{n}.sound.bin')==pin,'Rendered native bytes changed: '+n)
        reports.extend(x for x in r['reports']if 'path'in x)
    declared={x['path']:x['sha256']for x in reports}
    require(len(reports)==len(declared),'Duplicate WAV receipt identity')
    require(declared==spec['render_files'],'Render receipts do not match fixed WAV inventory')
    return bool(actual)

def evidence_files():
    values=list(BASE_EVIDENCE)
    if (ROOT/R2_GUARDS).exists():values.append(R2_GUARDS)
    return values

def receipt_paths():
    spec=inventory()
    return sorted(set(spec['source_files'])|set(spec['generated_files'])|set(evidence_files()))

def verify_receipt(source_only=False):
    audio=validate_data(source_only);receipt=read(ROOT/'evidence/current-status.json')
    required=read(ROOT/'REQUIRED-TESTS.json')['test_ids']
    require(receipt.get('status')=='PASS_SOURCE_AND_OFFLINE_EVIDENCE_R2','No completed R2 receipt')
    require(receipt.get('test_ids')==required and receipt.get('tests_run')==len(required),'Completed test inventory mismatch')
    exact(set(receipt['input_output_pins']),set(receipt_paths()),'Receipt-bound member')
    for name,pin in receipt['input_output_pins'].items():require(sha(ROOT/name)==pin,'Stale receipt: '+name)
    require(receipt['render_inventory']==inventory()['render_files'],'Completed render inventory mismatch')
    require(receipt['generated_inventory']==inventory()['generated_files'],'Completed generated inventory mismatch')
    return receipt,audio
