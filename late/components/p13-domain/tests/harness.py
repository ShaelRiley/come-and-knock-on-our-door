"""Identical domain interface over readable source and actual emitted SCI bytecode.

The accepted evaluators are copied byte-for-byte. Only construction/metadata is
adapted here; no instruction or source expression semantics are overridden.
"""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
H = Path(__file__).resolve().parents[1]
B = H / 'build/isolated'
sys.path.insert(0, str(H / 'tools'))
import domain_source_vm as source_base
import host_vm as emitted_base
from domain_metadata import declarations, literal

emitted_base.HERE = H / 'tools'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class SourceDomain(source_base.VM):
    def __init__(self, path=None, init=True):
        source = Path(path or H / 'src/module995.sc').read_text()
        ast = source_base.parse(source)
        cls = next(n for n in ast if n[:2] == ['class', 'P13State'])
        props = next(n[1:] for n in cls[2:] if isinstance(n, list) and n[0] == 'properties')
        if len(props) % 2:
            raise ValueError('Unpaired source properties')
        self.constants = {n[1]: n[2] for n in ast if n[0] == 'define'}
        self.p = {props[i]: literal(props[i+1], self.constants) for i in range(0, len(props), 2)}
        self.methods = {n[1][0]: n for n in cls[2:] if isinstance(n, list) and n[0] == 'method'}
        self.arrays = {a['name']: list(a['initial_words']) for a in declarations(source)}
        if init:
            self.call('p13Init')


class EmittedDomain:
    def __init__(self, build=None, init=True, budget=100000000):
        build = Path(build or B)
        receipt = json.loads((build / 'compile-receipt.json').read_text())
        if receipt['status'] != 'PASS_FRESH_COMPILE':
            raise RuntimeError('Fresh successful compile required')
        for row in receipt['modules']:
            original = H / ('tools/compiler-main.sc' if row['module'] == 0 else f"src/module{row['module']}.sc")
            if sha(original) != row['source_sha256']:
                raise RuntimeError(('Source changed since fresh compile', str(original)))
        if sha(H / 'toolchain/scicompile') != receipt['compiler_sha256']:
            raise RuntimeError('Compiler changed since fresh compile')
        if sha(build / 'selector-list.json') != receipt['selector_sha256']:
            raise RuntimeError('Selectors changed since fresh compile')
        abi = build / 'verification-checkpoint/source-provenance/ABI-MAPPINGS.json'
        if sha(abi) != receipt['abi_sha256'] or sha(build / 'ABI-MAPPINGS.json') != receipt['abi_sha256']:
            raise RuntimeError('ABI changed since fresh compile')
        if receipt.get('schema_sha256') and sha(H / 'manifest.json') != receipt['schema_sha256']:
            raise RuntimeError('Schema changed since fresh compile')
        for row in json.loads((H / 'tools/ACCEPTED-HELPERS.json').read_text())['files']:
            if sha(H / row['destination']) != row['sha256']:
                raise RuntimeError(('Accepted evaluator/helper changed', row['destination']))
        self.vm = emitted_base.HostVM(checkpoint=build / 'verification-checkpoint', build=build, budget=budget)
        self.object = self.vm.objects['p13State']
        self.p = self.object.p
        self.arrays = self.object.arrays
        if init:
            self.call('p13Init')

    def call(self, name, *args):
        return self.object.call(name, *args)


def snapshot(domain):
    return dict(properties=dict(domain.p), arrays={k: list(v) for k, v in domain.arrays.items()})


def compare_calls(calls, init=True):
    """Compare every return value and full state after each identical method call."""
    source, emitted = SourceDomain(init=init), EmittedDomain(init=init)
    assert snapshot(source) == snapshot(emitted), ('initial state', snapshot(source), snapshot(emitted))
    results = []
    for name, args in calls:
        left, right = source.call(name, *args), emitted.call(name, *args)
        assert left == right, ('return mismatch', name, args, left, right)
        assert snapshot(source) == snapshot(emitted), ('state mismatch', name, args, snapshot(source), snapshot(emitted))
        results.append(left)
    return source, emitted, results


if __name__ == '__main__':
    source, emitted, _ = compare_calls([('p13Init', ())])
    print('PASS_SOURCE_EMITTED_INITIALIZATION', len(source.p), 'properties', len(source.arrays), 'arrays', emitted.vm.steps, 'instructions')
