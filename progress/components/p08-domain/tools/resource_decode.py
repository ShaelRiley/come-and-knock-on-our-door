"""Read-only SCI1.1 script/heap dictionary and instruction decoder, reconstructed.
No import-time IO, no hardcoded missing historical paths, no native execution.
"""
import json,re,struct
from pathlib import Path

def words(blob,offset,count): return struct.unpack_from('<'+'H'*count,blob,offset)
def signed(v): return v-65536 if v>=32768 else v

def selectors(path):
    rows=json.loads(Path(path).read_text())
    return {r['selector_id']:r['name'] for r in rows} if isinstance(rows,list) else {v:k for k,v in rows.items()}

def layout(script,heap,names):
    script,heap=bytes(script),bytes(heap)
    local_count=words(heap,2,1)[0];off=4+2*local_count;classes=[];class_defs={}
    while off+18<=len(heap) and words(heap,off,1)[0]==0x1234:
        header=words(heap,off,9);size,propdict,methdict=header[1:4]
        vals=words(heap,off,size);name=heap[header[8]:].split(b'\0',1)[0].decode('ascii')
        if header[7]&0x8000:
            propids=words(script,propdict,size);class_defs[header[5]]=propids
        else: propids=class_defs.get(header[6],())
        mc=words(script,methdict,1)[0]
        methods={names.get(s,str(s)):p for s,p in [words(script,methdict+2+i*4,2) for i in range(mc)]}
        props={names.get(s,str(s)):signed(v) for s,v in zip(propids,vals)}
        classes.append(dict(name=name,offset=off,size=size,header=list(header),properties=props,property_offsets={i*2:names.get(s,str(s)) for i,s in enumerate(propids)},methods=methods))
        off+=size*2
    return dict(local_count=local_count,local_values=list(words(heap,4,local_count)),objects=classes)

def instruction_tables(compiler_dir):
    c=Path(compiler_dir)
    ops={int(v):k for k,v in re.findall(r'^\s*(\w+)\s*=\s*(\d+)',(c/'PMachine.h').read_text(),re.M) if int(v)<128}
    types=[re.findall(r'ot\w+',x) for x in re.findall(r'\{([^}]+)\}',(c/'PMachine.cpp').read_text().split('OpArgTypes_SCI0[TOTAL_OPCODES][3] = {')[1].split('};')[0])]
    assert len(types)==128
    return ops,types

def decode(blob,pc,argtypes):
    raw=blob[pc];op=raw>>1;p=pc+1;args=[]
    for ty in argtypes[op]:
        if ty=='otEMPTY': continue
        width=1 if ty=='otUINT8' or raw&1 else 2
        val=int.from_bytes(blob[p:p+width],'little');p+=width
        if ty in ('otLABEL','otINT') and val>=(1<<(width*8-1)):val-=1<<(width*8)
        args.append(val)
    return op,args,p

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('script',type=Path);a.add_argument('heap',type=Path);a.add_argument('selectors',type=Path);a.add_argument('--compiler-dir',type=Path);a.add_argument('--disassembly',type=Path)
    args=a.parse_args();b=args.script.read_bytes();ns=selectors(args.selectors);l=layout(b,args.heap.read_bytes(),ns);print(json.dumps(l,indent=2))
    if args.disassembly:
        ops,types=instruction_tables(args.compiler_dir);lines=[]
        for obj in l['objects']:
            methods=obj['methods'];ordered=sorted(methods.items(),key=lambda x:x[1])
            for i,(name,pc) in enumerate(ordered):
                end=ordered[i+1][1] if i+1<len(ordered) else words(b,0,1)[0]
                lines.append(f'\n{obj["name"]}.{name} @{pc:04x}')
                while pc<end:
                    op,v,nxt=decode(b,pc,types);extra=''
                    if op in (23,24,25):extra=f' ->{nxt+v[0]:04x}'
                    if op in range(49,57):extra=' '+obj['property_offsets'].get(v[0],'?')
                    if op==28 and v[0] in ns:extra=' selector? '+ns[v[0]]
                    lines.append(f'{pc:04x} {ops.get(op,str(op)):8} {v!s:17}{extra}');pc=nxt
        args.disassembly.write_text('\n'.join(lines)+'\n')
