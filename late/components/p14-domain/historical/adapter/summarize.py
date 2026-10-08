#!/usr/bin/env python3
"""Bind successful final logs and native proof reports to the exact built bytes."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent

def main():
 m=json.loads((HERE/'manifest.json').read_text())
 blob=(HERE/'build/compiled/996.scr.bin').read_bytes();heap=(HERE/'build/compiled/996.scr.bin.hep').read_bytes()
 sha=hashlib.sha256(blob).hexdigest()
 compiled=json.loads((HERE/'evidence/compiled-validation.json').read_text())
 finite=json.loads((HERE/'evidence/finite-approval-projection.json').read_text())
 assert compiled['passed'] and finite['passed']
 assert compiled['script_sha256']==finite['script_sha256']==sha
 assert json.loads((HERE/'evidence/static-validation.json').read_text())['passed']
 assert '0 hazards' in (HERE/'evidence/conditional-gate.log').read_text()
 log=(HERE/'evidence/source-tests.log').read_text()
 assert not re.search(r'\.\.\. (FAIL|ERROR)|^FAILED',log,re.M)
 ids=set(re.findall(r'^test_\w+ \(([^)]+)\) \.\.\. ok$',log,re.M))
 assert ids and '\nOK\n' in log
 r={'passed':True,'scope':'Isolated native SCI1.1 domain adapter and exact emitted-bytecode/model conformance; no campaign/native presentation/audio claim',
 'script':996,'export':0,'standalone_species':1,'production_reserved_species':18,'unique_test_cases':len(ids),'test_ids':sorted(ids),
 'persisted_words':len(m['persisted_properties']),'serial_slots':len(m['serials']),'source_count':len(m['sources']),'canonical_record_count':len(m['canonical_records']),
 'mandatory_credit_records':len(m['credit_order']),'optional_asset_records':len(m['asset_credits']),
 'approval_pin_projections':finite['approval_pin_projections'],'save_vectors':compiled['distinct_vectors'],'reachable_snapshots':compiled['reachable_snapshots'],
 'valid_vectors':compiled['valid'],'rejected_vectors':compiled['rejected'],'validator_instructions':compiled['instructions_executed'],'finite_projection_instructions':finite['instructions_executed'],
 'script_bytes':len(blob),'heap_bytes':len(heap),'combined_bytes':len(blob)+len(heap),'source_sha256':m['source_sha256'],'script_sha256':sha,'heap_sha256':hashlib.sha256(heap).hexdigest(),
 'stock_scummvm_run':False,'desktop_run':False,'audio_run':False,'remaining_gates':['full-universe production compilation and ownership integration','actual text pages, actor staging, date substitution and exact visible receipts','freeze-frame pixels and full credit typography/URL wrapping','native save-kernel and detached replay-session round trips','non-restored epoch lifecycle and controller/muted/reduced-motion flows','cleared final audio, single PCM owner, credit theme and final package notices','stock ScummVM full-game acceptance']}
 (HERE/'evidence/acceptance.json').write_text(json.dumps(r,indent=2)+'\n')
 print(f"Accepted {len(ids)} unique tests; script996 SHA-256 {sha}; {r['combined_bytes']} combined script/heap bytes")
if __name__=='__main__':main()
