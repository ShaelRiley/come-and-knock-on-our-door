#!/usr/bin/env python3
"""Receipt must match exact current source, test, nested output and compiled bytes."""
from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;status=H/'evidence/current-status.json'
try:
 if sys.flags.optimize:raise RuntimeError('Optimized Python forbidden')
 import gate_support as g
 g.check_inventories();g.check_build_inventory()
 d=json.loads(status.read_text());g.need(d['status']=='PASS_SOURCE_EMITTED_ONLY'and d['acceptance_schema']==1,'No current aggregate proof')
 expected=json.loads((H/'REQUIRED-TESTS.json').read_text());g.need(expected==d['required_tests'],'Test identity receipt changed')
 o=d['test_outcomes'];g.need(o['run']==len(expected)and bool(expected),'Incomplete tests')
 for k in('skipped','expected_failures','unexpected_successes','failures','errors'):g.need(o[k]==0,'Rejected result '+k)
 path=H/'evidence/verified-files.json';g.need(g.sha(path)==d['proof_manifest_sha256'],'Proof manifest modified');pins=json.loads(path.read_text())
 g.need(sorted(pins)==g.proof_files(),'Missing/extra proof resource or nested generated output')
 for rel,digest in pins.items():g.need(g.sha(H/rel)==digest,'Stale proof: '+rel)
 print('Verified current source/emitted proof only; native/listening not accepted')
except BaseException as exc:
 status.parent.mkdir(exist_ok=True)
 status.write_text(json.dumps(dict(status='FAILED',stage='receipt-verification',error=str(exc),native_acceptance=False,listening_accepted=False,live_activated=False),indent=2)+'\n')
 raise
