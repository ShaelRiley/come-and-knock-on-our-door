"""New original Audience component through actual integrated source/emitted routes.
Kernel clock/Sync/graphics are modeled; no native or listening acceptance.
"""
from pathlib import Path
import json,struct,sys,types,unittest,hashlib,importlib.util,copy
H=Path(__file__).resolve().parents[1];sys.path[:0]=[str(H),str(H/'tests'),str(H/'tools')];sys.dont_write_bytecode=True
import host,extend_dialogue as ext
from source_factory import VM as SourceVM
from source_tools import methods
from resource_codec import decode
from test_bindings import domain
spec=importlib.util.spec_from_file_location('audience_integration_renderer',H/'inputs/audience-component/audience.py');audience=importlib.util.module_from_spec(spec);spec.loader.exec_module(audience)
M=json.loads((H/'generated/manifest.json').read_text());OLD=json.loads((H/'inputs/gap-v0/generated/manifest.json').read_text());AM=json.loads((H/'inputs/audience-component/generated/manifest.json').read_text());EVIDENCE={}
ROUTES=[r for r in M['routes']+M['unit_routes']+M['variant_routes']+M['variant_unit_routes'] if r['page_count'] and M['pages'][r['first_page']]['speaker_id']=='audience']
class Stream:
 def __init__(self):self.events=[];self.i=0
 def step(self,args):
  if args[0]==0:
   name=audience.patch_name(*args[2:]);raw=(H/'generated/speech'/('#'+name[1:])).read_bytes();assert raw[:2]==b'\x8e\x00' and raw[-2:]==b'\xff\xff';self.events=list(struct.iter_unpack('<hh',raw[2:-2]));self.i=0;assert all(c==0 for _,c in self.events)
  elif args[0]==1:
   t,c=self.events[self.i] if self.i<len(self.events) else (-1,-1);self.i+=1;args[1].p.update(syncTime=t,syncCue=c)
  elif args[0]==2:self.events=[];self.i=0
  else:raise AssertionError('Unexpected Sync operation')
  return 0
class GroupVM(host.VM):
 def __init__(self):self.stream=Stream();super().__init__()
 def _kernel(self,k,args):
  if self.knames.get(k)=='DoSync':self.ktrace.append(('DoSync',tuple(args)));return self.stream.step(args)
  return super()._kernel(k,args)
class Adapter:
 def __init__(self,kind):
  self.kind=kind
  if kind=='source':
   self.d=SourceVM(H/'generated/module982.sc','SceneDialogue');self.a=SourceVM(H/'inputs/src/module980.sc','PresentationAudio',self.d.resources);self.vm=None;stream=Stream();original=self.a.ev
   def ev(audio,n,e):
    if isinstance(n,list) and n and n[0]=='DoSync':
     args=[audio.ev(v,e) for v in n[1:]];audio.kernel.append(('DoSync',args));return stream.step(args)
    return original(n,e)
   self.a.ev=types.MethodType(ev,self.a)
  else:self.vm=GroupVM();self.d=self.vm.objects['sceneDialogue'];self.a=self.vm.objects['presentationAudio']
 def position(self,tick):
  if self.vm:self.vm.audio_position=tick
  else:self.a.audio_position=tick
 def starts(self):return [list(v) for n,v in (self.vm.ktrace if self.vm else self.a.kernel) if n=='DoAudio' and v[0]==2]
 def accept(self,route):
  d,a=self.d,self.a;p=M['pages'][route['first_page']];assert d.call('sdOpen',route['document_id'],0,0,0,a)==1
  gen=d.p['sdGeneration'];assert d.p['sdVoice']==p['voice_index'] and d.p['sdVoiceEnd']==p['duration_ticks'] and d.p['sdSpeaker']==0
  assert d.call('sdSpeak',a,gen,0)==0 and d.call('sdPresented',gen,0,a.p['token'])==0
  assert d.call('sdDraw',0)==1 and str(d.arrays['sdTextBuffer'])==p['text']
  assert d.call('sdPresented',gen-1,0,a.p['token'])==0 and d.call('sdPresented',gen,1,a.p['token'])==0
  assert d.call('sdPresented',gen,0,a.p['token'])==1 and d.call('sdPresented',gen,0,a.p['token'])==0
  assert d.call('sdSpeak',a,gen,1)==0
  token=d.call('sdSpeak',a,gen,0);assert token==a.p['token'] and token>0 and a.p['lane']==1 and a.p['speaker']==a.p['mouth']==0
  assert d.call('sdSpeak',a,gen,0)==0
  return token,gen,p
class AudienceIntegrationTests(unittest.TestCase):
 def test_all14_real_routes_source_emitted_mute_duration_and_retirement(self):
  self.assertEqual(len(ROUTES),14);totals={}
  for kind in ('source','emitted'):
   v=Adapter(kind);a,d=v.a,v.d;cases=0
   for r in ROUTES:
    for muted in (0,1):
     a.p.update(voiceMuted=muted,voiceVolume=80,masterVolume=100,audienceMuted=1)
     token,gen,p=v.accept(r);self.assertEqual(v.starts()[-1],[2,911 if muted else 924,1 if muted else p['voice_index'],1,0,1])
     for tick in (0,1,p['duration_ticks']//2,p['duration_ticks']-1):v.position(tick);self.assertEqual(a.call('poll',tick,token),1);self.assertEqual((a.p['speaker'],a.p['mouth']),(0,0))
     v.position(p['duration_ticks'] if muted else -1);self.assertEqual(a.call('poll',p['duration_ticks'],token),0);self.assertEqual(a.p['mouth'],0);cases+=1
    a.p.update(voiceMuted=0,voiceVolume=80,masterVolume=100);token,gen,p=v.accept(r);v.position(19);a.call('setOff',1,1);self.assertEqual((a.p['silentClock'],a.p['voiceOffset']),(1,19));self.assertEqual(v.starts()[-1],[2,911,1,1,0,1]);a.call('setOff',1,0);self.assertEqual((a.p['silentClock'],a.p['lastGain']),(1,0))
    v.position(p['duration_ticks']-19);self.assertEqual(a.call('poll',p['duration_ticks'],token),0);cases+=1
    for voice,master in ((0,100),(80,0)):
     a.p.update(voiceMuted=0,voiceVolume=voice,masterVolume=master);token,gen,p=v.accept(r);self.assertEqual(v.starts()[-1],[2,911,1,1,0,1]);cases+=1
    a.p.update(voiceMuted=0,voiceVolume=80,masterVolume=100)
    for reason in (10,11,12,13,14):
     token,gen,p=v.accept(r);d.call('sdInterrupt',a,reason);self.assertNotEqual(a.p['token'],token);self.assertEqual((a.p['lane'],a.p['mouth'],d.p['sdArmed']),(0,0,0));self.assertEqual(d.call('sdSpeak',a,gen,0),0);self.assertEqual(a.call('poll',p['duration_ticks'],token),0);cases+=1
    token,gen,p=v.accept(r);d.call('sdAfterRestore',a);self.assertEqual(d.call('sdPresented',gen,0,a.p['token']),0);self.assertEqual(d.call('sdSpeak',a,gen,0),0);cases+=1
   totals[kind]=cases
  self.assertEqual(totals,{'source':154,'emitted':154});EVIDENCE['actual_integrated_route_scenario_groups']=totals
 def test_only_audience_page_fields_and_pcm_resources_change_from_gap(self):
  self.assertEqual(M['speech'][:39],OLD['speech']);self.assertEqual(M['routes'],OLD['routes']);self.assertEqual(M['unit_routes'],OLD['unit_routes']);self.assertEqual(M['variant_routes'],OLD['variant_routes']);self.assertEqual(M['variant_unit_routes'],OLD['variant_unit_routes'])
  allowed={'voice_index','audio_module','duration_ticks','delivery','role','mouth_gate','fields','audio_gap'};count=0
  for before,after in zip(OLD['pages'],M['pages']):
   if before['speaker_id']=='audience':
    changed={k for k in set(before)|set(after) if before.get(k)!=after.get(k)};self.assertLessEqual(changed,allowed);self.assertEqual([x for i,x in enumerate(after['fields']) if i!=5],[x for i,x in enumerate(before['fields']) if i!=5]);count+=1
   else:self.assertEqual(before,after)
  self.assertEqual(count,14);self.assertEqual((H/'generated/213.text.bin').read_bytes(),(H/'inputs/gap-v0/generated/213.text.bin').read_bytes())
  previous=(H/'inputs/gap-v0/generated/module982.sc').read_text();current=(H/'generated/module982.sc').read_text();self.assertEqual(methods(previous),methods(current))
  for name in ext.ARRAYS:
   a,b=ext.read_array(previous,name),ext.read_array(current,name);self.assertEqual(len(a),len(b));changed=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
   self.assertEqual(len(changed),14 if name in ('sdPageData','sdAudioModules','sdPageDurations') else 0,name)
  old=decode((H/'inputs/gap-v0/generated/fixture-game/resource.map').read_bytes(),(H/'inputs/gap-v0/generated/fixture-game/resource.000').read_bytes());new=decode((H/'generated/fixture-game/resource.map').read_bytes(),(H/'generated/fixture-game/resource.000').read_bytes());self.assertEqual(set(old),set(new));changed={k for k in old if old[k]!=new[k]};self.assertEqual(changed,{(17,982),(3,241)})
  EVIDENCE['changed_typed_resources_from_gap']=[list(x) for x in sorted(changed)]
 def test_exact_component_api_hashes_and_distinct_bindings_not_inferred_from_pcm(self):
  self.assertEqual(hashlib.sha256((H/'inputs/audience-component/audience.py').read_bytes()).hexdigest(),AM['renderer_sha256']);self.assertEqual(hashlib.sha256((H/'inputs/audience-component/audience-profile.json').read_bytes()).hexdigest(),AM['profile_sha256']);self.assertEqual(M['speech'][39:],[dict(row,profile_sha256=AM['profile_sha256'],renderer_sha256=AM['renderer_sha256'],generation='new_original_group_component_pending_independent_review',audible_gate='future_host_proves_actual_current_audience_eligibility_and_pa_cue_context',mouth_gate='no_principal_or_group_mouth') for row in AM['speech']])
  self.assertEqual(len({v['audio_sha256'] for v in AM['speech']}),4)
  for row in AM['speech']:
   for kind in ('audio','sync'):self.assertEqual((H/'generated/speech'/row[kind+'_file']).read_bytes(),(H/'inputs/audience-component/generated/speech'/row[kind+'_file']).read_bytes())
   if row['binding']:self.assertEqual(audience.select_observed_fragments(row['binding']['word_ids'],AM),[row])
  for bad in (None,[],[1,1,3],[True,2,3],[1,2,4]):
   with self.assertRaises(ValueError):audience.select_observed_fragments(bad,AM)
 def test_audio_completion_cannot_acknowledge_pending_audience_unit(self):
  state,ctx=domain((2,1,3),'audience_view');before=copy.deepcopy(state.p);lease=state.p['p12PresentationHi'],state.p['p12PresentationLo'];self.assertEqual(state.call('p12Count',5),0)
  v=Adapter('emitted');route=next(r for r in ROUTES if r['document_kind']=='variant_unit' and r['variant_id']=='cue_213');token,gen,p=v.accept(route);v.position(-1);self.assertEqual(v.a.call('poll',p['duration_ticks'],token),0)
  self.assertEqual(state.p,before);state.call('p12AudioFinished');self.assertEqual(state.call('p12Count',5),0);self.assertEqual(lease,(state.call('p12SerialHi',12),state.call('p12SerialLo',12)))
if __name__=='__main__':unittest.main()
