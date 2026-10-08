"""NEW portability adaptations; original/final retained payloads remain historical."""
from pathlib import Path
import re,json,difflib,hashlib
W=Path(__file__).resolve().parent; C=W/'component';D=C/'stock-sci/p13-domain-adapter'
# Preserve literal Python now. Gate admission hardening is applied only after contrast.
g=(D/'generate.py').read_text()
g=g.replace("sys.path.insert(0,str(ROOT))", "sys.path.insert(0,str(ROOT))\nfrom tools.verify_inputs import verify\nfrom tools.generate_fixture import fixture as current_fixture\nverify()")
a=g.index(" fixture=json.loads(");b=g.index(" lines={name",a)
g=g[:a]+''' fixture=json.loads((ROOT/'tests/fixtures/p13/canonical-bindings.json').read_text())
 expected=current_fixture()
 if fixture!=json.loads(json.dumps(expected)):raise RuntimeError('Stale or incomplete P13 fixture')
 authority=ROOT/'authority/CURRENT-SCRIPT-REVISION.json'
 records={x['id']:x for x in fixture['records']}
 records.update({x['id']:x for x in fixture['support_records']})
 objects=dict(json.loads((ROOT/'dependencies/p11-current-manifest.json').read_text())['objects'])
 own=json.loads((HERE/'object-bindings.json').read_text())
 if own!={'guest_program_card':432,'pledge_board':433,'screen_pull_tab':434}:raise RuntimeError('Local P13 proposals changed')
 if set(own.values())&set(objects.values()):raise RuntimeError('Local oracle identity collision')
 objects.update(own)
'''+g[b:]
g=g.replace("registry_sha256=sha(ROOT/'docs/native-resource-registry.json')","registry_sha256=sha(ROOT/'authority/retained-registry-subset.json')")
g=g.replace("sha(Path('/workspace/shared/cakood/ending-seam-20261005/current-gdd.txt'))","sha(ROOT/'authority/complete-body.md')")
g=g.replace("competition_contract_sha256=sha(Path('/workspace/shared/cakood/verbal-competitions-update/CANONICAL-CONTRACT.md'))","competition_fixture_sha256=sha(ROOT/'dependencies/data/canonical-bindings.json')")
g=g.replace('Isolated SCI1.1 domain bytecode; genuine host save and native acceptance pending','NEW current finite source oracle only; no compilation, host or native acceptance')
(D/'generate.py').write_text(g)
# Accepted source evaluator, new thin wrapper only, no transition duplication.
p12=W.parents[0]/'p12-reference-reconstruction/component/stock-sci/p12-domain-adapter/tests/source_vm.py'
(D/'tests/source_vm.py').write_text(p12.read_text().replace('P12','P13').replace('p12','p13').replace('994','995'))
t=(D/'tests/test_domain.py').read_text().replace('from compiled_vm import Compiled\n','')
t=t.replace('class BytecodeTests(DomainTests):VM=ByteVM\n','')
(D/'tests/test_domain.py').write_text(t)
# Original complete P13Tests class only. No recovery of absent P12/P14 tests.
first=(W/'historical/literal-read-partial/tests/test_late_campaign_models.py.lines1-85.part').read_text()
last=(W/'historical/literal-read-partial/tests/test_late_campaign_models.py.lines197-289.part').read_text()
header='''"""NEW import shell and selected retained helpers; full retained P13Tests below.
All these tests use synthetic-shaped contexts; genuine owner joins are separate.
No reconstruction of the missing historical late-campaign test suite is claimed.
"""
import copy,json,itertools,unittest
from dataclasses import replace
from pathlib import Path
from hashlib import sha256
from cakood.model import Verb
from cakood.p04_model import GateHandoff
from cakood.p10_model import TILE_IDS,ORDER
from cakood.p12_model import P12World,P12Context,CurrentRig,PEOPLE,COURTYARD,KITCHEN,LIVING,SIDE,PORCH
from cakood.p12_model import PREREQUISITES as P12REQ
from cakood.p13_model import P13World,P13Context,PREREQUISITES as P13REQ,PROGRAM,BOARD
from cakood.verbal_contest import VerbalContests,Phase
from test_verbal_contest import CATALOG,prepared,play,leave
'''
selected=first[first.index('RIG='):first.index('def approve14')]
selected='\n'.join(line for line in selected.split('\n') if not line.startswith('UNSIGNED=') and not line.startswith('def c14('))
klass=last[:last.index('\n\nclass P14Tests')]
(C/'tests/test_late_campaign_models.py').write_text(header+selected+klass+'\n')
# Record exact complete-class boundary independently.
(W/'provenance/retained-p13-test-class.py.txt').write_text(klass)
(W/'provenance/initial-portability.json').write_text(json.dumps({'classification':'NEW portability and import shell adaptations, no historical authorship claim','test_class_sha256':hashlib.sha256(klass.encode()).hexdigest()},indent=2)+'\n')
print('Working source adapters prepared; model literal remains unchanged')
