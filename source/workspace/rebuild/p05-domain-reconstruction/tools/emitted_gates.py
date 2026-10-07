#!/usr/bin/env python3
"""Fail-closed SCI1.1 structure and whole-method abstract-stack gates.

This checks emitted bytes, not source evaluation. It is a static proof with
unknown run-time values, not a VM, native run, or proof of semantic correctness.
Dynamic array indices and receiver identity still need execution tests.
"""
from __future__ import annotations
import json, re, struct
from collections import deque
from pathlib import Path

class GateError(RuntimeError):
    pass

def require(ok, *why):
    if not ok:
        raise GateError(': '.join(map(str, why)))

def u16(blob, offset):
    require(0 <= offset <= len(blob) - 2, 'Word outside resource', offset, len(blob))
    return struct.unpack_from('<H', blob, offset)[0]

def words(blob, offset, count):
    require(count >= 0 and 0 <= offset <= len(blob) - count * 2, 'Word array outside resource', offset, count)
    return [u16(blob, offset + i * 2) for i in range(count)]

def parse_source(text):
    tokens = re.findall(r';[^\n]*|"(?:\\.|[^"\\])*"|[()\[\]]|[^\s()\[\];]+', text)
    result, stack = [], []
    current = result
    for token in tokens:
        if token.startswith(';'):
            continue
        if token in ('(', '['):
            child = []; current.append(child); stack.append(current); current = child
        elif token in (')', ']'):
            require(stack, 'Unbalanced source'); current = stack.pop()
        else:
            current.append(token)
    require(not stack, 'Unbalanced source')
    return result

def source_metadata(text):
    result = {'classes': {}, 'instances': {}, 'properties': set(), 'methods': set(), 'exports': {}}
    for node in parse_source(text):
        if not isinstance(node, list) or not node:
            continue
        if node[0] == 'public':
            for name, slot in zip(node[1::2], node[2::2]): result['exports'][int(slot)] = name
        if node[0] not in ('class', 'instance'):
            continue
        name = node[1]; props = []; methods = {}
        for part in node[2:]:
            if not isinstance(part, list) or not part: continue
            if part[0] == 'properties': props.extend(part[1::2])
            if part[0] == 'method':
                signature = part[1]; args = signature[1:]
                temps = args.index('&tmp') if '&tmp' in args else len(args)
                require(signature[0] not in methods, 'Duplicate source method', name, signature[0])
                methods[signature[0]] = {'arity': temps, 'temp_words': sum(int(v[1]) if isinstance(v,list) else 1 for v in args[temps+1:]), 'switches': sum(1 for s in walk(part) if s and s[0]=='switch'), 'assembly': any(s and s[0]=='asm' for s in walk(part))}
        result['properties'].update(props); result['methods'].update(methods)
        if node[0] == 'class': result['classes'][name] = {'properties':props, 'methods':methods}
        else: result['instances'][name] = {'class': node[node.index('of')+1], 'properties':props, 'methods':methods}
    return result

def walk(node):
    if isinstance(node, list):
        yield node
        for child in node:
            yield from walk(child)

def selector_decode(blob):
    count = u16(blob, 0) + 1
    require(2 + 2 * count <= len(blob), 'Truncated selector table')
    result = {}
    for index in range(count):
        offset = u16(blob, 2 + index * 2); size = u16(blob, offset)
        require(offset >= 2 + count * 2 and offset + 2 + size <= len(blob), 'Selector name bounds', index)
        name = blob[offset+2:offset+2+size].decode('ascii')
        if name != 'BAD SELECTOR':
            require(name not in result, 'Duplicate selector name', name)
            result[name] = index
    return result

def selector_encode(selectors):
    require(len(set(selectors.values())) == len(selectors), 'Duplicate selector ID')
    count = max(selectors.values()) + 1
    payload = bytearray(struct.pack('<H', count-1) + bytes(2*count)); offsets = {}; reverse = {v:k for k,v in selectors.items()}
    for index in range(count):
        name = reverse.get(index, 'BAD SELECTOR')
        if name not in offsets:
            offsets[name] = len(payload); encoded = name.encode('ascii')
            payload += struct.pack('<H',len(encoded)) + encoded
        require(len(payload) <= 65535, 'Selector resource overflow')
        struct.pack_into('<H',payload,2+2*index,offsets[name])
    return bytes(payload)

def encode_resources(resources):
    volume = bytearray(); groups = {}; rows = []
    import hashlib
    for (kind,number),payload in sorted(resources.items()):
        require(0 <= kind < 127 and 0 <= number <= 65535 and 0 < len(payload) <= 65535, 'Resource bounds',kind,number)
        if len(volume)&1: volume.append(0)
        offset = len(volume); volume += struct.pack('<BHHHH',kind|128,number,len(payload),len(payload),0)+payload
        groups.setdefault(kind,[]).append((number,offset))
        rows.append({'type':kind,'number':number,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()})
    if len(volume)&1:volume.append(0)
    directory=bytearray();entries=bytearray();start=3*(len(groups)+1)
    for kind,group in sorted(groups.items()):
        require(start+len(entries)<=65535,'Map overflow')
        directory+=struct.pack('<BH',kind|128,start+len(entries))
        for number,offset in group:
            require(offset//2<1<<24,'Volume offset overflow')
            entries+=struct.pack('<H',number)+(offset//2).to_bytes(3,'little')
    require(start+len(entries)<=65535,'Map overflow')
    directory+=struct.pack('<BH',255,start+len(entries))
    return bytes(directory+entries),bytes(volume),rows

def decode_resources(root):
    root=Path(root);mapping=(root/'resource.map').read_bytes();volume=(root/'resource.000').read_bytes();dirs=[];pos=0
    while True:
        require(pos+3<=len(mapping),'Map directory truncated')
        kind=mapping[pos];offset=u16(mapping,pos+1);pos+=3
        require(kind>=128 and (not dirs or kind>dirs[-1][0]),'Map directory order')
        dirs.append((kind,offset))
        if kind==255:break
    require(len(dirs)>1 and dirs[0][1]==pos and dirs[-1][1]==len(mapping),'Map bounds')
    result={}
    for (kind,first),(_,last) in zip(dirs,dirs[1:]):
        require(pos<=first<last<=len(mapping) and (last-first)%5==0,'Map group bounds')
        for p in range(first,last,5):
            number=u16(mapping,p);v=int.from_bytes(mapping[p+2:p+5],'little')*2
            require(v+9<=len(volume),'Resource header truncated')
            k,n,packed,unpacked,compression=struct.unpack_from('<BHHHH',volume,v)
            require((k,n)==(kind,number) and packed==unpacked and compression==0,'Resource header mismatch')
            require(packed>0 and v+9+packed<=len(volume),'Resource truncated')
            key=(kind&127,number);require(key not in result,'Duplicate resource');result[key]=volume[v+9:v+9+packed]
    expected_map,expected_volume,_=encode_resources(result)
    require((mapping,volume)==(expected_map,expected_volume),'Noncanonical or hidden resource data')
    return result

def extract(script, heap, selectors):
    """Strict payload-relative SCI1.1 object, export and relocation extraction."""
    s,h=script,heap;reverse={v:k for k,v in selectors.items()}
    require(len(s)>=10 and len(h)>=6,'Truncated script/heap')
    combined=len(s)+len(h)+(2 if len(s)&2 else 0)
    require(combined<=65535,'SCI16 combined segment overflow',combined)
    sr,hr=u16(s,0),u16(h,0)
    require(sr%2==0 and hr%2==0 and sr>=8 and hr>=4,'Relocation table alignment/bounds')
    rels=words(s,sr+2,u16(s,sr));relh=words(h,hr+2,u16(h,hr))
    require(sr+2+2*len(rels)==len(s) and hr+2+2*len(relh)==len(h),'Trailing relocation data')
    require(len(set(rels))==len(rels) and len(set(relh))==len(relh),'Duplicate relocation')
    for p in rels:require(0<=p<sr-1 and u16(s,p)<hr,'Script relocation bounds',p)
    for p in relh:require(0<=p<hr-1 and u16(h,p)<hr,'Heap relocation bounds',p)
    local_count=u16(h,2);pos=4+2*local_count;require(pos<hr,'Local segment overflow')
    exports=words(s,8,u16(s,6));objects=[];property_dictionary_ranges=[];method_table_ranges=[]
    while u16(h,pos)==0x1234:
        count=u16(h,pos+2);require(count>=9 and pos+2*count<=hr,'Object bounds',pos,count)
        values=words(h,pos,count);pd,md=values[2:4]
        if values[7]&0x8000:
            props=words(s,pd,count);require(pd+2*count<=sr,'Class property dictionary bounds')
        else:
            parent=next((o for o in objects if o['is_class'] and o['species']==values[6]),None)
            require(parent is not None and parent['property_count']==count,'Instance requires same-module matching class layout')
            props=[p['selector_id'] for p in parent['properties']]
        mc=u16(s,md);require(md+2+4*mc<=sr,'Object method dictionary bounds')
        methods=[]
        for i in range(mc):
            selector,offset=words(s,md+2+4*i,2)
            require(selector in reverse and 8+len(exports)*2<=offset<sr,'Method selector/entry',selector,offset)
            methods.append({'selector':reverse[selector],'selector_id':selector,'code_offset':offset})
        require(len({x['selector_id'] for x in methods})==mc,'Duplicate method selector')
        nameptr=values[8];require(pos+16 in relh and pos+2*count<=hr,'Missing object name relocation')
        require(0<nameptr<hr and 0 in h[nameptr:hr],'Invalid object name string')
        name=h[nameptr:h.index(0,nameptr,hr)].decode('ascii')
        objects.append({'name':name,'heap_offset':pos,'property_count':count,'property_selector_offset':pd,'method_table_offset':md,'is_class':bool(values[7]&0x8000),'species':values[5],'superclass':values[6],'properties':[{'index':i,'selector_id':sel,'selector':reverse.get(sel),'raw_value':val} for i,(sel,val) in enumerate(zip(props,values))],'methods':methods})
        if values[7]&0x8000:
            require(all(p in reverse for p in props),'Unknown class property selector',name)
            property_dictionary_ranges.append((pd,pd+2*count))
        method_table_ranges.append((md,md+2+4*mc));pos+=2*count
    require(u16(h,pos)==0,'Heap object terminator')
    require(pos+2<=hr,'Heap strings bounds')
    for obj in objects:require(pos+2<=u16(h,obj['heap_offset']+16)<hr,'Object name outside strings')
    require(all(e in {o['heap_offset'] for o in objects} for e in exports),'Nonobject export unsupported')
    for i in range(len(exports)):require(8+i*2 in rels,'Export missing relocation',i)
    starts=sorted({m['code_offset'] for o in objects for m in o['methods']})
    require(starts,'No emitted methods')
    for a,b in property_dictionary_ranges+method_table_ranges:require(8+2*len(exports)<=a<=b<=starts[0],'Dictionary overlaps code')
    return {'combined_bytes':combined,'script_relocation_offset':sr,'script_relocations':rels,'heap_relocation_offset':hr,'heap_relocations':relh,'locals_word_count':local_count,'exports':exports,'objects':objects,'strings_start':pos+2}

# Unknown is represented by None. Constants are tracked only when guaranteed on
# every incoming path; conditional branches always explore both possible paths.
def decode(blob, pc, table, limit):
    require(0<=pc<limit,'Instruction offset bounds',pc)
    raw=blob[pc];op=raw>>1;p=pc+1;args=[]
    require(str(op) in table['opcodes'] and op not in (38,39,41,47,63),'Invalid/unsupported opcode',op,pc)
    for kind in table['argtypes'][op]:
        if kind=='otEMPTY':continue
        require(kind!='otDEBUGSTRING','Unsupported debug opcode')
        width=1 if kind in ('otUINT8','otINT8') else 2 if kind in ('otUINT16','otINT16') else 1 if raw&1 else 2
        require(p+width<=limit,'Instruction crosses method boundary',pc,limit)
        value=int.from_bytes(blob[p:p+width],'little');p+=width
        if kind in ('otLABEL','otINT','otINT8','otINT16') and value>=1<<(width*8-1):value-=1<<(width*8)
        args.append(value)
    return op,args,p

def audit_module(number,script,heap,layout,selectors,table,kernels,metadata,global_words,class_owners):
    reverse={v:k for k,v in selectors.items()};starts=sorted({m['code_offset'] for o in layout['objects'] for m in o['methods']});reports=[]
    for obj in layout['objects']:
        ownmeta=metadata['classes' if obj['is_class'] else 'instances'][obj['name']]
        propnames={p['selector'] for p in obj['properties']};propoffsets={p['index']*2 for p in obj['properties']}
        methods=ownmeta['methods']
        inherited=metadata['classes'].get(ownmeta.get('class',''),{}).get('methods',{})
        for method in obj['methods']:
            name=method['selector'];entry=method['code_offset'];index=starts.index(entry);limit=starts[index+1] if index+1<len(starts) else layout['script_relocation_offset']
            require(name in methods,'Source/emitted method mismatch',number,obj['name'],name)
            meta=methods[name];instructions={};pc=entry
            while pc<limit:
                instructions[pc]=decode(script,pc,table,limit);pc=instructions[pc][2]
            branches=[];calls=[];kernel_ids=set()
            for pc,(op,args,end) in instructions.items():
                if op in (23,24,25):require(end+args[0] in instructions,'Branch target outside method or instruction',number,name,pc,end+args[0]);branches.append((pc,end+args[0]))
                if op==32:require(end+args[0] in starts,'Local CALL does not target entry',number,name,pc)
                if op in (34,35):raise GateError(f'Unresolved external CALLB/CALLE in module {number}:{name}')
                if op==40:require(args[0] in range(len(class_owners)),'CLASS species outside universe',number,name,args)
                if op in range(49,57):require(args[0] in propoffsets,'Property access outside object',number,name,args[0])
                if op in (57,58):require(pc+1 in layout['script_relocations'] and (args[0] in {o['heap_offset'] for o in layout['objects']} or layout['strings_start']<=args[0]<layout['heap_relocation_offset']),'LOFS missing relocation or invalid target',number,name,pc)
                if op==33:
                    require(str(args[0]) in kernels,'Unknown SCI1.1 kernel',number,name,args[0]);kernel_ids.add(args[0])
                    require(number!=985,'Pure P05 domain must not call kernels',name,args[0])
            states={entry:((),None)};pending=deque([entry]);returns=set();max_stack=0;frames=meta['temp_words'];packets={};visited=set()
            if instructions[entry][0]==31 and meta['assembly'] and number!=985:
                frames=instructions[entry][1][0]
            while pending:
                pc=pending.popleft();stack0,acc=states[pc];stack=list(stack0);op,args,end=instructions[pc];arg=args[0] if args else None;visited.add(pc)
                def pop():
                    require(stack,'Operand stack underflow',number,name,pc);return stack.pop()
                def take(count):
                    require(0<count<=len(stack),'Call packet stack underflow',number,name,pc,count,len(stack));values=stack[-count:];del stack[-count:];return values
                def send_packet(size):
                    require(size%2==0 and 0<size<=255,'SCI1.1 send packet byte bound',number,name,pc,size)
                    packet=take(size//2);j=0;out=[]
                    while j<len(packet):
                        require(j+2<=len(packet),'Truncated selector packet',number,name,pc)
                        sel,argc=packet[j:j+2];j+=2
                        require(sel is not None and sel in reverse and argc is not None and 0<=argc<=len(packet)-j,'Unknown/invalid selector packet',number,name,pc,packet)
                        target=reverse[sel];out.append((target,argc));j+=argc
                        if op==42:
                            targetmeta=methods.get(target) or inherited.get(target)
                            if targetmeta:require((argc==targetmeta['arity'] if number==985 else argc>=targetmeta['arity']),'SELF method arity mismatch',number,name,pc,target,argc,targetmeta['arity'])
                            else:require(target in propnames and argc<=1,'SELF missing method/property',number,name,pc,target)
                    return out
                if op==31:require(pc==entry and not stack and arg==frames,'LINK frame differs from source',number,name,arg,frames)
                elif op==26:acc=arg
                elif op==27:stack.append(acc)
                elif op==28:stack.append(arg)
                elif op==29:pop()
                elif op==30:require(stack,'DUP underflow',number,name,pc);stack.append(stack[-1])
                elif op in (59,60,61):stack.append(op-59)
                elif op in (48,62):stack.append(None)
                elif op in (0,11,12):acc=None
                elif op in range(1,11) or op in range(13,23):pop();acc=None
                elif op in (37,42,43):
                    size=args[1] if op==43 else arg
                    require(op!=43,'SUPER requires explicit inheritance proof',number,name)
                    packets[pc]=send_packet(size);acc=None
                elif op in (32,33):
                    size=args[1];require(size%2==0 and 0<=size<=255,'Call byte count',number,name,pc,size)
                    packet=take(size//2+1);require(packet[0]==size//2,'CALL argument word differs from byte count',number,name,pc,packet[0],size)
                    packets[pc]=[('kernel:'+kernels[str(arg)] if op==33 else 'local:'+str(end+arg),size//2)];acc=None
                elif op==44:raise GateError(f'REST variable frame unsupported in static gate: {number}:{name}')
                elif op in (40,45,46,57):acc=None
                elif op==58:stack.append(None)
                elif op in (49,53,54):acc=None
                elif op in (51,55,56):stack.append(None)
                elif op==52:pop()
                elif op>=64:
                    scope=op&3;indexed=bool(op&8);family=(op-64)//16;tos=bool(op&4)
                    bound=(global_words,layout['locals_word_count'],frames,meta['arity']+1)[scope]
                    require(0<=arg<bound,'Variable base index outside declared frame',number,name,pc,scope,arg,bound)
                    if family==1:
                        if tos or indexed:pop()
                    elif tos:stack.append(None)
                    else:acc=None
                elif op not in (23,24,25,36,50):raise GateError(f'No stack semantics for opcode {op} at {number}:{name}:{pc}')
                max_stack=max(max_stack,len(stack));require(max_stack+frames+meta['arity']+1<=4096,'SCI operand stack resource budget exceeded',number,name,max_stack,frames)
                if op==36:
                    # SCI RET discards its frame. Compiler switch early returns may
                    # leave deciding words. Non-switch methods must be balanced.
                    require((meta['assembly'] and number!=985) or len(stack)<=meta['switches'],'Unexpected operand tail at RET',number,name,pc,len(stack),meta['switches'])
                    returns.add((pc,len(stack)));continue
                successors=[end+arg] if op==25 else [end,end+arg] if op in (23,24) else [end]
                new=(tuple(stack),acc)
                for nxt in successors:
                    require(nxt in instructions,'Reachable fallthrough out of method',number,name,pc,nxt)
                    if nxt not in states:states[nxt]=new;pending.append(nxt)
                    else:
                        oldstack,oldacc=states[nxt];require(len(oldstack)==len(stack),'Inconsistent stack depth at control-flow merge',number,name,nxt,len(oldstack),len(stack))
                        merged=(tuple(a if a==b else None for a,b in zip(oldstack,stack)),oldacc if oldacc==acc else None)
                        if merged!=states[nxt]:states[nxt]=merged;pending.append(nxt)
            require(returns,'Method has no reachable RET',number,name)
            reports.append({'object':obj['name'],'method':name,'entry':entry,'instructions':len(instructions),'reachable_instructions':len(visited),'branches':len(branches),'call_sites':len(packets),'max_operand_words':max_stack,'temp_words':frames,'return_depths':sorted({v for _,v in returns}),'kernels':[kernels[str(k)] for k in sorted(kernel_ids)]})
    return {'module':number,'status':'PASS_STATIC_EMITTED','methods':reports,'method_count':len(reports),'branches':sum(m['branches'] for m in reports),'call_sites':sum(m['call_sites'] for m in reports),'native_acceptance':False}
