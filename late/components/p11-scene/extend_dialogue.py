#!/usr/bin/env python3
"""Append P11 full-record and individual-unit routes without changing prior data."""
from pathlib import Path
import argparse
import importlib.util
import json
import re
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;SCI=HERE/'inputs/p08'
sys.path.insert(0,str(HERE/'tools'))
from source_tools import methods,spans
from caption_util import sha
ARRAYS=('sdStarts','sdCounts','sdPageData','sdLegacyVoiceDurations','sdTextResources','sdAudioModules','sdPageDurations')
def read_array(source,name):
 m=re.search(r'\['+name+r' (\d+)\] = \[([^]]*)\]',source)
 assert m is not None,'Missing '+name
 values=[int(v) for v in m[2].split()];assert len(values)==int(m[1]),'Array size '+name
 return values
def array(name,values):return '['+name+' '+str(len(values))+'] = ['+' '.join(map(str,values))+']'
def replace_once(source,old,new):
 assert source.count(old)==1,'Source shape '+old
 return source.replace(old,new)
def replace_array(source,name,values):
 matches=list(re.finditer(r'\['+name+r' \d+\] = \[[^]]*\]',source));assert len(matches)==1
 m=matches[0];return source[:m.start()]+array(name,values)+source[m.end():]
def merge_methods(source,replacements):
 ranges=spans(source);assert set(replacements)<=set(ranges)
 for name in sorted(replacements,key=lambda n:ranges[n][0],reverse=True):
  a,b=ranges[name];source=source[:a]+replacements[name]+source[b:]
 return source


def apply_source(source,manifest=None):
    assert not sys.flags.optimize,'Optimized Python forbidden'
    pin=json.loads((HERE/'COMPATIBILITY.json').read_text())['predecessor']
    assert len(source)>0,'Empty predecessor source'
    before_methods=methods(source)
    frozen_methods=methods((HERE/'inputs/src/module982.sc').read_text())
    for name in ('sdRoute','sdPageCount','hStaticAt'):
        assert before_methods[name]==frozen_methods[name],'Conflicting presentation API/table accessor '+name
    if manifest is None:manifest=json.loads((HERE/'generated/manifest.json').read_text())
    assert manifest['text_resource']==212 and manifest['audio_modules']==[923]
    docs=manifest['document_routes']
    assert [r['document_id'] for r in docs]==list(range(1300,1374))
    old={name:read_array(source,name) for name in ARRAYS}
    slots=len(old['sdStarts']);assert slots==1243 and len(old['sdCounts'])==slots,'Expected exact current P10 universe'
    assert len(old['sdPageData'])%8==0
    old_pages=len(old['sdPageData'])//8;assert old_pages==1241,'Missing prior P02–P10/contest pages'
    assert all(len(old[n])==old_pages for n in ARRAYS[4:])
    assert set(old['sdTextResources'])=={202,203,204,205,206,207,208,210,211,230},'Missing exact current text banks'
    assert set(old['sdAudioModules'])=={0,912,913,914,915,916,917,918,921,922,939}
    assert all(not 1300<=key<=1373 for key in old['sdPageData'][1::8]),'P11 global line collision'
    assert all(0<=count<=64 and (start==-1 if count==0 else 0<=start<=old_pages-count)
        for start,count in zip(old['sdStarts'][1:],old['sdCounts'][1:])),'Malformed prior route'
    for name in ARRAYS:
        assert sha(json.dumps(old[name],separators=(',',':')).encode())==pin['array_hashes'][name],'Predecessor array mismatch '+name
    assert len(manifest['pages'])==103
    assert [p['page_index'] for p in manifest['pages']]==list(range(103))
    assert [(r['first_page'],r['page_count']) for r in docs]==[(r['page_indices'][0],len(r['page_indices'])) for r in docs]
    assert [i for r in docs for i in r['page_indices']]==list(range(103))
    signatures=re.findall(r'\(method \(([^)]*)\)',source)
    arrays={name:values[:] for name,values in old.items()}
    arrays['sdStarts'].extend([-1]*(1374-slots));arrays['sdCounts'].extend([0]*(1374-slots))
    for route in docs:
        arrays['sdStarts'][route['document_id']]=old_pages+route['first_page']
        arrays['sdCounts'][route['document_id']]=route['page_count']
    for page in manifest['pages']:
        assert len(page['fields'])==8 and page['resource']==212
        assert page['audio_module']==(923 if page['voice_index'] else 0)
        arrays['sdPageData'].extend(page['fields']);arrays['sdTextResources'].append(212)
        arrays['sdAudioModules'].append(page['audio_module']);arrays['sdPageDurations'].append(page['duration_ticks'])
    for name in ARRAYS:
        assert arrays[name][:len(old[name])]==old[name]
        if arrays[name]!=old[name]:source=replace_array(source,name,arrays[name])
    total=len(arrays['sdTextResources'])
    assert source.count(f'(> document {slots-1})')==2,'Expected route and count bound'
    source=source.replace(f'(> document {slots-1})','(> document 1373)')
    source=replace_once(source,f'(>= index (* {old_pages} 8))',f'(>= index (* {total} 8))')
    for prop,new in (('sdResource',212),('sdAudioModule',923)):
        matches=list(re.finditer(r'\(and(?:\s+\(!= '+prop+r' \d+\))+\)',source));assert len(matches)==1,prop
        allow=matches[0].group();prior_allow=list(map(int,re.findall(prop+r' (\d+)',allow)))
        expected=pin['texts'] if prop=='sdResource' else [n for n in pin['audio_modules'] if n]
        assert sorted(prior_allow)==expected,'Conflicting prior resource allowlist '+prop
        assert new not in prior_allow
        source=replace_once(source,allow,allow[:-1]+f' (!= {prop} {new}))')
    rows=[f' ({i} (if (or (< index 0) (>= index {len(arrays[name])})) (return 0)) (return [{name} index]))' for i,name in enumerate(ARRAYS,1)]
    source=merge_methods(source,{'hStaticAt':'(method (hStaticAt table index) (switch table\n'+'\n'.join(rows)+'\n) (return 0))'})
    assert re.findall(r'\(method \(([^)]*)\)',source)==signatures
    for name,body in before_methods.items():
        if name not in ('sdRoute','sdPageCount','sdLoad','hStaticAt'):
            assert methods(source)[name]==body,'Unrelated reader method changed '+name
    for name in ARRAYS:assert read_array(source,name)==arrays[name]
    contract={'schema':1,'existing_pages':old_pages,'added_pages':len(manifest['pages']),'total_pages':total,
        'existing_document_slots':slots,'maximum_document':1373,'first_new_document':1300,
        'first_new_global_line_key':1300,'existing_page_stride':8,'existing_array_prefixes_unchanged':True,
        'existing_page_tuples_unchanged':True,'existing_method_signatures_unchanged':True,'unrelated_reader_methods_preserved_from_supplied_input':True,
        'changed_methods':['sdRoute','sdPageCount','sdLoad','hStaticAt'],'new_selectors':[],'shared_zero_clock':911,
        'text_resource':212,'audio_module':923,'arrays':arrays,
        'record_documents':[1300,1325],'unit_documents':[1326,1361],'variant_record_documents':[1362,1365],'variant_unit_documents':[1366,1373],
        'receipt_map':'generated/receipt-map.json','unit_document_map':'generated/unit-document-map.json'}
    return source,contract


extend=apply_source


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,default=HERE/'inputs/src/module982.sc')
    parser.add_argument('--output',type=Path,default=HERE/'generated/module982.sc')
    args=parser.parse_args();assert args.output.resolve().is_relative_to(HERE.resolve())
    from guard import input_check
    input_check()
    raw=args.input.read_bytes();source,contract=apply_source(raw.decode())
    (HERE/'snapshot').mkdir(exist_ok=True);args.output.parent.mkdir(parents=True,exist_ok=True)
    (HERE/'snapshot/module982-input.sc').write_bytes(raw);args.output.write_text(source)
    contract.update(input_source=str(args.input.resolve().relative_to(HERE)),input_sha256=sha(raw),output_source=str(args.output.resolve().relative_to(HERE)),
        output_sha256=sha(source.encode()),manifest_sha256=sha((HERE/'generated/manifest.json').read_bytes()))
    (HERE/'generated/extension-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
    (HERE/'generated/scene-tables.inc').write_text('\n'.join(array(n,v) for n,v in contract['arrays'].items())+'\n')
    import shutil,subprocess
    dest=HERE/'generated/src';dest.mkdir(exist_ok=True)
    for p in (HERE/'inputs/src').glob('*.sc'):shutil.copy2(p,dest/p.name)
    (dest/'module982.sc').write_text(source)
    result=subprocess.run([sys.executable,str(HERE/'tools/generate_static_guards.py')],capture_output=True,text=True)
    (HERE/'evidence/static-generation.log').write_text(result.stdout+result.stderr)
    assert result.returncode==0,result.stdout+result.stderr
    static=HERE/'generated/static'
    assert methods(source)['hStaticAt']==methods((static/'module982-methods.inc').read_text())['hStaticAt']
    previous=(dest/'module985.sc').read_text();guard=methods((static/'guard-methods.inc').read_text())
    updated=merge_methods(previous,{n:guard[n] for n in ['hStaticCount','hStaticFirst','hStaticLoad']})
    (dest/'module985.sc').write_text(updated)
    for name in methods(previous):
        if name not in ['hStaticCount','hStaticFirst','hStaticLoad']:assert methods(previous)[name]==methods(updated)[name],name
    for name in ['hStaticOwner','hStaticValue','hStaticRange','hStaticAll']:assert re.sub(r'\s+','',methods(previous)[name])==re.sub(r'\s+','',guard[name]),name
    assert methods((dest/'module981.sc').read_text())['hStaticAt']==methods((static/'module981-methods.inc').read_text())['hStaticAt']
    assert methods(previous)['hStaticAt']==methods((static/'module985-methods.inc').read_text())['hStaticAt']
    tables=json.loads((static/'manifest.json').read_text());assert len(tables['tables'])==20
    print(json.dumps({k:v for k,v in contract.items() if k!='arrays'},indent=2))


if __name__=='__main__':main()
