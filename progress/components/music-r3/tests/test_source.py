from support import *
import generate,hashlib,re
class SourceProof(unittest.TestCase):
 def test_01_exact_inputs_and_original_pairs(self):
  pins=json.loads((H/'INPUT-PINS.json').read_text())
  for rel,value in pins.items():self.assertEqual(hashlib.sha256((H/rel).read_bytes()).hexdigest(),value,rel)
  idx=json.loads((H/'inputs/music/analysis/score-index.json').read_text());self.assertEqual(len(idx['files']),38)
  for row in idx['files']:
   for key,kind in [('native_payload_path','native'),('midi_path','midi')]:self.assertEqual(hashlib.sha256((H/'inputs/music'/row[key]).read_bytes()).hexdigest(),row['sha256'][kind])
 def test_02_all_gate_and_restore_tables_derived_from_new_notes(self):
  for n in(151,152):
   m,t,notes=generate.derive(n);ref=json.loads((H/f'generated/{n}-tables.json').read_text());self.assertEqual(t,ref['tables']);self.assertEqual(len(m['edits']),16 if n==151 else 19)
   for off in range(0,len(t['keyWindows']),5):
    first,last,end,offset,count=t['keyWindows'][off:off+5]
    expected=sorted((c,p,v,release)for c,_,on,release,p,v in notes if on<=first<release)
    actual=sorted(tuple(t['heldNotes'][i:i+4])for i in range(offset,offset+count*4,4));self.assertEqual(actual,expected)
    self.assertGreaterEqual(end-last,7)
   original=json.loads((H/'inputs/accepted-v4/generated/tables.json').read_text())['rows']
   if n==152:self.assertNotEqual(t['keyWindows'],next(r['values']for r in original if r['name']=='keyWindows'))
 def test_03_all_phase_and_poll_offsets(self):
  report=[]
  for n in(151,152):
   m,t,notes=generate.derive(n);start,end=m['loop']['start_tick'],m['loop']['end_tick'];span=end-start;g=m['gates'];count=0;max_wait=0
   for phase in range(start,end):
    for offset in(0,1):
     candidates=[]
     for gate in g:
      for cycle in(0,1,2):
       a=gate['dispatch_first']+cycle*span;z=gate['dispatch_last']+cycle*span
       poll=phase+offset+max(0,(a-phase-offset+1)//2)*2
       if a<=poll<=z:candidates.append(poll-phase)
     self.assertTrue(candidates);delay=min(candidates);max_wait=max(max_wait,delay);count+=1
   bound=261 if n==151 else 257;self.assertLessEqual(max_wait,bound)
   report.append(dict(resource=n,cases=count,maximum_wait_ticks=max_wait,bound_ticks=bound,scope='source-derived scheduling only; native/guard execution costs unmeasured'))
  (H/'evidence/phase-sweep.json').write_text(json.dumps(report,indent=2)+'\n')
 def test_04_all_source_event_and_role_constraints(self):
  for n,old in((151,102),(152,140)):
   from music_generate import decode_sound
   oldev=decode_sound((H/f'inputs/music/native/{old}.sound.bin').read_bytes());new=generate.stream(n)
   strip=lambda d:{ch:[(t,m)for t,m in rows if not(m[0]&240==128 or(m[0]&240==144 and not m[2]))]for ch,rows in d.items()}
   self.assertEqual({k:v for k,v in strip(oldev).items()if k!=15},{k:v for k,v in strip(new).items()if k!=15});self.assertNotIn(7,new)
   self.assertLessEqual(set(oldev[15]),set(new[15]));self.assertEqual(set(new[15])-set(oldev[15]),{(g['dispatch_first'],bytes([207,g['cue']]))for g in generate.manifest(n)['gates']})
  self.assertEqual(json.loads((H/'generated/152-tables.json').read_text())['tables']['stateGains'],[r['volume']for n in range(140,146)for r in generate.manifest(n)['roles']])
 def test_05_no_gameplay_or_pcm_calls(self):
  s=(H/'src/broker-procedures.inc').read_text();self.assertNotRegex(s,r'\b(?:DoAudio|DoSync|Wait|Sleep)\b')
  self.assertLessEqual(set(re.findall(r'\(domain (\w+)',s)),{'vcRead','vcBusy','vcLoading','vcUncertain','vcReady'})
  for n in(941,942,943):self.assertNotRegex((H/f'generated/module{n}.sc').read_text(),r'\b(?:DoAudio|DoSync)\b')
 def test_06_protected_v3_and_runtime(self):
  for row in json.loads((H/'inputs/music/analysis/accepted-v3-lock.json').read_text())['files']:
   self.assertEqual(hashlib.sha256((H/'inputs/accepted-v3'/row['path']).read_bytes()).hexdigest(),row['sha256'])
  runtime=(H/'inputs/runtime-provenance.json').read_text();self.assertIn('2026.3.0',runtime);self.assertIn('2.4.4+dfsg-1+deb13u3',runtime)
 def test_07_typed_abi_and_unchanged_940_981(self):
  allocation=json.loads((H/'evidence/allocation-scan.json').read_text());self.assertEqual(allocation['status'],'PASS_FRESH_TYPED_MAP_AND_REGISTRY_SCAN');self.assertEqual(allocation['scripts'],[941,942,943]);self.assertEqual(allocation['text'],[245,246,247])
  layouts=json.loads((H/'evidence/layouts.json').read_text());original=json.loads((H/'inputs/original981/layout.json').read_text())
  for k in('script_sha256','heap_sha256'):self.assertEqual(layouts['981'][k],original[k])
  for n in(941,942):
   self.assertEqual(len(layouts[str(n)]['objects']),1);o=layouts[str(n)]['objects'][0];self.assertFalse(o['is_class']);self.assertEqual(o['superclass'],3);self.assertEqual(len(o['methods']),43)
  self.assertFalse(layouts['943']['objects'])
  old940=next(r for r in json.loads((H/'inputs/accepted-v4/compile.json').read_text())['modules']if r['module']==940)
  for k in('script_sha256','heap_sha256'):self.assertEqual(layouts['940'][k],old940[k])
  self.assertEqual((H/'build/fresh/src/module940.sc').read_bytes(),(H/'inputs/accepted-v4/generated/module940.sc').read_bytes())

 def test_08_audit_exact_all_emitted_entry_points(self):
  layouts=json.loads((H/'evidence/layouts.json').read_text());apis=json.loads((H/'generated/api.json').read_text());apis['940']=json.loads((H/'inputs/accepted-v4/generated/api.json').read_text())['exports']
  expected=set()
  for n in(940,941,942,943,981,986):
   layout=layouts[str(n)]
   expected.update((n,m['selector'])for o in layout['objects']for m in o['methods'])
   expected.update((n,name)for name in apis.get(str(n),{}))
  report=json.loads((H/'evidence/stack-audit.json').read_text());self.assertEqual(report['status'],'PASS');self.assertEqual({(r['module'],r['entry'])for r in report['entries']},expected)
