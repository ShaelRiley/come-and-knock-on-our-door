#!/usr/bin/env python3
"""Reuse proved binary structural checks; no native runtime launched."""
from pathlib import Path
import importlib.util
import json
import re
import struct
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('module_binary_checks', HERE.parent/'module-loading-proof/validate.py')
sys.path.insert(0, str(HERE.parent))
import pack
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)

def relocations(script, heap):
    result = {}
    for name, data in (('script', script), ('heap', heap)):
        start = checks.word(data, 0)
        count = checks.word(data, start)
        assert start + 2 + count * 2 == len(data)
        offsets = [checks.word(data, start + 2 + i * 2) for i in range(count)]
        assert len(offsets) == len(set(offsets))
        for offset in offsets:
            assert offset % 2 == 0 and 0 <= offset < start
            # This fixture relocates export0 and object-name pointers into heap.
            assert checks.word(data, offset) < checks.word(heap, 0)
        result[name] = {'table_offset': start, 'count': count, 'pointer_offsets': offsets}
    assert 8 in result['script']['pointer_offsets']
    return result


def main():
    packed = HERE/'build/compile-fixture'
    pack.validate_resources(packed)
    records = {(r['type'],r['number']):r for r in json.loads((packed/'manifest.json').read_text())['resources']}
    assert set(records) == {(2,0),(17,0),(2,994),(17,994),(6,996),(6,997),(7,0),(11,999)}
    volume = (packed/'resource.000').read_bytes()
    record = records[(6,996)]
    start = record['offset']+9
    assert volume[start:start+record['size']] == struct.pack('<4H',0,0,0,994)
    result = {'scope':'Compiled structure only; not native execution',
              'standalone_class_owners':[0,994], 'production_reserved_species':16,
              'scripts':[]}
    for number, source, classname, exported, species in (
            (0,'main','Game','p12Harness',0), (994,'module994','P12State','p12State',1)):
        path = HERE/f'build/compiled/{number}.scr.bin'
        script, heap = path.read_bytes(), Path(str(path)+'.hep').read_bytes()
        # Conservatively include padding to a four-byte script boundary.
        segment_bytes = len(script) + (-len(script) % 4) + len(heap)
        assert segment_bytes <= 65535
        assert checks.word(script,6) == 1
        relocs = relocations(script,heap)
        objects = checks.objects(script, heap)
        assert len(objects) == 2
        assert objects[0]['species'] == species and objects[0]['name'] == classname
        assert objects[0]['is_class'] and objects[0]['superclass'] == 65535
        assert objects[1]['superclass'] == species and objects[1]['name'] == exported
        assert not objects[1]['is_class'] and objects[1]['species'] == 65535
        assert checks.word(script,8) == objects[1]['offset']
        if number == 994:
            manifest = json.loads((HERE/'manifest.json').read_text())
            selectors = json.loads((HERE/'selectors.json').read_text())
            dictionary = checks.word(heap, objects[0]['offset'] + 4)
            assert objects[0]['properties'] == 9 + len(manifest['all_properties'])
            for index, name in enumerate(manifest['all_properties'], 9):
                assert checks.word(script, dictionary + index * 2) == selectors[name]
        interface = checks.sco(HERE/f'src/{source}.sco',number,classname,species,exported)
        result['scripts'].append({'script':number,'script_bytes':len(script),'heap_bytes':len(heap),
                                  'combined_bytes':len(script)+len(heap), 'segment_bytes_with_padding':segment_bytes,
                                  'objects':objects,'interface':interface,
                                  'relocations':relocs})
    # The compile-only caller must project the complete P12 context contract.
    harness = (HERE/'src/main.sc').read_text()
    context_call = re.search(r'\(helper p12Context:\s+([^()]*)\)', harness)
    assert context_call and len(context_call.group(1).split()) == 20
    result['harness_context_arity'] = 20
    source = (HERE/'src/module994.sc').read_text()
    for forbidden in ('SaveGame', 'RestoreGame', 'DoSound', 'DoAudio', 'GetFarText', '(method (save', 'ScriptID'):
        assert forbidden not in source
    selectors = json.loads((HERE/'selectors.json').read_text())
    assert len(selectors) == len(set(selectors.values()))
    assert 'save' not in selectors
    result['passed'] = True
    (HERE/'evidence/static-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
