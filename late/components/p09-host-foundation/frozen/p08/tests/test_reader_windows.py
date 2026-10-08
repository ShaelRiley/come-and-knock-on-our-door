"""Bounded source/emitted reader primitives. No display-derived gameplay receipts."""
import copy,json,hashlib
import host
from source_host import VM as SourceVM
from test_composition_initial import CompositionInitial

H=host.H
MAP=json.loads((H/'inputs/scene/line-document-unit-map.json').read_text())
WINDOWS=[r for r in MAP['output_windows'] if r['kind']=='unit_only']
assert len(WINDOWS)==37
OLD=json.loads((H/'inputs/window-basis/ABI-MAPPINGS.json').read_text())

def fresh(source):
    vm=SourceVM() if source else host.VM();vm.budget=900000000
    return vm,vm.objects['sceneDialogue'],vm.objects['cakood']

def props(d):return copy.deepcopy(d.p),list(d.arrays['sdWindowBounds'])

def expected_tuple(d,document,page):
    row=d.call('sdRoute',document)+page;data=d.arrays['sdPageData'][row*8:row*8+8]
    return data+[d.arrays[n][row] for n in ('sdTextResources','sdAudioModules','sdPageDurations')]

def actual_tuple(d):
    return [d.p[n] for n in ('sdEntry','sdLineKey','sdPart','sdPartCount','sdSpeaker','sdVoice','sdHeader','sdBytes','sdResource','sdAudioModule','sdVoiceEnd')]


class ReaderWindows(CompositionInitial):
    def test_04_immutable_tables_abi_and_other_modules(self):
        current=json.loads((H/'build/coherent/ABI-MAPPINGS.json').read_text())
        prior=json.loads((H/'inputs/window-basis/compile-receipt.json').read_text())
        now=json.loads((H/'build/coherent/compile-receipt.json').read_text())
        old982=OLD['modules']['982'];new982=current['modules']['982']
        self.assertEqual(new982['locals'][:-1],old982['locals'])
        self.assertEqual(new982['locals'][-1]['name'],'sdWindowBounds')
        self.assertEqual(new982['locals'][-1]['word_count'],2)
        self.assertEqual(new982['locals'][-1]['initial_words'],[0,0])
        oldprops=old982['classes'][0]['properties'];newprops=new982['classes'][0]['properties']
        self.assertEqual([(p['index'],p['selector_id'],p['selector']) for p in newprops],[(p['index'],p['selector_id'],p['selector']) for p in oldprops])
        self.assertEqual([p['signed_value'] for p in newprops if p['index']>=9],[p['signed_value'] for p in oldprops if p['index']>=9])
        oldids={r['name']:r['selector_id'] for r in OLD['selectors']}
        newids={r['name']:r['selector_id'] for r in current['selectors']}
        self.assertTrue(all(newids[n]==v for n,v in oldids.items()))
        self.assertEqual({n:v for n,v in newids.items() if n not in oldids},{'sdOpenWindow':2970,'sdWindowValue':2971})
        for old,new in zip(prior['modules'],now['modules']):
            self.assertEqual(old['module'],new['module'])
            if old['module']!=982:
                self.assertEqual((old['script_sha256'],old['heap_sha256']),(new['script_sha256'],new['heap_sha256']))
            self.assertLessEqual(new['combined_bytes'],65535)

    def test_05_all_37_exact_windows_pages_counter_and_no_receipts(self):
        for source in (False,True):
            vm,d,h=fresh(source);p08=vm.objects['p08State'];before=copy.deepcopy(p08.p),list(p08.arrays['p08Words'])
            for row in WINDOWS:
                document=row['document_id'];first=row['first_record_page'];count=row['page_count']
                total=d.call('sdPageCount',document)
                self.assertEqual(d.call('sdOpenWindow',document,first,count,0,0,0,0),1,row)
                self.assertEqual((d.p['sdDocument'],d.p['sdPage'],d.p['sdCount']),(document,first,total))
                self.assertEqual([d.call('sdWindowValue',f) for f in range(3)],[first,count,1])
                self.assertEqual(d.call('sdTurn',-32768,0),0)
                for page in range(first,first+count):
                    if d.p['sdPage']!=page:self.assertEqual(d.call('sdTurn',1,0),1)
                    self.assertEqual(actual_tuple(d),expected_tuple(d,document,page))
                    self.assertEqual(d.call('sdDraw',0),1)
                    self.assertEqual(str(d.arrays['sdCounter']),f'{page-first+1}/{count}')
                    self.assertEqual(d.p['sdCount'],total)
                self.assertEqual(d.call('sdTurn',32767,0),0)
                self.assertEqual(d.p['sdPage'],first+count-1)
                d.call('sdClose',0);self.assertEqual(list(d.arrays['sdWindowBounds']),[0,0])
            self.assertEqual((copy.deepcopy(p08.p),list(p08.arrays['p08Words'])),before)

    def test_06_every_old_full_document_page_remains_exact(self):
        for source in (False,True):
            vm,d,h=fresh(source);pages=0
            for document in range(1,973):
                count=d.call('sdPageCount',document)
                if not count:continue
                d.call('sdOpenWindow',973,4,1,0,0,0,0)
                self.assertEqual(d.call('sdOpen',document,0,0,0,0),1)
                self.assertEqual([d.call('sdWindowValue',f) for f in range(3)],[0,count,0])
                for page in range(count):
                    if page:self.assertEqual(d.call('sdTurn',1,0),1)
                    self.assertEqual(d.p['sdPage'],page);self.assertEqual(actual_tuple(d),expected_tuple(d,document,page));pages+=1
                self.assertEqual(d.call('sdTurn',1,0),0)
                self.assertEqual(d.p['sdPage'],count-1)
                self.assertEqual(d.call('sdAfterRestore',0),1)
                self.assertEqual(d.p['sdPage'],count-1)
            self.assertGreaterEqual(pages,1070)

    def test_07_invalid_admission_preserves_live_reader(self):
        for source in (False,True):
            vm,d,h=fresh(source)
            self.assertEqual(d.call('sdOpenWindow',973,4,1,0,0,0,0),1);before=props(d)
            for document,first,count in [(972,0,1),(1018,0,1),(973,-1,1),(973,0,0),(973,0,-1),(973,6,1),(973,5,2),(973,32767,2),(973,0,32767)]:
                self.assertEqual(d.call('sdOpenWindow',document,first,count,0,0,0,0),0)
                self.assertEqual(props(d),before)
            self.assertEqual(d.call('sdWindowValue',-1),-1);self.assertEqual(d.call('sdWindowValue',3),-1)

    def test_08_restore_exact_window_and_reject_bad_bounds(self):
        for source in (False,True):
            vm,d,h=fresh(source)
            self.assertEqual(d.call('sdOpenWindow',1008,1,1,0,0,0,0),1)
            d.call('sdDraw',0);oldgen=d.p['sdGeneration'];saved=vm.snapshot()
            self.assertEqual(d.call('sdAfterRestore',0),1)
            self.assertEqual((d.p['sdPage'],d.p['sdCount'],list(d.arrays['sdWindowBounds'])),(1,3,[1,1]))
            self.assertNotEqual(d.p['sdGeneration'],oldgen);self.assertEqual(d.p['sdPaintGeneration'],-1)
            self.assertEqual(d.p['sdPendingStart'],0)
            for kind in ('negative_first','zero_count','too_long','inactive','wrong_full_count','page_outside'):
                vm.restore(copy.deepcopy(saved))
                if kind=='negative_first':d.arrays['sdWindowBounds'][0]=-1
                elif kind=='zero_count':d.arrays['sdWindowBounds'][1]=0
                elif kind=='too_long':d.arrays['sdWindowBounds'][1]=3
                elif kind=='inactive':d.p['sdActive']=0
                elif kind=='wrong_full_count':d.p['sdCount']=4
                else:d.p['sdPage']=0
                self.assertEqual(d.call('sdAfterRestore',0),0,kind)
                self.assertEqual(d.p['sdActive'],0);self.assertNotEqual(d.p['sdFailure'],0)
                self.assertNotEqual(list(d.arrays['sdWindowBounds']),[0,0])

    def test_09_nonzero_page_never_loads_page_zero_or_broadens_failure(self):
        for source in (False,True):
            vm,d,h=fresh(source);start=d.call('sdRoute',973)
            expected=d.arrays['sdPageData'][(start+4)*8]
            vm.ktrace.clear();self.assertEqual(d.call('sdOpenWindow',973,4,1,0,0,0,0),1)
            reads=[a[1] for n,a in vm.ktrace if n=='GetFarText' and a[0]==208]
            self.assertEqual(reads[0],expected)
            self.assertNotIn(d.arrays['sdPageData'][start*8],reads)
            d.call('sdClose',0)
            d.arrays['sdPageData'][(start+4)*8]=32767
            self.assertEqual(d.call('sdOpenWindow',973,4,1,0,0,0,0),0)
            self.assertEqual(d.p['sdActive'],0);self.assertNotEqual(d.p['sdFailure'],0)
            self.assertEqual(list(d.arrays['sdWindowBounds']),[4,1])

    def test_10_controls_do_not_escape_explicit_window(self):
        for source in (False,True):
            vm,d,h=fresh(source)
            for document,first,count in ((973,4,1),(983,0,2),(1006,3,1),(1017,2,1)):
                d.call('sdOpenWindow',document,first,count,0,0,0,0)
                for page in range(first,first+count):
                    if d.p['sdPage']!=page:d.call('sdTurn',1,0)
                    h.p['uiControlCount']=0;d.call('sdBuildControls',h)
                    actions=[d.call('sdControlAction',i) for i in range(d.p['sdControls'])]
                    self.assertEqual(10 in actions,page>first);self.assertEqual(11 in actions,page<first+count-1)
                    self.assertTrue(all(action in (10,11,12,16,17) for action in actions))
                    self.assertEqual(d.call('sdDraw',0),1)
