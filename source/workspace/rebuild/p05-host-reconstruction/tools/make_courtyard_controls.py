from pathlib import Path
import json
H=Path(__file__).resolve().parents[1]
rects={64:[[183,83,233,113]],65:[[162,89,184,127]],66:[[233,90,253,114]],67:[[254,59,282,106]],68:[[251,106,282,125],[282,111,292,125]],70:[[192,68,226,84]]}
parts=[[164,61,282,129],[282,111,291,129]]
def subtract(a,b):
 x1,y1,x2,y2=a;u1,v1,u2,v2=b;l,t,r,bot=max(x1,u1),max(y1,v1),min(x2,u2),min(y2,v2)
 if l>=r or t>=bot:return [a]
 out=[[x1,y1,x2,t],[x1,bot,x2,y2],[x1,t,l,bot],[r,t,x2,bot]]
 return [z for z in out if z[0]<z[2] and z[1]<z[3]]
for rs in rects.values():
 for r in rs:parts=[p for a in parts for p in subtract(a,r)]
s=['; Additive host-only P05 courtyard controls. Native art pixels unchanged.','(method (hCourtControls)', ' (if (or (not hHost) (hHost onApron?) (!= (hHost location?) 4)) (return 0))', ' (hHost uiAddControl: 1 18 44 22 102 64 "LIVING ROOM")',' (hHost uiAddControl: 1 19 44 282 111 315 "SIDE GATE")',' (hHost uiAddControl: 1 9 119 306 144 320 "AUDIENCE EDGE")',' (if (self hCourtVisible:)','  (self hControl: 71 137 103 162 127)']
for obj,rs in rects.items():
 for r in rs:s.append(f'  (self hControl: {obj} '+ ' '.join(map(str,r))+')')
for r in parts:s.append('  (self hControl: 63 '+' '.join(map(str,r))+')')
s+=[' )',' (hHost uiAddControl: 1 32 2 160 12 211 "NOTES")',' (return 1))']
(H/'courtyard_controls.sc.in').write_text('\n'.join(s)+'\n')
(H/'evidence/courtyard-control-overlay.json').write_text(json.dumps({'scope':'Host-only additive hit/approach metadata, no art pixels or P08 layout state changed','source_transform':[41,0],'small_targets':rects,'kit63_carved':parts,'new_hardware_approach':[114,140,127],'slate71_original_approach':[111,139,127],'source_and_wiring_editable':[64,65,66],'speaker_push_aim_stays_domain_garage_only':True,'native_acceptance':False},indent=2)+'\n')
print('kit fragments',len(parts))
