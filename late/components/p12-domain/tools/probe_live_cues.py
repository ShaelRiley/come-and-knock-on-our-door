"""Independent P10 live-configuration to P12 handoff checks."""
from probe_gameplay import *
results=[]
for ids in (TILE_IDS,PAPER_IDS,(TILE_IDS[2],PAPER_IDS[0],TILE_IDS[0])):
    _,_,p10,_,_,_,_,c,_=owners(ids,'ordinary');original=p10.restored_at;pocket=set(c.inventory)
    def ctx():return P10Context(COURTYARD,flags=c.flags,inventory=frozenset(pocket))
    for perm in itertools.permutations(ids):
        for slot,cue in enumerate(tuple(p10.slots)):
            p10.remove(ctx(),slot)
            if cue in TILE_IDS:pocket.add(cue)
        eq(p10.restored_at,original,'Restored history preserved during removal')
        empty=P12World();before=empty.save()
        rejects(lambda:empty.start(replace(c,inventory=frozenset(pocket)),p10.cue_handoff),'Currently incomplete handoff')
        eq(empty.save(),before,'Incomplete handoff atomic')
        for slot,cue in enumerate(perm):p10.place(ctx(),cue,slot);pocket.discard(cue)
        eq(p10.restored_at,original,'Restored history survives reordering')
        h=p10.cue_handoff;eq(h['slots'],perm,'Actual live permutation')
        actual=replace(c,inventory=frozenset(pocket));pair=Pair();pair.start(actual,h)
        eq(pair.w.visible_order,(h['words'][1],h['words'][0],h['words'][2]),'Initial physical swap reflects live labels')
        pair.restore(actual)
        a=replace(actual,on_apron=True);pair.show(a,'self_view');pair.call(a,'release_catch','p12ReleaseCatch');pair.call(actual,'rotate_rack','p12Rotate')
        right=tuple(sorted(ids,key=lambda cue:ORDER.index(p10.labels[cue])))
        pair.call(actual,'order_cards','p12Order',right,native=tuple(M['objects'][cue] for cue in right))
        eq(pair.w.visible_order,ORDER,'Every live permutation remains solvable')
        eq(pair.w.reserved_external_objects,frozenset(('cue_rack',*ids)),'No lost or extra physical cards')
        results.append({'ids':list(ids),'permutation':list(perm),'handoff_words':list(h['words']),'first_restored_serial':original,'result':'PASS'})
out={'status':'PASS','optimized':sys.flags.optimize,'live_permutations':len(results),'comparisons':N['actions'],'restores':N['restores'],'results':results,'paired':MEASUREMENTS}
(R/'evidence'/('joined-live-cues.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
