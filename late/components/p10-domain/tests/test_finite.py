"""New bounded P10 SCI gates: reachable histories and genuine external ownership.

The exhaustive arbitrary/corrupt-save corpus in historical/literal is not run.
Every caller below maintains the original external ceramic identities itself.
"""
from test_domain import (Harness,ByteVM,source_vm,P10World,C,RACK,KNOWN,LIVING,COURTYARD,replace,
    TILE_IDS,PAPER_IDS,CUE_IDS,ORDER,M,encode_world,encode_save,decode_words,CO,HERE,unittest,json,itertools,sys,copy)
from harness import snapshot
MEASUREMENTS=[]

class PairedVM:
    def __init__(self):
        self.source=source_vm.VM();self.emitted=ByteVM();self.p=self.source.p
        self.calls=0
    def call(self,name,*args):
        self.emitted.p.update(self.p)
        left=self.source.call(name,*args);right=self.emitted.call(name,*args)
        self.calls+=1
        if left!=right or self.p!=self.emitted.p:
            raise AssertionError(('source/emitted state',name,args,left,right))
        actual=self.emitted.machine.domain.arrays
        for k,v in self.source.arrays.items():
            if v!=list(actual[k]):raise AssertionError(('source/emitted array',name,k))
        return left
    def persistent(self):return self.source.persistent()

class FiniteTests(unittest.TestCase):
    def test_all_48_material_install_routes_owned_once(self):
        routes=0;instructions=0;calls=0
        for bits,order in itertools.product(itertools.product((0,1),repeat=3),itertools.permutations(range(3))):
            h=Harness(PairedVM);pocket=set(C.inventory)|{'laundry_clips'}
            def ctx(room=LIVING):
                return replace(C,room=room,bunny_room=room,frankie_room=room,inventory=frozenset(pocket))
            h.action('introduce','p10Introduce',c=ctx());h.show('plan',ctx())
            h.action('prepare_paper','p10PreparePaper',c=ctx())
            ids=tuple((PAPER_IDS if bit else TILE_IDS)[i] for i,bit in enumerate(bits))
            for i,obj in enumerate(ids):h.action('write','p10Write',obj,ORDER[i],c=ctx())
            for i in order:
                result=h.action('place','p10Place',ids[i],i,c=ctx(COURTYARD))
                self.assertEqual(result.code,'cue_placed')
                if ids[i] in TILE_IDS:pocket.remove(ids[i])
                current=ctx(COURTYARD);h.project(current);h.w.validate_context(current)
                self.assertEqual(h.v.call('p10ValidateContext'),1)
                self.assertFalse(pocket & h.w.reserved_external_items)
                self.assertEqual(set(TILE_IDS),(pocket & set(TILE_IDS))|set(h.w.reserved_external_items))
                self.assertEqual(set(CUE_IDS), (pocket&set(TILE_IDS))|set(h.w.inventory)|set(h.w.slots)-{None})
                saved=json.loads(json.dumps(decode_words(list(h.v.persistent().values()))))
                self.assertEqual(encode_save(saved),h.v.persistent());h.restore()
            self.assertTrue(h.w.ready);first=h.w.restored_at;h.queries()
            # Rewriting an installed cue must remain live after permanent success.
            h.action('write','p10Write',ids[0],None,c=ctx(COURTYARD));h.restore()
            self.assertFalse(h.w.rack_correct);self.assertEqual(h.w.restored_at,first);h.queries()
            h.action('write','p10Write',ids[0],'SERVE',c=ctx(COURTYARD))
            for i in order:
                h.action('remove','p10Remove',i,c=ctx(COURTYARD))
                if ids[i] in TILE_IDS:pocket.add(ids[i])
                h.project(ctx(COURTYARD));self.assertEqual(h.v.call('p10ValidateContext'),1)
            h.restore();h.queries();self.assertTrue(h.w.ready);self.assertFalse(h.w.rack_correct)
            self.assertEqual(h.w.restored_at,first)
            self.assertTrue({'master_invitation','grease_pencil','laundry_clips',*TILE_IDS}<=pocket)
            self.assertEqual(set(h.w.inventory),set(PAPER_IDS))
            self.assertEqual(h.v.call('p10ReservedAt',0),0)
            routes+=1;calls+=h.v.calls;instructions+=h.v.emitted.machine.steps
        MEASUREMENTS.append(dict(gate='48_material_install_routes',routes=routes,paired_calls=calls,emitted_instructions=instructions,save_restore_per_placement=True,ownership='External original units retired on placement, returned on removal'))

    def test_paper_only_completion_without_ceramic_or_laundry(self):
        h=Harness(PairedVM);paper=replace(C,inventory=frozenset({'master_invitation','grease_pencil'}))
        rack=replace(paper,room=COURTYARD,bunny_room=COURTYARD,frankie_room=COURTYARD)
        h.action('introduce','p10Introduce',c=paper);h.show('plan',paper)
        h.action('prepare_paper','p10PreparePaper',c=paper)
        for i,obj in enumerate(PAPER_IDS):
            h.action('write','p10Write',obj,ORDER[i],c=paper)
            h.action('place','p10Place',obj,i,c=rack);h.restore()
        self.assertTrue(h.w.ready);self.assertEqual(h.w.reserved_external_items,frozenset())
        self.assertEqual(h.v.call('p10ReservedAt',0),0);h.queries()
        h.begin('credit',replace(rack,rita_room=COURTYARD))
        self.assertEqual(CO[h.v.p['p10Code']],'tile_substitution_required')

    def test_original_p03_grant_requires_explicit_unit_projection(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('p10_accepted_p03',HERE/'reference/dependencies/p03_numeric_model.py')
        p03=importlib.util.module_from_spec(spec);sys.modules[spec.name]=p03;spec.loader.exec_module(p03)
        p3=p03.P03();p3.context(6,0,1,1);p3.look(37);p3.begin_credit();p3.select(1)
        p3.context(2,0,1,1);p3.collect(38);p3.context(6,0,1,1);p3.pad(38);p3.give_slate()
        self.assertTrue(p3.validate());self.assertEqual(p3.inventory(),[35])
        self.assertEqual([p3.location(i) for i in (48,49,50)],[10,10,10]);before=copy.deepcopy(p3.state)
        h=Harness(PairedVM);group=replace(C,inventory=frozenset({'ceramic_sample_tiles','grease_pencil'}))
        h.action('pick_up_tiles','p10PickUpTiles',c=group)
        self.assertEqual(CO[h.v.p['p10Code']],'p03_tiles_required')
        self.assertEqual(h.w.inventory,())
        projected=replace(group,inventory=(group.inventory-{'ceramic_sample_tiles'})|set(TILE_IDS))
        h.action('pick_up_tiles','p10PickUpTiles',c=projected)
        self.assertEqual(CO[h.v.p['p10Code']],'existing_tiles');self.assertEqual(h.w.inventory,())
        self.assertEqual(p3.state,before)

    def test_legitimate_saved_history_roundtrips(self):
        from test_transport import snapshots
        states=snapshots();v=PairedVM()
        for state in states:
            self.assertEqual(encode_save(decode_words(list(state.values()))),state)
            P10World.load(decode_words(list(state.values())))
            v.p.update(state);self.assertEqual(v.call('p10AfterRestore'),1)
            self.assertEqual(v.persistent(),state)
            self.assertEqual(v.p['p10ContextValid'],0)
            self.assertEqual(v.source.arrays['p10Lease'],[0]*8)
            self.assertEqual(v.source.arrays['p10Held'],[0]*415)
        MEASUREMENTS.append(dict(gate='legitimate_save_history',states=len(states),paired_calls=v.calls,emitted_instructions=v.emitted.machine.steps))

    def test_high_limb_boolean_and_last_atomic_operations(self):
        count=0;instructions=0
        for revision in (32766,32767,32768,65535,65536,M['max_serial']-2,M['max_serial']-1,M['max_serial']):
            h=Harness(PairedVM,P10World(revision=revision));h.project(C)
            self.assertEqual(h.v.call('p10Present',0),1)
            self.assertEqual(h.v.call('p10Present',1),0)
            self.assertEqual(h.v.call('p10Earlier',1,0),1)
            before=h.v.persistent()
            if revision<=M['max_serial']-2:
                h.action('introduce','p10Introduce');self.assertEqual(h.w.revision,revision+2)
            else:
                h.v.call('p10Introduce');self.assertEqual(CO[h.v.p['p10Code']],'serial_exhausted')
                self.assertEqual(h.v.persistent(),before);self.assertEqual(h.v.p['p10EventCount'],0)
                # One last single commit remains possible at MAX-1.
                if revision==M['max_serial']-1:h.action('hint','p10Hint',1)
            h.restore();h.project(C);self.assertEqual(h.v.call('p10Validate'),1)
            count+=1;instructions+=h.v.emitted.machine.steps
        MEASUREMENTS.append(dict(gate='serial_limb_boundaries',cases=count,emitted_instructions=instructions))

    def test_receipt_ack_at_rollover_and_maximum(self):
        for revision in (32765,32766,M['max_serial']-3):
            h=Harness(PairedVM,P10World(revision=revision));h.action('introduce','p10Introduce')
            h.ack('intro',units=('P10.OPEN.001.01',));h.restore();h.project(C)
            if h.w.revision<M['max_serial']:
                h.ack('intro',record='P10.OPEN.001');h.queries()
            else:
                before=h.v.persistent();h.v.call('p10Resume',1)
                hi,lo=divmod(h.w.presentations['intro'].serial,32768)
                h.v.call('p10Acknowledge',1,hi,lo,h.epoch,M['line_ids']['P10.OPEN.001'],0,0)
                self.assertEqual(CO[h.v.p['p10Code']],'serial_exhausted');self.assertEqual(h.v.persistent(),before)
                # Repeated already visible unit is still idempotent at MAX.
                h.ack('intro',units=('P10.OPEN.001.01',));h.queries()

    def test_finite_callback_epoch_boundary(self):
        h=Harness(PairedVM);h.epoch=32765;h.action('introduce','p10Introduce')
        h.project(replace(C,rita_room=COURTYARD));self.assertEqual(h.v.p['p10Epoch'],32767)
        before=h.v.persistent()
        self.assertEqual(h.v.call('p10Context',1,0,1,0,1,1,6,0,0,32767),0)
        self.assertEqual(h.v.persistent(),before);self.assertEqual(h.v.p['p10ContextValid'],0)
        self.assertEqual(h.v.source.arrays['p10Lease'],[0]*8)
        with self.assertRaises(ValueError):h.v.call('p10Context',1,0,1,0,1,1,6,0,0,32768)
        h.restore();self.assertEqual(h.v.p['p10Epoch'],0)
        # The restored host must discard all prior callback objects and establish
        # a fresh context; native host event ownership is not implemented here.
        h.epoch=0;h.context=None;h.resume('intro');h.ack('intro',record='P10.OPEN.001')

    def test_current_mapping_and_literal_preservation(self):
        self.assertEqual([M['objects'][x] for x in TILE_IDS],[48,49,50])
        self.assertEqual(M['objects']['ceramic_sample_tiles'],35)
        self.assertEqual(M['own_objects'],dict(cue_rack=410,rack_spring_clips=411,**dict(zip(PAPER_IDS,[412,413,414]))))
        self.assertEqual(M['objects']['laundry_clips'],76)
        self.assertNotEqual(M['objects']['rack_spring_clips'],M['objects']['laundry_clips'])
        self.assertEqual((HERE/'historical/literal/src/methods.sc.in.txt').read_bytes(),(HERE/'src/methods.sc.in').read_bytes())
        self.assertEqual(len(M['persisted_properties']),61)
        self.assertEqual(len(M['line_ids']),23);self.assertEqual(len(M['speech_unit_ids']),20)
        # P09 is absent from the required input flags: evening is the gate.
        self.assertNotIn('RUMOR_CLEARED',C.flags)

if __name__=='__main__':unittest.main()
