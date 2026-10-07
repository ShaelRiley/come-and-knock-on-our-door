"""Editable geometry authority. Rectangles are half-open; DrawCel uses top-left."""
STAGE=(320,144)
ANCHOR=(26,78)
POSITIONS=['UNPLACED','HATCH','WALL','ALCOVE','LANE']
OBJECTS=['ceramic_carrier','pa_kit','completed_screen','serving_table','credit_slate']
# IDs from current host, not obsolete P08 pa73 proposal. Never add pocket token.
OBJECT_IDS={'ceramic_carrier':34,'pa_kit':63,'completed_screen':83,'serving_table':120,'credit_slate':40}
# Source view228 cels. P05 staging uses exact view227 instead.
CELS={'completed_screen':0,'serving_table':1,'pa_kit':2,'ceramic_carrier':4,'credit_slate':5}
ORIGINS={
 'ceramic_carrier':[(95,47),(84,79),(156,83),(230,91),(170,108)],
 'pa_kit':[(119,61),(81,78),(139,68),(211,77),(158,92)],
 'completed_screen':[(61,70),(84,51),(151,57),(226,54),(187,79)],
 'serving_table':[(4,92),(80,98),(145,95),(216,96),(160,111)],
 'credit_slate':[(135,52),(125,88),(187,88),(257,88),(222,124)]}
ZONE_RECTS={'HATCH':[77,73,147,124],'WALL':[148,64,224,124],'ALCOVE':[224,69,280,124],'LANE':[23,132,300,143]}
APPROACHES={'HATCH':[67,140,127],'WALL':[151,140,127],'ALCOVE':[272,140,127],'LANE':[148,140,127]}
MARKS=[(7,(80,110)),(8,(149,110)),(9,(221,110)),(10,(23,132))]
EXITS={'house_arch':{'object':18,'rect':[22,44,64,102],'approach':[44,124,127]},'side_gate':{'object':19,'rect':[282,44,315,111],'approach':[279,132,127]},'audience_edge':{'object':9,'rect':[306,119,320,144],'approach':[291,140,127]}}
HATCH={'object':121,'rect':[95,44,134,71],'approach':[75,135,127],'travel':False}
P05={'kit':{'object':63,'rect':[164,61,291,129],'approach':[114,140,127]},'slate':{'object':71,'rect':[137,103,162,127],'approach':[111,139,127]},'slate_origin':[137,103],'hardware_origins':{0:[139,92],1:[209,61],2:[209,61],3:[209,61],4:[119,91],5:[128,110],6:[129,92],9:[150,71],10:[140,84],11:[140,84],12:[189,92],13:[180,92]},'render_cel_order':['cable','console','tape','selector','socket','microphone','speaker','slate'],'visibility':'room4 and not onApron and committed P05 loan and PA owner1, before P08 ownership acknowledgment','document':462}

def actor_rect(feet,scale):
 x,y=feet;return [x-26*scale//128,y-78*scale//128,x-26*scale//128+52,y-78*scale//128+80]
def staging_components(connected,source,aim):
 return [6 if connected else 5,0,9,11 if source else 10,13 if connected else 12,4,1+aim]
def hit_p05(x,y,visible=True):
 for name,spec in [*EXITS.items(),('hatch',HATCH),('equipment_credit_slate',P05['slate']),('pa_kit',P05['kit'])]:
  if name in ['equipment_credit_slate','pa_kit'] and not visible:continue
  a,b,c,d=spec['rect']
  if a<=x<c and b<=y<d:return name
 return None

P05['hardware_origins']={c:[xy[0]+45,xy[1]] for c,xy in P05['hardware_origins'].items()}


def p08_object_choices(positions):
    if len(positions)!=5 or any(type(p) is not int or not 0<=p<=4 for p in positions):raise ValueError('Invalid position tuple')
    return [OBJECT_IDS[obj] for obj in OBJECTS]

def p08_hit_candidates(x,y,positions,sizes):
    # Every overlapping candidate is returned. Future host must open a canonical-
    # label chooser; picking only the topmost sprite is not an accepted adapter.
    p08_object_choices(positions);out=[]
    for obj,pos in zip(OBJECTS,positions):
        if obj=='pa_kit' and pos==0:a,b,c,d=P05['kit']['rect']
        else:
            a,b=ORIGINS[obj][pos];w,h=sizes[obj];c,d=a+w,b+h
        if a<=x<c and b<=y<d:out.append(OBJECT_IDS[obj])
    return out


def gate_open_from_state(gate):
    if type(gate) is not int or gate not in (0,1,2):raise ValueError('Invalid P04 gate state')
    return gate==1


def pa_layout_cel(connected,source,facing):
    if type(connected) is not int or connected not in (0,1) or type(source) is not int or source not in (0,1) or type(facing) is not int or facing not in (1,2):raise ValueError('Invalid preserved PA projection')
    if connected==source==1:return 2+(facing-1)
    return {(0,0):12,(0,1):14,(1,0):16}[connected,source]+facing-1
