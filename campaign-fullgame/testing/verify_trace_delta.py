"""Fail-closed source, exact-byte, complete-heap and structural-layout certificate."""
from pathlib import Path
import argparse, copy, hashlib, json, sys
sys.dont_write_bytecode = True
H = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(H/'source/tools'))
from source_tools import methods
OLD = {
    'audioTrace': 'c5058f6ecd2b4aaca41c2edad6a75f242d17510fcf5423ca74a2a57243058692',
    'hostTrace': '23caf2586324034e886e7345a323cb7422ad822943d0d5f5cda972b5156c013f',
    'speechTrace': '6568efb644608874035447a694243f3387d1c9767a4ceeceff44e41530e3ac6a',
}
BYTE_REPLACEMENTS = {
    1699: ('62ac00', '350048'),
    16451: ('39035b0401', '3500481818'),
    36608: ('633e18', '350048'),
}


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def normalized_layout(layout):
    result = copy.deepcopy(layout)
    for key in ('script', 'heap', 'script_sha256', 'heap_sha256'):
        result.pop(key)
    return result

def verify(baseline, candidate, diagnostic=False):
    B, C = baseline/'build/coherent', candidate/'build/coherent'
    old_receipt = json.loads((B/'compile-receipt.json').read_text())
    receipt = json.loads((C/'compile-receipt.json').read_text())
    assert receipt['status'] == 'PASS_FRESH_COMPILE'
    assert not diagnostic, 'This public verifier certifies production r17 against r16'
    assert sha(B/'compile-receipt.json') == 'b3f839512100c06368ce903ecc018bad8ac600ce6ccf647401f693b50c56ce48'
    assert sha(C/'compile-receipt.json') == '529836a5bed4111ec7917e94c9e40ac63d1d92bccf51fba6c26502f5fac1fda1'
    assert receipt['diagnostic_traces'] is False
    assert (baseline/'selectors.json').read_bytes() == (candidate/'selectors.json').read_bytes()
    assert {p.name for p in (baseline/'src').glob('*.sc')} == {p.name for p in (candidate/'src').glob('*.sc')}
    source_changes = {}
    for source in (baseline/'src').glob('*.sc'):
        before, after = source.read_text(), (candidate/'src'/source.name).read_text()
        if before == after: continue
        assert source.name == 'main.sc' and not diagnostic
        a, b = methods(before), methods(after)
        assert set(a) == set(b)
        names = {name for name in a if a[name] != b[name]}
        assert names == set(OLD)
        source_changes[source.name] = sorted(names)
        # Retain every byte outside these three complete method spans.
        for name in names: before = before.replace(a[name], ''); after = after.replace(b[name], '')
        assert before == after
    assert bool(source_changes) != diagnostic
    old_abi, abi = [json.loads((root/'ABI-MAPPINGS.json').read_text()) for root in (B, C)]
    assert old_abi['selectors'] == abi['selectors']
    assert set(old_abi['modules']) == set(abi['modules'])
    rows=[]; raw_artifacts=[]
    for old in old_receipt['modules']:
        number=old['module']; current=next(row for row in receipt['modules'] if row['module']==number)
        differences=[]
        for suffix, key in (('', 'script_sha256'), ('.hep', 'heap_sha256')):
            name=f'compiled/{number}.scr.bin{suffix}';a=(B/name).read_bytes();b=(C/name).read_bytes()
            assert sha(B/name)==old[key] and sha(C/name)==current[key],name
            assert len(a)==len(b),name
            if number==0 and not suffix and not diagnostic:
                expected=bytearray(a)
                for offset,(old_hex,new_hex) in BYTE_REPLACEMENTS.items():
                    old_bytes,new_bytes=bytes.fromhex(old_hex),bytes.fromhex(new_hex)
                    assert a[offset:offset+len(old_bytes)]==old_bytes
                    assert len(old_bytes)==len(new_bytes)
                    expected[offset:offset+len(old_bytes)]=new_bytes
                assert b==expected,'Exact 11-byte target FAILED'
                differences=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
                assert len(differences)==11
            else: assert a==b,('Unexpected compiled difference',name)
        old_module, module=old_abi['modules'][str(number)],abi['modules'][str(number)]
        old_layout=normalized_layout(old_module['reference_layout']); layout=normalized_layout(module['reference_layout'])
        if number==0 and not diagnostic:
            # The historical extractor reads a nonexistent instance selector table
            # from script code. Certify exactly two overlapping label artifacts;
            # do not ignore arbitrary metadata or change the extractor's output.
            old_instance=old_layout['objects'][2]; instance=layout['objects'][2]
            assert old_instance['name']==instance['name']=='cakood'
            assert old_instance['superclass']==instance['superclass']==0
            assert old_instance['property_selector_offset']==instance['property_selector_offset']==1546
            for index, old_id, old_label, new_id, new_label, inherited_id, inherited_name in (
                (76,25089,'__internal_6201',13569,'__internal_3501',18,'audioApron'),
                (77,172,'p02BoardRecords',18432,'__internal_4800',22,'audioDialogue')):
                previous=old_instance['properties'][index]; current_property=instance['properties'][index]
                assert (previous['selector_id'],previous['selector'])==(old_id,old_label)
                assert (current_property['selector_id'],current_property['selector'])==(new_id,new_label)
                inherited=old_layout['objects'][0]['properties'][index]
                assert (inherited['selector_id'],inherited['selector'])==(inherited_id,inherited_name)
                assert inherited==layout['objects'][0]['properties'][index]
                offset=1546+2*index
                original_code=(B/'compiled/0.scr.bin').read_bytes()[offset:offset+2]
                current_code=(C/'compiled/0.scr.bin').read_bytes()[offset:offset+2]
                assert int.from_bytes(original_code,'little')==old_id
                assert int.from_bytes(current_code,'little')==new_id
                raw_artifacts.append({'module':0,'object':'cakood','property_index':index,'heap_offset':previous['heap_offset'],
                    'misread_script_offset':offset,'original_script_bytes':original_code.hex(),'candidate_script_bytes':current_code.hex(),
                    'before':{'selector_id':old_id,'selector':old_label},'after':{'selector_id':new_id,'selector':new_label},
                    'unchanged_inherited_selector':{'selector_id':inherited_id,'selector':inherited_name}})
                current_property['selector_id']=old_id;current_property['selector']=old_label
                assert current_property==previous
        assert old_layout==layout,('Layout drift beyond certified raw extraction artifacts',number)
        assert old_module['locals']==module['locals'] and old_module['classes']==module['classes'],('ABI drift',number)
        rows.append({'module':number,'changed_script_offsets':differences,'script_sha256':current['script_sha256'],'heap_sha256':current['heap_sha256']})
    for name in ('resource.map','resource.000','selector-list.json'):
        assert (B/name).read_bytes()==(C/name).read_bytes(),name
    assert old_receipt['class_owners']==receipt['class_owners']
    result={'status':'PASS_ORIGINAL_DIAGNOSTIC_BUILD' if diagnostic else 'PASS_EXACT_ELEVEN_BYTE_PRODUCTION_TRACE_GUARD',
            'baseline_receipt_sha256':sha(B/'compile-receipt.json'),'candidate_receipt_sha256':sha(C/'compile-receipt.json'),
            'baseline_source_sha256':sha(baseline/'src/main.sc'),'candidate_source_sha256':sha(candidate/'src/main.sc'),
            'source_changes':source_changes,'modules':rows,'all_heaps_identical':True,'all_method_addresses_identical':True,
            'all_strings_and_relocations_identical':True,'all_effective_selectors_properties_locals_exports_identical':True,
            'raw_abi_instance_label_artifacts':raw_artifacts,
            'native_acceptance':False,'native_save_compatibility':'NOT_ASSESSED_BY_THIS_SOURCE_VERIFIER'}
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Compare two already-built public trees; no compile, runtime, or output mutation')
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--candidate',type=Path,required=True)
    a=parser.parse_args()
    if sys.flags.optimize:raise RuntimeError('Optimized Python is unsupported')
    verify(a.baseline.resolve(),a.candidate.resolve())
