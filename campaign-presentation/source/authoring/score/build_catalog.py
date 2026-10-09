#!/usr/bin/env python3
"""Exact-byte approved score catalog, explicit graph and A05 pitch-only connector."""
from pathlib import Path
import hashlib,importlib.util,json,re,shutil,sys
import derive_loop_transports as d
H=d.H;R=d.R;g=d.g
sys.path.insert(0,str(R/'tools'))
from music_generate import decode_sound,sound_resource,write_smf

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def replace_proc(s,name,body):
 m=re.search(r'(?m)^\(procedure \('+name+r'(?:\s|\))',s);assert m,name
 end=s.find('\n(procedure (',m.start()+1)
 if end<0:end=len(s)
 return s[:m.start()]+body.rstrip()+'\n'+s[end:]
def guard(prefix,text,rows):
 old=g.H;g.H=H
 try:return g.guards(prefix,text,rows)
 finally:g.H=old

def main():
 amendment=H/'metadata/connector220.json'
 a=json.loads(amendment.read_text());assert a['allocation']['sound']==220
 assert sha(H/'assets/153.sound.bin')==a['derivation']['source_sha256']
 src=decode_sound((H/'assets/153.sound.bin').read_bytes());dst={};changed=[]
 for ch,ev in src.items():
  dst[ch]=[]
  for tick,msg in ev:
   if ch not in(9,15) and msg[0]&240 in(128,144):
    assert 0<=msg[1]+2<=127
    changed.append([tick,ch,msg[1],msg[1]+2]);msg=bytes([msg[0],msg[1]+2,*msg[2:]])
   dst[ch].append((tick,msg))
 voices={r['channel']:r['voices']for r in g.manifest(153)['roles']}
 (H/'assets/220.sound.bin').write_bytes(sound_resource(dst,voices))
 assert decode_sound((H/'assets/220.sound.bin').read_bytes())==dst
 dump(H/'generated/CONNECTOR220-PROVENANCE.json',dict(source153_sha256=sha(H/'assets/153.sound.bin'),amendment_sha256=sha(amendment),native_sha256=sha(H/'assets/220.sound.bin'),changed_note_events=changed,all_other_bytes_equal=True,listening_accepted=False))
 # Frame60-derived SMF uses PPQ480 and500000us tempo:16 SMF ticks per native tick.
 midi=[(0,-1,b'\xff\x51\x03\x07\xa1\x20')]
 for ch,events in dst.items():
  if ch!=15:midi += [(t*16,i,msg)for i,(t,msg)in enumerate(events)]
 (H/'assets/220.mid').write_bytes(write_smf(midi,136*16))
 coverage=json.loads((H/'metadata/cue-sources.json').read_text())['cues']
 loops=json.loads((H/'generated/LOOP-TRANSPORTS.json').read_text())['transports'];lmap={r['cue']:r for r in loops};lmap[104]=lmap[101]
 # These are actual legal room/earned-state/event edges, not a wildcard bank.
 pairs=[]
 def edge(a,b,bridge,why,reverse=False):
  pairs.append([a,b,bridge,why])
  if reverse:pairs.append([b,a,148 if b not in(107,109,110)else 149,why+' return'])
 edge(101,102,122,'P02 committed reveal')
 edge(104,102,148,'porch/living route',True)
 edge(102,103,148,'living/kitchen route',True)
 edge(102,106,148,'living/courtyard route',True)
 edge(104,105,148,'porch/side-passage route',True)
 edge(105,106,148,'side-passage/courtyard route',True)
 edge(104,107,148,'porch/garage before sincere agreement',True)
 edge(104,108,148,'porch/garage after sincere agreement',True)
 edge(104,109,220,'A05 porch/conservatory before credit');edge(109,104,149,'A05 reverse conservatory/porch')
 edge(104,110,220,'A05 porch/conservatory after credit');edge(110,104,149,'A05 reverse conservatory/porch')
 edge(107,108,149,'committed sincere role agreement')
 edge(109,110,220,'A05 committed Rita credit')
 edge(102,120,148,'living HOME apron',True)
 edge(106,111,123,'explicit courtyard Ready starts E03')
 edge(111,112,148,'actual P09/P10 pressure introduction')
 edge(111,113,124,'actual E04 rescue ownership');edge(112,113,124,'actual E04 rescue ownership')
 edge(113,114,127,'P11 accepted help/coordination')
 edge(114,115,150,'P12 rack handoff after safe rescue')
 edge(113,115,127,'safe rescue completed before rack handoff')
 edge(115,129,150,'actual consequential introduction owns speech space')
 edge(129,128,0,'actual consequential words completed; confetti response')
 edge(129,116,0,'A08 actual consequential words complete before confetti commit')
 edge(116,128,150,'actual P12 confetti commit after honest-family entry')
 edge(115,128,150,'actual P12 confetti commit supersedes pending speech-space entry')
 edge(128,116,0,'committed response finishes into honest family')
 edge(115,116,150,'truth fully delivered without pending speech passage; confetti is a separate committed response')
 edge(116,117,125,'P12 collection completed then E06 starts')
 edge(117,118,150,'earned P13 toast and promises')
 edge(118,119,126,'GAME_COMPLETE committed P14')
 edge(119,121,0,'finale credits after painted freeze and celebration')
 # Four contest entrances and exact semantic scene returns.
 for source,cue in [(107,141),(108,141),(104,142),(114,143),(115,143),(117,144),(118,144)]:
  edge(source,cue,148 if source in(104,108,118)else 150,'committed contest ENTER')
  edge(cue,source,149,'committed contest EXIT; captured scene return')
 # Coincident movement then earned variants remain bounded legal retargets.
 edge(101,104,0,'authored exact byte alias');edge(104,101,0,'authored exact byte alias')
 edges=[];gatewords=[]
 def native(n):return 151 if n==102 else 152 if 140<=n<=145 else 101 if n==104 else n
 def gates(n):
  if n==102 or 140<=n<=145:
   m=g.manifest(native(n));return[dict(first=x['dispatch_first'],last=x['dispatch_last'],root=None,quality=None,beat=x['boundary_beat'],rationale=x['rationale'])for x in m['gates']],m['loop']
  if n not in lmap:return[],None
  m,t,notes=d.derive(lmap[n]['cue']);times=sorted({m['loop']['start_tick'],m['loop']['end_tick']}|{x for c,idx,on,off,p,v in notes for x in(on,off)})
  ret=[]
  for x,y in zip(times,times[1:]):
   if y-x<7 or any(on<=x<off for c,idx,on,off,p,v in notes):continue
   beat=(x-12)*m['bpm']/3600;h=[h for h in m['harmony']if h['beat']<=beat][-1]
   ret.append(dict(first=x+2,last=y-3,root=h['root_pc'],quality=h['quality'],beat=round(beat,6),rationale='Natural source note release; no note/event/tail modified'))
  return ret,m['loop']
 for i,(source,target,bridge,why)in enumerate(pairs,1):
  gs,loop=gates(source)
  if bridge==0:gs=[]
  if bridge and not gs:raise AssertionError(('no source gates',source,target))
  offset=len(gatewords)//3
  for v in gs:gatewords.extend([v['first'],v['last'],12])
  waits=[]
  if gs:
   waits=[gs[k+1]['first']-gs[k]['last']for k in range(len(gs)-1)]+[loop['end_tick']-gs[-1]['last']+gs[0]['first']-loop['start_tick']]
  edges.append(dict(id=i,source=source,target=target,connector=bridge,gate_offset=offset,gates=gs,priority=2 if source>=111 else 1,admitted=True,reason=why,worst_source_wait_ticks=max(waits,default=0)+2,source_native=native(source),target_native=native(target),release_or_reverb_silence_claim=False,cancel_policy='Latest pending destination replaces earlier target; source preserves its clock until both readings fit the same gate. Already-owned connector completes naturally; final target must pass destination and context admission.'))
 # Aliases and row changes are implicit identity within the exact resource. The
 # graph includes no generic edge granting arbitrary caller-provided cue access.
 cueRows=[];gainIndex=[];gainWords=[]
 for r in coverage:
  n=r['resource_id'];tr=941 if n==102 else 942 if 140<=n<=145 else lmap[n]['module']if n in lmap else 0
  mode=0 if r['loop']else 2 if 122<=n<=128 or n in(146,147)else 1
  guardid=246 if tr==941 else 247 if tr==942 else lmap[n]['guard']if tr else 249
  count=6 if 140<=n<=145 else 2 if tr else 1
  end=round(r['duration_seconds']*60);alias=101 if n==104 else 140 if 140<=n<=145 else n
  cueRows.append([n,native(n),tr,mode,guardid,end,r['loop']['start_tick']if r['loop']else 0,count,alias,int(n not in(146,147))])
  if 140<=n<=145:states=[x['volume']for k in range(140,146)for x in g.manifest(k)['roles']]
  elif n==102:states=g.derive(151)[1]['stateGains']
  elif n in lmap:states=d.derive(lmap[n]['cue'])[1]['stateGains']
  else:states=[x['volume']for x in g.manifest(n)['roles']]
  gainIndex.extend([len(gainWords),len(states)]);gainWords.extend(states)
 opening=[[100 if c==0 else 159+c,c*360,3600-c*360,0,0,1]for c in range(10)]
 edgeRows=[[e['source'],e['target'],e['id'],e['connector'],len(e['gates']),e['gate_offset'],e['priority'],1]for e in edges]
 rows=[('pmCues',[x for r in cueRows for x in r],False),('pmOpenings',[x for r in opening for x in r],False),('pmGainIndex',gainIndex,False),('pmGains',gainWords,False),('pmEdges',[x for r in edgeRows for x in r],False),('pmEdgeGates',gatewords,False)]
 pcmfile=H/'src/pcm-metadata.json';pcm=json.loads(pcmfile.read_text())
 rows += [(r['name'],r['values'],False)for r in pcm['rows']]
 query=(H/'src/metadata-procedures.inc').read_text()
 for name,body in pcm['procedures'].items():query=replace_proc(query,name,body)
 query=replace_proc(query,'pmEdge','''(procedure (pmEdge sourceCue targetCue field index &tmp i base at)
 (if (or (< field 0) (> field 7) (< index 0)) (return -1))
 (for ((= i 0)) (< i @EDGE_COUNT@) ((++ i))
  (= base (* i 8))
  (if (and (== [pmEdges base] sourceCue) (== [pmEdges (+ base 1)] targetCue))
   (if (and (>= field 3) (<= field 5))
    (if (>= index [pmEdges (+ base 4)]) (return -1))
    (= at (+ (* (+ [pmEdges (+ base 5)] index) 3) (- field 3)))
    (return [pmEdgeGates at]))
   (if index (return -1))
   (switch field (0 (return [pmEdges (+ base 2)])) (1 (return [pmEdges (+ base 3)]))
    (2 (return [pmEdges (+ base 4)])) (6 (return [pmEdges (+ base 6)])) (7 (return [pmEdges (+ base 7)])))))
 (return -1))''')
 query=query.replace('(2 (return 0))','(2 (return @EDGE_COUNT@))')
 for a,b in {'@CUE_COUNT@':len(cueRows),'@EDGE_COUNT@':len(edges),'@REACTION_COUNT@':pcm['reaction_count'],'@TAKE_COUNT@':pcm['take_count'],'@FOLEY_COUNT@':pcm['foley_count']}.items():query=query.replace(a,str(b))
 source=';;; Sierra Script 1.0 - (do not remove this comment)\n(script# 948)\n(public pmVerify 0 pmCue 1 pmEdge 2 pmReaction 3 pmTake 4 pmFoley 5 pmOpening 6 pmHeader 7)\n(local\n'+g.local(rows)+'\n [pmBuffer 64]\n)\n'+guard('pm',249,rows)+'\n'+query
 (H/'generated/module948.sc').write_text(source)
 dump(H/'generated/FULL-SCORE-CATALOG.json',dict(cues=cueRows,edges=edges,original_cues=coverage,admitted_optional=[False,False],source_timing_limit='Natural unmodified release apertures; no roughly-one-bar latency claim. Conditional release arrangements require phrase review before admission.',native_acceptance=False,listening_accepted=False))
 print('Catalog:',len(cueRows),'cues,',len(edges),'explicit edges;220 pitch-only derived')
if __name__=='__main__':main()
