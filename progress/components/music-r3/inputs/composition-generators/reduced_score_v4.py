#!/usr/bin/env python3
"""Same-clock quiet companions: change CC7 only, never notes/tempo/expression."""
import json,struct,copy
import score_v4_core as c
OUT=c.OUT;GAINS={0:99,1:83,2:0,3:71,4:73,5:44,6:0,9:59}
def main():
 for sub in('midi/reduced','native/reduced','analysis/reduced'):(OUT/sub).mkdir(exist_ok=True)
 rows=[]
 for f in sorted((OUT/'analysis').glob('*-manifest.json')):
  r=json.loads(f.read_text())
  if r['resource_id']>=140:continue
  data=(OUT/r['midi_path']).read_bytes();ppq,events=c.g.parse_smf(data);body=bytearray();prev=0
  for t,order,msg in events:
   if msg[0]<240 and msg[0]&240==176 and msg[1]==7:msg=bytes((msg[0],7,min(msg[2],GAINS[msg[0]&15])))
   if msg[0]==255:msg=msg[:2]+c.g.vlq(len(msg)-2)+msg[2:]
   body+=c.g.vlq(t-prev)+msg;prev=t
  smf=b'MThd'+struct.pack('>IHHH',6,0,1,ppq)+b'MTrk'+struct.pack('>I',len(body))+body
  stream=c.g.decode_sound((OUT/r['native_payload_path']).read_bytes())
  for ch,es in stream.items():
   if ch!=15:stream[ch]=[(t,bytes((msg[0],7,min(msg[2],GAINS[ch]))))if msg[0]&240==176 and msg[1]==7 else(t,msg)for t,msg in es]
  payload=c.g.sound_resource(stream,{role['channel']:role['voices']for role in r['roles']})
  mid=f"midi/reduced/{r['cue_id']}.mid";native=f"native/reduced/{r['resource_id']:03d}.sound.bin"
  (OUT/mid).write_bytes(smf);(OUT/native).write_bytes(payload);(OUT/'native/reduced'/f"sound.{r['resource_id']:03d}").write_bytes(b'\x84\0'+payload)
  row=dict(cue_id=r['cue_id'],resource_id=r['resource_id'],variant='REDUCED_CC7_ONLY',midi_path=mid,native_payload_path=native,sha256={'midi':c.sha(smf),'native':c.sha(payload)},same_notes_programs_expression_tempos_loop=True,gains={str(role['channel']):min(role['volume'],GAINS[role['channel']])for role in r['roles']},runtime='One existing parser with tested per-role state gains; these files are alternate audition/reference payloads, not concurrent players.',native_runtime_tested=False,human_listening_approved=False)
  (OUT/'analysis/reduced'/f"{r['cue_id']}-manifest.json").write_text(json.dumps(row,indent=2));rows.append(row)
 (OUT/'analysis/reduced-variants.json').write_text(json.dumps({'variants':rows,'count':len(rows)},indent=2));print('Quiet exact-clock companions:',len(rows))
if __name__=='__main__':main()
