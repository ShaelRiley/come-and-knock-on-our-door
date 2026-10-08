"""NEW finite portability/ABI adaptations; no historical source recovery claim."""
from pathlib import Path
W=Path(__file__).resolve().parent;C=W/'component';D=C/'stock-sci/p14-domain-adapter';A=W.parent/'p13-reference-reconstruction'
p=D/'generate.py';s=p.read_text();s=s.replace('sys.path.insert(0,str(ROOT))','sys.path.insert(0,str(ROOT))\nfrom tools.verify_inputs import verify\nfrom tools.generate_fixture import fixture as current_fixture\nverify()')
a=s.index(' fixture=json.loads(');b=s.index(' lines={name',a)
s=s[:a]+''' fixture=json.loads((ROOT/'tests/fixtures/p14/canonical-bindings.json').read_text())
 if fixture!=json.loads(json.dumps(current_fixture())):raise RuntimeError('Stale or incomplete current P14 fixture')
 authority=ROOT/'authority/CURRENT-SCRIPT-REVISION.json'
 records={x['id']:x for x in fixture['records']}
 objects=dict(json.loads((ROOT/'dependencies/p13-current-manifest.json').read_text())['objects'])
 own={model.CARD_IDS[p]:435+i for i,p in enumerate(model.PEOPLE)}
 if set(own.values())&set(objects.values()):raise RuntimeError('Local P14 proposal collision')
 objects.update(own)
 (HERE/'object-bindings.json').write_text(json.dumps(own,indent=2)+'\\n')
'''+s[b:]
s=s.replace("registry_sha256=sha(ROOT/'docs/native-resource-registry.json')","registry_sha256=sha(ROOT/'authority/retained-registry-subset.json')")
s=s.replace("sha(Path('/workspace/shared/cakood/ending-seam-20261005/current-gdd.txt'))","sha(ROOT/'authority/complete-body.md')")
s=s.replace('Isolated SCI1.1 domain bytecode; host and native presentation acceptance pending','NEW current finite source oracle only; compilation, host and native presentation acceptance pending')
p.write_text(s)
# Newly labeled wrapper over accepted SCI evaluator, no P14 transition implementation.
s=(A/'component/stock-sci/p13-domain-adapter/tests/source_vm.py').read_text().replace('P13','P14').replace('p13','p14').replace('995','996')
(D/'tests/source_vm.py').write_text(s)
p=D/'tests/test_domain.py';s=p.read_text();s=s.replace('from compiled_vm import Compiled\n','')
a=s.index('class ByteVM:');b=s.index('class Harness:',a);s=s[:a]+s[b:]
a=s.index('\n\nclass BytecodeTests(');b=s.index("\n\nif __name__",a);s=s[:a]+s[b:]
s=s.replace("active.enter('VC01', 0)","active.enter('VC01', 0, admitted=True)")
s=s.replace('Accepted P14 oracle versus source methods and actual emitted SCI instructions.','Retained P14 oracle tests adapted for current owner ABI and source methods only.')
s=s.replace('The compiled evaluator checks every self-send and return with a strict stack.','Compiled execution is excluded from this reference task.')
p.write_text(s)
p=D/'tests/test_validation.py';s=p.read_text().replace('del DomainTests, BytecodeTests','del DomainTests').replace('for typ in (source_vm.VM, ByteVM):','for typ in (source_vm.VM,):').replace('vm = ByteVM()','vm = source_vm.VM()')
s=s.replace("'scope': 'Actual emitted script996 validation; strict self sends and stack returns'","'scope': 'NEW source-only execution of retained P14 validation matrix; no emitted bytecode'")
s=s.replace("'instructions_executed': vm.machine.steps,\n            'script_sha256': hashlib.sha256(vm.machine.blob).hexdigest(),", "'source_sha256': hashlib.sha256((HERE/'src/module996.sc').read_bytes()).hexdigest(),")
s=s.replace("'instructions_executed': vm.machine.steps,\n            'script_sha256': hashlib.sha256(vm.machine.blob).hexdigest(),", "'source_sha256': hashlib.sha256((HERE/'src/module996.sc').read_bytes()).hexdigest(),")
s=s.replace("'actual_emitted_bytecode': True, 'strict_stack_balance': True,", "'actual_emitted_bytecode': False, 'source_only': True,")
s=s.replace("HERE / 'evidence/compiled-validation.json'","HERE / 'evidence/source-validation.json'")
s=s.replace("            if typ is ByteVM:\n                aliases = ('machine', 'locals')\n                arena_before = copy.deepcopy(source.machine.locals)\n            else:\n                aliases = ('arrays', 'array_values', 'cross_key_array')\n                arena_before = copy.deepcopy(source.arrays)","            aliases = ('arrays', 'array_values', 'cross_key_array')\n            arena_before = copy.deepcopy(source.arrays)")
s=s.replace("source.machine.locals if typ is ByteVM else source.arrays",'source.arrays')
p.write_text(s)
# Patch retained helper only for current accepted owner repertoire selection.
p=C/'tests/test_verbal_contest.py';s=p.read_text();s=s.replace("next(iter(w.catalog.pairs[pair].accepted_response_ids))", "next(iter(sorted(set(w.catalog.pairs[pair].accepted_response_ids) & set(w.available_responses()))))")
p.write_text(s)
print('Portable generator, source evaluator and retained-test shell prepared')
