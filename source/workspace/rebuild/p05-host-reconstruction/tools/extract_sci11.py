"""Read-only SCI1.1 script/heap extractor, reconstructed from pinned compiler format.

Entry point: extract(script_path, heap_path, selectors_path) -> JSON-safe dict.
All offsets are payload-relative byte offsets; locals indices are word indices.
Input resources have no two-byte patch wrapper. Values are unsigned raw words.
"""
from pathlib import Path
import struct,json,argparse,hashlib

def u16(b,p): return struct.unpack_from('<H',b,p)[0]
def words(b,p,n): return list(struct.unpack_from('<'+str(n)+'H',b,p))
def extract(script_path, heap_path, selectors_path):
    s,h=Path(script_path).read_bytes(),Path(heap_path).read_bytes()
    names={x['selector_id']:x['name'] for x in json.loads(Path(selectors_path).read_text())}
    def selector(x):return names.get(x,f'__internal_{x:04x}')
    def string(p):return h[p:h.find(b'\0',p)].decode('ascii') if 0<p<len(h) else None
    n=u16(h,2);p=4+n*2;objects=[]
    while u16(h,p)==0x1234:
        count,varoffs,methoffs=words(h,p+2,3)
        vals=words(h,p,count)
        selectors=words(s,varoffs,count)
        methods=[{'selector':selector(a),'selector_id':a,'code_offset':b} for a,b in [words(s,methoffs+2+i*4,2) for i in range(u16(s,methoffs))]]
        objects.append({'name':string(vals[8]),'heap_offset':p,'property_count':count,'property_selector_offset':varoffs,'method_table_offset':methoffs,'is_class':bool(vals[7]&0x8000),'species':vals[5],'superclass':vals[6], 'properties':[{'index':i,'heap_offset':p+i*2,'selector_id':a,'selector':selector(a),'raw_value':v,'signed_value':v if v<32768 else v-65536} for i,(a,v) in enumerate(zip(selectors,vals))],'methods':methods})
        p+=count*2
    assert u16(h,p)==0
    pointers=words(h,u16(h,0)+2,u16(h,u16(h,0)))
    sp=u16(s,0);sr=words(s,sp+2,u16(s,sp))
    return {'format':'SCI1.1','script':str(script_path),'heap':str(heap_path),'script_sha256':hashlib.sha256(s).hexdigest(),'heap_sha256':hashlib.sha256(h).hexdigest(),'script_relocation_offset':sp,'script_relocations':sr,'heap_relocation_offset':u16(h,0),'heap_relocations':pointers,'locals_heap_offset':4,'locals_word_count':n,'locals':words(h,4,n),'exports':words(s,8,u16(s,6)),'objects':objects,'strings_start':p+2}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('script');ap.add_argument('heap');ap.add_argument('selectors');ap.add_argument('-o','--output');a=ap.parse_args();v=json.dumps(extract(a.script,a.heap,a.selectors),indent=2)+'\n'
    if a.output:Path(a.output).write_text(v)
    else:print(v,end='')
