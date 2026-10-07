p='tests/fixtures/p08/canonical-bindings.json';f=json.load(open(p))
f['proposed_native_object_ids']={str(k):v for k,v in enumerate(['gate_lane','buffet_position','speaker_position','display_alcove','serving_table','kitchen_hatch','plan_overlay','placement_symbols'],116)}
f['reused_native_object_ids']={'circulation_plan':53,'sightline_plan':84,'ceramic_carrier':34,'ceramic_service':36,'credit_slate':40,'pa_kit':73,'completed_screen':83,'clean_towel':39,'clean_napkin':38,'hotpot_pot':103,'frankie':8,'bunny':2}
f['source_aliases']={'sightline_plan':'courtyard_plan'}
f['reserved_native_object_ids']=list(range(124,130))
open(p,'w').write(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
